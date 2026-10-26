import os
import sys
import django

# UTF-8 stdout sozlamasi Windows uchun
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import User, CoinShopItem, CoinTransaction


def seed_shop_and_users():
    print("=" * 60)
    print("🪙 EDUCOIN GAMIFIKATSIYA DO'KONI VA TRANZAKSIYALARINI YUKLASH")
    print("=" * 60)

    shop_items = [
        {
            'title': "Kurslar uchun -50% Chegirma Kuponi",
            'description': "Istalgan pulli kurs uchun to'lovda bir martalik 50% qo'shimcha chegirma taqdim etuvchi shaxsiy promokod. Sotib olgach promokod kodi profilingizda saqlanadi.",
            'price_coins': 120,
            'item_type': 'coupon_50',
            'icon': 'fa-solid fa-ticket-simple',
            'is_available': True,
        },
        {
            'title': "Oltin VIP Profil Nishoni & Toj",
            'description': "Platforma bo'ylab ismingiz va profilingizda yonib turuvchi Oltin VIP toj ramkasi. Talabalar va o'qituvchilar orasida alohida mavqega ega bo'ling!",
            'price_coins': 200,
            'item_type': 'vip_badge',
            'icon': 'fa-solid fa-crown',
            'is_available': True,
        },
        {
            'title': "Bosh Murabbiy bilan 1-ga-1 Mentorlik (45 daq)",
            'description': "Karyera rejalashtirish, kod tahlili (code review) yoki portfolioni tekshirish bo'yicha tajribali senior dasturchi bilan jonli video-muloqot.",
            'price_coins': 300,
            'item_type': 'mentor_call',
            'icon': 'fa-solid fa-headset',
            'is_available': True,
        },
        {
            'title': "SkillUp Brendli Premium Xudi & Stikerlar",
            'description': "O'zbekiston bo'ylab pochta orqali bepul yetkazib beriladigan yuqori sifatli paxtali SkillUp IT-xudisi va noutbuk stikerlari.",
            'price_coins': 450,
            'item_type': 'merch',
            'icon': 'fa-solid fa-shirt',
            'is_available': True,
        },
        {
            'title': "AI Prompt Muhandisligi & Cheat-Sheet To'plami",
            'description': "ChatGPT, Claude va Gemini uchun professional darajada yozilgan 500+ sinalgan dasturlash va tahlil promptlari kutubxonasi.",
            'price_coins': 100,
            'item_type': 'coupon_50',
            'icon': 'fa-solid fa-wand-magic-sparkles',
            'is_available': True,
        },
        {
            'title': "Oltin Muhrli Qattiq Muqovali Sertifikat (Pochta)",
            'description': "Tamomlagan kursingizning oltin bo'rtma muhrli, A4 formatdagi maxsus qattiq muqovali rasmiy sertifikati uyingizgacha yetkaziladi.",
            'price_coins': 250,
            'item_type': 'merch',
            'icon': 'fa-solid fa-stamp',
            'is_available': True,
        },
    ]

    for item_data in shop_items:
        obj, created = CoinShopItem.objects.update_or_create(
            title=item_data['title'],
            defaults=item_data
        )
        status = "Yangi qo'shildi" if created else "Yangilandi"
        print(f"[{status}] {obj.title} — {obj.price_coins} 🪙 ({obj.get_item_type_display()})")

    # Mavjud foydalanuvchilarga xush kelibsiz bonusi tranzaksiyasini yozish
    users = User.objects.all()
    bonus_count = 0
    for u in users:
        # Boshlang'ich tanga balansi
        if u.edu_coins < 100:
            u.edu_coins = 100
            u.save(update_fields=['edu_coins'])

        has_welcome = CoinTransaction.objects.filter(user=u, action_type='welcome_bonus').exists()
        if not has_welcome:
            CoinTransaction.objects.create(
                user=u,
                amount=100,
                action_type='welcome_bonus',
                description="Platformaga qo'shilganlik uchun boshlang'ich sovg'a (+100 🪙)"
            )
            bonus_count += 1

    print(f"\n✅ {bonus_count} ta foydalanuvchiga 'welcome_bonus' (+100 🪙) tranzaksiyasi rasmiylashtirildi.")
    print("=" * 60)


if __name__ == '__main__':
    seed_shop_and_users()
