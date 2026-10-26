import uuid
from django.utils import timezone
from .models import (
    Course, Module, Lesson, Enrollment, LessonProgress,
    Quiz, QuizAttempt, Certificate, UserProfile
)


def get_or_create_profile(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile


def award_xp(user, amount):
    if not user.is_authenticated:
        return 0
    profile = get_or_create_profile(user)
    profile.xp_points += amount
    profile.save(update_fields=['xp_points'])
    return profile.xp_points


def is_module_passed(user, module):
    """
    Modul o'tgan deb hisoblanishi uchun:
    1. Agar modulda test bo'lsa, foydalanuvchi undan kamida pass_percentage (standart 70%) to'plagan bo'lishi kerak.
    2. Agar test bo'lmasa, modulning barcha darslari tugallangan bo'lishi kerak.
    """
    if not hasattr(module, 'quiz'):
        # Agar test bo'lmasa, darslari to'liq tugatilganmi?
        lessons = module.lessons.all()
        if not lessons.exists():
            return True
        completed_count = LessonProgress.objects.filter(
            student=user,
            lesson__in=lessons,
            is_completed=True
        ).count()
        return completed_count >= lessons.count()

    quiz = module.quiz
    best_attempt = QuizAttempt.objects.filter(
        student=user,
        quiz=quiz,
        passed=True
    ).order_by('-percentage').first()

    return best_attempt is not None


def can_student_access_module(user, module):
    if not user.is_authenticated:
        return False
    if user.is_staff or getattr(user.profile, 'is_teacher', False):
        return True

    # Kursga yozilganligini tekshirish
    if not Enrollment.objects.filter(student=user, course=module.course).exists():
        return False

    # Oldingi barcha modullar 70% bilan topshirilgan bo'lishi shart!
    previous_modules = Module.objects.filter(
        course=module.course,
        order__lt=module.order
    ).order_by('order')

    for prev in previous_modules:
        if not is_module_passed(user, prev):
            return False

    return True


def can_student_access_lesson(user, lesson):
    if not user.is_authenticated:
        return lesson.is_free_preview

    if user.is_staff or getattr(user.profile, 'is_teacher', False):
        return True

    module = lesson.module
    if not can_student_access_module(user, module):
        return False

    # Shu modul ichidagi oldingi darslarni ko'rganmi?
    previous_lessons = Lesson.objects.filter(
        module=module,
        order__lt=lesson.order
    ).order_by('order')

    for prev in previous_lessons:
        progress = LessonProgress.objects.filter(
            student=user,
            lesson=prev,
            is_completed=True
        ).exists()
        if not progress:
            return False

    return True


def can_student_access_quiz(user, quiz):
    if not user.is_authenticated:
        return False
    if user.is_staff or getattr(user.profile, 'is_teacher', False):
        return True

    module = quiz.module
    if not can_student_access_module(user, module):
        return False

    # Moduldagi barcha darslar tugatilgan bo'lishi kerak
    lessons = module.lessons.all()
    if lessons.exists():
        completed_count = LessonProgress.objects.filter(
            student=user,
            lesson__in=lessons,
            is_completed=True
        ).count()
        if completed_count < lessons.count():
            return False

    return True


def get_course_progress_data(user, course):
    """
    Kurs bo'yicha to'liq progress xaritasi:
    Modullar, darslar, qulflangan/ochiq holatlari, umumiy foiz.
    """
    modules_data = []
    total_lessons = 0
    completed_lessons = 0
    total_quizzes = 0
    passed_quizzes = 0

    is_teacher_or_staff = user.is_authenticated and (user.is_staff or getattr(getattr(user, 'profile', None), 'is_teacher', False))
    is_enrolled = user.is_authenticated and Enrollment.objects.filter(student=user, course=course).exists()

    all_modules = course.modules.prefetch_related('lessons').all()

    prev_module_passed = True
    for mod in all_modules:
        mod_unlocked = is_teacher_or_staff or (is_enrolled and prev_module_passed)
        lessons_data = []
        mod_lessons = list(mod.lessons.all())
        prev_lesson_completed = True

        for les in mod_lessons:
            total_lessons += 1
            is_done = False
            if user.is_authenticated:
                is_done = LessonProgress.objects.filter(student=user, lesson=les, is_completed=True).exists()
            if is_done:
                completed_lessons += 1

            lesson_accessible = is_teacher_or_staff or (mod_unlocked and prev_lesson_completed) or (les.is_free_preview and not is_enrolled)

            lessons_data.append({
                'lesson': les,
                'is_completed': is_done,
                'is_accessible': lesson_accessible,
            })

            # Keyingi dars uchun tekshirish
            prev_lesson_completed = is_done

        # Modul testi
        quiz_data = None
        mod_quiz_passed = False
        if hasattr(mod, 'quiz'):
            total_quizzes += 1
            q = mod.quiz
            best_att = None
            if user.is_authenticated:
                best_att = QuizAttempt.objects.filter(student=user, quiz=q).order_by('-percentage').first()
                if best_att and best_att.passed:
                    mod_quiz_passed = True
                    passed_quizzes += 1

            quiz_accessible = is_teacher_or_staff or (mod_unlocked and prev_lesson_completed)

            quiz_data = {
                'quiz': q,
                'best_attempt': best_att,
                'is_passed': mod_quiz_passed,
                'is_accessible': quiz_accessible,
            }
        else:
            # Agar test bo'lmasa, barcha darslar tugagan bo'lsa o'tgan
            mod_quiz_passed = prev_lesson_completed

        modules_data.append({
            'module': mod,
            'is_unlocked': mod_unlocked,
            'is_passed': mod_quiz_passed,
            'lessons': lessons_data,
            'quiz_info': quiz_data,
        })

        prev_module_passed = mod_quiz_passed

    total_trackable = total_lessons + total_quizzes
    completed_trackable = completed_lessons + passed_quizzes
    overall_percentage = int((completed_trackable / total_trackable * 100)) if total_trackable > 0 else 0

    certificate = None
    if user.is_authenticated:
        certificate = Certificate.objects.filter(student=user, course=course).first()

    return {
        'modules_data': modules_data,
        'total_lessons': total_lessons,
        'completed_lessons': completed_lessons,
        'total_quizzes': total_quizzes,
        'passed_quizzes': passed_quizzes,
        'overall_percentage': overall_percentage,
        'is_enrolled': is_enrolled,
        'certificate': certificate,
    }


def check_and_award_certificate(user, course):
    if not user.is_authenticated:
        return None

    # Kursdagi barcha modullar testi topshirilganmi va darslar tugaganmi?
    progress = get_course_progress_data(user, course)

    # Agar 100% bo'lsa
    if progress['overall_percentage'] >= 100 or (
        progress['completed_lessons'] == progress['total_lessons'] and 
        progress['passed_quizzes'] == progress['total_quizzes']
    ):
        cert, created = Certificate.objects.get_or_create(
            student=user,
            course=course,
            defaults={
                'certificate_id': uuid.uuid4().hex[:12].upper(),
                'final_grade': 95.0,
            }
        )
        if created:
            # Sertifikat olganda bonus 100 XP
            award_xp(user, 100)
            # Enrollmentni is_completed deb belgilash
            Enrollment.objects.filter(student=user, course=course).update(
                is_completed=True,
                completed_at=timezone.now()
            )
        return cert

    return None
