from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from lms.models import (
    Course, Module, Lesson, Quiz, Question, Option,
    QuizAttempt, LessonProgress, Enrollment, Certificate, UserProfile
)
from lms.utils import (
    can_student_access_module, can_student_access_lesson,
    can_student_access_quiz, check_and_award_certificate
)


class EduQuizLmsTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Users
        self.teacher = User.objects.create_user(username='ustoz_test', password='password123')
        self.teacher.profile.role = 'teacher'
        self.teacher.profile.save()

        self.student = User.objects.create_user(username='talaba_test', password='password123')
        self.student.profile.role = 'student'
        self.student.profile.save()

        # Course
        self.course = Course.objects.create(
            title="Test Course",
            instructor=self.teacher,
            short_description="Short desc",
            description="Long desc"
        )

        # Module 1
        self.mod1 = Module.objects.create(course=self.course, title="Modul 1", order=1, pass_percentage=70)
        self.l1 = Lesson.objects.create(module=self.mod1, title="Dars 1.1", order=1, content="Content 1")
        self.l2 = Lesson.objects.create(module=self.mod1, title="Dars 1.2", order=2, content="Content 2")

        self.quiz1 = Quiz.objects.create(module=self.mod1, title="Quiz 1", passing_score=70, time_limit_minutes=10)
        self.q1 = Question.objects.create(quiz=self.quiz1, question_text="Savol 1?", points=10)
        self.opt1_correct = Option.objects.create(question=self.q1, option_text="A", is_correct=True)
        self.opt1_wrong = Option.objects.create(question=self.q1, option_text="B", is_correct=False)

        # Module 2
        self.mod2 = Module.objects.create(course=self.course, title="Modul 2", order=2, pass_percentage=70)
        self.l3 = Lesson.objects.create(module=self.mod2, title="Dars 2.1", order=1, content="Content 3")

    def test_module_locking_logic(self):
        """Student cannot access module 2 before finishing module 1 and passing quiz with >= 70%"""
        Enrollment.objects.create(student=self.student, course=self.course)

        # Before finishing mod1
        self.assertFalse(can_student_access_module(self.student, self.mod2))

        # Complete lessons in mod1
        LessonProgress.objects.create(student=self.student, lesson=self.l1, is_completed=True)
        LessonProgress.objects.create(student=self.student, lesson=self.l2, is_completed=True)

        # Still cannot access mod2 because quiz1 is not passed
        self.assertFalse(can_student_access_module(self.student, self.mod2))

        # Failed attempt on quiz1 (e.g. 50%)
        QuizAttempt.objects.create(student=self.student, quiz=self.quiz1, score=5, percentage=50.0, passed=False)
        self.assertFalse(can_student_access_module(self.student, self.mod2))

        # Passed attempt on quiz1 (e.g. 100%)
        QuizAttempt.objects.create(student=self.student, quiz=self.quiz1, score=10, percentage=100.0, passed=True)
        self.assertTrue(can_student_access_module(self.student, self.mod2))

    def test_quiz_submission_and_xp(self):
        """Taking quiz computes score, percentage, and awards XP"""
        self.client.login(username='talaba_test', password='password123')
        Enrollment.objects.create(student=self.student, course=self.course)
        LessonProgress.objects.create(student=self.student, lesson=self.l1, is_completed=True)
        LessonProgress.objects.create(student=self.student, lesson=self.l2, is_completed=True)

        initial_xp = self.student.profile.xp_points

        # Submit correct answer
        response = self.client.post(reverse('quiz_submit', args=[self.quiz1.id]), {
            f'question_{self.q1.id}': self.opt1_correct.id
        })

        self.assertEqual(response.status_code, 302)
        attempt = QuizAttempt.objects.filter(student=self.student, quiz=self.quiz1).first()
        self.assertIsNotNone(attempt)
        self.assertTrue(attempt.passed)
        self.assertEqual(attempt.percentage, 100.0)

        # XP should have increased: +10 for question + 50 bonus for passing = +60
        self.student.profile.refresh_from_db()
        self.assertEqual(self.student.profile.xp_points, initial_xp + 60)

    def test_views_availability(self):
        """Catalog, Home, Leaderboard, and Login views return 200 OK"""
        r_home = self.client.get(reverse('home'))
        self.assertEqual(r_home.status_code, 200)

        r_cat = self.client.get(reverse('catalog'))
        self.assertEqual(r_cat.status_code, 200)

        r_lead = self.client.get(reverse('leaderboard'))
        self.assertEqual(r_lead.status_code, 200)

        r_detail = self.client.get(reverse('course_detail', args=[self.course.slug]))
        self.assertEqual(r_detail.status_code, 200)
