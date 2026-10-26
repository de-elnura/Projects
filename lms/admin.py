from django.contrib import admin
from .models import (
    UserProfile, Category, Course, Module, Lesson,
    Enrollment, LessonProgress, Quiz, Question, Option,
    QuizAttempt, UserAnswer, Certificate
)


class OptionInline(admin.TabularInline):
    model = Option
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz', 'order', 'question_text', 'points')
    list_filter = ('quiz',)
    inlines = [OptionInline]


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'time_limit_minutes', 'passing_score')
    inlines = [QuestionInline]


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'pass_percentage')
    list_filter = ('course',)
    inlines = [LessonInline]


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'level', 'duration_hours', 'is_published')
    list_filter = ('level', 'is_published', 'category')
    search_fields = ('title', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'xp_points', 'rank_title')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order', 'duration_minutes', 'is_free_preview')
    list_filter = ('module__course', 'module')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'is_completed')
    list_filter = ('is_completed', 'course')


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'is_completed', 'completed_at')
    list_filter = ('is_completed',)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'score', 'percentage', 'passed', 'completed_at')
    list_filter = ('passed', 'quiz')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'certificate_id', 'final_grade', 'issue_date')
    search_fields = ('student__username', 'certificate_id')
