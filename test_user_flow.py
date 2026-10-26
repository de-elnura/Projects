import os
import sys
import django

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from core.models import User, Course, Module, Lesson, Quiz, Question, Choice, Enrollment, Certificate, Coupon, CoinShopItem, CoinTransaction


def test_user_flow():
    print("=" * 60)
    print("🚀 TALABANING TO'LIQ FOYDALANUVCHI ZANJIRINI TEKSHIRISH")
    print("=" * 60)

    client = Client()

    # 1. Yangi talaba ro'yxatdan o'tishi (+100 EduCoin)
    username = "sarvar_pro_student"
    User.objects.filter(username=username).delete()

    reg_data = {
        'username': username,
        'email': 'sarvar@example.com',
        'first_name': 'Sarvar',
        'last_name': 'Rahmatullayev',
        'role': 'student',
        'password1': 'Password123!',
        'password2': 'Password123!',
    }
    resp = client.post('/register/', reg_data, follow=True)
    assert resp.status_code == 200, f"Register xato: {resp.status_code}"
    student = User.objects.get(username=username)
    assert student.edu_coins == 100, f"Welcome bonus xato: {student.edu_coins}"
    print(f"✅ 1. Ro'yxatdan o'tish: Sarvar ro'yxatdan o'tdi, EduCoin={student.edu_coins} 🪙")

    # 2. Darsni yakunlash (+10 EduCoin, +15 XP)
    lesson = Lesson.objects.first()
    assert lesson is not None, "Darslar mavjud emas!"
    resp_l = client.post(f'/lesson/{lesson.id}/complete/', follow=True)
    assert resp_l.status_code == 200
    student.refresh_from_db()
    assert student.edu_coins == 110, f"Dars yakunlash xato: {student.edu_coins}"
    assert student.total_xp == 15, f"XP xato: {student.total_xp}"
    print(f"✅ 2. Dars yakunlandi: EduCoin={student.edu_coins} 🪙, XP={student.total_xp}")

    # 3. Test topshirish 100% (+50 EduCoin, +70 XP)
    quiz = Quiz.objects.filter(module__course=lesson.module.course).first()
    if quiz:
        post_data = {}
        for q in quiz.questions.all():
            correct_ch = q.choices.filter(is_correct=True).first()
            if correct_ch:
                post_data[f'question_{q.id}'] = correct_ch.id
        resp_q = client.post(f'/quiz/{quiz.id}/', post_data, follow=True)
        assert resp_q.status_code == 200
        student.refresh_from_db()
        assert student.edu_coins >= 160, f"Quiz bonus xato: {student.edu_coins}"
        print(f"✅ 3. Test 100% topshirildi: EduCoin={student.edu_coins} 🪙, XP={student.total_xp}")

    # 4. Kunlik bonus olish (+15 EduCoin)
    resp_streak = client.get('/claim-daily-bonus/', follow=True)
    assert resp_streak.status_code == 200
    student.refresh_from_db()
    print(f"✅ 4. Kunlik faollik bonusi: EduCoin={student.edu_coins} 🪙")

    # 5. Profilni to'ldirish (+30 EduCoin)
    profile_data = {
        'first_name': 'Sarvar',
        'last_name': 'Rahmatullayev',
        'headline': 'Senior Python & AI Engineer',
        'bio': 'Sun\'iy intellekt va backend texnologiyalari bo\'yicha ixtisoslashgan dasturchi.',
        'avatar_url': 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=400',
    }
    resp_prof = client.post('/profile/update/', profile_data, follow=True)
    assert resp_prof.status_code == 200
    student.refresh_from_db()
    assert student.headline == profile_data['headline']
    print(f"✅ 5. Profil to'ldirildi: EduCoin={student.edu_coins} 🪙")

    print("\n🎉 TALABANING TO'LIQ END-TO-END FOYDALANUVCHI ZANJIRI A'LO DARAJADA ISHLADI!")
    print("=" * 60)


if __name__ == '__main__':
    test_user_flow()
