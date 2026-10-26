from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Sum
from .models import (
    User, Course, Module, Lesson,
    Quiz, Question, Choice,
    UserLessonProgress, QuizResult, Certificate,
    Coupon, Enrollment, BundleEnrollment,
    CoinTransaction, CoinShopItem,
    Room, StudyGroup, Attendance,
    StudentPayment, TeacherSalary, Expense,
    Lead, TeacherReview
)

# Admin Panel Sarlavhalari
admin.site.site_header = "🎓 SkillUp / EduQuiz — Markaziy Boshqaruv Portali"
admin.site.site_title = "SkillUp LMS Admin"
admin.site.index_title = "Platforma Boshqaruv va Monitoring Markazi"


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'monthly_salary', 'total_xp', 'edu_coins', 'has_vip_badge', 'is_staff')
    list_filter = ('role', 'has_vip_badge', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ("EduQuiz Gamifikatsiya & Oylik Maosh", {'fields': ('role', 'monthly_salary', 'experience_years', 'specialties', 'students_count', 'total_xp', 'edu_coins', 'has_vip_badge', 'headline', 'bio', 'avatar_url')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("EduQuiz Gamifikatsiya & Oylik Maosh", {'fields': ('role', 'monthly_salary', 'total_xp', 'edu_coins', 'has_vip_badge')}),
    )


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    list_filter = ('quiz__module__course', 'quiz')
    inlines = [ChoiceInline]


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'passing_score', 'duration_minutes')
    inlines = [QuestionInline]


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    inlines = [LessonInline]


class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'schedule_type', 'schedule_time', 'price', 'discount_price', 'is_modern_profession', 'author')
    list_filter = ('category', 'schedule_type', 'is_modern_profession', 'author')
    search_fields = ('title', 'description')
    inlines = [ModuleInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order')
    list_filter = ('module__course', 'module')
    search_fields = ('title', 'content')


@admin.register(UserLessonProgress)
class UserLessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'is_completed', 'completed_at')
    list_filter = ('is_completed', 'completed_at')
    search_fields = ('user__username', 'lesson__title')


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'is_passed', 'created_at')
    list_filter = ('is_passed', 'quiz__module__course', 'created_at')
    search_fields = ('user__username', 'quiz__title')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_code', 'user', 'course', 'issued_date')
    search_fields = ('certificate_code', 'user__username', 'course__title')
    readonly_fields = ('certificate_code', 'issued_date')


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'is_active', 'used_count', 'max_uses', 'valid_until')
    list_filter = ('is_active', 'discount_percent')
    search_fields = ('code',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'user', 'course', 'amount_paid', 'payment_method', 'status', 'created_at')
    list_filter = ('payment_method', 'status', 'created_at')
    search_fields = ('transaction_id', 'user__username', 'course__title')
    readonly_fields = ('transaction_id', 'created_at')


@admin.register(BundleEnrollment)
class BundleEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'user', 'bundle_discount', 'final_amount', 'payment_method', 'status', 'created_at')
    list_filter = ('payment_method', 'status', 'created_at')
    search_fields = ('transaction_id', 'user__username')
    filter_horizontal = ('courses',)
    readonly_fields = ('transaction_id', 'created_at')


@admin.register(CoinTransaction)
class CoinTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'action_type', 'description', 'created_at')
    list_filter = ('action_type', 'created_at')
    search_fields = ('user__username', 'description')
    readonly_fields = ('created_at',)


@admin.register(CoinShopItem)
class CoinShopItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'item_type', 'price_coins', 'is_available')
    list_filter = ('item_type', 'is_available')
    search_fields = ('title', 'description')


# =============================================================================
# 🏢 LEARNING CENTER ERP / CRM ADMIN REGISTRATIONS
# =============================================================================

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'floor', 'equipment', 'color_code')
    search_fields = ('name', 'equipment')


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'room', 'days_schedule', 'start_time', 'end_time', 'monthly_fee', 'is_active')
    list_filter = ('days_schedule', 'is_active', 'teacher', 'room')
    search_fields = ('name', 'teacher__username', 'teacher__first_name')
    filter_horizontal = ('students',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'group', 'date', 'status', 'recorded_by')
    list_filter = ('status', 'date', 'group')
    search_fields = ('student__username', 'student__first_name', 'group__name')


@admin.register(StudentPayment)
class StudentPaymentAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'student', 'group', 'amount', 'payment_method', 'payment_month', 'status', 'payment_date')
    list_filter = ('status', 'payment_method', 'payment_month')
    search_fields = ('receipt_number', 'student__username', 'student__first_name')
    readonly_fields = ('receipt_number', 'created_at')


@admin.register(TeacherSalary)
class TeacherSalaryAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'month', 'calculation_type', 'percentage', 'total_student_revenue', 'final_salary', 'is_paid', 'paid_date')
    list_filter = ('month', 'calculation_type', 'is_paid')
    search_fields = ('teacher__username', 'teacher__first_name')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'amount', 'date', 'paid_to')
    list_filter = ('category', 'date')
    search_fields = ('title', 'description', 'paid_to')


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'interested_subject', 'preferred_teacher', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'preferred_teacher')
    search_fields = ('full_name', 'phone_number', 'interested_subject')


@admin.register(TeacherReview)
class TeacherReviewAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'author_name', 'author_role', 'rating', 'exam_result', 'created_at')
    list_filter = ('rating', 'teacher')
    search_fields = ('teacher__username', 'author_name', 'comment')

