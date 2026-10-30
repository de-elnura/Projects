from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Sum, Q

from .models import (
    UserProfile, Category, Course, Module, Lesson,
    Enrollment, LessonProgress, Quiz, Question, Option,
    QuizAttempt, UserAnswer, Certificate
)
from .forms import (
    UserRegisterForm, CourseForm, ModuleForm, LessonForm,
    QuizForm, QuestionForm
)
from .utils import (
    get_or_create_profile, award_xp, can_student_access_lesson,
    can_student_access_quiz, can_student_access_module,
    get_course_progress_data, check_and_award_certificate
)


def home_view(request):
    featured_courses = Course.objects.filter(is_published=True).select_related('instructor', 'category')[:6]
    categories = Category.objects.annotate(course_count=Count('courses')).order_by('-course_count')[:8]
    
    total_students = Enrollment.objects.values('student').distinct().count()
    total_courses = Course.objects.filter(is_published=True).count()
    total_certs = Certificate.objects.count()
    top_teachers = UserProfile.objects.filter(role__in=['teacher', 'admin']).select_related('user')[:4]

    return render(request, 'lms/home.html', {
        'featured_courses': featured_courses,
        'categories': categories,
        'total_students': total_students + 140, # visual base offset
        'total_courses': total_courses,
        'total_certs': total_certs + 56,
        'top_teachers': top_teachers,
    })


def catalog_view(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '')
    level = request.GET.get('level', '')

    courses = Course.objects.filter(is_published=True).select_related('instructor', 'category')

    if query:
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query)
        )
    if category_slug:
        courses = courses.filter(category__slug=category_slug)
    if level:
        courses = courses.filter(level=level)

    categories = Category.objects.annotate(course_count=Count('courses'))

    return render(request, 'lms/catalog.html', {
        'courses': courses,
        'categories': categories,
        'query': query,
        'selected_category': category_slug,
        'selected_level': level,
    })


def course_detail_view(request, slug):
    course = get_object_or_404(Course.objects.select_related('instructor', 'category'), slug=slug)
    progress_data = get_course_progress_data(request.user, course)

    # Birinchi dars
    first_lesson = Lesson.objects.filter(module__course=course).order_by('module__order', 'order').first()

    return render(request, 'lms/course_detail.html', {
        'course': course,
        'progress_data': progress_data,
        'first_lesson': first_lesson,
    })


@login_required
def enroll_course_view(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)

    if created:
        messages.success(request, f"«{course.title}» kursiga muvaffaqiyatli yozildingiz! Darslarni boshlashingiz mumkin.")
        award_xp(request.user, 20) # bonus for enrolling

    first_lesson = Lesson.objects.filter(module__course=course).order_by('module__order', 'order').first()
    if first_lesson:
        return redirect('classroom', course_slug=course.slug, lesson_id=first_lesson.id)
    return redirect('course_detail', slug=course.slug)


@login_required
def classroom_view(request, course_slug, lesson_id=None):
    course = get_object_or_404(Course, slug=course_slug)
    
    # Ro'yxatdan o'tganligini tekshirish
    is_teacher = request.user.is_staff or getattr(request.user.profile, 'is_teacher', False)
    if not is_teacher and not Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, "Darslarni ko'rish uchun avval kursga yoziling.")
        return redirect('course_detail', slug=course.slug)

    progress_data = get_course_progress_data(request.user, course)

    # Tanlangan darsni aniqlash
    current_lesson = None
    if lesson_id:
        current_lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)
    else:
        # Eng birinchi yoki hali tugatilmagan darsni topish
        for m_data in progress_data['modules_data']:
            for l_data in m_data['lessons']:
                if l_data['is_accessible'] and not l_data['is_completed']:
                    current_lesson = l_data['lesson']
                    break
            if current_lesson:
                break
        if not current_lesson:
            current_lesson = Lesson.objects.filter(module__course=course).order_by('module__order', 'order').first()

    if not current_lesson:
        messages.info(request, "Bu kursda hali darslar yuklanmagan.")
        return redirect('course_detail', slug=course.slug)

    # Ruxsat tekshiruvi: 1-darsni tugatmasdan yoki testdan 70% olmasdan o'ta olmasligi
    if not can_student_access_lesson(request.user, current_lesson):
        messages.error(request, "Ushbu dars hali qulflangan! Oldingi darslar va modul testini (kamida 70%) yakunlang.")
        # Ruxsat berilgan birinchi darsga yo'naltirish
        for m_data in progress_data['modules_data']:
            for l_data in m_data['lessons']:
                if l_data['is_accessible']:
                    return redirect('classroom', course_slug=course.slug, lesson_id=l_data['lesson'].id)
        return redirect('course_detail', slug=course.slug)

    # Joriy dars holati
    is_current_completed = LessonProgress.objects.filter(student=request.user, lesson=current_lesson, is_completed=True).exists()

    # Oldingi va keyingi darslarni topish
    all_lessons = list(Lesson.objects.filter(module__course=course).order_by('module__order', 'order'))
    prev_lesson = None
    next_lesson = None
    try:
        curr_idx = [l.id for l in all_lessons].index(current_lesson.id)
        if curr_idx > 0:
            prev_lesson = all_lessons[curr_idx - 1]
        if curr_idx < len(all_lessons) - 1:
            next_lesson = all_lessons[curr_idx + 1]
    except ValueError:
        pass

    # Joriy modul testi
    current_module_quiz = getattr(current_lesson.module, 'quiz', None)

    return render(request, 'lms/classroom.html', {
        'course': course,
        'current_lesson': current_lesson,
        'is_current_completed': is_current_completed,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'current_module_quiz': current_module_quiz,
        'progress_data': progress_data,
    })


@login_required
def complete_lesson_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.module.course

    # Darsni yakunlash
    progress, created = LessonProgress.objects.get_or_create(
        student=request.user,
        lesson=lesson,
        defaults={'is_completed': True, 'completed_at': timezone.now()}
    )
    if not progress.is_completed:
        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.save()
        award_xp(request.user, 15) # +15 XP dars uchun
        messages.success(request, f"«{lesson.title}» darsi muvaffaqiyatli yakunlandi! +15 XP berildi 🎯")

    # Modul testi bormi va modulning barcha darslari tugadimi?
    mod_lessons = lesson.module.lessons.all()
    completed_in_mod = LessonProgress.objects.filter(
        student=request.user,
        lesson__in=mod_lessons,
        is_completed=True
    ).count()

    if completed_in_mod == mod_lessons.count() and hasattr(lesson.module, 'quiz'):
        messages.info(request, f"Tabriklaymiz! {lesson.module.title} barcha darslari tugadi. Endi modul imtihonini (test) topshirishingiz mumkin.")
        return redirect('quiz_detail', quiz_id=lesson.module.quiz.id)

    # Keyingi darsga o'tish
    next_lesson = Lesson.objects.filter(
        module=lesson.module,
        order__gt=lesson.order
    ).order_by('order').first()

    if not next_lesson:
        # Keyingi modulning birinchi darsi
        next_module = Module.objects.filter(
            course=course,
            order__gt=lesson.module.order
        ).order_by('order').first()
        if next_module:
            next_lesson = next_module.lessons.order_by('order').first()

    if next_lesson:
        return redirect('classroom', course_slug=course.slug, lesson_id=next_lesson.id)

    # Sertifikat tekshiruvi
    check_and_award_certificate(request.user, course)

    return redirect('classroom', course_slug=course.slug, lesson_id=lesson.id)


@login_required
def quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz.objects.select_related('module__course'), id=quiz_id)
    course = quiz.module.course

    # Ruxsat tekshiruvi: talaba moduldagi barcha darslarni tugatgan bo'lishi kerak
    if not can_student_access_quiz(request.user, quiz):
        messages.error(request, "Imtihonni boshlash uchun ushbu modulning barcha darslarini to'liq o'rganib chiqishingiz shart!")
        return redirect('classroom', course_slug=course.slug)

    questions = quiz.questions.prefetch_related('options').all()
    if not questions.exists():
        messages.warning(request, "Ushbu testda hali savollar mavjud emas.")
        return redirect('classroom', course_slug=course.slug)

    # Qayta urinishlar soni
    attempts = QuizAttempt.objects.filter(student=request.user, quiz=quiz)
    best_attempt = attempts.order_by('-percentage').first()

    return render(request, 'lms/quiz.html', {
        'quiz': quiz,
        'course': course,
        'questions': questions,
        'total_questions': questions.count(),
        'attempts_count': attempts.count(),
        'best_attempt': best_attempt,
        'time_limit_seconds': quiz.time_limit_minutes * 60,
    })


@login_required
def quiz_submit_view(request, quiz_id):
    if request.method != 'POST':
        return redirect('quiz_detail', quiz_id=quiz_id)

    quiz = get_object_or_404(Quiz.objects.select_related('module__course'), id=quiz_id)
    questions = quiz.questions.prefetch_related('options').all()
    
    total_questions = questions.count()
    correct_count = 0
    total_score = 0

    # Yangi attempt yaratish
    attempt = QuizAttempt.objects.create(
        student=request.user,
        quiz=quiz,
        total_questions=total_questions
    )

    for question in questions:
        field_name = f'question_{question.id}'
        selected_option_id = request.POST.get(field_name)
        
        selected_option = None
        is_correct = False
        if selected_option_id:
            try:
                selected_option = Option.objects.get(id=int(selected_option_id), question=question)
                if selected_option.is_correct:
                    is_correct = True
                    correct_count += 1
                    total_score += question.points
            except (Option.DoesNotExist, ValueError):
                pass

        UserAnswer.objects.create(
            attempt=attempt,
            question=question,
            selected_option=selected_option,
            is_correct=is_correct
        )

    percentage = round((correct_count / total_questions * 100), 1) if total_questions > 0 else 0
    passed = percentage >= quiz.passing_score

    attempt.score = total_score
    attempt.correct_answers = correct_count
    attempt.percentage = percentage
    attempt.passed = passed
    attempt.save()

    # XP hisoblash: Har bir to'g'ri javob uchun +10 XP, imtihondan o'tsa +50 XP bonus!
    earned_xp = (correct_count * 10) + (50 if passed else 0)
    award_xp(request.user, earned_xp)

    # Sertifikat olish shartlarini tekshirish
    check_and_award_certificate(request.user, quiz.module.course)

    if passed:
        messages.success(request, f"Tabriklaymiz! Testdan muvaffaqiyatli o'tdingiz ({percentage}%). Keyingi modul ochildi! +{earned_xp} XP berildi 🎉")
    else:
        messages.warning(request, f"Natijangiz: {percentage}%. O'tish bali: {quiz.passing_score}%. Afsuski bu safar yetarli bo'lmadi, xatolaringizni ko'rib qayta topshirishingiz mumkin.")

    return redirect('quiz_result', attempt_id=attempt.id)


@login_required
def quiz_result_view(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt.objects.select_related('quiz__module__course', 'student'), id=attempt_id)
    if attempt.student != request.user and not request.user.is_staff:
        messages.error(request, "Boshqa foydalanuvchining test natijasini ko'ra olmaysiz.")
        return redirect('home')

    answers = attempt.answers.select_related('question', 'selected_option').prefetch_related('question__options').all()
    course = attempt.quiz.module.course

    # Keyingi modulni tekshirish
    next_module = Module.objects.filter(course=course, order__gt=attempt.quiz.module.order).order_by('order').first()

    return render(request, 'lms/quiz_result.html', {
        'attempt': attempt,
        'answers': answers,
        'course': course,
        'next_module': next_module,
    })


def leaderboard_view(request):
    top_students = UserProfile.objects.filter(role='student').select_related('user').order_by('-xp_points')[:25]
    
    user_rank = None
    if request.user.is_authenticated:
        user_xp = getattr(request.user.profile, 'xp_points', 0)
        user_rank = UserProfile.objects.filter(role='student', xp_points__gt=user_xp).count() + 1

    return render(request, 'lms/leaderboard.html', {
        'top_students': top_students,
        'user_rank': user_rank,
    })


@login_required
def profile_view(request):
    profile = get_or_create_profile(request.user)
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    
    courses_stats = []
    for enr in enrollments:
        progress = get_course_progress_data(request.user, enr.course)
        courses_stats.append({
            'course': enr.course,
            'enrolled_at': enr.enrolled_at,
            'progress': progress,
        })

    certificates = Certificate.objects.filter(student=request.user).select_related('course')
    attempts = QuizAttempt.objects.filter(student=request.user).select_related('quiz__module__course')[:10]

    return render(request, 'lms/profile.html', {
        'profile': profile,
        'courses_stats': courses_stats,
        'certificates': certificates,
        'attempts': attempts,
    })


@login_required
def certificate_view(request, certificate_id):
    # UUID yoki unikal id bo'yicha topish
    cert = get_object_or_404(Certificate.objects.select_related('student', 'course__instructor'), certificate_id=certificate_id)
    if cert.student != request.user:
        messages.error(request, "Xavfsizlik: Begona foydalanuvchining sertifikatini ko'rish mutlaqo taqiqlangan!")
        return redirect('profile')

    return render(request, 'lms/certificate.html', {
        'cert': cert,
    })


def instructors_view(request):
    instructors = UserProfile.objects.filter(role__in=['teacher', 'admin']).select_related('user')
    return render(request, 'lms/instructors.html', {
        'instructors': instructors,
    })


# ---------------- O'QITUVCHI BOSHQARUVI (TEACHER DASHBOARD) ---------------- #

@login_required
def teacher_dashboard_view(request):
    if not (request.user.is_staff or getattr(request.user.profile, 'is_teacher', False)):
        messages.error(request, "Bu sahifa faqat o'qituvchilar uchun mo'ljallangan.")
        return redirect('home')

    courses = Course.objects.filter(instructor=request.user).prefetch_related('modules__lessons', 'enrollments')
    total_students = Enrollment.objects.filter(course__instructor=request.user).count()
    total_lessons = Lesson.objects.filter(module__course__instructor=request.user).count()
    total_quizzes = Quiz.objects.filter(module__course__instructor=request.user).count()

    return render(request, 'lms/teacher/dashboard.html', {
        'courses': courses,
        'total_students': total_students,
        'total_lessons': total_lessons,
        'total_quizzes': total_quizzes,
    })


@login_required
def teacher_course_create_view(request):
    if not (request.user.is_staff or getattr(request.user.profile, 'is_teacher', False)):
        messages.error(request, "Faqat o'qituvchilar kurs yarata oladi.")
        return redirect('home')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, f"«{course.title}» kursi muvaffaqiyatli yaratildi! Endi modullar qo'shishingiz mumkin.")
            return redirect('teacher_dashboard')
    else:
        form = CourseForm()

    return render(request, 'lms/teacher/course_form.html', {'form': form, 'title': 'Yangi Kurs Yaratish'})


@login_required
def teacher_module_create_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            messages.success(request, f"«{module.title}» moduli qo'shildi!")
            return redirect('teacher_dashboard')
    else:
        form = ModuleForm(initial={'order': course.modules.count() + 1})

    return render(request, 'lms/teacher/module_form.html', {'form': form, 'course': course})


@login_required
def teacher_lesson_create_view(request, module_id):
    module = get_object_or_404(Module, id=module_id, course__instructor=request.user)
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()
            messages.success(request, f"«{lesson.title}» darsi muvaffaqiyatli qo'shildi!")
            return redirect('teacher_dashboard')
    else:
        form = LessonForm(initial={'order': module.lessons.count() + 1})

    return render(request, 'lms/teacher/lesson_form.html', {'form': form, 'module': module})


@login_required
def teacher_quiz_create_view(request, module_id):
    module = get_object_or_404(Module, id=module_id, course__instructor=request.user)
    quiz = getattr(module, 'quiz', None)

    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.module = module
            quiz.save()
            messages.success(request, "Modul imtihoni (Quiz) saqlandi! Endi savollar qo'shishingiz mumkin.")
            return redirect('teacher_quiz_questions', quiz_id=quiz.id)
    else:
        form = QuizForm(instance=quiz, initial={'title': f"{module.title} Yakuniy Testi"})

    return render(request, 'lms/teacher/quiz_form.html', {'form': form, 'module': module, 'quiz': quiz})


@login_required
def teacher_quiz_questions_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, module__course__instructor=request.user)
    
    if request.method == 'POST':
        question_text = request.POST.get('question_text', '').strip()
        points = int(request.POST.get('points', 10))
        explanation = request.POST.get('explanation', '').strip()
        
        opt1 = request.POST.get('option_1', '').strip()
        opt2 = request.POST.get('option_2', '').strip()
        opt3 = request.POST.get('option_3', '').strip()
        opt4 = request.POST.get('option_4', '').strip()
        correct_index = int(request.POST.get('correct_option', 1))

        if question_text and opt1 and opt2:
            question = Question.objects.create(
                quiz=quiz,
                question_text=question_text,
                points=points,
                explanation=explanation,
                order=quiz.questions.count() + 1
            )
            options_data = [(opt1, correct_index == 1), (opt2, correct_index == 2)]
            if opt3:
                options_data.append((opt3, correct_index == 3))
            if opt4:
                options_data.append((opt4, correct_index == 4))

            for text, is_corr in options_data:
                Option.objects.create(question=question, option_text=text, is_correct=is_corr)

            messages.success(request, "Savol va variantlar muvaffaqiyatli qo'shildi!")
            return redirect('teacher_quiz_questions', quiz_id=quiz.id)

    questions = quiz.questions.prefetch_related('options').all()
    return render(request, 'lms/teacher/quiz_questions.html', {'quiz': quiz, 'questions': questions})


# ---------------- AUTENTIFIKATSIYA ---------------- #

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.first_name}! Hisobingiz muvaffaqiyatli ochildi.")
            return redirect('catalog')
    else:
        form = UserRegisterForm()

    return render(request, 'lms/auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Qaytganingiz bilan, {user.get_full_name() or user.username}!")
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else 'catalog')
        else:
            messages.error(request, "Login yoki parol noto'g'ri kiritildi.")
    else:
        form = AuthenticationForm()

    return render(request, 'lms/auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Tizimdan chiqdingiz.")
    return redirect('home')
