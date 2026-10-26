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
from core.models import User, Course, Module, Lesson, Quiz, Question, Choice, Enrollment, BundleEnrollment


def run_comprehensive_tests():
    print("=" * 70)
    print("🧪 17 TA TO'GARAK, O'QITUVCHILAR OYLIGI VA PAKETLI CHEGIRMALAR TESTI")
    print("=" * 70)

    # 1. 17 ta to'garak mavjudligini tekshirish
    required_keywords = [
        "Savodxonlik", "Dasturlash Asoslari", "Backend Dasturlash", "Frontend Dasturlash",
        "Ingliz Tili", "CEFR", "IELTS", "Koreys Tili", "Rus Tili", "Xitoy Tili", "Turk Tili",
        "Ona Tili", "Adabiyot", "Matematika", "Shaxmat", "Futbol", "Ping-pong"
    ]
    for kw in required_keywords:
        c = Course.objects.filter(title__icontains=kw).first()
        assert c is not None, f"XATO: '{kw}' to'garagi topilmadi!"
        print(f"✅ To'garak mavjud: {c.title:<55} | {c.get_schedule_display_full()}")

    # 2. O'qituvchilar va ularning maoshlarini tekshirish (5 mln - 15 mln so'm)
    teachers = User.objects.filter(role='teacher')
    assert teachers.count() >= 10, f"O'qituvchilar soni kam: {teachers.count()}"
    print(f"\n✅ O'qituvchilar soni: {teachers.count()} nafar")

    for t in teachers:
        assert 5000000 <= t.monthly_salary <= 15000000, f"XATO: {t.username} maoshi 5-15 mln oralig'ida emas: {t.monthly_salary}"
        print(f"  + {t.get_full_name():<22} | Oyligi: {t.get_salary_display():<18} | Tajriba: {t.experience_years} yil | O'quvchilari: {t.students_count}")

    # 3. Zamonaviy kasblar qimmatroq ekanini tekshirish
    modern_courses = Course.objects.filter(is_modern_profession=True)
    assert modern_courses.exists(), "Zamonaviy kasblar topilmadi!"
    for mc in modern_courses:
        assert mc.get_effective_price() >= 550000, f"Zamonaviy kasb narxi past: {mc.title}"
        assert mc.author.monthly_salary >= 12000000, f"Zamonaviy kasb ustozi oyligi past: {mc.author.get_salary_display()}"
        print(f"✅ Zamonaviy qimmat kasb: {mc.title:<40} -> O'quvchi to'lovi: {mc.get_effective_price():,} so'm | Ustoz oyligi: {mc.author.get_salary_display()}")

    # 4. Kunlar jadvali (Toq, Juft, Hafta oxiri)
    toq_count = Course.objects.filter(schedule_type='toq').count()
    juft_count = Course.objects.filter(schedule_type='juft').count()
    hafta_oxiri_count = Course.objects.filter(schedule_type='hafta_oxiri').count()
    print(f"\nJadvallar taqsimoti: Toq kunlar={toq_count}, Juft kunlar={juft_count}, Hafta oxiri={hafta_oxiri_count}")
    assert toq_count > 0 and juft_count > 0 and hafta_oxiri_count > 0, "Barcha turdagi kunlar mavjud emas!"

    # 5. Paketli to'garaklar a'zoligi (2 tasiga 50k, 3 tasiga 100k chegirma)
    test_user, _ = User.objects.get_or_create(username='bundle_test_user', defaults={'role': 'student', 'edu_coins': 0})
    test_user.bundle_enrollments.all().delete()
    test_user.enrollments.all().delete()

    client = Client()
    client.force_login(test_user)

    # A) 2 ta to'garak tanlanganda: -50,000 so'm chegirma
    c1 = Course.objects.filter(schedule_type='toq').first()
    c2 = Course.objects.filter(schedule_type='juft').first()
    total_2 = c1.get_effective_price() + c2.get_effective_price()

    resp_bundle_2 = client.post('/bundle-enroll/pay/', {
        'selected_courses': [c1.id, c2.id],
        'payment_method': 'click',
    }, follow=True)
    assert resp_bundle_2.status_code == 200

    b2 = BundleEnrollment.objects.filter(user=test_user).first()
    assert b2 is not None, "2 ta kurs uchun BundleEnrollment yaratilmadi!"
    assert b2.bundle_discount == 50000, f"Chegirma 50 000 bo'lishi kerak edi, lekin: {b2.bundle_discount}"
    assert b2.final_amount == total_2 - 50000, f"Yakuniy to'lov xato: {b2.final_amount} != {total_2 - 50000}"
    assert test_user.enrollments.filter(course=c1).exists(), "1-kursga yozilmadi!"
    assert test_user.enrollments.filter(course=c2).exists(), "2-kursga yozilmadi!"
    print(f"\n✅ 2 TA KURS A'ZOLIGI: Asl narx={total_2:,} so'm, Chegirma={b2.bundle_discount:,} so'm, To'landi={b2.final_amount:,} so'm")

    # B) 3 ta to'garak tanlanganda: -100,000 so'm chegirma
    test_user_3, _ = User.objects.get_or_create(username='bundle_test_user_3', defaults={'role': 'student', 'edu_coins': 0})
    test_user_3.bundle_enrollments.all().delete()
    test_user_3.enrollments.all().delete()
    client.force_login(test_user_3)

    c3 = Course.objects.filter(schedule_type='hafta_oxiri').first()
    total_3 = c1.get_effective_price() + c2.get_effective_price() + c3.get_effective_price()

    resp_bundle_3 = client.post('/bundle-enroll/pay/', {
        'selected_courses': [c1.id, c2.id, c3.id],
        'payment_method': 'payme',
    }, follow=True)
    assert resp_bundle_3.status_code == 200

    b3 = BundleEnrollment.objects.filter(user=test_user_3).first()
    assert b3 is not None, "3 ta kurs uchun BundleEnrollment yaratilmadi!"
    assert b3.bundle_discount == 100000, f"Chegirma 100 000 bo'lishi kerak edi, lekin: {b3.bundle_discount}"
    assert b3.final_amount == total_3 - 100000, f"Yakuniy to'lov xato: {b3.final_amount} != {total_3 - 100000}"
    assert test_user_3.enrollments.filter(course=c1).exists()
    assert test_user_3.enrollments.filter(course=c2).exists()
    assert test_user_3.enrollments.filter(course=c3).exists()
    print(f"✅ 3 TA KURS A'ZOLIGI: Asl narx={total_3:,} so'm, Chegirma={b3.bundle_discount:,} so'm, To'landi={b3.final_amount:,} so'm")

    # 6. HTTP Sahifalar tekshiruvi
    # Fresh user for checkout page check
    fresh_user, _ = User.objects.get_or_create(username='fresh_checkout_user', defaults={'role': 'student'})
    client.force_login(fresh_user)

    test_urls = [
        ('/courses/', "Barcha kurslar"),
        ('/courses/?category=Savodxonlik', "Savodxonlik filtri"),
        ('/courses/?category=IT & Dasturlash', "Dasturlash filtri"),
        ('/courses/?schedule=toq', "Toq kunlar filtri"),
        ('/courses/?schedule=hafta_oxiri', "Hafta oxiri filtri"),
        ('/teachers/', "O'qituvchilar va oyliklar"),
        ('/bundle-enroll/', "Paketli chegirmalar"),
        (f'/course/{c1.id}/checkout/', "Yakka to'garakka qatnashish"),
    ]
    for url, desc in test_urls:
        resp = client.get(url)
        assert resp.status_code == 200, f"XATO: {url} -> {resp.status_code}"
        print(f"✅ HTTP 200 OK: {desc:<30} ({url})")

    print("\n🎉 BARCHA YANGI TALABLAR 100% TESTDAN MUVAFFAQIYATLI O'TDI!")
    print("=" * 70)


if __name__ == '__main__':
    run_comprehensive_tests()
