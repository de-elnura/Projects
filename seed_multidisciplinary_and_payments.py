import os
import sys
import django

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from core.models import (
    Course, Module, Lesson,
    Quiz, Question, Choice,
    UserLessonProgress, QuizResult, Certificate,
    Coupon, Enrollment
)

User = get_user_model()


def seed_multidisciplinary():
    print("🚀 Yangi sohalar, to'lov narxlari va promokodlarni yuklash boshlandi...")

    # =========================================================================
    # 1. FAOL PROMOKODLARNI YARATISH
    # =========================================================================
    coupons = [
        {'code': 'PROMO50', 'discount_percent': 50, 'max_uses': 500},
        {'code': 'SKILLUP30', 'discount_percent': 30, 'max_uses': 1000},
        {'code': 'BEPUL100', 'discount_percent': 100, 'max_uses': 200},
        {'code': 'BAHOR2026', 'discount_percent': 25, 'max_uses': 300},
        {'code': 'TALABA15', 'discount_percent': 15, 'max_uses': 1000},
    ]

    for c in coupons:
        obj, _ = Coupon.objects.get_or_create(
            code=c['code'],
            defaults={
                'discount_percent': c['discount_percent'],
                'max_uses': c['max_uses'],
                'is_active': True,
                'valid_until': timezone.now() + timedelta(days=90)
            }
        )
        obj.discount_percent = c['discount_percent']
        obj.save()

    print(f"✅ {len(coupons)} ta faol promokod yaratildi.")

    # =========================================================================
    # 2. NO-IT SOHALARDAGI 5 TA YANGI O'QITUVCHI
    # =========================================================================
    new_teachers = [
        {
            'username': 'kamola_design',
            'first_name': 'Kamola',
            'last_name': 'Karimova',
            'email': 'kamola.design@skillup.uz',
            'headline': 'Senior Product Designer & Design System Lead',
            'bio': "Figma, Adobe XD, Photoshop va zamonaviy UI/UX tadqiqotlar bo'yicha ekspert. 50+ yirik xalqaro loyihalar muallifi.",
            'avatar_url': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=250&q=80',
            'total_xp': 820
        },
        {
            'username': 'otabek_smm',
            'first_name': 'Otabek',
            'last_name': 'Zokirov',
            'email': 'otabek.marketing@skillup.uz',
            'headline': 'Digital Marketing Director & Target Specialist',
            'bio': "Meta Ads, Google Ads, TikTok marketing va brending bo'yicha 7+ yillik amaliy tajribaga ega yetakchi marketing strateg.",
            'avatar_url': 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=250&q=80',
            'total_xp': 740
        },
        {
            'username': 'gulnoza_ielts',
            'first_name': 'Gulnoza',
            'last_name': 'Saidova',
            'email': 'gulnoza.english@skillup.uz',
            'headline': 'IELTS 8.5 Instructor & Oxford Linguistics Graduate',
            'bio': "Xalqaro darajadagi ingliz tili murabbiyi. O'quvchilari IELTS 7.5-8.5 ball to'plab, xalqaro universitetlar grantlarini yutgan.",
            'avatar_url': 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?auto=format&fit=crop&w=250&q=80',
            'total_xp': 890
        },
        {
            'username': 'temur_finance',
            'first_name': 'Temur',
            'last_name': 'Fayziyev',
            'email': 'temur.finance@skillup.uz',
            'headline': 'Biznes Konsultant, Investor & Startap Mentori',
            'bio': "Investitsiyalar, shaxsiy byudjetni boshqarish, biznes modellari va startaplarga investitsiya jalb qilish bo'yicha amaliyotchi mutaxassis.",
            'avatar_url': 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=250&q=80',
            'total_xp': 770
        },
        {
            'username': 'rustam_bi',
            'first_name': 'Rustam',
            'last_name': 'Nazarov',
            'email': 'rustam.analytics@skillup.uz',
            'headline': 'Lead Business Intelligence (BI) Analyst',
            'bio': "Excel murakkab funksiyalari, PowerBI, SQL analitika va biznes qarorlar qabul qilish uchun interaktiv dashboardlar yaratish bo'yicha ekspert.",
            'avatar_url': 'https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?auto=format&fit=crop&w=250&q=80',
            'total_xp': 790
        }
    ]

    teacher_objects = {}
    for t in new_teachers:
        user, _ = User.objects.get_or_create(
            username=t['username'],
            defaults={
                'first_name': t['first_name'],
                'last_name': t['last_name'],
                'email': t['email'],
                'role': 'teacher',
                'headline': t['headline'],
                'bio': t['bio'],
                'avatar_url': t['avatar_url'],
                'total_xp': t['total_xp'],
            }
        )
        user.set_password('parol123')
        user.headline = t['headline']
        user.bio = t['bio']
        user.avatar_url = t['avatar_url']
        user.save()
        teacher_objects[t['username']] = user

    print(f"✅ {len(new_teachers)} ta yangi soha o'qituvchilari saqlandi.")

    # =========================================================================
    # 3. YANGI SOHALAR BO'YICHA TO'LOVLI VA CHEGIRMALI KURSLAR
    # =========================================================================
    multi_courses = [
        # Dizayn
        {
            'author_key': 'kamola_design',
            'title': "Figma va Zamonaviy Web & Mobile UI/UX Dizayn",
            'category': "Grafik Dizayn",
            'level': "Boshlang'ich / O'rta",
            'duration_hours': 26,
            'price': 450000,
            'discount_price': 299000,
            'is_free': False,
            'description': "Noldan boshlab professional veb-saytlar va mobil ilovalar dizaynini yarating. Figma vositalari, AutoLayout, Komponentlar, Variantlar, Design System va interaktiv prototiplash.",
            'modules': [
                {
                    'title': "Figma Asoslari, Frame va AutoLayout Texnologiyasi",
                    'lessons': [
                        ("Figma Interfeysi, Grid Tizimi va Tipografika", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Veb va mobil gridlar, shriftlar uyg'unligi va o'lchamlar ierarxiyasi."),
                        ("AutoLayout 5.0 va Responsiv UI Bloklar", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Matn o'zgarganda avtomatik moslashuvchi zamonaviy tugmalar va kartochkalar.")
                    ],
                    'quiz_title': "1-Modul: Figma va Layout Imtihoni",
                    'questions': [
                        ("Figma-da elementlarni moslashuvchan konteynerga olish funksiyasi qaysi?", [("AutoLayout (Shift + A)", True), ("Group (Ctrl + G)", False), ("Frame (F)", False), ("Mask", False)]),
                        ("Mobil ilovalar dizaynida standart 8pt grid tizimi nima uchun ishlatiladi?", [("Elementlar orasidagi masofalar mutanosibligi va dasturlashga qulaylik uchun", True), ("Fayl hajmini kamaytirish", False), ("Ranglarni tanlash uchun", False), ("Faqat shrift uchun", False)])
                    ]
                },
                {
                    'title': "Komponentlar, Variantlar va Design System Qurish",
                    'lessons': [
                        ("Komponentlar va Master Component Tamoyillari", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Bitta master komponentni o'zgartirish orqali butun loyihani bir zumda yangilash."),
                        ("Variantlar va Interaktiv Komponent Holatlari (Hover, Click)", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Tugmalar va inputlarning jonli holatlarini yaratish.")
                    ],
                    'quiz_title': "2-Modul: Komponentlar va Tizimlar Imtihoni",
                    'questions': [
                        ("Figma-da bitta komponentning turli holatlarini (masalan, Primary, Secondary) birlashtirish nima deyiladi?", [("Variants", True), ("Instances", False), ("Styles", False), ("Properties", False)]),
                        ("Design Tokens nimani anglatadi?", [("Ranglar, shriftlar va radiuslarning markazlashgan o'zgaruvchilari", True), ("Kriptovalyuta", False), ("Parol", False), ("Ikonkalar", False)])
                    ]
                },
                {
                    'title': "Interaktiv Prototiplash va Dasturchilarga Loyihani Topshirish (DevMode)",
                    'lessons': [
                        ("Smart Animate va Sahifalararo Animatsiyalar", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Mobil ilova real foydalanuvchiga qanday ko'rinishini jonli ko'rsatish."),
                        ("Figma DevMode orqali CSS kodlar va aktivlarni eksport qilish", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Frontend dasturchilar bilan professional hamkorlik.")
                    ],
                    'quiz_title': "Yakuniy Bitiruv Imtihoni: UI/UX Dizayn",
                    'questions': [
                        ("Figma-da silliq o'tish animatsiyasini ta'minlovchi rejim qaysi?", [("Smart Animate", True), ("Dissolve", False), ("Instant", False), ("Push", False)]),
                        ("DevMode imkoniyati qaysi mutaxassislar uchun mo'ljallangan?", [("Dasturchilar (Frontend/Mobile)", True), ("Faqat mijozlar", False), ("Buxgalterlar", False), ("Copywriterlar", False)])
                    ]
                }
            ]
        },

        # SMM va Marketing
        {
            'author_key': 'otabek_smm',
            'title': "SMM, Target va Raqamli Marketing Strategiyasi",
            'category': "Raqamli Marketing",
            'level': "Boshlang'ich / O'rta",
            'duration_hours': 24,
            'price': 500000,
            'discount_price': 349000,
            'is_free': False,
            'description': "Ijtimoiy tarmoqlarda professional auditoriya to'plash, sotuvchi kontent yaratish, Meta Ads orqali maqsadli target reklama va konversiyani oshirish.",
            'modules': [
                {
                    'title': "SMM Strategiya, Kontent Reja va Kopirayting",
                    'lessons': [
                        ("Maqsadli Auditoriyani (Target Audience) Aniq Belgilash", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Mijoz portretini (User Persona) chizish va uning ehtiyojlarini topish."),
                        ("AIDA va PAS Formulalari Asosida Sotuvchi Matnlar Yozish", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "E'tibor tortuvchi sarlavhalar va harakatga chaqiruvchi (CTA) yozish.")
                    ],
                    'quiz_title': "1-Modul: Kontent va Auditoriya Imtihoni",
                    'questions': [
                        ("AIDA marketing modelining ketma-ketligi qanday?", [("Attention -> Interest -> Desire -> Action", True), ("Action -> Idea -> Data -> Ads", False), ("Analyze -> Invest -> Do -> Act", False), ("Audience -> Info -> Deal -> Apply", False)]),
                        ("CTA (Call to Action) nimani bildiradi?", [("Foydalanuvchini aniq harakatga chorlovchi chaqiruv", True), ("Kompaniya shiori", False), ("Reklama narxi", False), ("Statistika", False)])
                    ]
                },
                {
                    'title': "Meta Ads Manager va Maqsadli Target Reklama",
                    'lessons': [
                        ("Facebook Ads Manager Tuzilishi va Kampaniyalar Yaratish", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Qiziqishlar, geografiya va demografiya bo'yicha aniq mo'ljalga olish."),
                        ("Meta Pixel O'rnatish va Retargeting Taktikalari", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Saytga kirib ketgan mijozlarni qayta jalb qilish sirlari.")
                    ],
                    'quiz_title': "2-Modul: Target Reklama Imtihoni",
                    'questions': [
                        ("Veb-saytga tashrif buyurgan foydalanuvchilar harakatini kuzatuvchi kod nima deyiladi?", [("Meta Pixel (Facebook Pixel)", True), ("Google Tag faqat", False), ("AdBlock", False), ("Cookie banner", False)]),
                        ("Retargeting qanday auditoriyaga reklama ko'rsatish hisoblanadi?", [("Avval sizning brendingiz yoki saytingiz bilan aloqa qilgan odamlarga", True), ("Mutlaqo yangi begonalarga", False), ("Faqat chet elliklarga", False), ("Kam yoshdagilarga", False)])
                    ]
                },
                {
                    'title': "Marketing Metriklari: ROAS, CPC, CTR va Tahlil",
                    'lessons': [
                        ("ROAS (Return on Ad Spend) va ROI ni To'g'ri Hisoblash", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Reklamaga sarflangan har bir so'm necha barobar foyda keltirayotganini aniqlash."),
                        ("A/B Testing orqali Eng Samarali Kreativlarni Topish", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Reklama byudjetini behuda yo'qotmaslik texnikasi.")
                    ],
                    'quiz_title': "Yakuniy Bitiruv Imtihoni: Raqamli Marketing",
                    'questions': [
                        ("CTR (Click-Through Rate) nimani ko'rsatadi?", [("Reklamani ko'rganlar orasida unga bosganlarning foizini", True), ("Jami sotuvlar sonini", False), ("Byudjet qoldig'ini", False), ("Kompaniya foydasini", False)]),
                        ("ROAS 400% nimani anglatadi?", [("Reklamaga tikilgan 1 dollarga 4 dollar daromad olinganini", True), ("Zarar 400% ekanini", False), ("Obunachilar sonini", False), ("Reklama narxi 4x oshganini", False)])
                    ]
                }
            ]
        },

        # Ingliz tili / IELTS
        {
            'author_key': 'gulnoza_ielts',
            'title': "IELTS 8.0+ va Professional Ingliz Tili Kursi",
            'category': "Chet Tillari",
            'level': "Barcha darajalar",
            'duration_hours': 30,
            'price': 400000,
            'discount_price': 249000,
            'is_free': False,
            'description': "Xalqaro IELTS imtihonida yuqori 7.5 - 8.5 ball to'plash strategiyalari. Listening, Reading, Writing Task 1 & 2 va Speaking bo'yicha ekspert qo'llanmasi.",
            'modules': [
                {
                    'title': "IELTS Listening va Reading: Yuqori Tezlik va Diqqat",
                    'lessons': [
                        ("Skimming and Scanning: 20 daqiqada matndan javob topish", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "True/False/Not Given va Headings savollarini xatosiz yechish sirlari."),
                        ("Listening: Distractorlarni ajratish va kalit so'zlar", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Audio tezlashganda ham fikrni yo'qotmaslik texnikasi.")
                    ],
                    'quiz_title': "1-Modul: Reading & Listening Imtihoni",
                    'questions': [
                        ("Matnda to'g'ridan-to'g'ri berilmagan, lekin inkor ham qilinmagan fakt nima deb belgilanadi?", [("NOT GIVEN", True), ("FALSE", False), ("TRUE", False), ("UNKNOWN", False)]),
                        ("Skimming texnikasining asosiy vazifasi nima?", [("Matnning umumiy mazmunini tezda tushunish", True), ("Har bir so'zning tarjimasini yodlash", False), ("Grammatikani tekshirish", False), ("Savollarni ko'chirish", False)])
                    ]
                },
                {
                    'title': "IELTS Academic Writing: Task 1 va Task 2 Masterclass",
                    'lessons': [
                        ("Task 1: Grafiklar, Jadvallar va Diagrammalarni Tasvirlash", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Trendlarni ifodalash uchun professional akademik so'z boyligi."),
                        ("Task 2: Insho (Essay) Strukturasi va Dalillash San'ati", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Mavzuga chuqur kirish, paragraflar bog'liqligi va xulosalash.")
                    ],
                    'quiz_title': "2-Modul: Academic Writing Imtihoni",
                    'questions': [
                        ("IELTS Writing Task 2 uchun minimal so'zlar soni qancha bo'lishi shart?", [("250 ta so'z", True), ("150 ta so'z", False), ("300 ta so'z", False), ("200 ta so'z", False)]),
                        ("Task 1 da shaxsiy fikr (opinion) yozish kerakmi?", [("Yo'q, faqat berilgan faktlar ob'ektiv tasvirlanishi shart", True), ("Ha, albatta", False), ("Faqat xulosada", False), ("Ixtiyoriy", False)])
                    ]
                },
                {
                    'title': "IELTS Speaking: Erkin Muloqot, Lug'at va Intonatsiya",
                    'lessons': [
                        ("Speaking Part 1, 2 va 3 dagi Baholash Mezonlari", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Fluency, Lexical Resource, Grammatical Range va Pronunciation."),
                        ("Cue Card bo'yicha 2 daqiqa to'xtovsiz qiziqarli gapirish", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Fikrlarni tizimlashtirish va hayajonni yengish.")
                    ],
                    'quiz_title': "Yakuniy Bitiruv Imtihoni: IELTS 8.0+",
                    'questions': [
                        ("Speaking Part 2 (Cue Card) da tayyorlanish uchun qancha vaqt beriladi?", [("1 daqiqa", True), ("2 daqiqa", False), ("30 soniya", False), ("Vaqt berilmaydi", False)]),
                        ("Quyidagi so'zlardan qaysi biri akademik insholarda ko'proq tavsiya etiladi?", [("Furthermore / Consequently", True), ("Also / But faqat", False), ("Like / You know", False), ("A lot of", False)])
                    ]
                }
            ]
        },

        # Biznes va Moliya
        {
            'author_key': 'temur_finance',
            'title': "Shaxsiy Moliya, Investitsiya va Startap Boshqaruvi",
            'category': "Biznes va Moliya",
            'level': "Boshlang'ich / O'rta",
            'duration_hours': 20,
            'price': 600000,
            'discount_price': 399000,
            'is_free': False,
            'description': "Moliyaviy erkinlikka erishish, aktivlar va passivlar, qimmatli qog'ozlar, ko'chmas mulk, startaplar yaratish va investitsiya jalb qilish qo'llanmasi.",
            'modules': [
                {
                    'title': "Moliyaviy Savodxonlik va Shaxsiy Byudjet",
                    'lessons': [
                        ("50/30/20 Qoidasi: Daromad va Xarajatlarni Boshqarish", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Zaruriy ehtiyojlar, xohishlar va investitsiya jamg'armasi."),
                        ("Inflyatsiya va Pulning Vaqt Qimmati (Time Value of Money)", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Pulni yostiq ostida emas, daromad keltiruvchi aktivlarda saqlash.")
                    ],
                    'quiz_title': "1-Modul: Moliyaviy Savodxonlik Imtihoni",
                    'questions': [
                        ("50/30/20 byudjet qoidasiga ko'ra 20% qayerga ajratilishi kerak?", [("Investitsiyalar va jamg'armaga", True), ("Xarajatlarga", False), ("Ko'ngilxushlikka", False), ("Soliqlarga", False)]),
                        ("Aktiv va Passivning asosiy farqi nima?", [("Aktiv cho'ntakka pul olib keladi, passiv cho'ntakdan pul olib ketadi", True), ("Farqi yo'q", False), ("Aktiv bu faqat uy", False), ("Passiv bu kredit kartasi faqat", False)])
                    ]
                },
                {
                    'title': "Investitsiya Asoslari: Qimmatli Qog'ozlar va Jamg'arma",
                    'lessons': [
                        ("Aksiyalar, Obligatsiyalar va ETF Fondlar", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "S&P 500 va xalqaro indeks fondlariga xavfsiz sarmoya kiritish."),
                        ("Murakkab Foiz (Compound Interest) Mo'jizasi", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Uzoq muddatli investitsiyada kapitalning geometrik progressiyada o'sishi.")
                    ],
                    'quiz_title': "2-Modul: Investitsiya Asoslari Imtihoni",
                    'questions': [
                        ("Diversifikatsiya nima?", [("Xatarlarni kamaytirish uchun mablag'larni turli aktivlarga bo'lib investitsiya qilish", True), ("Barcha pulni bitta aksiyaga tikish", False), ("Kredit olish", False), ("Soliqdan qochish", False)]),
                        ("ETF fondining afzalligi nimada?", [("Bitta qog'oz orqali yuzlab kompaniyalar aksiyasiga ega bo'lish", True), ("Faqat bitta kompaniyaga bog'liqlik", False), ("Kafolatlangan 100% foyda", False), ("Komissiyasiz", False)])
                    ]
                },
                {
                    'title': "Startap Yaratish, Biznes Model va Pitching",
                    'lessons': [
                        ("Business Model Canvas va Bozor Hajmini (TAM/SAM/SOM) Baholash", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "G'oyadan ishlovchi biznes modeliga o'tish bosqichlari."),
                        ("Investorlar Oldida Pitch Deck Taqdimoti va Baholash (Valuation)", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Kompaniya ulushini sotish va venchur investitsiyalar jalb qilish.")
                    ],
                    'quiz_title': "Yakuniy Bitiruv Imtihoni: Biznes va Investitsiya",
                    'questions': [
                        ("Startapning eng minimal ishlovchi mahsuloti qanday qisqartma bilan ataladi?", [("MVP (Minimum Viable Product)", True), ("KPI", False), ("ROI", False), ("SaaS", False)]),
                        ("Venchur kapitali (Venture Capital) qanday loyihalarga sarmoya kiritadi?", [("Yuqori xatarli, ammo juda tez o'suvchi innovatsion startaplarga", True), ("Kichik do'konlarga", False), ("Faqat davlat idoralariga", False), ("Faqat ko'chmas mulkka", False)])
                    ]
                }
            ]
        },

        # Biznes Analitika
        {
            'author_key': 'rustam_bi',
            'title': "Data Analytics: Excel, SQL va PowerBI Dashboardlar",
            'category': "Biznes Analitika",
            'level': "Boshlang'ich / O'rta",
            'duration_hours': 22,
            'price': 550000,
            'discount_price': 380000,
            'is_free': False,
            'description': "Katta hajmdagi ma'lumotlarni tahlil qilib, biznes uchun to'g'ri strategik qarorlar ishlab chiqish. Ilg'or Excel, PowerBI interaktiv hisobotlari va SQL analitika.",
            'modules': [
                {
                    'title': "Ilg'or Excel va Pivot Tables (Yig'ma Jadvallar)",
                    'lessons': [
                        ("XLOOKUP, INDEX/MATCH va Murakkab Mantiqiy Formulalar", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Katta jadvallardagi ma'lumotlarni bir zumda solishtirish va topish."),
                        ("Pivot Tables va Dinamik Slicerlar orqali Tezkor Hisobot", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Kompaniya oylik va yillik tushumlarini tezkor umumlashtirish.")
                    ],
                    'quiz_title': "1-Modul: Excel Analitika Imtihoni",
                    'questions': [
                        ("VLOOKUP o'rniga kelgan zamonaviy va moslashuvchan qidiruv funksiyasi qaysi?", [("XLOOKUP", True), ("SEARCH", False), ("FIND", False), ("HLOOKUP", False)]),
                        ("Pivot Table-da sanalar bo'yicha guruhlash nima beradi?", [("Oylar, choraklar va yillar bo'yicha dinamikani ko'rish", True), ("Ranglarni o'zgartirish", False), ("Faylni shifrlash", False), ("Shunchaki tartiblash", False)])
                    ]
                },
                {
                    'title': "PowerBI: Ma'lumotlarni Bog'lash va DAX Formulalari",
                    'lessons': [
                        ("Power Query orqali Turli Manbalardan Ma'lumot Yuklash (ETL)", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Excel, CSV va SQL bazalarini yagona modelga birlashtirish."),
                        ("DAX (Data Analysis Expressions): CALCULATE, RELATED va O'lchovlar", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Murakkab biznes metrikalarini avtomatik hisoblovchi formulalar.")
                    ],
                    'quiz_title': "2-Modul: PowerBI va DAX Imtihoni",
                    'questions': [
                        ("PowerBI-da eng ko'p ishlatiluvchi va filtr kontekstini o'zgartiruvchi asosiy DAX funksiyasi qaysi?", [("CALCULATE", True), ("SUM", False), ("COUNT", False), ("AVERAGE", False)]),
                        ("Power Query vositasi nima vazifani bajaradi?", [("Ma'lumotlarni tozalash, transformatsiya qilish va yuklash (ETL)", True), ("Grafik chizish faqat", False), ("Prezentatsiya tayyorlash", False), ("Kino ko'rish", False)])
                    ]
                },
                {
                    'title': "Interaktiv Dashboard Dizayni va Biznes Qarorlar",
                    'lessons': [
                        ("Executive Dashboard Yaratish: KPI ko'rsatkichlari va Diagrammalar", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Direktorlar va rahbarlar uchun qulay yagona boshqaruv ekrani."),
                        ("Data Storytelling: Raqamlar ortidagi haqiqatni taqdimot qilish", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Analitik xulosalarni jamoaga va mijozga tushunarli yetkazish.")
                    ],
                    'quiz_title': "Yakuniy Bitiruv Imtihoni: Data Analytics",
                    'questions': [
                        ("Kompaniyaning asosiy faoliyat samaradorligi ko'rsatkichlari nima deyiladi?", [("KPI (Key Performance Indicators)", True), ("API", False), ("SDK", False), ("CPU", False)]),
                        ("Dashboard dizaynida eng muhim prinsip qaysi?", [("Ortiqcha vizual shovqinsiz, asosiy biznes metrikalarni aniq ko'rsatish", True), ("Imkon qadar ko'p ranglar ishlatish", False), ("Hamma ma'lumotni bitta sahifaga tiqish", False), ("Faqat chiroyli rasm qo'yish", False)])
                    ]
                }
            ]
        }
    ]

    # Mavjud IT kurslariga ham narx va chegirmalarni belgilash
    existing_courses = Course.objects.all()
    for c in existing_courses:
        if 'Python' in c.title:
            c.price = 600000
            c.discount_price = 399000
            c.is_free = False
        elif 'Frontend' in c.title or 'React' in c.title:
            c.price = 550000
            c.discount_price = 350000
            c.is_free = False
        elif 'DevOps' in c.title:
            c.price = 700000
            c.discount_price = 490000
            c.is_free = False
        elif 'Kiberxavfsizlik' in c.title or 'Ethical' in c.title:
            c.price = 650000
            c.discount_price = 420000
            c.is_free = False
        elif 'Sun\'iy Intellekt' in c.title or 'Machine Learning' in c.title:
            c.price = 750000
            c.discount_price = 499000
            c.is_free = False
        elif 'Flutter' in c.title:
            c.price = 500000
            c.discount_price = 320000
            c.is_free = False
        elif 'Ma\'lumotlar Bazasi' in c.title or 'SQL' in c.title:
            # Ushbu kursni bepul qilish (Grant / Demo sifatida)
            c.price = 0
            c.discount_price = 0
            c.is_free = True
        c.save()

    total_new_courses = 0
    total_new_lessons = 0

    for c_data in multi_courses:
        author = teacher_objects[c_data['author_key']]
        course, _ = Course.objects.get_or_create(
            title=c_data['title'],
            defaults={
                'author': author,
                'category': c_data['category'],
                'level': c_data['level'],
                'duration_hours': c_data['duration_hours'],
                'price': c_data['price'],
                'discount_price': c_data['discount_price'],
                'is_free': c_data['is_free'],
                'description': c_data['description'],
            }
        )
        course.author = author
        course.category = c_data['category']
        course.level = c_data['level']
        course.duration_hours = c_data['duration_hours']
        course.price = c_data['price']
        course.discount_price = c_data['discount_price']
        course.is_free = c_data['is_free']
        course.description = c_data['description']
        course.save()

        total_new_courses += 1

        for m_idx, m_info in enumerate(c_data['modules'], start=1):
            module, _ = Module.objects.get_or_create(
                course=course,
                order=m_idx,
                defaults={'title': m_info['title']}
            )
            module.title = m_info['title']
            module.save()

            for l_idx, l_tuple in enumerate(m_info['lessons'], start=1):
                les_title, les_video, les_content = l_tuple
                lesson, _ = Lesson.objects.get_or_create(
                    module=module,
                    order=l_idx,
                    defaults={
                        'title': les_title,
                        'video_url': les_video,
                        'content': f"# 📌 {les_title}\n\n{les_content}\n\n### Amaliy Tavsiya:\nMavzuni to'liq o'rganib bo'lgach, 'Darsni tugatdim (+15 XP)' tugmasini bosing va o'z bilimingizni mustahkamlang!"
                    }
                )
                total_new_lessons += 1

            quiz, _ = Quiz.objects.get_or_create(
                module=module,
                defaults={
                    'title': m_info['quiz_title'],
                    'passing_score': 70,
                    'duration_minutes': 10
                }
            )
            quiz.title = m_info['quiz_title']
            quiz.save()

            for q_text, choices_list in m_info['questions']:
                q_obj, _ = Question.objects.get_or_create(quiz=quiz, text=q_text)
                for ch_text, is_corr in choices_list:
                    Choice.objects.get_or_create(question=q_obj, text=ch_text, defaults={'is_correct': is_corr})

    print(f"✅ {total_new_courses} ta yangi soha kurslari va {total_new_lessons} ta darslar yaratildi.")

    # Talaba 'talaba' uchun test xarid (Enrollment) yaratish:
    student_talaba = User.objects.get(username='talaba')
    sample_course = Course.objects.filter(is_free=False).first()
    if sample_course:
        Enrollment.objects.get_or_create(
            user=student_talaba,
            course=sample_course,
            defaults={
                'amount_paid': sample_course.get_effective_price(),
                'payment_method': 'click',
                'transaction_id': Enrollment.generate_transaction_id(student_talaba.id, sample_course.id),
                'status': 'completed'
            }
        )

    print("✨ Yangi sohalar, to'lov tizimi va promokodlar to'liq va muvaffaqiyatli saqlandi!")


if __name__ == '__main__':
    seed_multidisciplinary()
