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

from core.models import User, Course, Module, Lesson, Quiz, Question, Choice


def seed_teachers_and_clubs():
    print("=" * 70)
    print("🎓 17 TA TO'GARAK, O'QITUVCHILAR VA OYLIK MAOSHLARINI BAZAGA YUKLASH")
    print("=" * 70)

    # 1. O'QITUVCHILAR VA ULARNING OYLIK MAOSHLARI (5 mln - 15 mln so'm)
    teachers_data = [
        {
            'username': 'ustoz_alisher',
            'first_name': 'Alisher',
            'last_name': 'Rustamov',
            'email': 'alisher@skillup.uz',
            'headline': 'Senior Python & AI Architect (Zamonaviy Kasb Ustasi)',
            'bio': '10 yildan ortiq xalqaro IT kompaniyalarida yetakchi arxitektor bo\'lib ishlagan. FinTech va yirik sun\'iy intellekt tizimlari ishlab chiquvchisi.',
            'avatar_url': 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=500',
            'monthly_salary': 15000000,
            'experience_years': 10,
            'specialties': 'Python, Django REST, PyTorch, Microservices, System Design',
            'students_count': 1250,
        },
        {
            'username': 'ustoz_azizbek',
            'first_name': 'Azizbek',
            'last_name': 'Qodirov',
            'email': 'azizbek@skillup.uz',
            'headline': 'Dasturlash Asoslari & Algoritmlar Katta Murabbiyi',
            'bio': 'ACM-ICPC olimpiadalari finalisti, yoshlarga dasturlash va mantiqiy fikrlashni noldan o\'rgatish bo\'yicha 8 yillik yetakchi metodist.',
            'avatar_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500',
            'monthly_salary': 14000000,
            'experience_years': 8,
            'specialties': 'Data Structures, Python Core, Algorithms, Competitive Programming',
            'students_count': 980,
        },
        {
            'username': 'ustoz_malika',
            'first_name': 'Malika',
            'last_name': 'Rahimova',
            'email': 'malika@skillup.uz',
            'headline': 'Senior Frontend & UI/UX Muhandisi (Zamonaviy Kasb)',
            'bio': 'Yevropa va AQSh startaplarida 7 yillik amaliy tajribaga ega front-end yetakchisi. Zamonaviy React, Next.js va dizayn tizimlari mutaxassisi.',
            'avatar_url': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=500',
            'monthly_salary': 13500000,
            'experience_years': 7,
            'specialties': 'React.js, Next.js, TypeScript, TailwindCSS, Figma, Redux',
            'students_count': 1100,
        },
        {
            'username': 'ustoz_jasur',
            'first_name': 'Jasur',
            'last_name': 'Beknazarov',
            'email': 'jasur@skillup.uz',
            'headline': 'IELTS 8.5 & CEFR Bosh Koordinatori (Xalqaro Ekspert)',
            'bio': 'Britaniya Kengashi (British Council) sertifikatlangan xalqaro instruktori. O\'quvchilari 7.5+ va 8.0 natijalar ko\'rsatgan tajribali repetitor.',
            'avatar_url': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=500',
            'monthly_salary': 12500000,
            'experience_years': 9,
            'specialties': 'IELTS Academic 8.5, CEFR C1/C2, Essay Writing, Fluency Speaking',
            'students_count': 870,
        },
        {
            'username': 'ustoz_nilufar',
            'first_name': 'Nilufar',
            'last_name': 'Karimova',
            'email': 'nilufar@skillup.uz',
            'headline': 'Koreys (TOPIK 6) & Xitoy Tili (HSK 5) Mutaxassisi',
            'bio': 'Seul Milliy Universiteti magistri, Pekin til institutida amaliyot o\'tagan. Osiyo tillarini oson va interaktiv o\'zlashtirish dasturi muallifi.',
            'avatar_url': 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=500',
            'monthly_salary': 10000000,
            'experience_years': 6,
            'specialties': 'TOPIK II (Level 6), HSK 5, Koreys tili so\'zlashuv, Osiyo madaniyati',
            'students_count': 640,
        },
        {
            'username': 'ustoz_otabek',
            'first_name': 'Otabek',
            'last_name': 'Xoliqov',
            'email': 'otabek@skillup.uz',
            'headline': 'Matematika & Olimpiada Bosh Murabbiyi',
            'bio': 'O\'zbekiston Milliy Universiteti dotsenti, xalqaro matematika olimpiadalari hakamlar hay\'ati a\'zosi. Mental arifmetika va oliy matematika ustozi.',
            'avatar_url': 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=500',
            'monthly_salary': 9000000,
            'experience_years': 12,
            'specialties': 'Olimpiada matematikasi, Algebra, Geometriya, DTM 100% tayyorgarlik',
            'students_count': 1400,
        },
        {
            'username': 'ustoz_sardor',
            'first_name': 'Sardor',
            'last_name': 'Olimov',
            'email': 'sardor@skillup.uz',
            'headline': 'Turk Tili (TÖMER C1) & Rus Tili Katta O\'qituvchisi',
            'bio': 'Istanbul Universiteti bitiruvchisi, diplomatik tarjimon. Erkin so\'zlashuv va xalqaro til sertifikatlariga tayyorlash bo\'yicha 7 yillik tajriba.',
            'avatar_url': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=500',
            'monthly_salary': 8500000,
            'experience_years': 7,
            'specialties': 'TÖMER C1, TRKI Rus tili, Sinxron tarjima, Biznes muloqot',
            'students_count': 720,
        },
        {
            'username': 'ustoz_gulnoza',
            'first_name': 'Gulnoza',
            'last_name': 'Yoqubova',
            'email': 'gulnoza@skillup.uz',
            'headline': 'Ona Tili & Adabiyot (Milliy Sertifikat) Bosh Mutaxassisi',
            'bio': 'Oliy toifali filolog, DTM test tuzuvchilar seminarlari ishtirokchisi. Milliy sertifikatdan 90+ ball olgan yuzlab o\'quvchilar ustozi.',
            'avatar_url': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=500',
            'monthly_salary': 8000000,
            'experience_years': 11,
            'specialties': 'Milliy Sertifikat A+, Adabiyot tahlili, Ona tili grammatikasi',
            'students_count': 1300,
        },
        {
            'username': 'ustoz_bobur',
            'first_name': 'Bobur',
            'last_name': 'Mirzayev',
            'email': 'bobur@skillup.uz',
            'headline': 'Shaxmat & Shashka bo\'yicha Xalqaro FIDE Ustasi',
            'bio': 'FIDE Master (FM), Osiyo chempionati sovrindori. Mantiqiy strategik fikrlash, kombinatsiyalar va onlayn blitz musobaqalari bo\'yicha trener.',
            'avatar_url': 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=500',
            'monthly_salary': 7500000,
            'experience_years': 8,
            'specialties': 'FIDE 2350 Elo, Taktik kombinatsiyalar, Endshpil tahlili, Shashka 64/100',
            'students_count': 530,
        },
        {
            'username': 'ustoz_dildora',
            'first_name': 'Dildora',
            'last_name': 'Mahmudova',
            'email': 'dildora@skillup.uz',
            'headline': 'Boshlang\'ich Savodxonlik & Savod Chiqarish Metodisti',
            'bio': 'Bolalar va kattalarda tez va to\'g\'ri o\'qish-yozish ko\'nikmalarini shakllantiruvchi zamonaviy o\'yinli metodika yaratuvchisi.',
            'avatar_url': 'https://images.unsplash.com/photo-1567532939604-b6b5b0db2604?w=500',
            'monthly_salary': 6500000,
            'experience_years': 9,
            'specialties': 'Savod chiqarish, Chiroyli yozuv (Kalligrafiya), Tez o\'qish metodikasi',
            'students_count': 610,
        },
        {
            'username': 'ustoz_sanjar',
            'first_name': 'Sanjar',
            'last_name': 'Qosimov',
            'email': 'sanjar@skillup.uz',
            'headline': 'Futbol & Ping-pong Katta Murabbiyi (Hafta Oxiri Sport)',
            'bio': 'Jismoniy tarbiya instituti bitiruvchisi, stol tennisi bo\'yicha sport ustaligiga nomzod. Mini-futbol jamoalari va haftalik turnirlar koordinatori.',
            'avatar_url': 'https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=500',
            'monthly_salary': 5500000,
            'experience_years': 6,
            'specialties': 'Mini-futbol taktika, Ping-pong topspin, Hafta oxiri musobaqalari',
            'students_count': 490,
        },
    ]

    teacher_objects = {}
    for td in teachers_data:
        user, created = User.objects.get_or_create(
            username=td['username'],
            defaults={
                'role': 'teacher',
                'first_name': td['first_name'],
                'last_name': td['last_name'],
                'email': td['email'],
                'headline': td['headline'],
                'bio': td['bio'],
                'avatar_url': td['avatar_url'],
                'monthly_salary': td['monthly_salary'],
                'experience_years': td['experience_years'],
                'specialties': td['specialties'],
                'students_count': td['students_count'],
                'edu_coins': 500,
                'has_vip_badge': True,
            }
        )
        if not created:
            user.first_name = td['first_name']
            user.last_name = td['last_name']
            user.headline = td['headline']
            user.bio = td['bio']
            user.avatar_url = td['avatar_url']
            user.monthly_salary = td['monthly_salary']
            user.experience_years = td['experience_years']
            user.specialties = td['specialties']
            user.students_count = td['students_count']
            user.has_vip_badge = True
            user.save()
        user.set_password('parol123')
        user.save()
        teacher_objects[td['username']] = user
        status = "Yangi" if created else "Yangilandi"
        print(f"[{status}] O'qituvchi: {user.get_full_name()} — Oyligi: {user.get_salary_display()}")

    # 2. FOYDALANUVCHI AYTGAN 17 TA TO'LIQ TO'GARAKLAR VA KURS RO'YXATI
    clubs_data = [
        {
            'title': "Boshlang'ich Savodxonlik (Savod Chiqarish To'garagi)",
            'category': "Savodxonlik",
            'level': "Boshlang'ich",
            'author': teacher_objects['ustoz_dildora'],
            'price': 300000,
            'discount_price': 250000,
            'duration_hours': 24,
            'schedule_type': 'toq',
            'schedule_time': '09:00 - 10:30',
            'lesson_format': 'Online (Jonli darslar)',
            'is_modern_profession': False,
            'thumbnail_url': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=600',
            'description': "Harflar, tovushlar, to'g'ri bo'g'inlab o'qish, chiroyli yozuv (husnixat) va mantiqiy fikrlashni shakllantiruvchi interaktiv savodxonlik to'garagi. Ertadan boshlanadi!",
        },
        {
            'title': "Dasturlash Asoslari: Algoritmlar va Mantiq",
            'category': "IT & Dasturlash",
            'level': "Boshlang'ich",
            'author': teacher_objects['ustoz_azizbek'],
            'price': 550000,
            'discount_price': 450000,
            'duration_hours': 36,
            'schedule_type': 'juft',
            'schedule_time': '14:00 - 15:30',
            'lesson_format': 'Online (Interaktiv kodlash)',
            'is_modern_profession': False,
            'thumbnail_url': 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=600',
            'description': "Dasturlash dunyosiga ilk qadam: o'zgaruvchilar, shartlar, sikllar, funksiyalar va qiziqarli dasturlar yaratish ko'nikmalari.",
        },
        {
            'title': "Backend Dasturlash (Python, Django REST API & PostgreSQL)",
            'category': "IT & Dasturlash",
            'level': "O'rta / Yuqori",
            'author': teacher_objects['ustoz_alisher'],
            'price': 850000,
            'discount_price': 650000,
            'duration_hours': 48,
            'schedule_type': 'toq',
            'schedule_time': '18:00 - 19:30',
            'lesson_format': 'Online (Jonli Masterklass)',
            'is_modern_profession': True, # Zamonaviy qimmat kasb
            'thumbnail_url': 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=600',
            'description': "Zamonaviy IT kasb: Katta ma'lumotlar bilan ishlash, server arxitekturasi, xavfsizlik, JWT autentifikatsiya va yuqori maoshli backend ishlab chiqish.",
        },
        {
            'title': "Frontend Dasturlash (React.js, Next.js & Zamonaviy Web)",
            'category': "IT & Dasturlash",
            'level': "O'rta / Yuqori",
            'author': teacher_objects['ustoz_malika'],
            'price': 800000,
            'discount_price': 600000,
            'duration_hours': 45,
            'schedule_type': 'juft',
            'schedule_time': '18:00 - 19:30',
            'lesson_format': 'Online (Jonli Kodlash)',
            'is_modern_profession': True, # Zamonaviy qimmat kasb
            'thumbnail_url': 'https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=600',
            'description': "Zamonaviy IT kasb: Chiroyli interfeyslar, dinamik veb-ilovalar, API integratsiyasi va xalqaro frilans bozoriga tayyorgarlik.",
        },
        {
            'title': "Ingliz Tili: General English (A1 dan B2 gacha)",
            'category': "Xorijiy Tillar",
            'level': "Boshlang'ich - O'rta",
            'author': teacher_objects['ustoz_jasur'],
            'price': 450000,
            'discount_price': 350000,
            'duration_hours': 30,
            'schedule_type': 'toq',
            'schedule_time': '10:00 - 11:30',
            'lesson_format': 'Online (Muloqotli)',
            'is_modern_profession': False,
            'thumbnail_url': 'https://images.unsplash.com/photo-1457369804613-52c61a468e7d?w=600',
            'description': "Erkin gapirish, kundalik iboralar, eshitish (Listening) va grammatikani yodlashsiz tabiiy o'zlashtirish to'garagi.",
        },
        {
            'title': "CEFR B2 & C1 Davlat Imtihoniga Maxsus Tayyorgarlik",
            'category': "Xorijiy Tillar",
            'level': "Yuqori",
            'author': teacher_objects['ustoz_jasur'],
            'price': 500000,
            'discount_price': 400000,
            'duration_hours': 32,
            'schedule_type': 'juft',
            'schedule_time': '16:00 - 17:30',
            'lesson_format': 'Online (Imtihon Simulyatsiyasi)',
            'is_modern_profession': False,
            'thumbnail_url': 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=600',
            'description': "Milliy CEFR imtihoni topshiruvchilar uchun 100% test strategiyalari, listening fokus va speaking mezonlari bo'yicha intensiv to'garak.",
        },
        {
            'title': "IELTS 7.5+ Target Intensive (Katta Murabbiy Bilan)",
            'category': "Xorijiy Tillar",
            'level': "Yuqori / Professional",
            'author': teacher_objects['ustoz_jasur'],
            'price': 750000,
            'discount_price': 550000,
            'duration_hours': 40,
            'schedule_type': 'toq',
            'schedule_time': '15:00 - 16:30',
            'lesson_format': 'Online (Intensiv guruh)',
            'is_modern_profession': True, # Zamonaviy yuqori to'lov
            'thumbnail_url': 'https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=600',
            'description': "IELTS 7.5 va 8.0 ballni ko'zlaganlar uchun: Writing Task 1-2 tahlili, Reading skimm-scan usullari va haqiqiy imtihon muhiti.",
        },
        {
            'title': "Koreys Tili (TOPIK I-II va Jonli So'zlashuv)",
            'category': "Sharq Tillari",
            'level': "Boshlang'ich - O'rta",
            'author': teacher_objects['ustoz_nilufar'],
            'price': 480000,
            'discount_price': 380000,
            'duration_hours': 30,
            'schedule_type': 'juft',
            'schedule_time': '10:00 - 11:30',
            'lesson_format': 'Online (Jonli)',
            'is_modern_profession': False,
            'thumbnail_url': 'https://images.unsplash.com/photo-1517154421773-0529f29ea451?w=600',
            'description': "Hangil alifbosi, TOPIK I-II imtihoniga tayyorgarlik va Janubiy Koreya universitetlari hamda GKS grantlariga yo'llanma to'garagi.",
        },
        {
            'title': "Rus Tili: Erkin Muloqot va Amaliy Grammatika",
            'category': "Xorijiy Tillar",
            'level': "Boshlang'ich - O'rta",
            'author': teacher_objects['ustoz_sardor'],
            'price': 400000,
            'discount_price': 300000,
            'duration_hours': 28,
            'schedule_type': 'toq',
            'schedule_time': '14:00 - 15:30',
            'lesson_format': 'Online (Muloqotli)',
            'is_modern_profession': False,
            'thumbnail_url': 'https://images.unsplash.com/photo-1513326738677-b964603b136d?w=600',
            'description': "Rus tilida erkin va ravon gapirish, ishbilarmonlik suhbatlari, to'g'ri talaffuz va kundalik hayotda qo'llash sirlari.",
        },
        {
            'title': "Xitoy Tili: HSK 1-4 va Ierogliflar San'ati",
            'category': "Sharq Tillari",
            'level': "Boshlang'ich",
            'author': teacher_objects['ustoz_nilufar'],
            'price': 520000,
            'discount_price': 420000,
            'duration_hours': 32,
            'schedule_type': 'juft',
            'schedule_time': '11:30 - 13:00',
            'lesson_format': 'Online (Jonli)',
            'is_modern_profession': False,
            'thumbnail_url': 'https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=600',
            'description': "Xitoy tili ohanglari (Pinyin), 600+ asosiy ierogliflar, HSK 1-3 xalqaro sertifikatiga noldan tayyorlanish.",
        },
        {
            'title': "Turk Tili (TÖMER va Sayohat / O'qish Uchun So'zlashuv)",
            'category': "Xorijiy Tillar",
            'level': "Boshlang'ich - O'rta",
            'author': teacher_objects['ustoz_sardor'],
            'price': 420000,
            'discount_price': 320000,
            'duration_hours': 26,
            'schedule_type': 'toq',
            'schedule_time': '16:30 - 18:00',
            'lesson_format': 'Online (Jonli)',
            'is_modern_profession': False,
            'thumbnail_url': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=600',
            'description': "Turkiya madaniyati, TÖMER imtihoni, Istanbul lahjasida ravon so'zlashish va Turkiyada ta'lim olishga tayyorgarlik.",
        },
        {
            'title': "Ona Tili: Imlo Madaniyati va To'g'ri Grammatika",
            'category': "Milliy Fanlar",
            'level': "Boshlang'ich - O'rta",
            'author': teacher_objects['ustoz_gulnoza'],
            'price': 350000,
            'discount_price': 280000,
            'duration_hours': 24,
            'schedule_type': 'juft',
            'schedule_time': '09:00 - 10:30',
            'lesson_format': 'Online (Jonli)',
            'is_modern_profession': False,
            'thumbnail_url': 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=600',
            'description': "Lotin yozuvida to'g'ri yozish, so'z yasalishi, morfologiya va sintaksis qoidalari bo'yicha mustahkam bilim.",
        },
        {
            'title': "Adabiyot va Tahlil (Milliy Sertifikat Tayyorgarligi)",
            'category': "Milliy Fanlar",
            'level': "Yuqori",
            'author': teacher_objects['ustoz_gulnoza'],
            'price': 450000,
            'discount_price': 350000,
            'duration_hours': 30,
            'schedule_type': 'toq',
            'schedule_time': '11:30 - 13:00',
            'lesson_format': 'Online (Imtihon yo\'naltirilgan)',
            'is_modern_profession': False,
            'thumbnail_url': 'https://images.unsplash.com/photo-1476275466078-4007374efbbe?w=600',
            'description': "Klassik va zamonaviy adabiyot, badiiy asarlar tahlili va Milliy Sertifikatdan 90+ ball to'plash strategiyasi.",
        },
        {
            'title': "Matematika & Mantiqiy Fikrlash (Olimpiada va DTM)",
            'category': "Aniq Fanlar",
            'level': "Boshlang'ich - Yuqori",
            'author': teacher_objects['ustoz_otabek'],
            'price': 480000,
            'discount_price': 380000,
            'duration_hours': 36,
            'schedule_type': 'juft',
            'schedule_time': '15:00 - 16:30',
            'lesson_format': 'Online (Interaktiv)',
            'is_modern_profession': False,
            'thumbnail_url': 'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=600',
            'description': "Mental arifmetika, tenglamalar, geometrik yasashlar va nostandart olimpiada masalalarini oson yechish usullari.",
        },
        {
            'title': "Shaxmat & Shashka Musobaqasi (Strategik Fikrlash To'garagi)",
            'category': "Sport & Musobaqalar",
            'level': "Barcha darajalar",
            'author': teacher_objects['ustoz_bobur'],
            'price': 320000,
            'discount_price': 250000,
            'duration_hours': 20,
            'schedule_type': 'hafta_oxiri',
            'schedule_time': '14:00 - 16:00 (Shanba-Yakshanba)',
            'lesson_format': 'Online (Lichess & Live tahlil)',
            'is_modern_profession': False,
            'thumbnail_url': 'https://images.unsplash.com/photo-1529699211952-734e80c4d42b?w=600',
            'description': "Debyutlar nazariyasi, taktik zarbalar, endshpil san'ati hamda har shanba-yakshanba kunlari onlayn turnir va sovrinlar!",
        },
        {
            'title': "Hafta Oxiri Futbol Rejalashtirilishi & Taktik Tahlil",
            'category': "Sport & Musobaqalar",
            'level': "Barcha darajalar",
            'author': teacher_objects['ustoz_sanjar'],
            'price': 280000,
            'discount_price': 200000,
            'duration_hours': 16,
            'schedule_type': 'hafta_oxiri',
            'schedule_time': '17:00 - 19:00 (Shanba-Yakshanba)',
            'lesson_format': 'Online (Taktik rejalashtirish & Turnir)',
            'is_modern_profession': False,
            'thumbnail_url': 'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=600',
            'description': "Hafta davomida jismoniy mashqlar, o'yin taktikalari va dam olish kunlari mini-futbol bellashuvlarini tashkil etish to'garagi.",
        },
        {
            'title': "Ping-pong (Stol Tennisi) Mahorat Darslari & Chempionat",
            'category': "Sport & Musobaqalar",
            'level': "Boshlang'ich - O'rta",
            'author': teacher_objects['ustoz_sanjar'],
            'price': 300000,
            'discount_price': 220000,
            'duration_hours': 16,
            'schedule_type': 'hafta_oxiri',
            'schedule_time': '10:00 - 12:00 (Yakshanba)',
            'lesson_format': 'Online (Texnika & Turnir)',
            'is_modern_profession': False,
            'thumbnail_url': 'https://images.unsplash.com/photo-1534158914592-062992fbe900?w=600',
            'description': "Tezkor reaksiya, to'g'ri raketka ushlash, aylanma zarbalar (topspin) va yakshanba kungi jonli chempionatlar.",
        },
    ]

    for cd in clubs_data:
        course, created = Course.objects.update_or_create(
            title=cd['title'],
            defaults=cd
        )
        status = "Yangi" if created else "Yangilandi"
        print(f"[{status}] To'garak: {course.title} — {course.get_effective_price():,} so'm ({course.get_schedule_display_full()})")

        # Modul va darslar yaratish (agar yo'q bo'lsa)
        if not course.modules.exists():
            mod1 = Module.objects.create(
                course=course,
                title="1-Modul: Asosiy tushunchalar va kirish mashg'ulotlari",
                order=1
            )
            Lesson.objects.create(
                module=mod1,
                title=f"{course.title}ga Kirish va Mashg'ulot Rejasi",
                content=f"""Hush kelibsiz! Ushbu mashg'ulotda biz '{course.title}' to'garagining asosiy qoidalari, maqsadlari va ertadan boshlanadigan darslar tartibini o'rganamiz.\n\nKunlar tartibi: {course.get_schedule_display_full()}.\nFormat: {course.lesson_format}.\n\nO'qituvchi: {course.author.get_full_name()} (Oyligi: {course.author.get_salary_display()}).\n\nTayyor bo'lsangiz, 'Darsni tugatdim' tugmasini bosing va birinchi XP hamda EduCoin tangalaringizni qo'lga kiriting!""",
                video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                order=1
            )
            Lesson.objects.create(
                module=mod1,
                title=f"2-Dars: Amaliy Ko'nikmalar va Mashqlar",
                content=f"""Amaliyot qismi: Ushbu darsda o'rganilgan nazariyani amalda qo'llash va keyingi modulga o'tish uchun imtihonga tayyorlanish vazifalari berilgan.\n\nEslatib o'tamiz: Modul testidan kamida 70% to'plashingiz kerak!""",
                video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                order=2
            )

            # Modul uchun Test yaratish
            quiz = Quiz.objects.create(
                module=mod1,
                title=f"{course.title} — 1-Modul Nazorat Testi",
                passing_score=70,
                duration_minutes=10
            )
            q1 = Question.objects.create(
                quiz=quiz,
                text=f"{course.title} to'garagida darslar qaysi vaqtda o'tkaziladi?"
            )
            Choice.objects.create(question=q1, text=f"{course.schedule_time} da", is_correct=True)
            Choice.objects.create(question=q1, text="Tungi soat 03:00 da", is_correct=False)
            Choice.objects.create(question=q1, text="Faqat yoz oylarida", is_correct=False)

            q2 = Question.objects.create(
                quiz=quiz,
                text=f"Ushbu to'garak muallifi va ustozi kim?"
            )
            Choice.objects.create(question=q2, text=f"{course.author.get_full_name()}", is_correct=True)
            Choice.objects.create(question=q2, text="Noma'lum kishi", is_correct=False)
            Choice.objects.create(question=q2, text="Sun'iy intellekt bot", is_correct=False)

            q3 = Question.objects.create(
                quiz=quiz,
                text=f"SkillUp platformasida 2 ta kursga bir vaqtda qatnashilsa qancha chegirma beriladi?"
            )
            Choice.objects.create(question=q3, text="50 000 so'm chegirma", is_correct=True)
            Choice.objects.create(question=q3, text="Chegirma berilmaydi", is_correct=False)
            Choice.objects.create(question=q3, text="1 000 so'm", is_correct=False)

    print("\n✅ Barcha 17 ta to'garak, modullar va testlar muvaffaqiyatli saqlandi!")
    print("=" * 70)


if __name__ == '__main__':
    seed_teachers_and_clubs()
