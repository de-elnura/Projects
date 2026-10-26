from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('bundle-enroll/', views.bundle_enroll, name='bundle_enroll'),
    path('bundle-enroll/pay/', views.process_bundle_payment, name='process_bundle_payment'),
    path('course/<int:course_id>/checkout/', views.checkout, name='checkout'),
    path('course/<int:course_id>/pay/', views.process_payment, name='process_payment'),
    path('teachers/', views.teachers_list, name='teachers_list'),
    path('classroom/<int:lesson_id>/', views.classroom, name='classroom'),
    path('lesson/<int:lesson_id>/complete/', views.complete_lesson, name='complete_lesson'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('coin-shop/', views.coin_shop, name='coin_shop'),
    path('coin-shop/buy/<int:item_id>/', views.buy_shop_item, name='buy_shop_item'),
    path('claim-daily-bonus/', views.claim_daily_bonus, name='claim_daily_bonus'),
    path('certificate/<str:code>/', views.certificate_detail, name='certificate_detail'),
    path('parent-report/', views.parent_report, name='parent_report'),
    path('parent-report/<int:user_id>/', views.parent_report, name='parent_report_student'),
    path('statistics/', views.statistics_view, name='statistics'),

    # =========================================================================
    # 🏢 LEARNING CENTER ERP / CRM & FINANCE URLS
    # =========================================================================
    path('erp/', views.erp_dashboard, name='erp_dashboard'),
    path('finance/', views.finance_dashboard, name='finance_dashboard'),
    path('finance/pay/', views.add_student_payment, name='add_student_payment'),
    path('finance/expense/', views.add_expense, name='add_expense'),
    path('finance/salary-calc/', views.teacher_salary_calculator, name='teacher_salary_calculator'),
    path('timetable/', views.timetable_view, name='timetable'),
    path('attendance/', views.attendance_view, name='attendance'),
    path('attendance/<int:group_id>/', views.attendance_view, name='attendance_group'),
    path('crm/leads/', views.leads_management, name='leads_management'),
    path('crm/lead/submit/', views.submit_lead, name='submit_lead'),
    path('crm/lead/<int:lead_id>/status/', views.update_lead_status, name='update_lead_status'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
