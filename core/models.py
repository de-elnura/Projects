import uuid
import re
from django.db import models
from django.contrib.auth.models import AbstractUser, Group as AuthGroup, Permission
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Talaba'),
        ('teacher', "O'qituvchi"),
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student',
        verbose_name="Foydalanuvchi roli"
    )
    total_xp = models.PositiveIntegerField(
        default=0,
        verbose_name="Umumiy XP ballari"
    )
    headline = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name="Kasbi yoki unvoni"
    )
    bio = models.TextField(
        blank=True,
        default='',
        verbose_name="Haqida / Tajriba"
    )
    avatar_url = models.CharField(
        max_length=500,
        blank=True,
        default='',
        verbose_name="Avatar rasm havolasi"
    )
    edu_coins = models.PositiveIntegerField(
        default=0,
        verbose_name="EduCoin Balansi"
    )
    has_vip_badge = models.BooleanField(
        default=False,
        verbose_name="Oltin VIP Profil Nishoni"
    )
    monthly_salary = models.PositiveIntegerField(
        default=5000000,
        verbose_name="Oylik maoshi (so'm)"
    )
    experience_years = models.PositiveIntegerField(
        default=4,
        verbose_name="Ish tajribasi (yil)"
    )
    specialties = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name="Mutaxassisliklari va sertifikatlari"
    )
    students_count = models.PositiveIntegerField(
        default=50,
        verbose_name="O'quvchilar soni"
    )
    exam_results_summary = models.CharField(
        max_length=255,
        blank=True,
        default="O'quvchilarining 92% qismi Milliy Sertifikat / IELTS 7.5+ olgan",
        verbose_name="Imtihon ko'rsatkichlari (IELTS/Sertifikat)"
    )

    # Nomlar to'qnashuvi bo'lmasligi uchun custom_user_set berildi
    groups = models.ManyToManyField(
        AuthGroup,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='user',
    )

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        full_name = self.get_full_name()
        if full_name:
            return f"{full_name} ({self.username}) - {self.get_role_display()}"
        return f"{self.username} - {self.get_role_display()}"

    def get_salary_display(self):
        """O'qituvchining oylik maoshini formatlab qaytaradi."""
        return f"{self.monthly_salary:,} so'm / oy"

    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_teacher(self):
        return self.role == 'teacher' or self.is_staff or self.is_superuser

    def get_average_rating(self):
        """O'qituvchining ota-onalar va talabalar tomonidan berilgan o'rtacha reytingi."""
        reviews = self.reviews.all()
        if reviews.exists():
            avg = reviews.aggregate(models.Avg('rating'))['rating__avg']
            return round(avg, 1) if avg else 4.9
        return min(5.0, round(4.6 + (self.experience_years * 0.04), 1))

    def get_parent_reviews(self):
        """O'qituvchiga qoldirilgan ota-onalar sharhlari."""
        return self.reviews.all()[:5]

    def get_active_teaching_groups(self):
        """O'qituvchi dars o'tadigan faol guruhlar."""
        return self.teaching_groups.filter(is_active=True)


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Kurs nomi")
    description = models.TextField(verbose_name="Kurs tavsifi")
    category = models.CharField(
        max_length=50,
        default='Backend',
        verbose_name="Kategoriya"
    )
    level = models.CharField(
        max_length=30,
        default="Boshlang'ich",
        verbose_name="Daraja"
    )
    duration_hours = models.PositiveIntegerField(
        default=15,
        verbose_name="Davomiyligi (soat)"
    )
    thumbnail_url = models.CharField(
        max_length=500,
        blank=True,
        default='',
        verbose_name="Kurs muqovasi havolasi"
    )
    price = models.PositiveIntegerField(
        default=0,
        verbose_name="Asl narxi (so'm)"
    )
    discount_price = models.PositiveIntegerField(
        default=0,
        verbose_name="Chegirmali narxi (so'm)"
    )
    is_free = models.BooleanField(
        default=False,
        verbose_name="Bepul kursmi?"
    )
    SCHEDULE_CHOICES = (
        ('toq', 'Toq kunlari (Dushanba - Chorshanba - Juma)'),
        ('juft', 'Juft kunlari (Seshanba - Payshanba - Shanba)'),
        ('hafta_oxiri', 'Hafta oxiri (Shanba - Yakshanba)'),
        ('har_kuni', 'Har kuni (Intensiv)'),
    )
    schedule_type = models.CharField(
        max_length=30,
        choices=SCHEDULE_CHOICES,
        default='toq',
        verbose_name="Mashg'ulot kunlari"
    )
    schedule_time = models.CharField(
        max_length=50,
        default='18:00 - 19:30',
        verbose_name="Dars vaqti (Online)"
    )
    lesson_format = models.CharField(
        max_length=50,
        default='Online (Jonli efir)',
        verbose_name="Dars formati"
    )
    is_modern_profession = models.BooleanField(
        default=False,
        verbose_name="Zamonaviy qimmat kasbmi?"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name="Muallif / O'qituvchi"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"

    def __str__(self):
        return self.title

    def get_effective_price(self):
        """Haqiqiy to'lanadigan narxni qaytaradi."""
        if self.is_free:
            return 0
        if self.discount_price > 0:
            return self.discount_price
        return self.price

    def get_discount_percent(self):
        """Chegirma foizini hisoblaydi."""
        if self.price > 0 and self.discount_price > 0 and self.discount_price < self.price:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0

    def get_schedule_display_full(self):
        """Dars kunlari va vaqtini chiroyli formatda qaytaradi."""
        return f"{self.get_schedule_type_display()} • {self.schedule_time}"

    def is_user_enrolled(self, user):
        """Foydalanuvchi kursga yozilganligini tekshiradi."""
        if not user or not user.is_authenticated:
            return False
        if self.is_free or user.is_teacher or user.is_staff or self.author == user:
            return True
        return self.enrollments.filter(user=user, status='completed').exists()

    def get_total_lessons(self):
        return Lesson.objects.filter(module__course=self).count()

    def get_first_lesson(self):
        """Kursning eng birinchi darsini topadi."""
        return Lesson.objects.filter(module__course=self).order_by('module__order', 'order').first()

    def get_total_quizzes(self):
        return Quiz.objects.filter(module__course=self).count()

    def is_completed_by(self, user):
        """Talaba kursning barcha testlaridan muvaffaqiyatli o'tganligini tekshiradi."""
        if not user.is_authenticated:
            return False
        quizzes = Quiz.objects.filter(module__course=self)
        if not quizzes.exists():
            # Agar testlar bo'lmasa, barcha darslar tugatilganligini tekshirish
            total_lessons = self.get_total_lessons()
            if total_lessons == 0:
                return False
            completed_count = UserLessonProgress.objects.filter(
                user=user,
                lesson__module__course=self,
                is_completed=True
            ).count()
            return completed_count >= total_lessons

        passed_quizzes = QuizResult.objects.filter(
            user=user,
            quiz__in=quizzes,
            is_passed=True
        ).values('quiz_id').distinct().count()

        return passed_quizzes >= quizzes.count()


class Module(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name="Tegishli kurs"
    )
    title = models.CharField(max_length=255, verbose_name="Modul nomi")
    order = models.PositiveIntegerField(default=1, verbose_name="Tartib raqami")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Modul"
        verbose_name_plural = "Modullar"

    def __str__(self):
        return f"{self.course.title} -> {self.order}-Modul: {self.title}"

    def get_previous_module(self):
        """Ushbu moduldan oldingi modulni qaytaradi."""
        return Module.objects.filter(
            course=self.course,
            order__lt=self.order
        ).order_by('-order').first()

    def is_unlocked_for(self, user):
        """
        Talaba oldingi modul testidan kamida passing_score (70%) to'plagan bo'lsa,
        ushbu modul ochiladi. 1-modul har doim ochiq bo'ladi.
        """
        if not user or not user.is_authenticated:
            return False

        # O'qituvchi yoki admin uchun barcha modullar doim ochiq
        if user.is_teacher or user.is_staff:
            return True

        prev_module = self.get_previous_module()
        if not prev_module:
            # Oldingi modul yo'q (birinchi modul) — ochiq!
            return True

        # Oldingi modulda test bormi?
        if hasattr(prev_module, 'quiz') and prev_module.quiz:
            has_passed = QuizResult.objects.filter(
                user=user,
                quiz=prev_module.quiz,
                is_passed=True
            ).exists()
            return has_passed

        # Agar oldingi modulda test bo'lmasa, undagi barcha darslar tugatilgan bo'lishi kerak
        prev_lessons = prev_module.lessons.all()
        if not prev_lessons.exists():
            return True

        completed_count = UserLessonProgress.objects.filter(
            user=user,
            lesson__in=prev_lessons,
            is_completed=True
        ).count()
        return completed_count >= prev_lessons.count()


class Lesson(models.Model):
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name="Tegishli modul"
    )
    title = models.CharField(max_length=255, verbose_name="Dars mavzusi")
    video_url = models.URLField(blank=True, null=True, verbose_name="Video havola (YouTube / MP4)")
    content = models.TextField(blank=True, verbose_name="Dars matni va nazariya")
    order = models.PositiveIntegerField(default=1, verbose_name="Tartib raqami")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"

    def __str__(self):
        return f"{self.module.title} -> {self.order}-dars: {self.title}"

    def get_embed_video_url(self):
        """YouTube havolasini avtomatik embed formatga o'giradi."""
        if not self.video_url:
            return None
        url = self.video_url.strip()
        # https://www.youtube.com/watch?v=VIDEO_ID
        match = re.search(r'(?:v=|\/embed\/|youtu\.be\/)([a-zA-Z0-9_-]{11})', url)
        if match:
            return f"https://www.youtube.com/embed/{match.group(1)}?rel=0&modestbranding=1"
        return url

    def is_completed_by(self, user):
        if not user or not user.is_authenticated:
            return False
        return UserLessonProgress.objects.filter(user=user, lesson=self, is_completed=True).exists()

    def is_unlocked_for(self, user):
        """Dars o'zining moduli ochiq bo'lsa ochiq hisoblanadi."""
        return self.module.is_unlocked_for(user)

    def get_next_lesson(self):
        """Keyingi darsni topadi (shu moduldan yoki keyingi moduldan)."""
        next_in_module = Lesson.objects.filter(
            module=self.module,
            order__gt=self.order
        ).order_by('order').first()
        if next_in_module:
            return next_in_module

        # Agar modulda dars qolmagan bo'lsa, keyingi modulning 1-darsi
        next_module = Module.objects.filter(
            course=self.module.course,
            order__gt=self.module.order
        ).order_by('order').first()
        if next_module:
            return next_module.lessons.order_by('order').first()
        return None

    def get_previous_lesson(self):
        """Oldingi darsni topadi."""
        prev_in_module = Lesson.objects.filter(
            module=self.module,
            order__lt=self.order
        ).order_by('-order').first()
        if prev_in_module:
            return prev_in_module

        prev_module = Module.objects.filter(
            course=self.module.course,
            order__lt=self.module.order
        ).order_by('-order').first()
        if prev_module:
            return prev_module.lessons.order_by('-order').first()
        return None


class Quiz(models.Model):
    module = models.OneToOneField(
        Module,
        on_delete=models.CASCADE,
        related_name='quiz',
        verbose_name="Tegishli modul"
    )
    title = models.CharField(max_length=255, verbose_name="Test nomi")
    passing_score = models.PositiveIntegerField(
        default=70,
        verbose_name="O'tish bali (%)"
    )
    duration_minutes = models.PositiveIntegerField(
        default=10,
        verbose_name="Ajratilgan vaqt (daqiqa)"
    )

    class Meta:
        verbose_name = "Test (Imtihon)"
        verbose_name_plural = "Testlar (Imtihonlar)"

    def __str__(self):
        return f"{self.module.title} — {self.title}"

    def is_unlocked_for(self, user):
        """Test topshirish uchun modul ochiq bo'lishi kerak."""
        return self.module.is_unlocked_for(user)

    def get_user_latest_result(self, user):
        if not user or not user.is_authenticated:
            return None
        return self.results.filter(user=user).order_by('-created_at').first()


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name="Tegishli test"
    )
    text = models.TextField(verbose_name="Savol matni")

    class Meta:
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"

    def __str__(self):
        return f"{self.quiz.title} | {self.text[:50]}"


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices',
        verbose_name="Tegishli savol"
    )
    text = models.CharField(max_length=255, verbose_name="Variant matni")
    is_correct = models.BooleanField(default=False, verbose_name="To'g'ri javobmi?")

    class Meta:
        verbose_name = "Javob varianti"
        verbose_name_plural = "Javob variantlari"

    def __str__(self):
        mark = "✓" if self.is_correct else "✗"
        return f"[{mark}] {self.text}"


class UserLessonProgress(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='lesson_progress',
        verbose_name="Foydalanuvchi"
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='progress',
        verbose_name="Dars"
    )
    is_completed = models.BooleanField(default=False, verbose_name="Tugatilganmi?")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Tugatilgan vaqt")

    class Meta:
        unique_together = ('user', 'lesson')
        verbose_name = "Dars o'zlashtirish jarayoni"
        verbose_name_plural = "Dars o'zlashtirish jarayonlari"

    def __str__(self):
        status = "Bajarildi" if self.is_completed else "Jarayonda"
        return f"{self.user.username} - {self.lesson.title}: {status}"


class QuizResult(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='quiz_results',
        verbose_name="Foydalanuvchi"
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name="Test"
    )
    score = models.FloatField(verbose_name="To'plangan foiz (%)")
    is_passed = models.BooleanField(default=False, verbose_name="O'tdimi?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Topshirilgan vaqt")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Test natijasi"
        verbose_name_plural = "Test natijalari"

    def __str__(self):
        status = "O'tdi" if self.is_passed else "Yiqildi"
        return f"{self.user.username} - {self.quiz.title}: {self.score}% ({status})"


class Certificate(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='certificates',
        verbose_name="Talaba"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='certificates',
        verbose_name="Tugatilgan kurs"
    )
    issued_date = models.DateTimeField(auto_now_add=True, verbose_name="Berilgan sana")
    certificate_code = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="Unikal sertifikat kodi"
    )

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = "Sertifikat"
        verbose_name_plural = "Sertifikatlar"

    def __str__(self):
        return f"Sertifikat: {self.user.username} - {self.course.title} [{self.certificate_code}]"

    @classmethod
    def generate_code(cls, course_id, user_id):
        random_suffix = uuid.uuid4().hex[:8].upper()
        return f"SKILLUP-C{course_id}-U{user_id}-{random_suffix}"


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Promokod")
    discount_percent = models.PositiveIntegerField(default=20, verbose_name="Chegirma foizi (%)")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")
    valid_until = models.DateTimeField(null=True, blank=True, verbose_name="Amal qilish muddati")
    max_uses = models.PositiveIntegerField(default=100, verbose_name="Maksimal ishlatishlar soni")
    used_count = models.PositiveIntegerField(default=0, verbose_name="Ishlatilgan soni")

    class Meta:
        verbose_name = "Promokod / Kupon"
        verbose_name_plural = "Promokodlar va Kuponlar"

    def __str__(self):
        return f"{self.code} (-{self.discount_percent}%)"

    def is_valid(self):
        if not self.is_active:
            return False
        if self.max_uses > 0 and self.used_count >= self.max_uses:
            return False
        if self.valid_until and timezone.now() > self.valid_until:
            return False
        return True


class Enrollment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('click', 'Click Up'),
        ('payme', 'Payme'),
        ('uzum', 'Uzum Bank'),
        ('free_promo', 'Bepul Promokod / Grant'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name="Talaba"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name="Kurs"
    )
    amount_paid = models.PositiveIntegerField(default=0, verbose_name="To'langan summa (so'm)")
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Qo'llangan Promokod"
    )
    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,
        default='click',
        verbose_name="To'lov usuli"
    )
    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Kvitansiya / Chek ID"
    )
    status = models.CharField(max_length=20, default='completed', verbose_name="Holati")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Xarid vaqti")

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'course')
        verbose_name = "Kursga a'zolik / Xarid"
        verbose_name_plural = "Kursga a'zoliklar va Xaridlar"

    def __str__(self):
        return f"{self.user.username} -> {self.course.title} ({self.amount_paid:,} so'm)"

    @classmethod
    def generate_transaction_id(cls, user_id, course_id):
        suffix = uuid.uuid4().hex[:10].upper()
        return f"TXN-{user_id}-{course_id}-{suffix}"


class BundleEnrollment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bundle_enrollments',
        verbose_name="Talaba"
    )
    courses = models.ManyToManyField(
        Course,
        related_name='bundle_enrollments',
        verbose_name="Tanlangan To'garaklar"
    )
    total_original_price = models.PositiveIntegerField(default=0, verbose_name="Boshlang'ich umumiy summa")
    bundle_discount = models.PositiveIntegerField(default=0, verbose_name="Paketli chegirma miqdori (50k yoki 100k)")
    final_amount = models.PositiveIntegerField(default=0, verbose_name="Yakuniy to'langan summa")
    payment_method = models.CharField(max_length=50, default='click', verbose_name="To'lov tizimi")
    transaction_id = models.CharField(max_length=100, unique=True, verbose_name="Kvitansiya ID")
    start_date_str = models.CharField(max_length=100, default="Ertadan boshlanadi", verbose_name="Mashg'ulot boshlanish sanasi")
    status = models.CharField(max_length=20, default='completed', verbose_name="Holati")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="A'zolik vaqti")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Paketli To'garaklar A'zoligi"
        verbose_name_plural = "Paketli To'garaklar A'zoliklari"

    def __str__(self):
        return f"{self.user.username} -> {self.courses.count()} ta to'garak ({self.final_amount:,} so'm)"

    @classmethod
    def generate_transaction_id(cls, user_id):
        suffix = uuid.uuid4().hex[:10].upper()
        return f"BUNDLE-{user_id}-{suffix}"


class CoinTransaction(models.Model):
    ACTION_CHOICES = (
        ('attendance_streak', 'Darsga o\'z vaqtida kelish (Davomat) (+15 🪙)'),
        ('homework_perfect', 'Uy vazifasini 100% a\'lo bajarish (+25 🪙)'),
        ('class_activity', 'Darsda faollik (Savol-javob & amaliyot) (+20 🪙)'),
        ('quiz_passed', 'Modul testidan o\'tish (70%+) (+30 🪙)'),
        ('quiz_perfect', 'Imtihondan 100% a\'lo natija (+50 🪙)'),
        ('book_reading', 'Badiiy kitob mutolaasi va taqdimoti (+35 🪙)'),
        ('weekly_streak', 'Haftalik intizom va faollik bonusi (+40 🪙)'),
        ('course_completed', 'Kursni tamomlab Sertifikat olish (+150 🪙)'),
        ('welcome_bonus', 'Xush Kelibsiz Bonusi (+100 🪙)'),
        ('lesson_completed', 'Dars Tugatildi (+10 🪙)'),
        ('daily_streak', 'Kunlik Faollik (+15 🪙)'),
        ('course_enrolled', 'Yangi Kurs Xaridi (+40 🪙)'),
        ('profile_completed', 'Profil To\'ldirildi (+30 🪙)'),
        ('shop_purchase', 'Do\'kondan Xarid (- 🪙)'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='coin_transactions',
        verbose_name="Talaba"
    )
    amount = models.IntegerField(verbose_name="Tanga miqdori (+ yoki -)")
    action_type = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES,
        default='lesson_completed',
        verbose_name="Yutuq / Harakat turi"
    )
    description = models.CharField(max_length=255, verbose_name="Tavsif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Vaqti")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "EduCoin Tranzaksiyasi"
        verbose_name_plural = "EduCoin Tranzaksiyalari"

    def __str__(self):
        mark = f"+{self.amount}" if self.amount > 0 else f"{self.amount}"
        return f"{self.user.username}: {mark} 🪙 ({self.description})"


class CoinShopItem(models.Model):
    ITEM_TYPE_CHOICES = (
        ('coupon_50', '-50% Chegirma Kuponi'),
        ('vip_badge', 'Oltin VIP Profil Nishoni'),
        ('mentor_call', 'Murabbiy bilan 1-ga-1 Konsultatsiya'),
        ('merch', 'SkillUp Brendli Merch To\'plami'),
    )
    title = models.CharField(max_length=255, verbose_name="Sovg'a nomi")
    description = models.TextField(verbose_name="Batafsil tavsifi")
    price_coins = models.PositiveIntegerField(default=100, verbose_name="Narxi (EduCoin)")
    item_type = models.CharField(
        max_length=50,
        choices=ITEM_TYPE_CHOICES,
        default='coupon_50',
        verbose_name="Sovg'a toifasi"
    )
    icon = models.CharField(
        max_length=60,
        default='fa-solid fa-gift',
        verbose_name="Ikonka klassi"
    )
    is_available = models.BooleanField(default=True, verbose_name="Mavjudmi?")

    class Meta:
        ordering = ['price_coins']
        verbose_name = "Do'kon Mahsuloti"
        verbose_name_plural = "Do'kon Mahsulotlari"

    def __str__(self):
        return f"{self.title} ({self.price_coins} 🪙)"


# =============================================================================
# 🏢 LEARNING CENTER ERP / CRM & FINANCE MODELLARI
# =============================================================================

class Room(models.Model):
    """O'quv markaz dars xonalari va laboratoriyalari."""
    name = models.CharField(max_length=100, verbose_name="Xona nomi / raqami")
    capacity = models.PositiveIntegerField(default=16, verbose_name="Sig'imi (o'quvchi o'rni)")
    floor = models.CharField(max_length=50, default="1-qavat", verbose_name="Bino qavati")
    equipment = models.CharField(
        max_length=255,
        default="Proyektor, elektron doska, konditsioner, yuqori tezlikdagi Wi-Fi",
        verbose_name="Jihozlar"
    )
    color_code = models.CharField(max_length=20, default="#4f46e5", verbose_name="Jadvaldagi rangi")

    class Meta:
        ordering = ['name']
        verbose_name = "O'quv xonasi"
        verbose_name_plural = "O'quv xonalari"

    def __str__(self):
        return f"{self.name} ({self.capacity} o'rin)"


class StudyGroup(models.Model):
    """O'quv markaz guruhlari."""
    SCHEDULE_CHOICES = (
        ('toq', 'Toq kunlar (Dushanba - Chorshanba - Juma)'),
        ('juft', 'Juft kunlar (Seshanba - Payshanba - Shanba)'),
        ('hafta_oxiri', 'Hafta oxiri (Shanba - Yakshanba)'),
        ('har_kuni', 'Har kuni (Intensiv guruh)'),
    )
    name = models.CharField(max_length=150, verbose_name="Guruh nomi")
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='study_groups',
        verbose_name="Tegishli kurs / fan"
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='teaching_groups',
        verbose_name="Mas'ul o'qituvchi"
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='study_groups',
        verbose_name="Dars xonasi"
    )
    days_schedule = models.CharField(
        max_length=30,
        choices=SCHEDULE_CHOICES,
        default='toq',
        verbose_name="Dars kunlari tartibi"
    )
    start_time = models.CharField(max_length=20, default="14:00", verbose_name="Boshlanish vaqti")
    end_time = models.CharField(max_length=20, default="16:00", verbose_name="Tugash vaqti")
    monthly_fee = models.PositiveIntegerField(default=500000, verbose_name="Oylik to'lov summasi (so'm)")
    students = models.ManyToManyField(
        User,
        blank=True,
        related_name='study_groups',
        verbose_name="Guruh talabalari"
    )
    is_active = models.BooleanField(default=True, verbose_name="Faol guruhmi?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Tashkil etilgan sana")

    class Meta:
        ordering = ['-is_active', 'name']
        verbose_name = "O'quv Guruhi"
        verbose_name_plural = "O'quv Guruhlari"

    def __str__(self):
        return f"{self.name} | {self.teacher.get_full_name() or self.teacher.username} ({self.get_days_schedule_display()})"

    def get_active_students_count(self):
        return self.students.count()

    def get_expected_monthly_revenue(self):
        return self.students.count() * self.monthly_fee

    def get_schedule_badge(self):
        return f"{self.start_time} - {self.end_time} &bull; {self.get_days_schedule_display()}"


# Qisqartma taxallus (alias)
Group = StudyGroup


class Attendance(models.Model):
    """Guruh talabalarining darslardagi davomati."""
    STATUS_CHOICES = (
        ('present', 'Keldi (Bor)'),
        ('excused', 'Sababli kelmadi'),
        ('absent', 'Sababsiz kelmadi (Qoldirdi)'),
    )
    group = models.ForeignKey(
        StudyGroup,
        on_delete=models.CASCADE,
        related_name='attendances',
        verbose_name="Guruh"
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='attendances',
        verbose_name="Talaba"
    )
    date = models.DateField(default=timezone.now, verbose_name="Dars sanasi")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='present',
        verbose_name="Davomat holati"
    )
    recorded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recorded_attendances',
        verbose_name="Qayd etgan o'qituvchi/admin"
    )
    notes = models.CharField(max_length=255, blank=True, default='', verbose_name="Sabab / Izoh")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group', 'student', 'date')
        ordering = ['-date', 'student__first_name']
        verbose_name = "Davomat qaydi"
        verbose_name_plural = "Davomat jurnali"

    def __str__(self):
        return f"{self.student.username} - {self.group.name} [{self.date}]: {self.get_status_display()}"

    @classmethod
    def get_consecutive_absences_students(cls, consecutive_count=3):
        """
        Ketma-ket 3 kun (yoki belgilangan sondan ko'p) dars qoldirgan talabalar ro'yxatini qaytaradi.
        Bu administrator paneli uchun muhim ogohlantirish (Alert) beradi.
        """
        alerts = []
        active_groups = StudyGroup.objects.filter(is_active=True).prefetch_related('students')
        for grp in active_groups:
            for st in grp.students.all():
                recent_records = cls.objects.filter(
                    group=grp,
                    student=st
                ).order_by('-date')[:consecutive_count]

                if recent_records.count() >= consecutive_count:
                    # Agar oxirgi barcha qaydlar 'absent' (sababsiz kelmadi) bo'lsa
                    if all(r.status == 'absent' for r in recent_records):
                        dates_str = ", ".join([r.date.strftime("%d.%m") for r in recent_records])
                        alerts.append({
                            'student': st,
                            'group': grp,
                            'consecutive_count': consecutive_count,
                            'dates': dates_str,
                            'phone': getattr(st, 'headline', '') or "Bog'lanish kutilmoqda",
                        })
        return alerts


class StudentPayment(models.Model):
    """Talabalar oylik to'lovlari (Finance & Accounting)."""
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Naqd pul'),
        ('click', 'Click Up'),
        ('payme', 'Payme'),
        ('uzum', 'Uzum Bank'),
        ('transfer', 'Bank hisob raqami'),
    )
    STATUS_CHOICES = (
        ('paid', "To'langan (To'liq)"),
        ('partial', "Qisman to'langan"),
        ('debt', "Qarzdor"),
        ('cancelled', "Bekor qilingan"),
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='student_payments',
        verbose_name="Talaba"
    )
    group = models.ForeignKey(
        StudyGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name="O'quv guruhi"
    )
    amount = models.PositiveIntegerField(default=0, verbose_name="To'langan summa (so'm)")
    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES,
        default='click',
        verbose_name="To'lov usuli"
    )
    payment_date = models.DateField(default=timezone.now, verbose_name="To'lov sanasi")
    payment_month = models.CharField(
        max_length=30,
        default="2026-10",
        verbose_name="Qaysi oy uchun (Masalan: 2026-10)"
    )
    receipt_number = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="Kvitansiya / Chek ID"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='paid',
        verbose_name="To'lov holati"
    )
    notes = models.TextField(blank=True, default='', verbose_name="To'lov izohi")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-payment_date', '-created_at']
        verbose_name = "Talaba To'lovi"
        verbose_name_plural = "Talabalar To'lovlari"

    def __str__(self):
        return f"{self.student.username} -> {self.amount:,} so'm ({self.payment_month}) [{self.receipt_number}]"

    @classmethod
    def generate_receipt_number(cls, student_id):
        suffix = uuid.uuid4().hex[:6].upper()
        return f"REC-{timezone.now().strftime('%Y%m')}-U{student_id}-{suffix}"


class TeacherSalary(models.Model):
    """O'qituvchilar maoshi hisob-kitobi (Kalkulyator va qaydlar)."""
    CALCULATION_CHOICES = (
        ('percentage', "Talabalar to'lovidan foiz (40-50%)"),
        ('fixed', "Qat'iy oylik stavka"),
        ('mixed', "Stavka + Bonus/Foiz"),
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='salary_records',
        verbose_name="O'qituvchi"
    )
    month = models.CharField(max_length=30, default="2026-10", verbose_name="Hisob oyi (YYYY-MM)")
    calculation_type = models.CharField(
        max_length=30,
        choices=CALCULATION_CHOICES,
        default='percentage',
        verbose_name="Maosh hisoblash turi"
    )
    percentage = models.PositiveIntegerField(default=45, verbose_name="O'quvchi to'lovidan foiz (%)")
    fixed_amount = models.PositiveIntegerField(default=5000000, verbose_name="Qat'iy stavka (so'm)")
    total_student_revenue = models.PositiveIntegerField(default=0, verbose_name="Guruhlardan tushgan tushum")
    calculated_salary = models.PositiveIntegerField(default=0, verbose_name="Hisoblangan maosh summasi")
    bonus = models.PositiveIntegerField(default=0, verbose_name="Rag'batlantirish bonusi")
    deductions = models.PositiveIntegerField(default=0, verbose_name="Ushlanmalar")
    final_salary = models.PositiveIntegerField(default=0, verbose_name="Yakuniy to'lanadigan sof maosh")
    is_paid = models.BooleanField(default=False, verbose_name="To'lab berildimi?")
    paid_date = models.DateField(null=True, blank=True, verbose_name="To'langan sana")
    notes = models.TextField(blank=True, default='', verbose_name="Moliya bo'limi izohi")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-month', '-created_at']
        unique_together = ('teacher', 'month')
        verbose_name = "O'qituvchi Maoshi Qaydi"
        verbose_name_plural = "O'qituvchilar Maoshlari Qaydlari"

    def __str__(self):
        status = "To'langan" if self.is_paid else "Kutilmoqda"
        return f"{self.teacher.get_full_name() or self.teacher.username} | {self.month}: {self.final_salary:,} so'm ({status})"

    def calculate_salary(self):
        """Avtomatik ravishda maoshni hisoblaydi."""
        if self.calculation_type == 'percentage':
            base = int(self.total_student_revenue * (self.percentage / 100.0))
        elif self.calculation_type == 'fixed':
            base = self.fixed_amount
        else: # mixed
            base = self.fixed_amount + int(self.total_student_revenue * (self.percentage / 100.0))
        
        self.calculated_salary = base
        self.final_salary = max(0, base + self.bonus - self.deductions)
        return self.final_salary


class Expense(models.Model):
    """O'quv markaz xarajatlar daftari (Accounting & Expenses)."""
    CATEGORY_CHOICES = (
        ('rent', "Bino ijarasi"),
        ('utilities', "Kommunal to'lovlar (Elektr, Issiqlik, Suv, Internet)"),
        ('marketing', "Marketing va Reklama (Target, Banner, Flayer)"),
        ('office', "Ofis va kantselyariya (Qog'oz, ruchka, qahva/choy)"),
        ('salary', "Xodimlar va texnik xodimlar maoshi"),
        ('tax', "Soliqlar va litsenziya to'lovlari"),
        ('equipment', "Mebel, kompyuter va texnika ta'miri"),
        ('other', "Boshqa kutilmagan xo'jalik xarajatlari"),
    )
    title = models.CharField(max_length=255, verbose_name="Xarajat nomi / maqsadi")
    category = models.CharField(
        max_length=40,
        choices=CATEGORY_CHOICES,
        default='office',
        verbose_name="Xarajat toifasi"
    )
    amount = models.PositiveIntegerField(verbose_name="Summasi (so'm)")
    date = models.DateField(default=timezone.now, verbose_name="Xarajat sanasi")
    description = models.TextField(blank=True, default='', verbose_name="Batafsil ma'lumot")
    paid_to = models.CharField(max_length=255, blank=True, default='', verbose_name="To'langan shaxs / tashkilot")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = "Xarajat"
        verbose_name_plural = "Xarajatlar Daftari"

    def __str__(self):
        return f"{self.title} - {self.amount:,} so'm ({self.get_category_display()})"


class Lead(models.Model):
    """Lidlar (Mijozlar oqimi va Sinov darsiga yozilish - CRM)."""
    STATUS_CHOICES = (
        ('new', "Yangi ariza (Kutilmoqda)"),
        ('contacted', "Qo'ng'iroq qilindi (Muloqotda)"),
        ('trial', "Sinov darsiga yozildi"),
        ('enrolled', "Guruhga qo'shildi (To'lov qildi)"),
        ('cancelled', "Rad etildi / Qiziqmadi"),
    )
    full_name = models.CharField(max_length=255, verbose_name="F.I.SH. (Ism va Familiya)")
    phone_number = models.CharField(max_length=40, verbose_name="Telefon raqami")
    interested_subject = models.CharField(max_length=150, verbose_name="Qiziqqan fani / to'garak")
    preferred_teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_leads',
        verbose_name="Tanlangan o'qituvchi"
    )
    preferred_time = models.CharField(
        max_length=80,
        blank=True,
        default="14:00 - 18:00 (Kunduzgi)",
        verbose_name="Qulay dars vaqti"
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Lid holati"
    )
    notes = models.TextField(blank=True, default='', verbose_name="Menejer qaydlari va eslatmasi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ariza kelib tushgan vaqt")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Lid / Ariza (CRM)"
        verbose_name_plural = "Lidlar va Sinov darslari (CRM)"

    def __str__(self):
        return f"{self.full_name} ({self.phone_number}) - {self.interested_subject} [{self.get_status_display()}]"


class TeacherReview(models.Model):
    """Ota-onalar va talabalar tomonidan o'qituvchiga qoldirilgan baho va fikrlar."""
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="O'qituvchi"
    )
    author_name = models.CharField(max_length=150, verbose_name="Ota-ona yoki Talaba ismi")
    author_role = models.CharField(max_length=50, default="Ota-ona", verbose_name="Kim tomonidan")
    rating = models.PositiveIntegerField(default=5, verbose_name="Baho (1 dan 5 gacha yulduz)")
    comment = models.TextField(verbose_name="Fikr / Tavsiya")
    exam_result = models.CharField(
        max_length=120,
        blank=True,
        default="Farzandi IELTS 7.5 oldi",
        verbose_name="Erishilgan natija"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "O'qituvchi Sharhi"
        verbose_name_plural = "O'qituvchilar Sharhlari va Baholari"

    def __str__(self):
        return f"{self.teacher.get_full_name()} <- {self.author_name} ({self.rating} ⭐)"

