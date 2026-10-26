from django.urls import path
from . import views

urlpatterns = [
    # Asosiy sahifalar
    path('', views.home_view, name='home'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('course/<slug:slug>/', views.course_detail_view, name='course_detail'),
    path('course/<slug:slug>/enroll/', views.enroll_course_view, name='enroll_course'),
    
    # Classroom (Udemy / Coursera style UI)
    path('classroom/<slug:course_slug>/', views.classroom_view, name='classroom_default'),
    path('classroom/<slug:course_slug>/lesson/<int:lesson_id>/', views.classroom_view, name='classroom'),
    path('lesson/<int:lesson_id>/complete/', views.complete_lesson_view, name='complete_lesson'),

    # Quiz Engine (Interactive exam, countdown timer, question palette)
    path('quiz/<int:quiz_id>/', views.quiz_view, name='quiz_detail'),
    path('quiz/<int:quiz_id>/submit/', views.quiz_submit_view, name='quiz_submit'),
    path('quiz/attempt/<int:attempt_id>/result/', views.quiz_result_view, name='quiz_result'),

    # Reyting (Leaderboard), Profil va Sertifikat
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('profile/', views.profile_view, name='profile'),
    path('certificate/<str:certificate_id>/', views.certificate_view, name='certificate_detail'),
    path('instructors/', views.instructors_view, name='instructors'),

    # O'qituvchi boshqaruv studiyasi (Teacher Portal)
    path('teacher/dashboard/', views.teacher_dashboard_view, name='teacher_dashboard'),
    path('teacher/course/new/', views.teacher_course_create_view, name='teacher_course_create'),
    path('teacher/course/<int:course_id>/module/new/', views.teacher_module_create_view, name='teacher_module_create'),
    path('teacher/module/<int:module_id>/lesson/new/', views.teacher_lesson_create_view, name='teacher_lesson_create'),
    path('teacher/module/<int:module_id>/quiz/', views.teacher_quiz_create_view, name='teacher_quiz_create'),
    path('teacher/quiz/<int:quiz_id>/questions/', views.teacher_quiz_questions_view, name='teacher_quiz_questions'),

    # Autentifikatsiya
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
