import os
import sys
import random
import django

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from datetime import date, timedelta
from django.utils import timezone
from core.models import (
    User, Course, Quiz, QuizResult, CoinTransaction,
    StudyGroup, Attendance
)

def run_seed():
    print("=" * 70)
    print("🎓 1. HAR BIR KURS UCHUN UNIKAL VA MAVZUGA MOS RASMLARNI O'RNATISH")
    print("=" * 70)

    # 1. Kurslar rasmlarini unikal va mavzuga mos qilib yangilash
    course_thumbnails = {
        "kiberxavfsizlik": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=600",
        "ethical": "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=600",
        "baza": "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?w=600",
        "sql": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600",
        "savodxonlik": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=600",
        "algoritm": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=600",
        "backend": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=600",
        "frontend": "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=600",
        "general english": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=600",
        "ingliz": "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?w=600",
        "cefr": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=600",
        "ielts": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=600",
        "koreys": "https://images.unsplash.com/photo-1517154421773-0529f29ea451?w=600",
        "rus": "https://images.unsplash.com/photo-1513326738677-b964603b136d?w=600",
        "xitoy": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=600",
        "turk": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=600",
        "ona tili": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=600",
        "adabiyot": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=600",
        "matematika": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=600",
        "shaxmat": "https://images.unsplash.com/photo-1529699211952-734e80c4d42b?w=600",
        "futbol": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=600",
        "ping": "https://images.unsplash.com/photo-1534158914592-062992fbe900?w=600",
        "flutter": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=600",
        "devops": "https://images.unsplash.com/photo-1607799279861-4dd421887fb3?w=600",
    }

    # Barcha kurslarni ko'rib chiqish va har biriga o'ziga xos rasm qo'yish
    all_courses = Course.objects.all()
    used_images = set()

    for c in all_courses:
        title_lower = c.title.lower()
        cat_lower = c.category.lower()
        assigned_img = None

        for keyword, img_url in course_thumbnails.items():
            if keyword in title_lower or keyword in cat_lower:
                if img_url not in used_images:
                    assigned_img = img_url
                    used_images.add(img_url)
                    break
        
        if not assigned_img:
            # Agar mos kalit topilmasa yoki band bo'lsa, unikal tasodifiy tema rasmi
            fallback_pool = [
                "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=600",
                "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=600",
                "https://images.unsplash.com/photo-1581092921461-eab62e97a780?w=600",
                "https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=600",
                "https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=600",
                "https://images.unsplash.com/photo-1509062522246-3755977927d7?w=600",
            ]
            for fb in fallback_pool:
                if fb not in used_images:
                    assigned_img = fb
                    used_images.add(fb)
                    break
            if not assigned_img:
                assigned_img = f"https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=600&id={c.id}"

        c.thumbnail_url = assigned_img
        c.save()
        print(f"   [Rasm Yangilandi] Kurs #{c.id}: {c.title[:45]} -> {assigned_img[:50]}...")

    print(f"\n[OK] Jami {all_courses.count()} ta kurslarning barchasiga unikal rasmlar biriktirildi!\n")

    print("=" * 70)
    print("👥 2. 150 NAFAR REAL TALABALAR VA 8 XIL AMALIY FAOLIYATLARNI YUKLASH")
    print("=" * 70)

    # 2. 150 nafar o'zbek talabalarni generatsiya qilish
    first_names_male = [
        'Jasurbek', 'Bobur', 'Shohruh', 'Azizbek', 'Sardor', 'Javohir', 'Bekzod', 'Otabek',
        'Rustam', 'Sherzod', 'Ulugbek', 'Sanjar', 'Davron', 'Nodirbek', 'Mirzo', 'Akmal',
        'Asadbek', 'Shohjahon', 'Anvar', 'Mansur', 'Jahongir', 'Diyorbek', 'Farrux', 'Ilhom',
        'Samandar', 'Zafar', 'Temur', 'Shahzod', 'Humoyun', 'Abbos', 'Bunyod', 'Shavkat'
    ]
    first_names_female = [
        'Madinabonu', 'Sevinch', 'Gulhayo', 'Nilufar', 'Dildora', 'Mohinur', 'Zilola', 'Shaxnoza',
        'Zarnigor', 'Kamola', 'Farangiz', 'Gulzoda', 'Umida', 'Rayhon', 'Dilnoza', 'Nozima',
        'Gulnoza', 'Iroda', 'Maftuna', 'Sabina', 'Zuhra', 'Fotima', 'Shodiya', 'Shahrizoda',
        'Feruza', 'Munisa', 'Gulasal', 'Robiyaxon', 'Malika', 'Nargiza', 'Laylo', 'Zarina'
    ]
    last_names = [
        'Rahimov', 'Karimov', 'Mirzayev', 'Olimov', 'Qodirov', 'Tursunov', 'Aliyev', 'Usmonov',
        'Sattorov', 'Mahmudov', 'Xolmatov', 'Yoqubov', 'Rustamov', 'Ismoilov', 'Yusupov',
        'Sobirov', 'G\'ofurov', 'Tojiyev', 'Murodov', 'Saidov', 'Ergashev', 'Normatov',
        'Sharipov', 'Hamroyev', 'Jo\'rayev', 'Xasanov', 'Ibrohimov', 'Omonov', 'Bozorov', 'Ahmedov'
    ]

    student_avatars = [
        "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300",
        "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300",
        "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=300",
        "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=300",
        "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=300",
        "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=300",
        "https://images.unsplash.com/photo-1501196354995-cbb51c65aaea?w=300",
        "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=300",
        "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=300",
        "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300",
        "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=300",
        "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300",
        "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300",
        "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=300",
        "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=300",
    ]

    action_blueprints = [
        ('attendance_streak', 15, 20, "Darsga o'z vaqtida kelish (Davomat) (+15 🪙)"),
        ('homework_perfect', 25, 35, "Uy vazifasini 100% a'lo bajarish (+25 🪙)"),
        ('class_activity', 20, 30, "Darsda faollik (Savol-javob & amaliyot) (+20 🪙)"),
        ('quiz_passed', 30, 50, "Modul testidan o'tish (70%+) (+30 🪙)"),
        ('quiz_perfect', 50, 100, "Imtihondan 100% a'lo natija (+50 🪙)"),
        ('book_reading', 35, 45, "Badiiy kitob mutolaasi va taqdimoti (+35 🪙)"),
        ('weekly_streak', 40, 60, "Haftalik intizom va faollik bonusi (+40 🪙)"),
        ('course_completed', 150, 200, "Kursni tamomlab Sertifikat olish (+150 🪙)"),
    ]

    all_quizzes = list(Quiz.objects.all())
    active_groups = list(StudyGroup.objects.filter(is_active=True))

    TARGET_COUNT = 150
    existing_students = list(User.objects.filter(role='student'))
    created_count = 0

    print(f"Mavjud talabalar soni: {len(existing_students)} ta.")
    print(f"Jami talabalar soni {TARGET_COUNT} taga yetkaziladi...")

    for i in range(1, TARGET_COUNT + 1):
        username = f"student_{i}"
        user = User.objects.filter(username=username).first()

        is_female = (i % 2 == 0)
        fname = random.choice(first_names_female if is_female else first_names_male)
        lname_base = random.choice(last_names)
        lname = f"{lname_base}a" if is_female else lname_base
        
        # Rank taqsimoti: birinchi o'rinlar 8000-9500 XP, o'rtalar 3000-6000 XP, yangilar 500-2000 XP
        if i <= 3:
            total_xp = 9500 - (i * 250) + random.randint(10, 80)
            edu_coins = 1350 - (i * 90) + random.randint(5, 30)
            has_vip = True
        elif i <= 20:
            total_xp = 7500 - (i * 120) + random.randint(5, 50)
            edu_coins = 900 - (i * 20) + random.randint(5, 20)
            has_vip = (i <= 10)
        elif i <= 60:
            total_xp = 4800 - (i * 45) + random.randint(5, 30)
            edu_coins = 550 - (i * 5) + random.randint(2, 15)
            has_vip = False
        else:
            total_xp = max(450, 2800 - (i * 16) + random.randint(2, 20))
            edu_coins = max(40, 320 - (i * 2) + random.randint(2, 10))
            has_vip = False

        avatar_url = student_avatars[(i - 1) % len(student_avatars)]
        headlines = [
            "Bo'lajak Full-Stack Dasturchi", "IELTS 8.0 ga intiluvchi talaba",
            "Matematika olimpiadasi qatnashchisi", "Kiberxavfsizlik ixlosmandi",
            "Milliy sertifikat A+ sohibi", "Python va Django o'rganuvchisi",
            "Shaxmat bo'yicha 1-toifali sportchi", "Koreys tili TOPIK Level 3 egasi",
            "A'lochi va faol talaba"
        ]
        headline = headlines[i % len(headlines)]

        if not user:
            user = User.objects.create_user(
                username=username,
                email=f"{username}@student.skillup.uz",
                password="parol123",
                first_name=fname,
                last_name=lname,
                role='student',
                total_xp=total_xp,
                edu_coins=edu_coins,
                has_vip_badge=has_vip,
                avatar_url=avatar_url,
                headline=headline,
                bio=f"{fname} {lname} — SkillUp markazining faol o'quvchisi. O'z yo'nalishida a'lo natijalar ko'rsatib kelmoqda."
            )
            created_count += 1
        else:
            user.first_name = fname
            user.last_name = lname
            user.total_xp = total_xp
            user.edu_coins = edu_coins
            user.has_vip_badge = has_vip
            user.avatar_url = avatar_url
            user.headline = headline
            user.role = 'student'
            user.save()

        # 8 ta amaliy harakat bo'yicha CoinTransaction yozuvlarini yaratish
        # Har bir talabada 6-12 ta amaliy faoliyat yozuvlari bo'lsin
        existing_tx_count = user.coin_transactions.count()
        if existing_tx_count < 5:
            num_actions = random.randint(6, 12)
            today = date.today()
            for a_idx in range(num_actions):
                action = random.choice(action_blueprints)
                act_code, act_coins, act_xp, act_desc = action
                days_ago = random.randint(0, 30)
                tx_date = timezone.now() - timedelta(days=days_ago)

                CoinTransaction.objects.create(
                    user=user,
                    amount=act_coins,
                    action_type=act_code,
                    description=act_desc,
                    created_at=tx_date
                )

        # Sinov natijalari (QuizResult) yaratish
        if all_quizzes and user.quiz_results.count() < 3:
            for qz in random.sample(all_quizzes, min(len(all_quizzes), 4)):
                score_val = random.choice([75.0, 80.0, 85.0, 90.0, 95.0, 100.0])
                QuizResult.objects.get_or_create(
                    user=user,
                    quiz=qz,
                    defaults={
                        'score': score_val,
                        'is_passed': True
                    }
                )

        # Guruhlarga biriktirish
        if active_groups and user.study_groups.count() == 0:
            assigned_group = random.choice(active_groups)
            assigned_group.students.add(user)

    total_final_students = User.objects.filter(role='student').count()
    print(f"\n[OK] Jami {total_final_students} nafar talaba bazada muvaffaqiyatli shakllantirildi! (Yangi yaratilgan: {created_count} ta)")

    # 3. TOP 3 Shohsupa tekshiruvi
    top_3 = User.objects.filter(role='student').order_by('-total_xp')[:3]
    print("\n🏆 TOP-3 Shohsupa yetakchilari:")
    for idx, s in enumerate(top_3, start=1):
        print(f"   #{idx} {s.get_full_name()} (@{s.username}) — {s.total_xp} XP | {s.edu_coins} 🪙")

    print("\nBARCHA MA'LUMOTLAR MUVAFFAQIYATLI YUKLANDI!")

if __name__ == '__main__':
    run_seed()
