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
from django.utils import timezone
from core.models import User, Course, Module, Lesson, Quiz, Question, Choice, Enrollment, Certificate, Coupon, CoinShopItem, CoinTransaction
from core.views import award_edu_coins, COIN_REWARDS


def run_tests():
    print("=" * 60)
    print("🧪 EDUCOIN 8 XIL RAG'BAT VA DO'KON TIZIMINI TESTLASH")
    print("=" * 60)

    # 1. 8 xil reward konfiguratsiyasini tekshirish
    expected_actions = [
        'welcome_bonus', 'lesson_completed', 'quiz_passed', 'quiz_perfect',
        'course_completed', 'course_enrolled', 'profile_completed', 'daily_streak'
    ]
    for act in expected_actions:
        assert act in COIN_REWARDS, f"Xato: {act} COIN_REWARDS da topilmadi!"
        amount, desc = COIN_REWARDS[act]
        print(f"✅ Harakat: {act:<18} -> +{amount:<3} 🪙 | {desc}")

    # 2. Test foydalanuvchisini olish yoki yaratish
    test_user, _ = User.objects.get_or_create(username='test_student_educoin', defaults={'role': 'student', 'total_xp': 0, 'edu_coins': 0})
    test_user.edu_coins = 0
    test_user.has_vip_badge = False
    test_user.save()
    test_user.coin_transactions.all().delete()

    print(f"\nBoshlang'ich test foydalanuvchi: {test_user.username}, Balans: {test_user.edu_coins} 🪙")

    # 3. 8 xil amaliy rag'batni berish va tekshirish
    gained_coins = {}
    for act in expected_actions:
        coins = award_edu_coins(test_user, act)
        gained_coins[act] = coins
        test_user.refresh_from_db()
        print(f"  + Berildi: {act} -> +{coins} 🪙 (Yangi balans: {test_user.edu_coins} 🪙)")

    expected_total = sum(amount for amount, _ in COIN_REWARDS.values())
    assert test_user.edu_coins == expected_total, f"Balans xato! Kutilgan: {expected_total}, Hozirgi: {test_user.edu_coins}"
    print(f"✅ Barcha 8 xil harakat uchun jami to'g'ri qo'shildi: {test_user.edu_coins} 🪙")

    # 4. Tranzaksiyalar yozuvini tekshirish
    tx_count = CoinTransaction.objects.filter(user=test_user).count()
    assert tx_count == 8, f"Tranzaksiyalar soni xato: {tx_count}"
    print(f"✅ Barcha 8 ta tranzaksiya ma'lumotlar bazasida saqlandi.")

    # 5. Do'kon mahsulotlari xaridini tekshirish
    client = Client()
    client.force_login(test_user)

    # VIP nishon sotib olish
    vip_item = CoinShopItem.objects.filter(item_type='vip_badge').first()
    assert vip_item is not None, "VIP mahsulot do'konda topilmadi!"
    
    current_coins = test_user.edu_coins
    resp_vip = client.post(f'/coin-shop/buy/{vip_item.id}/', follow=True)
    assert resp_vip.status_code == 200
    test_user.refresh_from_db()
    assert test_user.has_vip_badge == True, "VIP nishoni foydalanuvchiga berilmadi!"
    assert test_user.edu_coins == current_coins - vip_item.price_coins, "Tangalar to'g'ri yechilmadi!"
    print(f"✅ VIP xaridi muvaffaqiyatli: has_vip_badge={test_user.has_vip_badge}, Qoldiq: {test_user.edu_coins} 🪙")

    # -50% kupon sotib olish
    coupon_item = CoinShopItem.objects.filter(item_type='coupon_50').first()
    current_coins = test_user.edu_coins
    resp_cp = client.post(f'/coin-shop/buy/{coupon_item.id}/', follow=True)
    assert resp_cp.status_code == 200
    test_user.refresh_from_db()
    generated_coupon = Coupon.objects.filter(code__startswith=f"COIN50-{test_user.id}-").first()
    assert generated_coupon is not None, "Kupon kodi generatsiya qilinmadi!"
    print(f"✅ -50% Kupon xaridi muvaffaqiyatli: Kod={generated_coupon.code}, Qoldiq: {test_user.edu_coins} 🪙")

    # 6. HTTP sahifalar yuklanishini tekshirish
    pages = [
        ('/coin-shop/', "EduCoin Do'koni"),
        ('/profile/', "Shaxsiy Profil"),
        ('/courses/', "Kurslar Katalogi"),
        ('/teachers/', "O'qituvchilar"),
        ('/leaderboard/', "Reyting"),
        ('/parent-report/', "Ota-onalar hisoboti"),
    ]
    for url, label in pages:
        res = client.get(url)
        assert res.status_code == 200, f"Xato: {url} status {res.status_code} qaytardi!"
        print(f"✅ HTTP 200 OK: {label} ({url})")

    print("\n🎉 BARCHA TEKSHIRUVLAR 100% MUVAFFAQIYATLI O'TDI!")
    print("=" * 60)


if __name__ == '__main__':
    run_tests()
