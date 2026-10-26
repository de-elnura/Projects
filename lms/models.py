import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Talaba'),
        ('teacher', "O'qituvchi"),
        ('admin', 'Administrator'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    xp_points = models.PositiveIntegerField(default=0, verbose_name="XP Ballari")
    bio = models.TextField(blank=True, verbose_name="Haqida")
    headline = models.CharField(max_length=255, blank=True, verbose_name="Kasbi yoki unvoni")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    avatar_url = models.CharField(max_length=500, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()}) - {self.xp_points} XP"

    @property
    def display_name(self):
        full = self.user.get_full_name()
        return full if full else self.user.username

    @property
    def rank_title(self):
        if self.xp_points >= 800:
            return "Grandmaster 🏆"
        elif self.xp_points >= 500:
            return "Senior Expert 🌟"
        elif self.xp_points >= 300:
            return "Professional ⚡"
        elif self.xp_points >= 150:
            return "Faol Izlanuvchi 🚀"
        return "Boshlovchi 🌱"

    @property
    def is_teacher(self):
        return self.role in ('teacher', 'admin') or self.user.is_superuser


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True, verbose_name="Kategoriya nomi")
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    icon = models.CharField(max_length=60, default='fas fa-code', help_text="FontAwesome yoki Tailwind ikonka nomi")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(models.Model):
    LEVEL_CHOICES = (
        ('beginner', "Boshlang'ich"),
        ('intermediate', "O'rta"),
        ('advanced', "Murakkab"),
    )

    title = models.CharField(max_length=255, verbose_name="Kurs nomi")
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instructed_courses', verbose_name="O'qituvchi")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    short_description = models.CharField(max_length=300, verbose_name="Qisqa tavsif")
    description = models.TextField(verbose_name="Batafsil ma'lumot")
    thumbnail = models.ImageField(upload_to='courses/', blank=True, null=True)
    thumbnail_url = models.CharField(max_length=500, blank=True, default='')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    duration_hours = models.PositiveIntegerField(default=12, verbose_name="Umumiy soati")
    is_published = models.BooleanField(default=True, verbose_name="Chop etilgan")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or 'kurs'
            unique_slug = base_slug
            counter = 1
            while Course.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def total_lessons_count(self):
        return Lesson.objects.filter(module__course=self).count()

    @property
    def total_students_count(self):
        return self.enrollments.count()


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255, verbose_name="Modul nomi")
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1, verbose_name="Tartibi")
    pass_percentage = models.PositiveIntegerField(default=70, verbose_name="O'tish foizi (standart 70%)")

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.course.title} - {self.order}-Modul: {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255, verbose_name="Dars nomi")
    order = models.PositiveIntegerField(default=1, verbose_name="Tartibi")
    video_url = models.CharField(max_length=500, blank=True, help_text="YouTube embed link yoki video URL")
    content = models.TextField(verbose_name="Dars matni va amaliy mashqlar")
    duration_minutes = models.PositiveIntegerField(default=15, verbose_name="Davomiyligi (daqiqa)")
    is_free_preview = models.BooleanField(default=False, verbose_name="Bepul tanishuv darsi")

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.module.title} -> {self.order}. {self.title}"

    @property
    def embed_video_url(self):
        if not self.video_url:
            return ""
        url = self.video_url.strip()
        if "watch?v=" in url:
            video_id = url.split("watch?v=")[1].split("&")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        return url


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} -> {self.course.title}"


class LessonProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progresses')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='student_progresses')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student.username} - {self.lesson.title}: {'Bajarildi' if self.is_completed else 'Bajarilmagan'}"


class Quiz(models.Model):
    module = models.OneToOneField(Module, on_delete=models.CASCADE, related_name='quiz')
    title = models.CharField(max_length=255, verbose_name="Test nomi")
    description = models.TextField(blank=True, verbose_name="Test haqida qisqacha yo'riqnoma")
    time_limit_minutes = models.PositiveIntegerField(default=10, verbose_name="Vaqt chegarasi (daqiqa)")
    passing_score = models.PositiveIntegerField(default=70, verbose_name="O'tish foizi (%)")

    class Meta:
        verbose_name = "Imtihon / Quiz"
        verbose_name_plural = "Imtihonlar / Quizlar"

    def __str__(self):
        return f"{self.module.course.title} - {self.module.title} Testi"

    @property
    def total_questions_count(self):
        return self.questions.count()


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    order = models.PositiveIntegerField(default=1)
    question_text = models.TextField(verbose_name="Savol matni")
    points = models.PositiveIntegerField(default=10, verbose_name="Ball (XP)")
    explanation = models.TextField(blank=True, verbose_name="To'g'ri javob izohi")

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.quiz.title} - {self.order}-savol"


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=500, verbose_name="Variant matni")
    is_correct = models.BooleanField(default=False, verbose_name="To'g'ri javob")

    def __str__(self):
        return f"{self.option_text} ({'To\'g\'ri' if self.is_correct else 'Noto\'g\'ri'})"


class QuizAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    passed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title}: {self.percentage:.1f}% ({'Otdi' if self.passed else 'Otmadi'})"


class UserAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Urinish #{self.attempt.id} - Savol #{self.question.id}: {self.is_correct}"


class Certificate(models.Model):
    certificate_id = models.CharField(max_length=40, unique=True, default=uuid.uuid4)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    issue_date = models.DateTimeField(auto_now_add=True)
    final_grade = models.FloatField(default=100.0)

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-issue_date']

    def __str__(self):
        return f"Sertifikat: {self.student.username} - {self.course.title} ({self.certificate_id})"

    @property
    def formatted_id(self):
        return f"SKILL-{str(self.certificate_id)[:8].upper()}"
