import os
import sys
import django

# Windows konsolida UTF-8 muammosini oldini olish
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# Django muhitini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from core.models import (
    Course, Module, Lesson,
    Quiz, Question, Choice,
    UserLessonProgress, QuizResult, Certificate
)

User = get_user_model()


def seed_database():
    print("🚀 Baza ma'lumotlarini yaratish boshlandi...")

    # 1. Foydalanuvchilarni yaratish
    # Admin
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={
            'first_name': 'Administrator',
            'last_name': 'Boshqaruvchi',
            'email': 'admin@skillup.uz',
            'is_staff': True,
            'is_superuser': True,
            'role': 'teacher',
            'total_xp': 500
        }
    )
    admin_user.set_password('admin123')
    admin_user.save()

    # O'qituvchi
    teacher_user, _ = User.objects.get_or_create(
        username='ustoz',
        defaults={
            'first_name': 'Anvar',
            'last_name': 'Qodirov',
            'email': 'anvar@skillup.uz',
            'is_staff': False,
            'role': 'teacher',
            'total_xp': 350
        }
    )
    teacher_user.set_password('parol123')
    teacher_user.save()

    # Talaba 1 (O'rganuvchi)
    student1, _ = User.objects.get_or_create(
        username='talaba',
        defaults={
            'first_name': 'Sanjar',
            'last_name': 'Aliyev',
            'email': 'sanjar@student.uz',
            'role': 'student',
            'total_xp': 95
        }
    )
    student1.set_password('parol123')
    student1.save()

    # Talaba 2 (A'lochi bitiruvchi)
    student2, _ = User.objects.get_or_create(
        username='jasur',
        defaults={
            'first_name': 'Jasur',
            'last_name': 'Mahmudov',
            'email': 'jasur@student.uz',
            'role': 'student',
            'total_xp': 420
        }
    )
    student2.set_password('parol123')
    student2.save()

    # Talaba 3
    student3, _ = User.objects.get_or_create(
        username='malika_dev',
        defaults={
            'first_name': 'Malika',
            'last_name': 'Rustamova',
            'email': 'malika@student.uz',
            'role': 'student',
            'total_xp': 280
        }
    )
    student3.set_password('parol123')
    student3.save()

    print("✅ Foydalanuvchilar (admin, ustoz, talaba, jasur, malika_dev) yaratildi.")

    # 2. Asosiy Kursni yaratish: Python Dasturlash Asoslari
    course1, _ = Course.objects.get_or_create(
        title="Python Dasturlash Asoslari va Algoritmlar",
        defaults={
            'description': "Noldan boshlab professional darajagacha Python dasturlash tili, sintaksis, funksiyalar, ma'lumotlar tuzilmasi va OOP asoslarini o'rganing. Har bir modul so'ngida interaktiv testlar mavjud.",
            'author': teacher_user
        }
    )

    # ---------------- 1-MODUL ----------------
    mod1, _ = Module.objects.get_or_create(
        course=course1,
        order=1,
        defaults={'title': "Python Kirish va Sintaksis"}
    )

    les1_1, _ = Lesson.objects.get_or_create(
        module=mod1,
        order=1,
        defaults={
            'title': "Python o'rnatish va birinchi 'Hello World' dasturi",
            'video_url': "https://www.youtube.com/watch?v=kqtD5dpn9C8",
            'content': """# 🐍 Python Dasturlash Tiliga Kirish

Python — dunyodagi eng ommabop, o'qilishi oson va kuchli dasturlash tillaridan biri.

### Dasturni ishga tushirish:
Birinchi dasturimizni yozamiz:
```python
print("Salom, Dunyo! SkillUp platformasiga xush kelibsiz!")
```

### Asosiy qoidalar:
1. Python sintaksisi qat'iy chekinishlarga (indentation / 4 ta probel) asoslanadi.
2. Har bir satr alohida ko'rsatma hisoblanadi.
3. Katta va kichik harflar bir-biridan farqlanadi (`name` va `Name` boshqa-boshqa).

Darsni diqqat bilan o'rganib bo'lgach, "Darsni tugatdim (+15 XP)" tugmasini bosing!"""
        }
    )

    les1_2, _ = Lesson.objects.get_or_create(
        module=mod1,
        order=2,
        defaults={
            'title': "O'zgaruvchilar va Asosiy Ma'lumot Turlari",
            'video_url': "https://www.youtube.com/watch?v=kqtD5dpn9C8",
            'content': """# 📦 O'zgaruvchilar va Ma'lumot Turlari

Python-da o'zgaruvchilarni e'lon qilishda maxsus kalit so'z shart emas, qiymat berilsa yetarli.

### Asosiy turlar:
- `int` — butun sonlar (masalan: `x = 25`)
- `float` — o'nlik kasr sonlar (masalan: `pi = 3.1415`)
- `str` — matnlar (masalan: `ism = "Ali"`)
- `bool` — mantiqiy qiymatlar (`True` yoki `False`)

```python
yosh = 20
narx = 49.99
talabami = True
til = "Python"

print(f"{til} o'rganayotgan talaba: {yosh} yoshda.")
```"""
        }
    )

    # 1-Modul Testi
    quiz1, _ = Quiz.objects.get_or_create(
        module=mod1,
        defaults={
            'title': "1-Modul Bo'yicha Imtihon Testi",
            'passing_score': 70,
            'duration_minutes': 5
        }
    )

    # 1-Modul Savollari
    q1_1, _ = Question.objects.get_or_create(
        quiz=quiz1,
        text="Python-da ekranga ma'lumot chiqarish uchun qaysi funksiya ishlatiladi?"
    )
    Choice.objects.get_or_create(question=q1_1, text="print()", defaults={'is_correct': True})
    Choice.objects.get_or_create(question=q1_1, text="echo()", defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q1_1, text="console.log()", defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q1_1, text="write()", defaults={'is_correct': False})

    q1_2, _ = Question.objects.get_or_create(
        quiz=quiz1,
        text="Quyidagilardan qaysi biri to'g'ri o'nlik kasr (float) turi hisoblanadi?"
    )
    Choice.objects.get_or_create(question=q1_2, text="3.14", defaults={'is_correct': True})
    Choice.objects.get_or_create(question=q1_2, text="'3.14'", defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q1_2, text="3", defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q1_2, text="True", defaults={'is_correct': False})

    q1_3, _ = Question.objects.get_or_create(
        quiz=quiz1,
        text="Python bloklarni ajratishda nimalardan foydalanadi?"
    )
    Choice.objects.get_or_create(question=q1_3, text="Chekinishlar (Indentation / Probellar)", defaults={'is_correct': True})
    Choice.objects.get_or_create(question=q1_3, text="Figurali qavslar { }", defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q1_3, text="Nuqta-vergul ;", defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q1_3, text="BEGIN va END kalit so'zlari", defaults={'is_correct': False})

    # ---------------- 2-MODUL ----------------
    mod2, _ = Module.objects.get_or_create(
        course=course1,
        order=2,
        defaults={'title': "Shartlar, Sikllar va Mantiq"}
    )

    les2_1, _ = Lesson.objects.get_or_create(
        module=mod2,
        order=1,
        defaults={
            'title': "If-Else Shart Operatorlari va Mantiqiy Amallar",
            'video_url': "https://www.youtube.com/watch?v=kqtD5dpn9C8",
            'content': """# 🔀 Shart Operatorlari

Dasturimiz ma'lum bir shartlar asosida qaror qabul qilishi uchun `if`, `elif` va `else` ishlatiladi.

```python
ball = 85

if ball >= 90:
    print("Baho: A'lo")
elif ball >= 70:
    print("Baho: Yaxshi (Imtihondan o'tdingiz)")
else:
    print("Baho: Qoniqarsiz")
```"""
        }
    )

    les2_2, _ = Lesson.objects.get_or_create(
        module=mod2,
        order=2,
        defaults={
            'title': "For va While Sikl Operatorlari",
            'video_url': "https://www.youtube.com/watch?v=kqtD5dpn9C8",
            'content': """# 🔄 Takrorlanish Operatorlari (Sikllar)

Bir nechta amalni bir necha bor qaytarishda `for` va `while` operatorlaridan foydalanamiz.

```python
# 1 dan 5 gacha bo'lgan sonlarni chiqarish
for i in range(1, 6):
    print(f"Qadam: {i}")

# Ro'yxat elementlarini aylanib chiqish
dasturchilar = ["Ali", "Vali", "Hasan", "Zuhra"]
for ism in dasturchilar:
    print(f"Salom, dasturchi {ism}!")
```"""
        }
    )

    # 2-Modul Testi
    quiz2, _ = Quiz.objects.get_or_create(
        module=mod2,
        defaults={
            'title': "2-Modul Bo'yicha Imtihon Testi",
            'passing_score': 70,
            'duration_minutes': 5
        }
    )

    q2_1, _ = Question.objects.get_or_create(
        quiz=quiz2,
        text="`range(1, 4)` funksiyasi qanday sonlar ketma-ketligini beradi?"
    )
    Choice.objects.get_or_create(question=q2_1, text="1, 2, 3", defaults={'is_correct': True})
    Choice.objects.get_or_create(question=q2_1, text="1, 2, 3, 4", defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q2_1, text="0, 1, 2, 3", defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q2_1, text="0, 1, 2, 3, 4", defaults={'is_correct': False})

    q2_2, _ = Question.objects.get_or_create(
        quiz=quiz2,
        text="Siklni muddatidan oldin butunlay to'xtatish uchun qaysi kalit so'z ishlatiladi?"
    )
    Choice.objects.get_or_create(question=q2_2, text="break", defaults={'is_correct': True})
    Choice.objects.get_or_create(question=q2_2, text="continue", defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q2_2, text="pass", defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q2_2, text="stop", defaults={'is_correct': False})

    # ---------------- 3-MODUL (YAKUNIY) ----------------
    mod3, _ = Module.objects.get_or_create(
        course=course1,
        order=3,
        defaults={'title': "Funksiyalar va OOP Asoslari"}
    )

    les3_1, _ = Lesson.objects.get_or_create(
        module=mod3,
        order=1,
        defaults={
            'title': "Funksiyalar yaratish va parametrlar uzatish",
            'video_url': "https://www.youtube.com/watch?v=kqtD5dpn9C8",
            'content': """# 🛠️ Funksiyalar (Functions)

Funksiya — ma'lum vazifani bajarishga mo'ljallangan kod bloki. `def` orqali e'lon qilinadi.

```python
def hisobla_xp(dars_soni, test_soni):
    return (dars_soni * 15) + (test_soni * 50)

talaba_xp = hisobla_xp(4, 2)
print("Jami XP:", talaba_xp)
```"""
        }
    )

    les3_2, _ = Lesson.objects.get_or_create(
        module=mod3,
        order=2,
        defaults={
            'title': "Klasslar va Obyektlar (OOP)",
            'video_url': "https://www.youtube.com/watch?v=kqtD5dpn9C8",
            'content': """# 🏛️ Obyektga Yo'naltirilgan Dasturlash (OOP)

OOP — dasturlarni obyektlar va klasslar atrofida qurish metodologiyasi.

```python
class Talaba:
    def __init__(self, ism, xp=0):
        self.ism = ism
        self.xp = xp
        
    def xp_qosh(self, miqdor):
        self.xp += miqdor
        print(f"{self.ism} yangi ball oldi: {self.xp} XP")

jasur = Talaba("Jasur", 100)
jasur.xp_qosh(50)
```"""
        }
    )

    # 3-Modul Testi
    quiz3, _ = Quiz.objects.get_or_create(
        module=mod3,
        defaults={
            'title': "Yakuniy Kurs Bitiruv Imtihoni (OOP & Funksiyalar)",
            'passing_score': 70,
            'duration_minutes': 10
        }
    )

    q3_1, _ = Question.objects.get_or_create(
        quiz=quiz3,
        text="Python-da funksiya e'lon qilish uchun qaysi kalit so'z ishlatiladi?"
    )
    Choice.objects.get_or_create(question=q3_1, text="def", defaults={'is_correct': True})
    Choice.objects.get_or_create(question=q3_1, text="function", defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q3_1, text="fun", defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q3_1, text="define", defaults={'is_correct': False})

    q3_2, _ = Question.objects.get_or_create(
        quiz=quiz3,
        text="Klass ichidagi konstruktor metod nomi nima?"
    )
    Choice.objects.get_or_create(question=q3_2, text="__init__", defaults={'is_correct': True})
    Choice.objects.get_or_create(question=q3_2, text="__create__", defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q3_2, text="__start__", defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q3_2, text="constructor", defaults={'is_correct': False})

    print("✅ Kurs, modullar, darslar va test savollari muvaffaqiyatli saqlandi.")

    # 3. Sinov talabalari progressini belgilash
    # Talaba 'talaba': 1-modul darslarini tugatgan va 1-testdan 100% o'tgan
    UserLessonProgress.objects.get_or_create(user=student1, lesson=les1_1, defaults={'is_completed': True, 'completed_at': timezone.now()})
    UserLessonProgress.objects.get_or_create(user=student1, lesson=les1_2, defaults={'is_completed': True, 'completed_at': timezone.now()})
    QuizResult.objects.get_or_create(user=student1, quiz=quiz1, defaults={'score': 100.0, 'is_passed': True})

    # Talaba 'jasur' (A'lochi): Barcha modullarni tugatgan, barcha testlardan o'tgan va Sertifikat olgan!
    for les in [les1_1, les1_2, les2_1, les2_2, les3_1, les3_2]:
        UserLessonProgress.objects.get_or_create(user=student2, lesson=les, defaults={'is_completed': True, 'completed_at': timezone.now()})

    for qz in [quiz1, quiz2, quiz3]:
        QuizResult.objects.get_or_create(user=student2, quiz=qz, defaults={'score': 95.0, 'is_passed': True})

    Certificate.objects.get_or_create(
        user=student2,
        course=course1,
        defaults={'certificate_code': Certificate.generate_code(course1.id, student2.id)}
    )

    print("🎓 'jasur' talabasi uchun sertifikat va natijalar yaratildi.")
    print("✨ Baza muvaffaqiyatli to'ldirildi!")


if __name__ == '__main__':
    seed_database()
