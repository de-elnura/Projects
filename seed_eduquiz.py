import os
import sys
import django

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from lms.models import (
    UserProfile, Category, Course, Module, Lesson,
    Enrollment, LessonProgress, Quiz, Question, Option,
    QuizAttempt, UserAnswer, Certificate
)
from django.utils import timezone


def seed():
    print("=== EduQuiz / SkillUp LMS Ma'lumotlarni yaratish boshlandi ===")

    # 1. Superuser / Admin
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@skillup.uz', 'first_name': 'Administrator', 'last_name': 'EduQuiz'}
    )
    admin_user.set_password('admin123')
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    p_admin, _ = UserProfile.objects.get_or_create(user=admin_user)
    p_admin.role = 'admin'
    p_admin.headline = "Bosh Administrator"
    p_admin.xp_points = 950
    p_admin.save()
    print("✓ Admin: admin / admin123")

    # 2. Teachers
    ustoz_user, _ = User.objects.get_or_create(
        username='ustoz',
        defaults={'email': 'ustoz@skillup.uz', 'first_name': 'Anvar', 'last_name': 'Qodirov'}
    )
    ustoz_user.set_password('parol123')
    ustoz_user.is_staff = True
    ustoz_user.save()
    p_ustoz, _ = UserProfile.objects.get_or_create(user=ustoz_user)
    p_ustoz.role = 'teacher'
    p_ustoz.headline = "Senior Python & Backend Architect"
    p_ustoz.bio = "10 yildan ortiq vaqt davomida yirik ta'lim va moliyaviy tizimlar arxitekturasi bilan shug'ullanib kelayotgan yetakchi muhandis."
    p_ustoz.xp_points = 1450
    p_ustoz.save()
    print("✓ Ustoz: ustoz / parol123")

    malika_user, _ = User.objects.get_or_create(
        username='malika',
        defaults={'email': 'malika@skillup.uz', 'first_name': 'Malika', 'last_name': 'Karimova'}
    )
    malika_user.set_password('parol123')
    malika_user.is_staff = True
    malika_user.save()
    p_malika, _ = UserProfile.objects.get_or_create(user=malika_user)
    p_malika.role = 'teacher'
    p_malika.headline = "Lead Frontend & Full-Stack Engineer"
    p_malika.bio = "Zamonaviy veb texnologiyalar, UI/UX interfeyslar va JavaScript ekotizimi bo'yicha xalqaro sertifikatlar sohibi."
    p_malika.xp_points = 1120
    p_malika.save()
    print("✓ Ustoz 2: malika / parol123")

    # 3. Students
    talaba_user, _ = User.objects.get_or_create(
        username='talaba',
        defaults={'email': 'talaba@skillup.uz', 'first_name': 'Sardor', 'last_name': 'Aliyev'}
    )
    talaba_user.set_password('parol123')
    talaba_user.save()
    p_talaba, _ = UserProfile.objects.get_or_create(user=talaba_user)
    p_talaba.role = 'student'
    p_talaba.headline = "Bo'lajak Backend Dasturchi"
    p_talaba.xp_points = 240
    p_talaba.save()
    print("✓ Talaba: talaba / parol123")

    jasur_user, _ = User.objects.get_or_create(
        username='jasur',
        defaults={'email': 'jasur@skillup.uz', 'first_name': 'Jasur', 'last_name': 'Toshmatov'}
    )
    jasur_user.set_password('parol123')
    jasur_user.save()
    p_jasur, _ = UserProfile.objects.get_or_create(user=jasur_user)
    p_jasur.role = 'student'
    p_jasur.headline = "Python & Algoritmlar ustasi"
    p_jasur.xp_points = 680
    p_jasur.save()

    madina_user, _ = User.objects.get_or_create(
        username='madina',
        defaults={'email': 'madina@skillup.uz', 'first_name': 'Madina', 'last_name': 'Usmonova'}
    )
    madina_user.set_password('parol123')
    madina_user.save()
    p_madina, _ = UserProfile.objects.get_or_create(user=madina_user)
    p_madina.role = 'student'
    p_madina.headline = "Web dasturlash o'rganuvchisi"
    p_madina.xp_points = 430
    p_madina.save()

    # 4. Categories
    cat_prog, _ = Category.objects.get_or_create(
        name="Dasturlash Asoslari",
        defaults={'icon': 'fas fa-code', 'description': 'Python, C++, Java va boshqa asosiy tillar'}
    )
    cat_web, _ = Category.objects.get_or_create(
        name="Web Dasturlash",
        defaults={'icon': 'fas fa-globe', 'description': 'Frontend, Backend, HTML, CSS, JavaScript va Frameworklar'}
    )
    cat_sec, _ = Category.objects.get_or_create(
        name="Kiberxavfsizlik",
        defaults={'icon': 'fas fa-shield-halved', 'description': 'Tarmoq xavfsizligi va axborot himoyasi'}
    )

    # 5. Course 1: Python Dasturlash Asoslari
    course1, _ = Course.objects.get_or_create(
        slug="python-dasturlash-asoslari",
        defaults={
            'title': "Python Dasturlash Asoslari va Interaktiv Algoritmlar",
            'instructor': ustoz_user,
            'category': cat_prog,
            'short_description': "Python dasturlash tilini noldan professional darajada o'rganing. Har bir modul oxirida 70% o'tish baliga ega testlar mavjud.",
            'description': """Ushbu kurs Python dasturlash tilining barcha asosiy tushunchalarini amaliyotga yo'naltirilgan tarzda o'rgatadi.

Kurs o'z ichiga quyidagilarni oladi:
- O'zgaruvchilar va ma'lumot turlari (int, float, str, bool)
- Shart operatorlari va mantiqiy amallar
- Ro'yxatlar, lug'atlar va kortejlar bilan ishlash
- Funksiyalar, parametrlar va modullilik
- Obyektga Yo'naltirilgan Dasturlash (OOP) tamoyillari

Har bir modul oxirida vaqtga bog'langan maxsus test mavjud bo'lib, keyingi modulga o'tish uchun kamida 70% natija ko'rsatish talab etiladi. Kurs yakunida rasmiy sertifikat taqdim etiladi.""",
            'thumbnail_url': 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&auto=format&fit=crop&q=80',
            'level': 'beginner',
            'duration_hours': 14,
            'is_published': True
        }
    )

    # Module 1
    mod1, _ = Module.objects.get_or_create(
        course=course1,
        order=1,
        defaults={'title': "1-Modul: Python Sintaksisi va Asosiy Operatorlar", 'pass_percentage': 70}
    )

    Lesson.objects.get_or_create(
        module=mod1,
        order=1,
        defaults={
            'title': "Python tiliga kirish va muhitni o'rnatish",
            'video_url': 'https://www.youtube.com/watch?v=_uQrJ0TkZlc',
            'duration_minutes': 12,
            'is_free_preview': True,
            'content': """# Python tiliga kirish

Python — bugungi kunda dunyodagi eng mashhur, o'rganish uchun qulay va kuchli dasturlash tillaridan biridir.

### Nima uchun Python?
1. **O'qilishi oson sintaksis:** Kod deyarli ingliz tilidagi matn kabi o'qiladi.
2. **Keng qo'llanish sohasi:** Web dasturlash (Django, FastAPI), Sun'iy Intellekt (AI/ML), Ma'lumotlar tahlili, Skriptlar va avtomatlashtirish.
3. **Katta hamjamiyat:** Minglab tayyor kutubxonalar va qo'llanmalar mavjud.

### Birinchi dastur:
```python
print("Salom, Dunyo!")
```
Yuqoridagi kod ekranga `Salom, Dunyo!` matnini chiqaradi."""
        }
    )

    Lesson.objects.get_or_create(
        module=mod1,
        order=2,
        defaults={
            'title': "O'zgaruvchilar va Ma'lumot Turlari",
            'video_url': 'https://www.youtube.com/watch?v=kqtD5dpn9C8',
            'duration_minutes': 18,
            'content': """# O'zgaruvchilar va Ma'lumot Turlari

Python tilida o'zgaruvchilar qiymat saqlash uchun idish vazifasini bajaradi. O'zgaruvchi yaratishda uning turini oldindan yozish shart emas — Python dinamik tiplashga ega!

```python
ism = "Ali"          # str (matn)
yosh = 20            # int (butun son)
narx = 19.99         # float (haqiqiy son)
talabami = True      # bool (rost yoki yolg'on)
```

### Arifmetik amallar:
- `+` : Qo'shish
- `-` : Ayirish
- `*` : Ko'paytirish
- `/` : Bo'lish (natija doim float bo'ladi)
- `//` : Butun qismini olib bo'lish (10 // 3 -> 3)
- `%` : Qoldiqni topish (10 % 3 -> 1)
- `**` : Darajaga ko'tarish (2 ** 3 -> 8)"""
        }
    )

    Lesson.objects.get_or_create(
        module=mod1,
        order=3,
        defaults={
            'title': "Shart Operatorlari (if, elif, else)",
            'video_url': 'https://www.youtube.com/watch?v=AWek49wXGzI',
            'duration_minutes': 15,
            'content': """# Shart Operatorlari

Dasturimiz ma'lum bir shart bajarilganda bir ishni, bajarilmaganda boshqa ishni qilishi uchun `if-elif-else` konstruksiyasidan foydalanamiz.

```python
ball = 85

if ball >= 90:
    print("A'lo daraja! 🏆")
elif ball >= 70:
    print("Imtihondan o'tdingiz! 🎉")
else:
    print("Qayta topshirish kerak ⚠️")
```

Esda tuting: Python tilida bloklar jingalak qavslar `{}` emas, aynan **surilish (indentation - 4 ta bo'shliq)** orqali belgilanadi!"""
        }
    )

    # Quiz 1
    quiz1, _ = Quiz.objects.get_or_create(
        module=mod1,
        defaults={
            'title': "1-Modul Imtihoni: Sintaksis va Asoslar",
            'time_limit_minutes': 8,
            'passing_score': 70,
            'description': "Ushbu test 1-moduldagi mavzularni o'zlashtirganingizni tekshiradi. Keyingi modulni ochish uchun kamida 70% to'plashingiz shart!"
        }
    )

    if not quiz1.questions.exists():
        q1 = Question.objects.create(
            quiz=quiz1, order=1, points=10,
            question_text="Python tilida ekranga matn chiqarish uchun qaysi standart funksiya ishlatiladi?",
            explanation="Python tilida standart konsolga ma'lumot chiqarish print() funksiyasi orqali amalga oshiriladi."
        )
        Option.objects.create(question=q1, option_text="print()", is_correct=True)
        Option.objects.create(question=q1, option_text="console.log()", is_correct=False)
        Option.objects.create(question=q1, option_text="echo()", is_correct=False)
        Option.objects.create(question=q1, option_text="write()", is_correct=False)

        q2 = Question.objects.create(
            quiz=quiz1, order=2, points=10,
            question_text="Quyidagilardan qaysi biri Python tilida butun qismini oluvchi bo'lish operatori hisoblanadi?",
            explanation="// operatori bo'lish amalidan keyin qoldiqni tashlab faqat butun qismini qaytaradi."
        )
        Option.objects.create(question=q2, option_text="//", is_correct=True)
        Option.objects.create(question=q2, option_text="/", is_correct=False)
        Option.objects.create(question=q2, option_text="%", is_correct=False)
        Option.objects.create(question=q2, option_text="div", is_correct=False)

        q3 = Question.objects.create(
            quiz=quiz1, order=3, points=10,
            question_text="Python kodida bloklar (masalan if yoki funksiya tanasi) qanday ajratiladi?",
            explanation="Python kod bloklarini ajratish uchun jingalak qavslar emas, balki qat'iy surilishlar (indentation) dan foydalanadi."
        )
        Option.objects.create(question=q3, option_text="Surilish (Indentation / 4 ta bo'shliq) orqali", is_correct=True)
        Option.objects.create(question=q3, option_text="{ } jingalak qavslar orqali", is_correct=False)
        Option.objects.create(question=q3, option_text="begin ... end kalit so'zlari orqali", is_correct=False)
        Option.objects.create(question=q3, option_text="Nuqtali vergul (;) orqali", is_correct=False)

        q4 = Question.objects.create(
            quiz=quiz1, order=4, points=10,
            question_text="bool('Salom') ifodasi qanday qiymat qaytaradi?",
            explanation="Bo'sh bo'lmagan satrlar (strings) mantiqiy kontekstda doimo True qiymatiga ega bo'ladi."
        )
        Option.objects.create(question=q4, option_text="True", is_correct=True)
        Option.objects.create(question=q4, option_text="False", is_correct=False)
        Option.objects.create(question=q4, option_text="None", is_correct=False)
        Option.objects.create(question=q4, option_text="Error", is_correct=False)

    # Module 2
    mod2, _ = Module.objects.get_or_create(
        course=course1,
        order=2,
        defaults={'title': "2-Modul: Ro'yxatlar, Lug'atlar va Funksiyalar", 'pass_percentage': 70}
    )

    Lesson.objects.get_or_create(
        module=mod2,
        order=1,
        defaults={
            'title': "Ro'yxatlar (Lists) va Ular Ustida Amallar",
            'video_url': 'https://www.youtube.com/watch?v=W8KRzm-HUcc',
            'duration_minutes': 20,
            'content': """# Ro'yxatlar (Lists)

Ro'yxat — bir nechta elementlarni bitta o'zgaruvchida tartiblangan holda saqlash imkonini beruvchi tuzilma.

```python
mevalar = ["olma", "anor", "shaftoli"]

# Element qo'shish
mevalar.append("banan")

# Elementni o'chirish
mevalar.remove("anor")

# Indeks bo'yicha murojaat
print(mevalar[0])  # olma
```"""
        }
    )

    Lesson.objects.get_or_create(
        module=mod2,
        order=2,
        defaults={
            'title': "Funksiyalar va def kalit so'zi",
            'video_url': 'https://www.youtube.com/watch?v=9Os0o3wzS_I',
            'duration_minutes': 25,
            'content': """# Funksiyalar

Funksiya — ma'lum bir vazifani bajarish uchun yozilgan, qayta-qayta chaqirilishi mumkin bo'lgan kod blokidir.

```python
def salom_ber(ism):
    return f"Assalomu alaykum, {ism}!"

xabar = salom_ber("Sardor")
print(xabar)
```"""
        }
    )

    # Quiz 2
    quiz2, _ = Quiz.objects.get_or_create(
        module=mod2,
        defaults={
            'title': "2-Modul Imtihoni: Kolleksiyalar va Funksiyalar",
            'time_limit_minutes': 10,
            'passing_score': 70,
            'description': "2-modul bo'yicha bilimlaringizni sinovdan o'tkazing."
        }
    )

    if not quiz2.questions.exists():
        q21 = Question.objects.create(
            quiz=quiz2, order=1, points=10,
            question_text="Ro'yxat oxiriga yangi element qo'shish uchun qaysi metod ishlatiladi?",
            explanation="append() metodi yangi elementni ro'yxatning oxiriga joylaydi."
        )
        Option.objects.create(question=q21, option_text="append()", is_correct=True)
        Option.objects.create(question=q21, option_text="push()", is_correct=False)
        Option.objects.create(question=q21, option_text="insert_end()", is_correct=False)
        Option.objects.create(question=q21, option_text="add()", is_correct=False)

        q22 = Question.objects.create(
            quiz=quiz2, order=2, points=10,
            question_text="Python tilida funksiya qaysi kalit so'z orqali e'lon qilinadi?",
            explanation="Funksiyalarni e'lon qilish def (define so'zidan) bilan boshlanadi."
        )
        Option.objects.create(question=q22, option_text="def", is_correct=True)
        Option.objects.create(question=q22, option_text="function", is_correct=False)
        Option.objects.create(question=q22, option_text="fn", is_correct=False)
        Option.objects.create(question=q22, option_text="func", is_correct=False)

    # Module 3
    mod3, _ = Module.objects.get_or_create(
        course=course1,
        order=3,
        defaults={'title': "3-Modul: Obyektga Yo'naltirilgan Dasturlash (OOP)", 'pass_percentage': 70}
    )

    Lesson.objects.get_or_create(
        module=mod3,
        order=1,
        defaults={
            'title': "Sinflar (Class) va Konstruktor (__init__)",
            'video_url': 'https://www.youtube.com/watch?v=JeznW_7DlB0',
            'duration_minutes': 22,
            'content': """# Obyektga Yo'naltirilgan Dasturlash (OOP)

OOP — dasturlashning real dunyo obyektlari modeli asosida dastur tuzish usulidir.

```python
class Avtomobil:
    def __init__(self, model, rang):
        self.model = model
        self.rang = rang

    def signal(self):
        return f"{self.model}: Bip-bip!"

gentra = Avtomobil("Gentra", "Qora")
print(gentra.signal())
```"""
        }
    )

    quiz3, _ = Quiz.objects.get_or_create(
        module=mod3,
        defaults={
            'title': "3-Modul: Yakuniy Bitiruv Imtihoni",
            'time_limit_minutes': 10,
            'passing_score': 70,
            'description': "Kurs yakuniy imtihoni. 70% dan yuqori topshirsangiz, sizga avtomatik tarzda rasmiy sertifikat taqdim etiladi!"
        }
    )

    if not quiz3.questions.exists():
        q31 = Question.objects.create(
            quiz=quiz3, order=1, points=15,
            question_text="Klass konstruktori (yangi obyekt hosil bo'lganda ishga tushuvchi metod) qanday nomlanadi?",
            explanation="__init__ — klass konstruktori hisoblanadi."
        )
        Option.objects.create(question=q31, option_text="__init__", is_correct=True)
        Option.objects.create(question=q31, option_text="__construct__", is_correct=False)
        Option.objects.create(question=q31, option_text="__new_obj__", is_correct=False)
        Option.objects.create(question=q31, option_text="__create__", is_correct=False)

    # 6. Course 2: Web Dasturlash
    course2, _ = Course.objects.get_or_create(
        slug="zamonaviy-web-dasturlash",
        defaults={
            'title': "Zamonaviy Web Dasturlash: Frontend va Backend Asoslari",
            'instructor': malika_user,
            'category': cat_web,
            'short_description': "HTML5, zamonaviy CSS, JavaScript va Django orqali to'liq ishlaydigan veb saytlar yaratishni o'rganing.",
            'description': "Ushbu kurs veb texnologiyalar olamiga qadam qo'yayotganlar uchun qulay qo'llanma bo'lib xizmat qiladi.",
            'thumbnail_url': 'https://images.unsplash.com/photo-1547658719-da2b51169166?w=800&auto=format&fit=crop&q=80',
            'level': 'intermediate',
            'duration_hours': 20,
            'is_published': True
        }
    )

    mod_w1, _ = Module.objects.get_or_create(
        course=course2,
        order=1,
        defaults={'title': "1-Modul: HTML5 va CSS3 Zamonaviy Stilistika", 'pass_percentage': 70}
    )

    Lesson.objects.get_or_create(
        module=mod_w1,
        order=1,
        defaults={
            'title': "HTML Strukturasi va Semantik Teglar",
            'video_url': 'https://www.youtube.com/watch?v=kUMe1FH4CHE',
            'duration_minutes': 15,
            'is_free_preview': True,
            'content': "# HTML5 Asoslari\n\nVeb sahifaning suyagi hisoblangan HTML teglar bilan tanishamiz."
        }
    )

    # 7. Setup initial enrollment & progress for `talaba` in Course 1
    # Enroll talaba
    Enrollment.objects.get_or_create(student=talaba_user, course=course1)

    # Complete Lesson 1 & 2 for talaba
    l1 = Lesson.objects.filter(module=mod1, order=1).first()
    l2 = Lesson.objects.filter(module=mod1, order=2).first()
    l3 = Lesson.objects.filter(module=mod1, order=3).first()

    if l1:
        LessonProgress.objects.get_or_create(student=talaba_user, lesson=l1, defaults={'is_completed': True, 'completed_at': timezone.now()})
    if l2:
        LessonProgress.objects.get_or_create(student=talaba_user, lesson=l2, defaults={'is_completed': True, 'completed_at': timezone.now()})
    if l3:
        LessonProgress.objects.get_or_create(student=talaba_user, lesson=l3, defaults={'is_completed': True, 'completed_at': timezone.now()})

    # Talaba passed Quiz 1 with 100%!
    att1, _ = QuizAttempt.objects.get_or_create(
        student=talaba_user,
        quiz=quiz1,
        defaults={
            'score': 40,
            'total_questions': 4,
            'correct_answers': 4,
            'percentage': 100.0,
            'passed': True
        }
    )

    # 8. Setup Jasur who completed Course 1 and received a Certificate
    Enrollment.objects.get_or_create(student=jasur_user, course=course1, defaults={'is_completed': True})
    for l in Lesson.objects.filter(module__course=course1):
        LessonProgress.objects.get_or_create(student=jasur_user, lesson=l, defaults={'is_completed': True})

    # Jasur passed all quizzes
    for qz in Quiz.objects.filter(module__course=course1):
        QuizAttempt.objects.get_or_create(
            student=jasur_user,
            quiz=qz,
            defaults={'score': 40, 'total_questions': 4, 'correct_answers': 4, 'percentage': 100.0, 'passed': True}
        )

    # Jasur Certificate
    cert, _ = Certificate.objects.get_or_create(
        student=jasur_user,
        course=course1,
        defaults={
            'certificate_id': '8942FE26B1',
            'final_grade': 98.5
        }
    )

    print("✓ Namunaviy ma'lumotlar, kurslar, modullar, darslar va testlar muvaffaqiyatli yaratildi!")
    print("=== TAYYOR ===")


if __name__ == '__main__':
    seed()
