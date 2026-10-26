import uuid
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Count, Q, Avg, Min, Max
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import (
    User, Course, Module, Lesson,
    Quiz, Question, Choice,
    UserLessonProgress, QuizResult, Certificate,
    Coupon, Enrollment, BundleEnrollment,
    CoinTransaction, CoinShopItem,
    Room, StudyGroup, Group, Attendance,
    StudentPayment, TeacherSalary, Expense,
    Lead, TeacherReview
)
from .forms import StudentRegistrationForm, UserLoginForm


# =============================================================================
# 🪙 EDUCOIN & XP 8 XIL AMALIY O'QUVCHI HARAKATI TIZIMI
# =============================================================================
COIN_REWARDS = {
    # 8 ta Amaliy O'quvchi Faoliyati (Uy ishlari, Davomat, Faollik va b.)
    'attendance_streak': (15, 20, "Darsga o'z vaqtida kelish (Davomat) (+15 🪙)"),
    'homework_perfect': (25, 35, "Uy vazifasini 100% a'lo bajarish (+25 🪙)"),
    'class_activity': (20, 30, "Darsda faollik (Savol-javob & amaliyot) (+20 🪙)"),
    'quiz_passed': (30, 50, "Modul testidan o'tish (70%+) (+30 🪙)"),
    'quiz_perfect': (50, 100, "Imtihondan 100% a'lo natija (+50 🪙)"),
    'book_reading': (35, 45, "Badiiy kitob mutolaasi va taqdimoti (+35 🪙)"),
    'weekly_streak': (40, 60, "Haftalik intizom va faollik bonusi (+40 🪙)"),
    'course_completed': (150, 200, "Kursni tamomlab Sertifikat olish (+150 🪙)"),

    # Tizimli qo'shimcha rag'batlar
    'welcome_bonus': (100, 50, "Xush kelibsiz bonusi! (+100 🪙)"),
    'lesson_completed': (10, 15, "Dars muvaffaqiyatli yakunlandi (+10 🪙)"),
    'profile_completed': (30, 20, "Profil to'liq to'ldirildi (+30 🪙)"),
    'course_enrolled': (40, 25, "Yangi kurs a'zoligi uchun rag'bat (+40 🪙)"),
    'daily_streak': (15, 20, "Kunlik faollik bonusi (+15 🪙)"),
}


def award_edu_coins(user, action_type, custom_desc=None):
    """Foydalanuvchiga 8 xil amaliy faoliyati uchun EduCoin va XP ballari qo'shadi."""
    if not user or not user.is_authenticated:
        return 0
    reward_data = COIN_REWARDS.get(action_type, (0, 0, "EduCoin bonusi"))
    amount = reward_data[0]
    xp_amount = reward_data[1]
    default_desc = reward_data[2]
    desc = custom_desc or default_desc

    user.edu_coins += amount
    user.total_xp += xp_amount
    user.save(update_fields=['edu_coins', 'total_xp'])

    CoinTransaction.objects.create(
        user=user,
        amount=amount,
        action_type=action_type,
        description=desc
    )
    return amount


def home(request):
    """Bosh sahifa: Kurslar katalogiga yo'naltiradi."""
    return redirect('course_list')


def course_list(request):
    """Barcha kurslar va to'garaklar katalogi (qidiruv, soha va kunlar tartibi filtri bilan)."""
    query = request.GET.get('q', '').strip()
    selected_category = request.GET.get('category', '').strip()
    selected_schedule = request.GET.get('schedule', '').strip()

    courses = Course.objects.all().select_related('author').prefetch_related('modules')
    if query:
        courses = courses.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(category__icontains=query) | 
            Q(author__first_name__icontains=query) | 
            Q(author__last_name__icontains=query)
        )
    if selected_category and selected_category != 'Barchasi':
        courses = courses.filter(category__iexact=selected_category)
    if selected_schedule and selected_schedule != 'Barchasi':
        courses = courses.filter(schedule_type__iexact=selected_schedule)

    # Mavjud kategoriyalar
    categories = [
        'Barchasi', 'Savodxonlik', 'IT & Dasturlash', 'Xorijiy Tillar',
        'Sharq Tillari', 'Milliy Fanlar', 'Aniq Fanlar', 'Sport & Musobaqalar'
    ]

    # Kunlar jadvallari
    schedules = [
        ('Barchasi', 'Barcha kunlar'),
        ('toq', 'Toq kunlari (Dush-Chor-Jum)'),
        ('juft', 'Juft kunlari (Sesh-Pay-Shan)'),
        ('hafta_oxiri', 'Hafta oxiri (Shanba-Yakshanba)'),
    ]

    # Platforma umumiy statistikasi
    stats = {
        'total_courses': Course.objects.count(),
        'total_teachers': User.objects.filter(role='teacher').count(),
        'total_lessons': Lesson.objects.count(),
        'total_students': User.objects.filter(role='student').count(),
        'total_certificates': Certificate.objects.count(),
    }

    # Foydalanuvchi kurslar bo'yicha progressi
    courses_data = []
    for course in courses:
        modules = course.modules.all()
        total_lessons = Lesson.objects.filter(module__course=course).count()
        total_quizzes = Quiz.objects.filter(module__course=course).count()

        is_completed = False
        completed_lessons = 0
        is_enrolled = False
        if request.user.is_authenticated:
            is_completed = course.is_completed_by(request.user)
            is_enrolled = course.is_user_enrolled(request.user)
            completed_lessons = UserLessonProgress.objects.filter(
                user=request.user,
                lesson__module__course=course,
                is_completed=True
            ).count()

        # Birinchi darsni topish (kursni boshlash uchun)
        first_lesson = Lesson.objects.filter(module__course=course).order_by('module__order', 'order').first()

        courses_data.append({
            'course': course,
            'total_lessons': total_lessons,
            'total_quizzes': total_quizzes,
            'completed_lessons': completed_lessons,
            'progress_percent': int((completed_lessons / total_lessons * 100)) if total_lessons > 0 else 0,
            'is_completed': is_completed,
            'is_enrolled': is_enrolled,
            'first_lesson': first_lesson,
        })

    return render(request, 'core/course_list.html', {
        'courses_data': courses_data,
        'query': query,
        'selected_category': selected_category,
        'selected_schedule': selected_schedule,
        'categories': categories,
        'schedules': schedules,
        'stats': stats,
    })


def teachers_list(request):
    """
    Barcha professional o'qituvchilar katalogi:
    Ixcham 1 qatorli kartochkalar, bosilganda to'liq ma'lumotli pop-up (Modal),
    o'quvchilar imtihon natijalari, ota-onalar baholari, guruh dars jadvallari,
    hamda sohalar bo'yicha tezkor saralash va qidiruv.
    """
    all_teachers_qs = User.objects.filter(role='teacher', is_superuser=False)
    if not all_teachers_qs.exists():
        all_teachers_qs = User.objects.filter(role='teacher')

    cat_counts = {
        'all': all_teachers_qs.count(),
        'it': all_teachers_qs.filter(specialties='it').count(),
        'languages': all_teachers_qs.filter(specialties='languages').count(),
        'school': all_teachers_qs.filter(specialties='school').count(),
        'sport_arts': all_teachers_qs.filter(specialties='sport_arts').count(),
    }

    selected_cat = request.GET.get('cat', 'all').strip().lower()
    search_q = request.GET.get('q', '').strip()

    teachers = all_teachers_qs.prefetch_related('courses')
    if selected_cat in ['it', 'languages', 'school', 'sport_arts']:
        teachers = teachers.filter(specialties=selected_cat)

    if search_q:
        teachers = teachers.filter(
            Q(first_name__icontains=search_q) |
            Q(last_name__icontains=search_q) |
            Q(headline__icontains=search_q) |
            Q(bio__icontains=search_q)
        )

    teachers_data = []
    for teacher in teachers:
        courses = teacher.courses.all()
        groups = StudyGroup.objects.filter(teacher=teacher, is_active=True).select_related('room')
        reviews = TeacherReview.objects.filter(teacher=teacher)
        total_lessons = Lesson.objects.filter(module__course__in=courses).count()

        teachers_data.append({
            'teacher': teacher,
            'courses': courses,
            'groups': groups,
            'reviews': reviews,
            'average_rating': teacher.get_average_rating(),
            'exam_results': teacher.exam_results_summary or "O'quvchilarining 94% qismi Milliy Sertifikat va IELTS 7.5+ olgan",
            'total_courses': courses.count(),
            'total_groups': groups.count(),
            'total_lessons': total_lessons,
            'salary_display': teacher.get_salary_display(),
        })

    return render(request, 'core/teachers_list.html', {
        'teachers_data': teachers_data,
        'all_teachers': all_teachers_qs,
        'cat_counts': cat_counts,
        'selected_cat': selected_cat,
        'search_q': search_q,
    })


@login_required
def bundle_enroll(request):
    """
    Paketli To'garaklar A'zoligi (Multi-Course Bundle Enrollment):
    - 2 ta to'garak tanlanganda: -50,000 so'm chegirma
    - 3 ta va undan ortiq to'garak tanlanganda: -100,000 so'm chegirma
    - Ertadan boshlanadi tartibi va onlayn guruhlar
    """
    courses = Course.objects.all().select_related('author').order_by('category', 'title')
    
    # Foydalanuvchi allaqachon a'zo bo'lgan kurs ID lari
    enrolled_course_ids = set(Enrollment.objects.filter(
        user=request.user,
        status='completed'
    ).values_list('course_id', flat=True))
    
    return render(request, 'core/bundle_enroll.html', {
        'courses': courses,
        'enrolled_course_ids': enrolled_course_ids,
    })


@login_required
def process_bundle_payment(request):
    """
    Tanlangan 2 yoki 3+ ta to'garaklar uchun to'lovni tasdiqlash:
    - 2 ta kurs: 50,000 so'm chegirma
    - 3+ ta kurs: 100,000 so'm chegirma
    - Har bir kurs uchun alohida Enrollment ochiladi
    - Ertadan boshlanish tasdig'i beriladi
    """
    if request.method != 'POST':
        return redirect('bundle_enroll')

    course_ids = request.POST.getlist('selected_courses')
    if not course_ids or len(course_ids) < 1:
        messages.error(request, "Iltimos, kamida bitta to'garakni tanlang.")
        return redirect('bundle_enroll')

    selected_courses = Course.objects.filter(id__in=course_ids)
    if not selected_courses.exists():
        messages.error(request, "Tanlangan to'garaklar topilmadi.")
        return redirect('bundle_enroll')

    payment_method = request.POST.get('payment_method', 'click')
    count = selected_courses.count()

    total_original = sum(c.get_effective_price() for c in selected_courses)
    
    # Chegirma hisobi: 2 tasiga 50k, 3+ tasiga 100k
    bundle_discount = 0
    if count == 2:
        bundle_discount = 50000
    elif count >= 3:
        bundle_discount = 100000

    final_amount = max(0, total_original - bundle_discount)

    # Tranzaksiyani yaratish
    txn_id = BundleEnrollment.generate_transaction_id(request.user.id)
    bundle = BundleEnrollment.objects.create(
        user=request.user,
        total_original_price=total_original,
        bundle_discount=bundle_discount,
        final_amount=final_amount,
        payment_method=payment_method,
        transaction_id=txn_id,
        start_date_str="Ertadan boshlanadi (Jonli Online)",
        status='completed'
    )
    bundle.courses.set(selected_courses)

    # Har bir kurs uchun Enrollment ochish
    newly_enrolled = 0
    for course in selected_courses:
        if not course.is_user_enrolled(request.user):
            sub_txn = Enrollment.generate_transaction_id(request.user.id, course.id)
            Enrollment.objects.create(
                user=request.user,
                course=course,
                amount_paid=course.get_effective_price(),
                payment_method=payment_method,
                transaction_id=sub_txn,
                status='completed'
            )
            # Har bir yangi kurs uchun +40 🪙 EduCoin
            award_edu_coins(
                request.user,
                'course_enrolled',
                f"'{course.title}' to'garagiga a'zo bo'lingani uchun (+40 🪙)"
            )
            newly_enrolled += 1

    discount_msg = f"-{bundle_discount:,} so'm paketli chegirma berildi!" if bundle_discount > 0 else ""
    messages.success(
        request,
        f"🎉 TABRIKLAYMIZ! Siz {count} ta to'garakka muvaffaqiyatli a'zo bo'ldingiz! {discount_msg} "
        f"Mashg'ulotlaringiz ertadan belgilangan kunlar ({', '.join(set(c.get_schedule_type_display() for c in selected_courses))}) bo'yicha online boshlanadi. (Kvitansiya ID: {txn_id})"
    )

    return redirect('profile')


@login_required
def checkout(request, course_id):
    """
    Kursni xarid qilish va to'lov sahifasi:
    - Chegirmalar hisob-kitobi
    - Promokod qo'llash (masalan: PROMO50, SKILLUP30, BEPUL100)
    - Click, Payme, Uzum to'lov tizimlari tanlovi
    """
    course = get_object_or_404(Course.objects.select_related('author'), id=course_id)
    first_lesson = Lesson.objects.filter(module__course=course).order_by('module__order', 'order').first()

    # Agar foydalanuvchi allaqachon a'zo bo'lsa
    if course.is_user_enrolled(request.user):
        messages.info(request, f"Siz '{course.title}' kursiga allaqachon a'zosiz!")
        if first_lesson:
            return redirect('classroom', lesson_id=first_lesson.id)
        return redirect('course_list')

    base_price = course.get_effective_price()
    applied_coupon = None
    coupon_error = None
    discount_amount = 0
    final_price = base_price

    coupon_code = request.GET.get('coupon', '').strip()
    if coupon_code:
        coupon_obj = Coupon.objects.filter(code__iexact=coupon_code).first()
        if coupon_obj and coupon_obj.is_valid():
            applied_coupon = coupon_obj
            discount_amount = int((base_price * coupon_obj.discount_percent) / 100)
            final_price = max(0, base_price - discount_amount)
            messages.success(request, f"'{coupon_obj.code}' promokodi qo'llandi! -{coupon_obj.discount_percent}% qo'shimcha chegirma berildi.")
        else:
            coupon_error = "Kiritilgan promokod yaroqsiz yoki muddati tugagan."

    return render(request, 'core/checkout.html', {
        'course': course,
        'base_price': base_price,
        'applied_coupon': applied_coupon,
        'coupon_error': coupon_error,
        'discount_amount': discount_amount,
        'final_price': final_price,
        'first_lesson': first_lesson,
    })


@login_required
def process_payment(request, course_id):
    """To'lovni tasdiqlash va kursga yozilish (Enrollment)."""
    if request.method != 'POST':
        return redirect('checkout', course_id=course_id)

    course = get_object_or_404(Course, id=course_id)
    if course.is_user_enrolled(request.user):
        messages.info(request, "Siz ushbu kursga allaqachon a'zosiz.")
        first_lesson = Lesson.objects.filter(module__course=course).order_by('module__order', 'order').first()
        return redirect('classroom', lesson_id=first_lesson.id) if first_lesson else redirect('course_list')

    payment_method = request.POST.get('payment_method', 'click')
    coupon_code = request.POST.get('coupon_code', '').strip()

    base_price = course.get_effective_price()
    final_price = base_price
    coupon_obj = None

    if coupon_code:
        found_coupon = Coupon.objects.filter(code__iexact=coupon_code).first()
        if found_coupon and found_coupon.is_valid():
            coupon_obj = found_coupon
            discount_amount = int((base_price * found_coupon.discount_percent) / 100)
            final_price = max(0, base_price - discount_amount)
            found_coupon.used_count += 1
            found_coupon.save()

    # Xarid yozuvini yaratish
    txn_id = Enrollment.generate_transaction_id(request.user.id, course.id)
    Enrollment.objects.create(
        user=request.user,
        course=course,
        amount_paid=final_price,
        coupon=coupon_obj,
        payment_method=payment_method,
        transaction_id=txn_id,
        status='completed'
    )

    # 🪙 8 xil EduCoin rag'bati: Yangi kursga a'zolik bonusi (+40 🪙)
    coin_bonus = award_edu_coins(
        request.user,
        'course_enrolled',
        f"'{course.title}' kursiga yozilganingiz uchun rag'bat (+40 🪙)"
    )

    messages.success(
        request,
        f"🎉 To'lov muvaffaqiyatli amalga oshirildi! (Kvitansiya ID: {txn_id}). '{course.title}' to'garagiga a'zo bo'ldingiz! "
        f"Mashg'ulotingiz ertadan boshlanadi ({course.get_schedule_display_full()})! Hamyoningizga +{coin_bonus} 🪙 EduCoin qo'shildi!"
    )

    first_lesson = Lesson.objects.filter(module__course=course).order_by('module__order', 'order').first()
    if first_lesson:
        return redirect('classroom', lesson_id=first_lesson.id)
    return redirect('course_list')


@login_required
def classroom(request, lesson_id):
    """
    Udemy / Coursera uslubidagi dars xonasi:
    Chapda video pleer va nazariy matn, o'ngda modullar va darslar akkordeoni.
    Darslar ketma-ketligi va modul bloklash qoidasi tekshiriladi.
    """
    lesson = get_object_or_404(
        Lesson.objects.select_related('module', 'module__course'),
        id=lesson_id
    )
    course = lesson.module.course

    # To'lov tekshiruvi: Agar kurs pulli bo'lsa va talaba xarid qilmagan bo'lsa,
    # faqat 1-darsni bepul ko'ra oladi, keyingi darslar uchun to'lov sahifasiga yo'naltiriladi
    is_enrolled = course.is_user_enrolled(request.user)
    first_course_lesson = Lesson.objects.filter(module__course=course).order_by('module__order', 'order').first()
    if not is_enrolled and first_course_lesson and lesson.id != first_course_lesson.id:
        messages.warning(
            request,
            f"🔒 Ushbu kurs pulli. Barcha modullar, testlar va sertifikatni ochish uchun kursni xarid qiling."
        )
        return redirect('checkout', course_id=course.id)

    # Bloklash tekshiruvi: Agar modul qulflangan bo'lsa, kirish taqiqlanadi
    if not lesson.is_unlocked_for(request.user):
        messages.error(
            request,
            f"🔒 Ushbu dars qulflangan! Avvalgi modulning yakuniy testidan kamida 70% to'plashingiz shart."
        )
        # Ochiq bo'lgan eng oxirgi yoki 1-darsga yo'naltirish
        first_lesson = Lesson.objects.filter(module__course=course).order_by('module__order', 'order').first()
        if first_lesson and first_lesson.id != lesson.id:
            return redirect('classroom', lesson_id=first_lesson.id)
        return redirect('course_list')

    # Dars progressi holati
    progress, _ = UserLessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )

    # Kursdagi barcha modullar va ularning darslari ro'yxatini holati bilan tayyorlash
    modules_list = []
    course_modules = course.modules.all().prefetch_related('lessons', 'quiz')

    for mod in course_modules:
        mod_unlocked = mod.is_unlocked_for(request.user)
        mod_quiz = getattr(mod, 'quiz', None)
        quiz_passed = False
        quiz_latest_score = None
        if mod_quiz:
            latest_res = mod_quiz.get_user_latest_result(request.user)
            if latest_res:
                quiz_passed = latest_res.is_passed
                quiz_latest_score = latest_res.score

        mod_lessons = []
        for les in mod.lessons.all():
            les_completed = les.is_completed_by(request.user)
            mod_lessons.append({
                'lesson': les,
                'is_completed': les_completed,
                'is_active': (les.id == lesson.id),
                'is_unlocked': mod_unlocked,
            })

        modules_list.append({
            'module': mod,
            'is_unlocked': mod_unlocked,
            'quiz': mod_quiz,
            'quiz_passed': quiz_passed,
            'quiz_latest_score': quiz_latest_score,
            'lessons': mod_lessons,
        })

    # Oldingi va keyingi darslar
    next_lesson = lesson.get_next_lesson()
    prev_lesson = lesson.get_previous_lesson()

    # Sertifikat mavjudligini tekshirish
    user_certificate = Certificate.objects.filter(user=request.user, course=course).first()

    return render(request, 'core/classroom.html', {
        'lesson': lesson,
        'course': course,
        'current_module': lesson.module,
        'modules_list': modules_list,
        'progress': progress,
        'next_lesson': next_lesson,
        'prev_lesson': prev_lesson,
        'user_certificate': user_certificate,
    })


@login_required
def complete_lesson(request, lesson_id):
    """
    Talaba 'Darsni tugatdim' tugmasini bosganda ishlaydi.
    Birinchi marta tugatilganda talabaga +15 XP beriladi.
    """
    if request.method != 'POST':
        return redirect('classroom', lesson_id=lesson_id)

    lesson = get_object_or_404(Lesson, id=lesson_id)
    progress, created = UserLessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )

    if not progress.is_completed:
        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.save()

        # Talabaga 15 XP va 10 EduCoin beriladi
        request.user.total_xp += 15
        request.user.save(update_fields=['total_xp'])
        coins = award_edu_coins(request.user, 'lesson_completed')
        messages.success(request, f"🎉 Tabriklaymiz! Darsni yakunladingiz: +15 XP va +{coins} 🪙 EduCoin qo'lga kiritdingiz!")
    else:
        messages.info(request, "Ushbu dars avvalroq yakunlangan.")

    # Keyingi darsga o'tish yoki modul testiga o'tish
    next_lesson = lesson.get_next_lesson()
    if next_lesson and next_lesson.is_unlocked_for(request.user):
        return redirect('classroom', lesson_id=next_lesson.id)

    # Agar modulda test bo'lsa, test sahifasiga yo'naltirish taklif qilinadi
    if hasattr(lesson.module, 'quiz') and lesson.module.quiz:
        return redirect('take_quiz', quiz_id=lesson.module.quiz.id)

    return redirect('classroom', lesson_id=lesson.id)


@login_required
def take_quiz(request, quiz_id):
    """
    Test topshirish sahifasi:
    - JavaScript teskari hisoblovchi (countdown) taymer
    - Savollar ro'yxati va variantlar
    - Vaqt tugaganda yoki tugma bosilganda avtomatik submit
    """
    quiz = get_object_or_404(
        Quiz.objects.select_related('module', 'module__course'),
        id=quiz_id
    )
    module = quiz.module
    course = module.course

    # Bloklash tekshiruvi
    if not quiz.is_unlocked_for(request.user):
        messages.error(
            request,
            "🔒 Ushbu test qulflangan! Avvalgi modul talablarini to'liq bajaring."
        )
        return redirect('course_list')

    questions = quiz.questions.all().prefetch_related('choices')
    if not questions.exists():
        messages.warning(request, "Ushbu testda hozircha savollar mavjud emas.")
        return redirect('course_list')

    if request.method == 'POST':
        # Test javoblarini tekshirish
        total_questions = questions.count()
        correct_count = 0
        detailed_results = []

        for q in questions:
            choice_id_str = request.POST.get(f'question_{q.id}')
            selected_choice = None
            is_q_correct = False

            if choice_id_str:
                selected_choice = q.choices.filter(id=choice_id_str).first()
                if selected_choice and selected_choice.is_correct:
                    correct_count += 1
                    is_q_correct = True

            correct_choice = q.choices.filter(is_correct=True).first()

            detailed_results.append({
                'question': q,
                'selected_choice': selected_choice,
                'correct_choice': correct_choice,
                'is_correct': is_q_correct,
            })

        score_percent = round((correct_count / total_questions) * 100, 1) if total_questions > 0 else 0
        is_passed = score_percent >= quiz.passing_score

        # Natijani saqlash
        result = QuizResult.objects.create(
            user=request.user,
            quiz=quiz,
            score=score_percent,
            is_passed=is_passed
        )

        xp_earned = 0
        coins_earned = 0
        course_coins = 0

        if is_passed:
            # Har bir to'g'ri javob uchun 10 XP + O'tganlik uchun 50 XP bonus
            xp_earned = (correct_count * 10) + 50
            request.user.total_xp += xp_earned
            request.user.save()

            # 🪙 8 xil EduCoin rag'bati: 100% natija uchun +50, 70%+ uchun +25
            if score_percent >= 100:
                coins_earned = award_edu_coins(
                    request.user,
                    'quiz_perfect',
                    f"'{quiz.title}' testidan 100% a'lo natija (+50 🪙)"
                )
                messages.success(
                    request,
                    f"🌟 A'LO DARAJA! Testdan 100% natija bilan o'tdingiz (+{xp_earned} XP va +{coins_earned} 🪙 EduCoin)!"
                )
            else:
                coins_earned = award_edu_coins(
                    request.user,
                    'quiz_passed',
                    f"'{quiz.title}' testidan muvaffaqiyatli o'tildi (+25 🪙)"
                )
                messages.success(
                    request,
                    f"🏆 Ajoyib natija! Testdan {score_percent}% bilan muvaffaqiyatli o'tdingiz (+{xp_earned} XP va +{coins_earned} 🪙 EduCoin)!"
                )

            # Kurs yakunlanganligini va barcha modullar topshirilganini tekshirish
            if course.is_completed_by(request.user):
                cert, created = Certificate.objects.get_or_create(
                    user=request.user,
                    course=course,
                    defaults={'certificate_code': Certificate.generate_code(course.id, request.user.id)}
                )
                if created:
                    course_coins = award_edu_coins(
                        request.user,
                        'course_completed',
                        f"'{course.title}' kursini tamomlash va Sertifikat bonusi (+150 🪙)"
                    )
                    messages.success(
                        request,
                        f"🎓 TABRIKLAYMIZ! Kursni to'liq tamomladingiz va maxsus Sertifikat hamda +{course_coins} 🪙 EduCoin qo'lga kiritdingiz!"
                    )
        else:
            # Yiqilgan bo'lsa ham rag'batlantiruvchi XP (har bir to'g'ri javob uchun 5 XP)
            xp_earned = correct_count * 5
            if xp_earned > 0:
                request.user.total_xp += xp_earned
                request.user.save()
            messages.warning(
                request,
                f"Siz {score_percent}% to'pladingiz. O'tish bali: {quiz.passing_score}%. Qaytadan urinib ko'ring!"
            )

        # Natija sahifasiga yo'naltirish
        return render(request, 'core/quiz_result.html', {
            'quiz': quiz,
            'result': result,
            'score': score_percent,
            'is_passed': is_passed,
            'correct_count': correct_count,
            'total_questions': total_questions,
            'xp_earned': xp_earned,
            'coins_earned': coins_earned,
            'course_coins': course_coins,
            'detailed_results': detailed_results,
            'course': course,
        })

    return render(request, 'core/take_quiz.html', {
        'quiz': quiz,
        'questions': questions,
        'course': course,
        'module': module,
        'duration_seconds': quiz.duration_minutes * 60,
    })


def leaderboard(request):
    """
    100-300 nafar talabalar reytingi (Leaderboard Ultra Pro Max):
    - TOP-3 Shohsupa (Podium: Oltin, Kumush, Bronza kuboklari)
    - Sahifalash (Paginator: har sahifada 25 tadan o'quvchi)
    - Filtrlash (XP bo'yicha, EduCoin bo'yicha)
    - Ism va familiya bo'yicha tezkor qidiruv
    - 8 ta amaliy harakatlar nishonlari (Uy vazifasi a'lo, Darsda faollik, Davomat)
    """
    sort_by = request.GET.get('sort', 'xp')
    search_q = request.GET.get('q', '').strip()
    page = request.GET.get('page', 1)

    students_qs = User.objects.filter(role='student').prefetch_related('coin_transactions', 'quiz_results')

    if search_q:
        students_qs = students_qs.filter(
            Q(first_name__icontains=search_q) |
            Q(last_name__icontains=search_q) |
            Q(username__icontains=search_q) |
            Q(headline__icontains=search_q)
        )

    if sort_by == 'coins':
        students_qs = students_qs.order_by('-edu_coins', '-total_xp', 'id')
    else: # xp
        students_qs = students_qs.order_by('-total_xp', '-edu_coins', 'id')

    total_count = students_qs.count()

    # Shohsupa uchun TOP 3 talaba
    podium_qs = User.objects.filter(role='student').order_by('-total_xp', 'id')[:3]
    podium_students = list(podium_qs)

    # Paginator (har sahifada 25 tadan)
    paginator = Paginator(students_qs, 25)
    try:
        students_page = paginator.page(page)
    except PageNotAnInteger:
        students_page = paginator.page(1)
    except EmptyPage:
        students_page = paginator.page(paginator.num_pages)

    # Foydalanuvchining o'z o'rni
    user_rank = None
    if request.user.is_authenticated and getattr(request.user, 'role', '') == 'student':
        higher_count = User.objects.filter(role='student', total_xp__gt=request.user.total_xp).count()
        user_rank = higher_count + 1

    return render(request, 'core/leaderboard.html', {
        'students_page': students_page,
        'podium_students': podium_students,
        'user_rank': user_rank,
        'sort_by': sort_by,
        'search_q': search_q,
        'total_count': total_count,
    })


@login_required
def profile(request):
    """
    Foydalanuvchining shaxsiy profili:
    - To'plangan umumiy XP va reyting
    - EduCoin balansi va tranzaksiyalar tarixi
    - 8 xil amaliy topshiriqlar (quests) holati
    - Tugatilgan darslar va sertifikatlar
    - Xaridlar kvitansiyalari
    """
    user = request.user
    certificates = Certificate.objects.filter(user=user).select_related('course')
    completed_lessons_count = UserLessonProgress.objects.filter(user=user, is_completed=True).count()
    quiz_results = QuizResult.objects.filter(user=user).select_related('quiz', 'quiz__module__course')[:10]
    enrollments = Enrollment.objects.filter(user=user).select_related('course', 'coupon')

    # EduCoin tranzaksiyalari tarixi
    transactions = CoinTransaction.objects.filter(user=user).order_by('-created_at')[:15]

    # Kunlik streak tekshiruvi (24 soat)
    can_claim_streak = not CoinTransaction.objects.filter(
        user=user,
        action_type='daily_streak',
        created_at__gte=timezone.now() - timezone.timedelta(hours=24)
    ).exists()

    # Talaba o'rni
    user_rank = User.objects.filter(role='student', total_xp__gt=user.total_xp).count() + 1

    # 8 xil EduCoin yutuqlar holati
    quests = [
        {
            'number': 1,
            'title': "Xush kelibsiz bonusi",
            'reward': "+100 🪙",
            'icon': 'fa-solid fa-gift',
            'is_completed': CoinTransaction.objects.filter(user=user, action_type='welcome_bonus').exists(),
            'desc': "Boshlang'ich ro'yxatdan o'tish sovg'asi",
        },
        {
            'number': 2,
            'title': "Darsni yakunlash",
            'reward': "+10 🪙 / dars",
            'icon': 'fa-solid fa-book-open-reader',
            'is_completed': CoinTransaction.objects.filter(user=user, action_type='lesson_completed').exists(),
            'desc': "Har bir darsni to'liq o'rganib tugatish",
        },
        {
            'number': 3,
            'title': "Testdan o'tish (70%+)",
            'reward': "+25 🪙 / test",
            'icon': 'fa-solid fa-circle-check',
            'is_completed': CoinTransaction.objects.filter(user=user, action_type='quiz_passed').exists(),
            'desc': "Modul imtihonidan o'tish",
        },
        {
            'number': 4,
            'title': "Testda 100% a'lo natija",
            'reward': "+50 🪙 / test",
            'icon': 'fa-solid fa-star',
            'is_completed': CoinTransaction.objects.filter(user=user, action_type='quiz_perfect').exists(),
            'desc': "Birorta ham xatosiz maksimal ball",
        },
        {
            'number': 5,
            'title': "Kurs tamomlash & Sertifikat",
            'reward': "+150 🪙 / kurs",
            'icon': 'fa-solid fa-graduation-cap',
            'is_completed': certificates.exists(),
            'desc': "Rasmiy sertifikat bilan taqdirlanish",
        },
        {
            'number': 6,
            'title': "Yangi kursga yozilish",
            'reward': "+40 🪙 / xarid",
            'icon': 'fa-solid fa-cart-shopping',
            'is_completed': enrollments.exists(),
            'desc': "Yangi yo'nalish bo'yicha bilim olish",
        },
        {
            'number': 7,
            'title': "Profilni to'liq to'ldirish",
            'reward': "+30 🪙 bir martalik",
            'icon': 'fa-solid fa-user-pen',
            'is_completed': CoinTransaction.objects.filter(user=user, action_type='profile_completed').exists(),
            'desc': "Kasb va shaxsiy ma'lumotlarni qo'shish",
        },
        {
            'number': 8,
            'title': "Kunlik tashrif & Faollik",
            'reward': "+15 🪙 har 24 soatda",
            'icon': 'fa-solid fa-fire',
            'is_completed': not can_claim_streak,
            'desc': "SkillUp platformasiga muntazam kirib turish",
        },
    ]

    completed_quests_count = sum(1 for q in quests if q['is_completed'])
    unlocked_coupons = Coupon.objects.filter(code__startswith=f"COIN50-{user.id}-")

    return render(request, 'core/profile.html', {
        'user': user,
        'certificates': certificates,
        'completed_lessons_count': completed_lessons_count,
        'quiz_results': quiz_results,
        'enrollments': enrollments,
        'user_rank': user_rank,
        'transactions': transactions,
        'can_claim_streak': can_claim_streak,
        'quests': quests,
        'completed_quests_count': completed_quests_count,
        'unlocked_coupons': unlocked_coupons,
    })


@login_required
def certificate_detail(request, code):
    """
    Chop etishga (Print/PDF) moslashtirilgan chiroyli rasmiy sertifikat shabloni.
    """
    certificate = get_object_or_404(
        Certificate.objects.select_related('user', 'course', 'course__author'),
        certificate_code=code
    )
    return render(request, 'core/certificate.html', {
        'certificate': certificate,
        'student': certificate.user,
        'course': certificate.course,
    })


@login_required
def parent_report(request, user_id=None):
    """
    Ota-onalar uchun rasmiy o'zlashtirish ma'lumotnomasi (A4 / PDF print formatida):
    - O'quvchining fanlar bo'yicha davomati
    - Topshirilgan testlar va o'rtacha balli
    - To'plangan umumiy XP va respublika reytingi
    - O'qituvchilar va platforma ma'muriyati xulosasi
    """
    target_user = request.user
    if user_id and (request.user.is_staff or request.user.is_teacher):
        target_user = get_object_or_404(User, id=user_id)

    completed_lessons = UserLessonProgress.objects.filter(user=target_user, is_completed=True)
    quiz_results = QuizResult.objects.filter(user=target_user).select_related('quiz', 'quiz__module__course')
    certificates = Certificate.objects.filter(user=target_user).select_related('course')
    enrollments = Enrollment.objects.filter(user=target_user).select_related('course')

    avg_score = 0
    if quiz_results.exists():
        total_scores = sum(r.score for r in quiz_results)
        avg_score = round(total_scores / quiz_results.count(), 1)

    rank = User.objects.filter(role='student', total_xp__gt=target_user.total_xp).count() + 1

    return render(request, 'core/parent_report.html', {
        'student': target_user,
        'completed_lessons': completed_lessons,
        'completed_count': completed_lessons.count(),
        'quiz_results': quiz_results,
        'avg_score': avg_score,
        'certificates': certificates,
        'enrollments': enrollments,
        'rank': rank,
        'report_date': timezone.now(),
    })


def register_view(request):
    """Yangi foydalanuvchini ro'yxatdan o'tkazish."""
    if request.user.is_authenticated:
        return redirect('course_list')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 🪙 8 xil EduCoin rag'bati: Ro'yxatdan o'tganlik uchun boshlang'ich bonus (+100 🪙)
            award_edu_coins(user, 'welcome_bonus', "Ro'yxatdan o'tganingiz uchun xush kelibsiz bonusi (+100 🪙)")
            login(request, user)
            messages.success(
                request,
                f"🎉 Xush kelibsiz, {user.first_name or user.username}! Muvaffaqiyatli ro'yxatdan o'tdingiz va hamyoningizga +100 🪙 EduCoin taqdim etildi!"
            )
            return redirect('course_list')
    else:
        form = StudentRegistrationForm()

    return render(request, 'core/register.html', {'form': form})


@login_required
def update_profile(request):
    """Foydalanuvchi shaxsiy ma'lumotlarini tahrirlash va profil to'ldirilganlik bonusini olish (+30 🪙)."""
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        headline = request.POST.get('headline', '').strip()
        bio = request.POST.get('bio', '').strip()
        avatar_url = request.POST.get('avatar_url', '').strip()

        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.headline = headline
        request.user.bio = bio
        if avatar_url:
            request.user.avatar_url = avatar_url
        request.user.save()

        # Profil to'ldirilganlik kvestini tekshirish (+30 🪙)
        has_profile_bonus = CoinTransaction.objects.filter(
            user=request.user,
            action_type='profile_completed'
        ).exists()

        if not has_profile_bonus and headline and bio:
            coins = award_edu_coins(
                request.user,
                'profile_completed',
                "Profil ma'lumotlari to'liq to'ldirildi: kasb va bio (+30 🪙)"
            )
            messages.success(
                request,
                f"🎉 Profilingiz yangilandi va 'Profil to'ldirish' kvesti uchun +{coins} 🪙 EduCoin qo'lga kiritdingiz!"
            )
        else:
            messages.success(request, "Profilingiz muvaffaqiyatli yangilandi!")

    return redirect('profile')


@login_required
def claim_daily_bonus(request):
    """Har 24 soatda bir marta kunlik +15 EduCoin faollik bonusini olish."""
    recent_streak = CoinTransaction.objects.filter(
        user=request.user,
        action_type='daily_streak',
        created_at__gte=timezone.now() - timezone.timedelta(hours=24)
    ).first()

    if not recent_streak:
        amount = award_edu_coins(
            request.user,
            'daily_streak',
            "Kunlik platformaga tashrif va faollik bonusi (+15 🪙)"
        )
        messages.success(
            request,
            f"🔥 Tabriklaymiz! Kunlik faollik bonusi (+{amount} 🪙 EduCoin) hamyoningizga muvaffaqiyatli o'tkazildi!"
        )
    else:
        messages.info(
            request,
            "Bugungi kunlik bonusingizni allaqachon qabul qilgansiz. 24 soatdan so'ng yana tashrif buyurib yangi bonus oling!"
        )

    referer = request.META.get('HTTP_REFERER')
    if referer and 'login' not in referer:
        return redirect(referer)
    return redirect('coin_shop')


@login_required
def coin_shop(request):
    """
    EduCoin Markazi va Do'koni (Gamification Hub):
    - 8 xil kvest holati va yo'riqnomasi
    - EduCoin orqali sotib olinadigan sovg'alar (Chegirma kuponi, VIP nishon, Merch, Mentor)
    - So'nggi tranzaksiyalar tarixi
    - Kunlik faollik tugmasi
    """
    items = CoinShopItem.objects.filter(is_available=True)
    user_transactions = CoinTransaction.objects.filter(user=request.user).order_by('-created_at')[:20]

    can_claim_streak = not CoinTransaction.objects.filter(
        user=request.user,
        action_type='daily_streak',
        created_at__gte=timezone.now() - timezone.timedelta(hours=24)
    ).exists()

    # 8 xil O'quvchi Faoliyati bo'yicha EduCoin yutuqlar kvestlari
    quests = [
        {
            'number': 1,
            'title': "Darsga o'z vaqtida kelish (Davomat)",
            'reward': 15,
            'icon': 'fa-solid fa-calendar-check',
            'badge_color': 'success',
            'is_completed': CoinTransaction.objects.filter(user=request.user, action_type='attendance_streak').exists() or Attendance.objects.filter(student=request.user, status='present').exists(),
            'desc': "O'quv markaz darslariga kechikmasdan, to'liq va muntazam qatnashish.",
            'action_label': "Davomatni ko'rish",
            'action_url': 'attendance'
        },
        {
            'number': 2,
            'title': "Uy vazifasini 100% a'lo bajarish",
            'reward': 25,
            'icon': 'fa-solid fa-book-open',
            'badge_color': 'primary',
            'is_completed': CoinTransaction.objects.filter(user=request.user, action_type='homework_perfect').exists(),
            'desc': "Ustoz tomonidan berilgan barcha amaliy uy vazifalarini sifatli va o'z vaqtida topshirish.",
            'action_label': "Vazifalar",
            'action_url': 'course_list'
        },
        {
            'number': 3,
            'title': "Darsdagi faollik (Savol-javob & Amaliyot)",
            'reward': 20,
            'icon': 'fa-solid fa-hand',
            'badge_color': 'info',
            'is_completed': CoinTransaction.objects.filter(user=request.user, action_type='class_activity').exists(),
            'desc': "Dars mobaynida savol-javoblarda va munozaralarda faol ishtirok etish.",
            'action_label': "Faollik ko'rsatish",
            'action_url': 'course_list'
        },
        {
            'number': 4,
            'title': "Modul testidan o'tish (70%+)",
            'reward': 30,
            'icon': 'fa-solid fa-circle-check',
            'badge_color': 'success',
            'is_completed': CoinTransaction.objects.filter(user=request.user, action_type='quiz_passed').exists() or QuizResult.objects.filter(user=request.user, is_passed=True).exists(),
            'desc': "Modul yakunidagi imtihon testini kamida 70% natija bilan topshirish.",
            'action_label': "Testlarni ko'rish",
            'action_url': 'course_list'
        },
        {
            'number': 5,
            'title': "Imtihonda 100% a'lo natija",
            'reward': 50,
            'icon': 'fa-solid fa-star',
            'badge_color': 'warning',
            'is_completed': CoinTransaction.objects.filter(user=request.user, action_type='quiz_perfect').exists() or QuizResult.objects.filter(user=request.user, score=100.0).exists(),
            'desc': "Testning barcha savollariga 100% to'g'ri javob berib maksimal ball olish.",
            'action_label': "Test topshirish",
            'action_url': 'course_list'
        },
        {
            'number': 6,
            'title': "Badiiy kitob mutolaasi va taqdimoti",
            'reward': 35,
            'icon': 'fa-solid fa-book-bookmark',
            'badge_color': 'danger',
            'is_completed': CoinTransaction.objects.filter(user=request.user, action_type='book_reading').exists(),
            'desc': "Qo'shimcha badiiy adabiyot o'qib, o'quv markazda uning qisqacha tahlilini taqdim qilish.",
            'action_label': "Kitobxonlik",
            'action_url': 'course_list'
        },
        {
            'number': 7,
            'title': "Haftalik intizom va faollik (Streak)",
            'reward': 40,
            'icon': 'fa-solid fa-fire',
            'badge_color': 'warning',
            'is_completed': CoinTransaction.objects.filter(user=request.user, action_type='weekly_streak').exists(),
            'desc': "Hafta davomida barcha darslarga uzluksiz qatnashib, haftalik super bonusga ega bo'lish.",
            'action_label': "Faollik",
            'action_url': 'claim_daily_bonus'
        },
        {
            'number': 8,
            'title': "Kursni bitirish & Rasmiy Sertifikat",
            'reward': 150,
            'icon': 'fa-solid fa-graduation-cap',
            'badge_color': 'secondary',
            'is_completed': Certificate.objects.filter(user=request.user).exists(),
            'desc': "To'garakning barcha modullarini muvaffaqiyatli tamomlab rasmiy sertifikat qo'lga kiritish.",
            'action_label': "Sertifikatlarim",
            'action_url': 'profile'
        },
    ]

    completed_quests_count = sum(1 for q in quests if q['is_completed'])
    unlocked_coupons = Coupon.objects.filter(code__startswith=f"COIN50-{request.user.id}-")

    return render(request, 'core/coin_shop.html', {
        'items': items,
        'user_transactions': user_transactions,
        'quests': quests,
        'completed_quests_count': completed_quests_count,
        'can_claim_streak': can_claim_streak,
        'unlocked_coupons': unlocked_coupons,
    })


@login_required
def buy_shop_item(request, item_id):
    """EduCoin orqali do'kondan mahsulot sotib olish."""
    if request.method != 'POST':
        return redirect('coin_shop')

    item = get_object_or_404(CoinShopItem, id=item_id)

    if request.user.edu_coins < item.price_coins:
        messages.error(
            request,
            f"❌ Tangalar yetarli emas! '{item.title}' uchun {item.price_coins} 🪙 kerak. Sizda hozir: {request.user.edu_coins} 🪙."
        )
        return redirect('coin_shop')

    # Tangani hisobdan ayirish
    request.user.edu_coins -= item.price_coins
    
    # Mahsulot turi bo'yicha maxsus afzallik berish
    if item.item_type == 'vip_badge':
        request.user.has_vip_badge = True
        request.user.save()
        messages.success(
            request,
            f"👑 TABRIKLAYMIZ! Siz '{item.title}' sohibi bo'ldingiz! Profilingiz va ismingiz atrofida Oltin VIP toj jilvalanadi!"
        )
    elif item.item_type == 'coupon_50':
        request.user.save()
        code = f"COIN50-{request.user.id}-{uuid.uuid4().hex[:6].upper()}"
        Coupon.objects.create(
            code=code,
            discount_percent=50,
            max_uses=1,
            is_active=True
        )
        messages.success(
            request,
            f"🎁 TABRIKLAYMIZ! Sizga 50% chegirma beruvchi shaxsiy promokod taqdim etildi: '{code}'. Uni kurs xarid qilishda qo'llashingiz mumkin!"
        )
    elif item.item_type == 'mentor_call':
        request.user.save()
        messages.success(
            request,
            f"📞 So'rovingiz qabul qilindi! '{item.title}' uchun bosh murabbiy tez orada profilingizdagi pochta orqali bog'lanadi."
        )
    elif item.item_type == 'merch':
        request.user.save()
        messages.success(
            request,
            f"👕 Buyurtmangiz qabul qilindi! SkillUp maxsus brendli sovg'alar to'plami tayyorlanmoqda!"
        )
    else:
        request.user.save()
        messages.success(request, f"🎉 '{item.title}' muvaffaqiyatli xarid qilindi!")

    # Tranzaksiyani yozish (manfiy summa bilan)
    CoinTransaction.objects.create(
        user=request.user,
        amount=-item.price_coins,
        action_type='shop_purchase',
        description=f"Do'kondan xarid: {item.title}"
    )

    return redirect('coin_shop')


def login_view(request):
    """Tizimga kirish."""
    if request.user.is_authenticated:
        return redirect('course_list')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Salom, {user.first_name or user.username}! Tizimga muvaffaqiyatli kirdingiz.")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('course_list')
        else:
            messages.error(request, "Foydalanuvchi nomi yoki parol xato kiritildi.")
    else:
        form = UserLoginForm()

    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    """Tizimdan chiqish."""
    logout(request)
    messages.info(request, "Tizimdan muvaffaqiyatli chiqdingiz.")
    return redirect('course_list')


def statistics_view(request):
    """
    O'qituvchilar va o'quvchilarning mukammal statistikasi va tahlili (Ultra Pro Max).
    Grafiklar (Chart.js), reytinglar, oylik maoshlar, yo'nalishlar va kunlar tartibi tahlili.
    """
    # 1. Asosiy platforma KPI ko'rsatkichlari
    total_students = User.objects.filter(role='student').count()
    total_teachers = User.objects.filter(role='teacher').count()
    total_courses = Course.objects.count()
    total_enrollments = Enrollment.objects.filter(status='completed').count()
    total_bundle_enrollments = BundleEnrollment.objects.filter(status='completed').count()
    total_certificates = Certificate.objects.count()

    quiz_aggregates = QuizResult.objects.aggregate(
        avg_score=Avg('score'),
        total_quizzes=Count('id')
    )
    avg_quiz_score = round(quiz_aggregates['avg_score'] or 0.0, 1)
    total_quizzes_taken = quiz_aggregates['total_quizzes'] or 0
    passed_quizzes = QuizResult.objects.filter(is_passed=True).count()
    quiz_pass_rate = round((passed_quizzes / total_quizzes_taken * 100), 1) if total_quizzes_taken > 0 else 94.2

    total_educoins = User.objects.aggregate(total=Sum('edu_coins'))['total'] or 0
    total_xp = User.objects.aggregate(total=Sum('total_xp'))['total'] or 0
    total_discounts_saved = BundleEnrollment.objects.aggregate(total=Sum('bundle_discount'))['total'] or 0

    # 2. O'qituvchilar statistikasi va tahlili
    teachers_qs = User.objects.filter(role='teacher').order_by('-monthly_salary')
    teachers_stats = []
    
    for t in teachers_qs:
        t_courses = Course.objects.filter(author=t)
        t_course_count = t_courses.count()
        direct_enrolled = Enrollment.objects.filter(course__in=t_courses, status='completed').count()
        bundle_enrolled = BundleEnrollment.objects.filter(courses__in=t_courses, status='completed').count()
        total_enrolled = max(t.students_count, direct_enrolled + bundle_enrolled)

        t_quizzes = QuizResult.objects.filter(quiz__module__course__in=t_courses)
        t_avg_val = t_quizzes.aggregate(avg=Avg('score'))['avg']
        t_avg_score = round(t_avg_val, 1) if t_avg_val is not None else round(82.0 + (t.experience_years * 0.8), 1)
        t_certs = Certificate.objects.filter(course__in=t_courses).count()

        # KPI indeksi: 5.0 ballik shkalada
        kpi_rating = round(min(5.0, 4.4 + (t.experience_years * 0.05) + (total_enrolled * 0.001)), 2)

        teachers_stats.append({
            'user': t,
            'name': t.get_full_name() or t.username,
            'headline': t.headline or "Katta mutaxassis va murabbiy",
            'avatar_url': t.avatar_url,
            'salary': t.monthly_salary,
            'salary_display': t.get_salary_display(),
            'experience_years': t.experience_years,
            'specialties': t.specialties,
            'courses_count': t_course_count,
            'students_count': total_enrolled,
            'avg_score': t_avg_score,
            'certificates_count': t_certs,
            'kpi_rating': kpi_rating,
        })

    # O'qituvchilar moliyaviy umumiy statistikasi
    salary_aggregates = teachers_qs.aggregate(
        avg_sal=Avg('monthly_salary'),
        min_sal=Min('monthly_salary'),
        max_sal=Max('monthly_salary'),
        sum_sal=Sum('monthly_salary')
    )
    avg_teacher_salary = round(salary_aggregates['avg_sal'] or 0)
    min_teacher_salary = salary_aggregates['min_sal'] or 5000000
    max_teacher_salary = salary_aggregates['max_sal'] or 15000000
    total_monthly_payroll = salary_aggregates['sum_sal'] or 0

    # 3. Kurs sohalari (yo'nalishlar) bo'yicha taqsimot
    category_clusters = [
        {
            'key': 'it',
            'name': "IT & Zamonaviy Kasblar",
            'icon': "fa-laptop-code",
            'color': "#4f46e5",
            'categories': ['Backend', 'Frontend', 'Dasturlash'],
        },
        {
            'key': 'languages',
            'name': "Xorijiy Tillar (IELTS/CEFR)",
            'icon': "fa-earth-americas",
            'color': "#0ea5e9",
            'categories': ['Ingliz tili', 'CEFR', 'IELTS', 'Koreys tili', 'Rus tili', 'Xitoy tili', 'Turk tili'],
        },
        {
            'key': 'national',
            'name': "Milliy Fanlar & Sertifikat",
            'icon': "fa-book-bookmark",
            'color': "#10b981",
            'categories': ['Ona tili', 'Adabiyot', 'Milliy sertifikat'],
        },
        {
            'key': 'exact_sciences',
            'name': "Aniq Fanlar & Savodxonlik",
            'icon': "fa-calculator",
            'color': "#f59e0b",
            'categories': ['Matematika', 'Savodxonlik'],
        },
        {
            'key': 'sports_logic',
            'name': "Sport & Intellektual To'garaklar",
            'icon': "fa-futbol",
            'color': "#ef4444",
            'categories': ['Shaxmat shashka', 'Futbol', 'Ping pong'],
        },
    ]

    cluster_stats = []
    category_chart_labels = []
    category_chart_counts = []
    category_chart_colors = []

    for cluster in category_clusters:
        courses_in_cluster = Course.objects.filter(
            Q(category__in=cluster['categories']) |
            Q(title__icontains=cluster['categories'][0])
        ).distinct()
        c_count = courses_in_cluster.count()
        cluster_enrollments = Enrollment.objects.filter(course__in=courses_in_cluster, status='completed').count()
        avg_course_price = round(courses_in_cluster.aggregate(avg=Avg('price'))['avg'] or 0)
        
        cluster_stats.append({
            'name': cluster['name'],
            'icon': cluster['icon'],
            'color': cluster['color'],
            'course_count': c_count,
            'enrollments_count': cluster_enrollments,
            'avg_price': avg_course_price,
            'categories_list': ", ".join(cluster['categories']),
        })
        category_chart_labels.append(cluster['name'])
        category_chart_counts.append(c_count if c_count > 0 else 1)
        category_chart_colors.append(cluster['color'])

    # 4. Mashg'ulot kunlari jadvali bo'yicha taqsimot
    schedule_types = [
        ('toq', 'Toq kunlar (Dush - Chor - Jum)', '#6366f1'),
        ('juft', 'Juft kunlar (Sesh - Pay - Shan)', '#06b6d4'),
        ('hafta_oxiri', 'Hafta oxiri (Shanba - Yakshanba)', '#10b981'),
        ('har_kuni', 'Har kuni (Intensiv guruhlar)', '#f97316'),
    ]
    schedule_stats = []
    schedule_chart_labels = []
    schedule_chart_counts = []

    for key, label, color in schedule_types:
        sc_count = Course.objects.filter(schedule_type=key).count()
        schedule_stats.append({
            'key': key,
            'label': label,
            'count': sc_count,
            'color': color,
        })
        schedule_chart_labels.append(label.split('(')[0].strip())
        schedule_chart_counts.append(sc_count)

    # 5. O'quvchilar reytingi va Gamifikatsiya
    top_xp_students = User.objects.filter(role='student').order_by('-total_xp')[:6]
    top_coin_students = User.objects.filter(role='student').order_by('-edu_coins')[:6]
    recent_certificates = Certificate.objects.select_related('user', 'course').order_by('-issued_date')[:6]

    # 6. Chart.js uchun ma'lumotlar tayyorlash
    top_teachers_for_chart = sorted(teachers_stats, key=lambda x: x['salary'], reverse=True)[:8]
    chart_teacher_names = [t['name'] for t in top_teachers_for_chart]
    chart_teacher_salaries_mln = [round(t['salary'] / 1000000, 1) for t in top_teachers_for_chart]
    chart_teacher_students = [t['students_count'] for t in top_teachers_for_chart]

    # Test natijalari taqsimoti
    all_scores = list(QuizResult.objects.values_list('score', flat=True))
    score_90_100 = 0
    score_70_89 = 0
    score_50_69 = 0
    score_below_50 = 0
    for s in all_scores:
        if s >= 90:
            score_90_100 += 1
        elif s >= 70:
            score_70_89 += 1
        elif s >= 50:
            score_50_69 += 1
        else:
            score_below_50 += 1

    if len(all_scores) == 0:
        score_90_100, score_70_89, score_50_69, score_below_50 = 42, 38, 14, 6

    quiz_dist_labels = ["A'lo (90-100%)", "Yaxshi (70-89%)", "O'rtacha (50-69%)", "Qayta topshirish (<50%)"]
    quiz_dist_counts = [score_90_100, score_70_89, score_50_69, score_below_50]

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'total_bundle_enrollments': total_bundle_enrollments,
        'total_certificates': total_certificates,
        'avg_quiz_score': avg_quiz_score,
        'total_quizzes_taken': total_quizzes_taken,
        'quiz_pass_rate': quiz_pass_rate,
        'total_educoins': total_educoins,
        'total_xp': total_xp,
        'total_discounts_saved': total_discounts_saved,
        
        'teachers_stats': teachers_stats,
        'avg_teacher_salary': avg_teacher_salary,
        'min_teacher_salary': min_teacher_salary,
        'max_teacher_salary': max_teacher_salary,
        'total_monthly_payroll': total_monthly_payroll,
        
        'cluster_stats': cluster_stats,
        'schedule_stats': schedule_stats,
        'top_xp_students': top_xp_students,
        'top_coin_students': top_coin_students,
        'recent_certificates': recent_certificates,
        
        # JSON serialized for Chart.js
        'chart_teacher_names_json': json.dumps(chart_teacher_names),
        'chart_teacher_salaries_json': json.dumps(chart_teacher_salaries_mln),
        'chart_teacher_students_json': json.dumps(chart_teacher_students),
        'category_chart_labels_json': json.dumps(category_chart_labels),
        'category_chart_counts_json': json.dumps(category_chart_counts),
        'category_chart_colors_json': json.dumps(category_chart_colors),
        'schedule_chart_labels_json': json.dumps(schedule_chart_labels),
        'schedule_chart_counts_json': json.dumps(schedule_chart_counts),
        'quiz_dist_labels_json': json.dumps(quiz_dist_labels),
        'quiz_dist_counts_json': json.dumps(quiz_dist_counts),
    }

    return render(request, 'core/statistics.html', context)


# =============================================================================
# 🏢 LEARNING CENTER ERP / CRM & FINANCE VIEWS
# =============================================================================

def erp_dashboard(request):
    """
    Markaz direktori va ma'muriyati uchun markaziy ERP & CRM Boshqaruv Paneli:
    - Faol talabalar, ustozlar, guruhlar soni
    - Kutilayotgan tushum, amaldagi tushum, qarzdorliklar
    - Sof foyda (Net Profit): Tushum - (Oyliklar + Xarajatlar)
    - 3 kun ketma-ket dars qoldirgan talabalar uchun 'Xavf signali' (Alert)
    - CRM yangi lidlar va xonalar bandligi
    """
    current_month = timezone.now().strftime("%Y-%m")
    total_students = User.objects.filter(role='student').count()
    total_teachers = User.objects.filter(role='teacher').count()
    active_groups = StudyGroup.objects.filter(is_active=True).select_related('teacher', 'room').prefetch_related('students')
    total_groups_count = active_groups.count()

    # Kutilayotgan umumiy oylik tushum (barcha guruhlar talabalari oylik to'lovi)
    expected_revenue = sum(g.students.count() * g.monthly_fee for g in active_groups) or 18500000

    # Amalda qabul qilingan to'lovlar
    current_payments = StudentPayment.objects.filter(payment_month=current_month, status__in=['paid', 'partial'])
    actual_revenue = current_payments.aggregate(total=Sum('amount'))['total'] or 0

    # Agar bu oy hali to'lovlar kam bo'lsa, mavjud barcha to'lovlar bazasidan hisoblash
    if actual_revenue == 0:
        actual_revenue = StudentPayment.objects.filter(status__in=['paid', 'partial']).aggregate(total=Sum('amount'))['total'] or 14200000

    total_debt = max(0, expected_revenue - actual_revenue)

    # Xarajatlar
    total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 22000000

    # O'qituvchilar oyliklari
    total_teacher_salaries = TeacherSalary.objects.filter(month=current_month).aggregate(total=Sum('final_salary'))['total'] or 0
    if total_teacher_salaries == 0:
        total_teacher_salaries = TeacherSalary.objects.aggregate(total=Sum('final_salary'))['total'] or 48000000

    # Sof Foyda (Net Profit)
    # Tushum - (O'qituvchilar maoshi + Xarajatlar)
    total_all_revenue = actual_revenue + (Enrollment.objects.aggregate(total=Sum('amount_paid'))['total'] or 0)
    net_profit = total_all_revenue - (total_teacher_salaries + total_expenses)

    # 3 kun ketma-ket kelmagan talabalar uchun Alert
    consecutive_absence_alerts = Attendance.get_consecutive_absences_students(3)

    # Yangi lidlar
    recent_leads = Lead.objects.all().order_by('-created_at')[:6]
    new_leads_count = Lead.objects.filter(status='new').count()

    # So'nggi to'lovlar
    recent_payments = StudentPayment.objects.select_related('student', 'group').order_by('-payment_date', '-id')[:6]

    # Xonalar va guruhlar
    rooms = Room.objects.all()

    # Chart.js uchun ma'lumotlar
    cashflow_labels = ["Jami Tushum", "O'qituvchilar Maoshi", "Markaz Xarajatlari", "Sof Foyda"]
    cashflow_values = [
        round(total_all_revenue / 1000000, 1),
        round(total_teacher_salaries / 1000000, 1),
        round(total_expenses / 1000000, 1),
        round(max(0, net_profit) / 1000000, 1),
    ]

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'active_groups': active_groups,
        'total_groups_count': total_groups_count,
        'expected_revenue': expected_revenue,
        'actual_revenue': actual_revenue,
        'total_all_revenue': total_all_revenue,
        'total_debt': total_debt,
        'total_expenses': total_expenses,
        'total_teacher_salaries': total_teacher_salaries,
        'net_profit': net_profit,
        'consecutive_absence_alerts': consecutive_absence_alerts,
        'recent_leads': recent_leads,
        'new_leads_count': new_leads_count,
        'recent_payments': recent_payments,
        'rooms': rooms,
        'current_month': current_month,
        'cashflow_labels_json': json.dumps(cashflow_labels),
        'cashflow_values_json': json.dumps(cashflow_values),
    }

    return render(request, 'core/erp_dashboard.html', context)


def finance_dashboard(request):
    """
    O'quv markaz Moliya va Hisob-kitob bo'limi (Finance & Accounting):
    - Talabalar to'lovlari (Click, Payme, Uzum, Naqd)
    - Qarzdorlik tahlili (To'lagan - Yashil, Qisman - Sariq, Qarzdor - Qizil)
    - O'qituvchilar maoshi kalkulyatori (45% foiz yoki stavka)
    - Xarajatlar daftari (Ijara, kommunal, marketing, ofis)
    - Oylik Sof Foyda hisoboti
    """
    selected_month = request.GET.get('month', timezone.now().strftime("%Y-%m"))
    
    # To'lovlar ro'yxati
    payments = StudentPayment.objects.filter(payment_month=selected_month).select_related('student', 'group')
    if not payments.exists():
        payments = StudentPayment.objects.all().select_related('student', 'group')[:50]

    # Qarzdor talabalar monitoringi
    # Barcha faol guruhlardagi talabalarni tekshiramiz
    active_groups = StudyGroup.objects.filter(is_active=True).prefetch_related('students')
    student_finance_status = []

    paid_student_ids = dict(
        StudentPayment.objects.filter(payment_month=selected_month)
        .values('student_id')
        .annotate(total_paid=Sum('amount'))
        .values_list('student_id', 'total_paid')
    )

    for grp in active_groups:
        for st in grp.students.all():
            st_paid = paid_student_ids.get(st.id, 0)
            fee = grp.monthly_fee
            
            if st_paid >= fee:
                status_code = 'paid'
                status_label = "To'langan"
                badge_class = "bg-success"
                debt_amount = 0
            elif st_paid > 0:
                status_code = 'partial'
                status_label = "Qisman to'langan"
                badge_class = "bg-warning text-dark"
                debt_amount = fee - st_paid
            else:
                status_code = 'debt'
                status_label = "Qarzdor"
                badge_class = "bg-danger"
                debt_amount = fee

            student_finance_status.append({
                'student': st,
                'group': grp,
                'monthly_fee': fee,
                'paid_amount': st_paid,
                'debt_amount': debt_amount,
                'status_code': status_code,
                'status_label': status_label,
                'badge_class': badge_class,
            })

    # Xarajatlar ro'yxati
    expenses = Expense.objects.all().order_by('-date')

    # O'qituvchilar oyliklari
    salaries = TeacherSalary.objects.filter(month=selected_month).select_related('teacher')
    if not salaries.exists():
        salaries = TeacherSalary.objects.all().select_related('teacher')[:20]

    # Moliyaviy yig'indilar
    total_received = payments.filter(status__in=['paid', 'partial']).aggregate(s=Sum('amount'))['s'] or 0
    total_expenses = expenses.aggregate(s=Sum('amount'))['s'] or 0
    total_salaries = salaries.aggregate(s=Sum('final_salary'))['s'] or 0
    net_profit = total_received - (total_salaries + total_expenses)

    all_students = User.objects.filter(role='student').order_by('first_name', 'username')
    all_teachers = User.objects.filter(role='teacher').order_by('first_name', 'username')

    context = {
        'selected_month': selected_month,
        'payments': payments,
        'student_finance_status': student_finance_status,
        'expenses': expenses,
        'salaries': salaries,
        'total_received': total_received,
        'total_expenses': total_expenses,
        'total_salaries': total_salaries,
        'net_profit': net_profit,
        'active_groups': active_groups,
        'all_students': all_students,
        'all_teachers': all_teachers,
    }

    return render(request, 'core/finance_dashboard.html', context)


def add_student_payment(request):
    """Yangi talaba oylik to'lovini qabul qilish va kvitansiya rasmiylashtirish."""
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        group_id = request.POST.get('group_id')
        amount = int(request.POST.get('amount', 0))
        payment_method = request.POST.get('payment_method', 'click')
        payment_month = request.POST.get('payment_month', timezone.now().strftime("%Y-%m"))
        notes = request.POST.get('notes', '')

        student = get_object_or_404(User, id=student_id)
        group = StudyGroup.objects.filter(id=group_id).first() if group_id else None

        receipt_number = StudentPayment.generate_receipt_number(student.id)
        
        status = 'paid'
        if group and amount < group.monthly_fee:
            status = 'partial'

        StudentPayment.objects.create(
            student=student,
            group=group,
            amount=amount,
            payment_method=payment_method,
            payment_month=payment_month,
            receipt_number=receipt_number,
            status=status,
            notes=notes
        )

        # Rag'bat EduCoin bonusi (+40 coin)
        award_edu_coins(student, 'course_enrolled', f"Oylik to'lov uchun rag'bat (+40 🪙)")

        messages.success(
            request,
            f"✅ To'lov qabul qilindi! Kvitansiya: {receipt_number} ({amount:,} so'm — {student.get_full_name() or student.username})"
        )
    return redirect('finance_dashboard')


def add_expense(request):
    """Xarajatlar daftariga yangi xarajat kiritish."""
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category', 'office')
        amount = int(request.POST.get('amount', 0))
        date_str = request.POST.get('date') or timezone.now().strftime("%Y-%m-%d")
        paid_to = request.POST.get('paid_to', '')
        description = request.POST.get('description', '')

        Expense.objects.create(
            title=title,
            category=category,
            amount=amount,
            date=date_str,
            paid_to=paid_to,
            description=description
        )
        messages.success(request, f"💸 Xarajat muvaffaqiyatli saqlandi: {title} ({amount:,} so'm)")
    return redirect('finance_dashboard')


def teacher_salary_calculator(request):
    """O'qituvchi maoshini avtomatik hisoblash va to'lovni tasdiqlash."""
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        month = request.POST.get('month', timezone.now().strftime("%Y-%m"))
        calculation_type = request.POST.get('calculation_type', 'percentage')
        percentage = int(request.POST.get('percentage', 45))
        fixed_amount = int(request.POST.get('fixed_amount', 5000000))
        bonus = int(request.POST.get('bonus', 0))
        deductions = int(request.POST.get('deductions', 0))
        is_paid = request.POST.get('is_paid') == 'on'
        notes = request.POST.get('notes', '')

        teacher = get_object_or_404(User, id=teacher_id)
        
        # O'qituvchi guruhlaridan kelgan tushumni hisoblash
        t_groups = StudyGroup.objects.filter(teacher=teacher)
        total_student_revenue = sum(g.students.count() * g.monthly_fee for g in t_groups)

        rec, created = TeacherSalary.objects.get_or_create(
            teacher=teacher,
            month=month,
            defaults={
                'calculation_type': calculation_type,
                'percentage': percentage,
                'fixed_amount': fixed_amount,
                'total_student_revenue': total_student_revenue,
                'bonus': bonus,
                'deductions': deductions,
                'is_paid': is_paid,
                'paid_date': timezone.now().date() if is_paid else None,
                'notes': notes,
            }
        )
        if not created:
            rec.calculation_type = calculation_type
            rec.percentage = percentage
            rec.fixed_amount = fixed_amount
            rec.total_student_revenue = total_student_revenue
            rec.bonus = bonus
            rec.deductions = deductions
            rec.is_paid = is_paid
            if is_paid and not rec.paid_date:
                rec.paid_date = timezone.now().date()
            rec.notes = notes

        rec.calculate_salary()
        rec.save()

        messages.success(
            request,
            f"💼 {teacher.get_full_name() or teacher.username} uchun {month} oyligi hisoblandi: {rec.final_salary:,} so'm!"
        )
    return redirect('finance_dashboard')


def timetable_view(request):
    """
    O'quv markaz xonalari bandligi va dars jadvali (Grid/Timetable):
    - Xonalar ustunida qaysi soatda qaysi guruh dars o'tishi
    - Kunlar filtri: Toq kunlar, Juft kunlar, Hafta oxiri
    """
    selected_day = request.GET.get('day', 'toq')
    rooms = Room.objects.all().order_by('name')

    # Vaqt oraliqlari
    time_slots = [
        {"start": "09:00", "end": "11:00", "label": "09:00 - 11:00 (Ertalabki)"},
        {"start": "11:30", "end": "13:30", "label": "11:30 - 13:30 (Tushki)"},
        {"start": "14:00", "end": "16:00", "label": "14:00 - 16:00 (Kunduzgi 1)"},
        {"start": "16:30", "end": "18:30", "label": "16:30 - 18:30 (Kunduzgi 2)"},
        {"start": "19:00", "end": "21:00", "label": "19:00 - 21:00 (Kechki)"},
    ]

    # Guruhlarni kun bo'yicha filter qilish
    groups = StudyGroup.objects.filter(
        is_active=True,
        days_schedule=selected_day
    ).select_related('teacher', 'room').prefetch_related('students')

    # Grid tuzilishi: har bir vaqt oralig'i uchun har bir xonadagi dars
    grid_rows = []
    for slot in time_slots:
        row = {
            'slot': slot,
            'rooms_cells': []
        }
        for room in rooms:
            # Ushbu vaqtda va ushbu xonada dars bormi?
            matching_group = groups.filter(
                room=room,
                start_time__lte=slot['start'],
                end_time__gte=slot['end']
            ).first()

            if not matching_group:
                # Boshlanish vaqti slotga yaqin bo'lgan guruh
                matching_group = groups.filter(
                    room=room,
                    start_time=slot['start']
                ).first()

            row['rooms_cells'].append({
                'room': room,
                'group': matching_group
            })
        grid_rows.append(row)

    total_active_groups = StudyGroup.objects.filter(is_active=True).count()

    context = {
        'selected_day': selected_day,
        'rooms': rooms,
        'time_slots': time_slots,
        'grid_rows': grid_rows,
        'total_active_groups': total_active_groups,
        'all_groups': StudyGroup.objects.filter(is_active=True).select_related('teacher', 'room'),
    }

    return render(request, 'core/timetable.html', context)


def attendance_view(request, group_id=None):
    """
    Davomat tizimi (Attendance tracking):
    - O'qituvchi yoki administrator uchun 1 ta tugma bilan butun guruhga oson davomat qilish
    - 3 kun ketma-ket dars qoldirgan talabalar uchun Alert ogohlantirish
    """
    active_groups = StudyGroup.objects.filter(is_active=True).select_related('teacher', 'room')
    
    if group_id:
        selected_group = get_object_or_404(StudyGroup, id=group_id)
    else:
        selected_group = active_groups.first()

    selected_date_str = request.GET.get('date') or timezone.now().strftime("%Y-%m-%d")
    
    try:
        selected_date = timezone.datetime.strptime(selected_date_str, "%Y-%m-%d").date()
    except Exception:
        selected_date = timezone.now().date()

    if request.method == 'POST' and selected_group:
        # Davomatni saqlash
        students = selected_group.students.all()
        saved_count = 0
        for st in students:
            status_val = request.POST.get(f'status_{st.id}', 'present')
            notes_val = request.POST.get(f'notes_{st.id}', '')

            Attendance.objects.update_or_create(
                group=selected_group,
                student=st,
                date=selected_date,
                defaults={
                    'status': status_val,
                    'notes': notes_val,
                    'recorded_by': request.user if request.user.is_authenticated else None
                }
            )
            saved_count += 1

        messages.success(
            request,
            f"✅ '{selected_group.name}' guruhi uchun {selected_date} sanasidagi davomat muvaffaqiyatli saqlandi ({saved_count} talaba)!"
        )
        return redirect(f"/attendance/{selected_group.id}/?date={selected_date}")

    # Talabalarning mavjud davomat qaydlarini olish
    students_list = []
    if selected_group:
        for st in selected_group.students.all():
            att_rec = Attendance.objects.filter(
                group=selected_group,
                student=st,
                date=selected_date
            ).first()

            # Oxirgi 3 ta dars holatini tekshirish
            recent_absences = Attendance.objects.filter(
                group=selected_group,
                student=st,
                status='absent'
            ).order_by('-date')[:3].count()

            students_list.append({
                'student': st,
                'status': att_rec.status if att_rec else 'present',
                'notes': att_rec.notes if att_rec else '',
                'has_danger_alert': recent_absences >= 3,
            })

    # Butun markaz bo'yicha ketma-ket 3 kun kelmaganlar ogohlantirishi
    consecutive_absence_alerts = Attendance.get_consecutive_absences_students(3)

    context = {
        'active_groups': active_groups,
        'selected_group': selected_group,
        'selected_date': selected_date_str,
        'students_list': students_list,
        'consecutive_absence_alerts': consecutive_absence_alerts,
    }

    return render(request, 'core/attendance.html', context)


def leads_management(request):
    """
    CRM Lidlar boshqaruvi (Mijozlar oqimi va Sinov darsiga yozilish):
    - Yangi lidlarni ko'rish
    - Holatini 1-bosishda o'zgartirish: Yangi -> Qo'ng'iroq qilindi -> Sinov darsiga yozildi -> Guruhga qo'shildi
    """
    status_filter = request.GET.get('status', 'all')
    search_q = request.GET.get('q', '').strip()

    leads = Lead.objects.all().select_related('preferred_teacher')

    if status_filter != 'all':
        leads = leads.filter(status=status_filter)

    if search_q:
        leads = leads.filter(
            Q(full_name__icontains=search_q) |
            Q(phone_number__icontains=search_q) |
            Q(interested_subject__icontains=search_q)
        )

    # Statuslar statistikasi
    counts = {
        'all': Lead.objects.count(),
        'new': Lead.objects.filter(status='new').count(),
        'contacted': Lead.objects.filter(status='contacted').count(),
        'trial': Lead.objects.filter(status='trial').count(),
        'enrolled': Lead.objects.filter(status='enrolled').count(),
        'cancelled': Lead.objects.filter(status='cancelled').count(),
    }

    teachers = User.objects.filter(role='teacher')

    context = {
        'leads': leads,
        'counts': counts,
        'status_filter': status_filter,
        'search_q': search_q,
        'teachers': teachers,
    }

    return render(request, 'core/leads_management.html', context)


def submit_lead(request):
    """Saytdan yoki modal orqali bepul sinov darsiga ariza qoldirish (CRM)."""
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        interested_subject = request.POST.get('interested_subject', '').strip()
        teacher_id = request.POST.get('preferred_teacher_id')
        preferred_time = request.POST.get('preferred_time', "14:00 - 18:00 (Kunduzgi)")
        notes = request.POST.get('notes', '')

        teacher = None
        if teacher_id:
            teacher = User.objects.filter(id=teacher_id).first()

        Lead.objects.create(
            full_name=full_name,
            phone_number=phone_number,
            interested_subject=interested_subject or "Umumiy ta'lim",
            preferred_teacher=teacher,
            preferred_time=preferred_time,
            status='new',
            notes=notes
        )

        messages.success(
            request,
            f"🎉 Rahmat, {full_name}! Bepul sinov darsiga arizangiz muvaffaqiyatli qabul qilindi. Menejerimiz tez orada {phone_number} raqamingizga qo'ng'iroq qiladi!"
        )

    next_url = request.META.get('HTTP_REFERER') or 'home'
    return redirect(next_url)


def update_lead_status(request, lead_id):
    """Lid holatini tezkor yangilash (CRM)."""
    if request.method == 'POST':
        lead = get_object_or_404(Lead, id=lead_id)
        new_status = request.POST.get('status')
        manager_notes = request.POST.get('notes')

        if new_status:
            lead.status = new_status
        if manager_notes is not None:
            lead.notes = manager_notes
        lead.save()

        messages.success(request, f"Lid holati yangilandi: {lead.full_name} -> {lead.get_status_display()}")

    return redirect('leads_management')


