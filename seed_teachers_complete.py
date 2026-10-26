import os
import sys
import django

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import User, Course, Room, StudyGroup, TeacherReview, TeacherSalary

def seed_teachers():
    print("=== 1. Rooms Setup ===")
    rooms_data = [
        ("101-xona (Frontend & IT Lab)", 20),
        ("102-xona (IELTS & Til Markazi)", 22),
        ("103-xona (Backend & AI Laboratoriyasi)", 18),
        ("201-xona (Matematika & Milliy Sertifikat)", 25),
        ("202-xona (Sharq Tillari Hub - Koreys & Xitoy)", 18),
        ("203-xona (Raqamli Dizayn & SMM Studiyasi)", 16),
        ("205-xona (Bolalar Savodxonligi & Mental Arifmetika)", 20),
        ("Sport Majmuasi (Shaxmat, Futbol & Ping-Pong)", 30),
    ]
    created_rooms = {}
    for r_name, cap in rooms_data:
        room, _ = Room.objects.get_or_create(name=r_name, defaults={'capacity': cap})
        created_rooms[r_name] = room
    print(f"Total rooms verified: {len(created_rooms)}")

    # Curated 25 100% UNIQUE Unsplash high-resolution portrait headshots of educators
    # Each photo ID is completely distinct!
    TEACHERS_CONFIG = [
        {
            "username": "ustoz_anvar",
            "first_name": "Anvar",
            "last_name": "Qodirov",
            "headline": "Senior Python & Backend Architect",
            "specialties": "it",
            "photo_id": "photo-1507003211169-0a1dd7228f2d",
            "monthly_salary": 14500000,
            "experience_years": 8,
            "students_count": 240,
            "exam_results_summary": "45+ shogirdi xalqaro IT kompaniyalarda Middle/Senior dasturchi",
            "bio": "8 yillik dasturlash va arxitektura tajribasiga ega. EPAM va Yandex loyihalarida ishtirok etgan. O'quvchilarga backend arxitektura, toza kod va algoritmlarni chuqur o'rgatadi.",
            "course_ids": [1, 2],
            "group_name": "Python Backend Bootcamp (Guruh A-1)",
            "room": "103-xona (Backend & AI Laboratoriyasi)",
            "days": "odd",
            "time": ("14:00", "16:00"),
            "reviews": [
                ("Dilnoza Olimova (Ona)", "Ota-ona", 5, "Ustozning tushuntirish uslubi juda oson va aniq. O'g'lim 3 oyda mustaqil sayt yarata oldi!", "Junior Backend dasturchi bo'ldi"),
                ("Javohirbek Ergashov", "Talaba", 5, "Amaliy loyihalar va Django bo'yicha eng zo'r kurs. Hozirda IT kompaniyada amaliyotdaman.", "EPAM tanlovidan o'tdi")
            ]
        },
        {
            "username": "malika_frontend",
            "first_name": "Malika",
            "last_name": "Rustamova",
            "headline": "Senior Frontend & React.js Team Lead",
            "specialties": "it",
            "photo_id": "photo-1573496359142-b8d87734a5a2",
            "monthly_salary": 13500000,
            "experience_years": 6,
            "students_count": 190,
            "exam_results_summary": "Bitiruvchilarning 92% qismi zamonaviy React & Next.js loyihalarini muvaffaqiyatli topshirgan",
            "bio": "Zamonaviy SPA web ilovalar, TypeScript, React hamda TailwindCSS mutaxassisi. Xalqaro fintex startaplarida yetakchi frontend dasturchi bo'lib faoliyat yuritgan.",
            "course_ids": [3, 17],
            "group_name": "React & Next.js Pro (Guruh F-1)",
            "room": "101-xona (Frontend & IT Lab)",
            "days": "even",
            "time": ("16:30", "18:30"),
            "reviews": [
                ("Sardorbek Rahmonov", "Talaba", 5, "React va Reduxni bunchalik qiziqarli va sodda o'rganaman deb o'ylamagandim. Katta rahmat!", "Next.js portfolioga ega bo'ldi"),
                ("Gulchehra opa (Ona)", "Ota-ona", 5, "Qizim frontend darslariga juda qiziqish bilan bormoqda, ustoz juda e'tiborli.", "Xalqaro hakaton sovrindori")
            ]
        },
        {
            "username": "bobur_ai",
            "first_name": "Bobur",
            "last_name": "Mirzayev",
            "headline": "AI & Machine Learning Research Scientist",
            "specialties": "it",
            "photo_id": "photo-1500648767791-00dcc994a43e",
            "monthly_salary": 15000000,
            "experience_years": 9,
            "students_count": 160,
            "exam_results_summary": "Shogirdlari Kaggle musobaqalarida Top-5% natija qayd etgan",
            "bio": "Sun'iy intellekt, neyron tarmoqlar (PyTorch, TensorFlow) va Computer Vision sohasida 9 yillik ilmiy va amaliy tajriba sohibi. Germaniya va Janubiy Koreya laboratoriyalari bilan hamkorlik qiladi.",
            "course_ids": [4],
            "group_name": "Sun'iy Intellekt & Data Science Lab",
            "room": "103-xona (Backend & AI Laboratoriyasi)",
            "days": "odd",
            "time": ("18:30", "20:30"),
            "reviews": [
                ("Farrux Murodov", "Talaba", 5, "AI modellarini noldan o'rganish uchun O'zbekistondagi eng kuchli amaliy kurs!", "Kaggle Bronze Medal"),
                ("Shahzod Aliyev", "Talaba", 5, "Ustoz murakkab matematik tushunchalarni vizual va qiziqarli qilib tushuntiradilar.", "AI muhandisi bo'lib ishga kirdi")
            ]
        },
        {
            "username": "jamshid_devops",
            "first_name": "Jamshid",
            "last_name": "Alimov",
            "headline": "Lead DevOps & Cloud Engineer (AWS Certified)",
            "specialties": "it",
            "photo_id": "photo-1519085360753-af0119f7cbe7",
            "monthly_salary": 14000000,
            "experience_years": 7,
            "students_count": 130,
            "exam_results_summary": "30+ o'quvchisi AWS va Docker xalqaro sertifikatlarini olgan",
            "bio": "CI/CD avtomatizatsiyasi, Kubernetes, Terraform va bulutli infratuzilma bo'yicha mutaxassis. Xalqaro telekom va bank tizimlarining infratuzilmasini boshqargan.",
            "course_ids": [5],
            "group_name": "DevOps & Cloud Production",
            "room": "103-xona (Backend & AI Laboratoriyasi)",
            "days": "even",
            "time": ("18:30", "20:30"),
            "reviews": [
                ("Oybek To'laganov", "Talaba", 5, "Serverlarni boshqarish va Docker bo'yicha olgan bilimlarim oylik daromadimni 2 barobar oshirdi.", "AWS Certified Solutions Architect"),
                ("Rustamjon Nurmatov", "Talaba", 5, "Nazariyadan ko'ra 90% amaliyotga urg'u berilishi darslarni juda samarali qiladi.", "DevOps Engineer lavozimiga o'tdi")
            ]
        },
        {
            "username": "nigora_cyber",
            "first_name": "Nigora",
            "last_name": "Karimova",
            "headline": "Cybersecurity & Ethical Hacking Specialist",
            "specialties": "it",
            "photo_id": "photo-1580489944761-15a19d654956",
            "monthly_salary": 13000000,
            "experience_years": 6,
            "students_count": 110,
            "exam_results_summary": "O'quvchilari Markaziy Osiyo kiberxavfsizlik CTF musobaqalarida 1-o'rinni egallagan",
            "bio": "Penetration testing, tarmoq xavfsizligi, OWASP Top 10 va zaifliklarni aniqlash bo'yicha yetakchi ekspert. Shogirdlariga axloqiy xakerlik va kiberhimoya asoslarini o'rgatadi.",
            "course_ids": [6],
            "group_name": "Cyber Defense & Ethical Hacking",
            "room": "101-xona (Frontend & IT Lab)",
            "days": "odd",
            "time": ("16:30", "18:30"),
            "reviews": [
                ("Kamron Shokirov", "Talaba", 5, "Ustoz Nigora juda chuqur bilimga ega. CTF lablarida ishlash juda qiziqarli!", "CTF Hackathon g'olibi"),
                ("Shahnoza opa (Ona)", "Ota-ona", 5, "O'g'lim kiberxavfsizlikka qiziqib, kompyuterda vaqtini endi faqat foydali ishga sarflayapti.", "Kiberxavfsizlik stipendiyasi sohibi")
            ]
        },
        {
            "username": "sardor_mobile",
            "first_name": "Sardor",
            "last_name": "Toshmatov",
            "headline": "Senior Flutter & Mobile App Architect",
            "specialties": "it",
            "photo_id": "photo-1472099645785-5658abf4ff4e",
            "monthly_salary": 12500000,
            "experience_years": 5,
            "students_count": 145,
            "exam_results_summary": "Google Play va App Store'da o'quvchilarining 35+ ta ilovasi faol ishlamoqda",
            "bio": "Dart & Flutter orqali krossplatformali mobil ilovalar ishlab chiqish ustasi. 20 dan ortiq tijoriy ilovalar muallifi.",
            "course_ids": [7],
            "group_name": "Flutter Mobile Master (iOS & Android)",
            "room": "101-xona (Frontend & IT Lab)",
            "days": "even",
            "time": ("14:00", "16:00"),
            "reviews": [
                ("Diyorbek Zohidov", "Talaba", 5, "Kurs davomida o'zimning dastlabki e-tijorat ilovamni App Store'ga chiqardim!", "App Store'da ilovasi nashr etildi"),
                ("Olim aka (Ota)", "Ota-ona", 5, "O'qituvchining har bir talaba bilan individual shug'ullanishi tahsinga loyiq.", "Mobil startap asoschisi")
            ]
        },
        {
            "username": "dilshod_db",
            "first_name": "Dilshodbek",
            "last_name": "Yusupov",
            "headline": "Database Architect & Highload SQL Expert",
            "specialties": "it",
            "photo_id": "photo-1506794778202-cad84cf45f1d",
            "monthly_salary": 12000000,
            "experience_years": 8,
            "students_count": 125,
            "exam_results_summary": "100+ o'quvchisi PostgreSQL va Oracle DBA sertifikatlariga ega",
            "bio": "Katta hajmli ma'lumotlar bazalari, replikatsiya, indekslash va so'rovlarni optimallashtirish bo'yicha tajribali mutaxassis.",
            "course_ids": [8],
            "group_name": "PostgreSQL & Database Optimization",
            "room": "103-xona (Backend & AI Laboratoriyasi)",
            "days": "weekend",
            "time": ("10:00", "13:00"),
            "reviews": [
                ("Jasurbek Qosimov", "Talaba", 5, "SQL so'rovlarini optimallashtirish bo'yicha bu kurs haqiqiy kashfiyot bo'ldi.", "Katta bankda DBA mutaxassisi"),
                ("Nodir Mahmudov", "Talaba", 5, "Murakkab indekslar va partitioningni juda oson tushuntirib berdilar.", "PostgreSQL Certified")
            ]
        },
        {
            "username": "kamola_design",
            "first_name": "Kamola",
            "last_name": "Karimova",
            "headline": "Lead UI/UX Designer & Product Specialist",
            "specialties": "it",
            "photo_id": "photo-1544005313-94ddf0286df2",
            "monthly_salary": 11500000,
            "experience_years": 6,
            "students_count": 210,
            "exam_results_summary": "O'quvchilarining Behance va Dribbble portfoliolari xalqaro darajada e'tirof etilgan",
            "bio": "Figma, Design Systems, UX Research va foydalanuvchi psixologiyasi bo'yicha ekspert. 50 dan ortiq veb va mobil mahsulotlar dizayni muallifi.",
            "course_ids": [9],
            "group_name": "UI/UX & Figma Product Design Pro",
            "room": "203-xona (Raqamli Dizayn & SMM Studiyasi)",
            "days": "odd",
            "time": ("14:00", "16:00"),
            "reviews": [
                ("Madinaxon Jo'rayeva", "Talaba", 5, "Kamola ustoz nafaqat Figma, balki dizaynerlik fikrlashini ham mukammal shakllantirdilar.", "Dribbble Trending dizayneri"),
                ("Mohira opa (Ona)", "Ota-ona", 5, "Qizim kursni bitirib, xalqaro frilans platformalarda buyurtmalar ola boshladi.", "Upwork Top Rated dizayner")
            ]
        },
        {
            "username": "otabek_smm",
            "first_name": "Otabek",
            "last_name": "Zokirov",
            "headline": "Digital Marketing & Growth Target Strategist",
            "specialties": "it",
            "photo_id": "photo-1560250097-0b93528c311a",
            "monthly_salary": 10500000,
            "experience_years": 6,
            "students_count": 280,
            "exam_results_summary": "O'quvchilari boshqarayotgan brendlarning oylik savdosi o'rtacha 350% ga o'sgan",
            "bio": "Meta Ads, Google Marketing, TikTok strategiyasi va savdo voronkalari (funnel) arxitektori. Katta brendlar uchun $1M+ byudjetlarni samarali boshqargan.",
            "course_ids": [10],
            "group_name": "Targeting & SMM Growth Master",
            "room": "203-xona (Raqamli Dizayn & SMM Studiyasi)",
            "days": "even",
            "time": ("16:30", "18:30"),
            "reviews": [
                ("Shuhrat Beknazarov", "Talaba", 5, "Kursda o'rgangan bilimlarim orqali shaxsiy biznesim savdosi 4 barobar oshdi!", "ROI 420% natija"),
                ("Mansur aka (Ota)", "Ota-ona", 5, "O'g'lim hozirda bir nechta kompaniyalarga marketing xizmati ko'rsatmoqda.", "Target agentligi rahbari")
            ]
        },
        {
            "username": "gulnoza_ielts",
            "first_name": "Gulnoza",
            "last_name": "Saidova",
            "headline": "IELTS 8.5 Master Instructor & British Council Alumna",
            "specialties": "languages",
            "photo_id": "photo-1573497019940-1c28c88b4f3e",
            "monthly_salary": 13000000,
            "experience_years": 10,
            "students_count": 350,
            "exam_results_summary": "O'quvchilarining 96% qismi IELTS 7.5+ va 8.0 natijalarini qo'lga kiritgan",
            "bio": "10 yillik tajribaga ega xalqaro toifadagi til o'qituvchisi. Writing va Speaking qismlarida kafolatlangan balga chiqarish metodikasi muallifi.",
            "course_ids": [11, 20],
            "group_name": "IELTS 8.0+ Target Intensive (Guruh I-1)",
            "room": "102-xona (IELTS & Til Markazi)",
            "days": "odd",
            "time": ("09:00", "11:00"),
            "reviews": [
                ("Sarvarbek Toshpulatov", "Talaba", 5, "Gulnoza ustozning Writing strategiyalari tufayli 1-urinishda IELTS 8.0 oldim!", "IELTS 8.0 natija"),
                ("Dildora opa (Ona)", "Ota-ona", 5, "Farzandim Buyuk Britaniya universitetiga 100% grant yutib oldi, ustozga cheksiz minnatdorchilik!", "Buyuk Britaniya granti sohibi")
            ]
        },
        {
            "username": "temur_finance",
            "first_name": "Temur",
            "last_name": "Fayziyev",
            "headline": "Moliyaviy Savodxonlik & CFA Charterholder",
            "specialties": "it",
            "photo_id": "photo-1534528741775-53994a69daeb",
            "monthly_salary": 11000000,
            "experience_years": 7,
            "students_count": 180,
            "exam_results_summary": "80+ o'quvchisi shaxsiy investitsiya portfellarini shakllantirib, moliyaviy mustaqillikka erishgan",
            "bio": "Investitsiyalar, aksiyalar bozori, shaxsiy byudjetni boshqarish va startap moliyaviy tahlili bo'yicha professional maslahatchi.",
            "course_ids": [12],
            "group_name": "Shaxsiy Moliya & Investitsiya Akademiyasi",
            "room": "201-xona (Matematika & Milliy Sertifikat)",
            "days": "weekend",
            "time": ("14:00", "17:00"),
            "reviews": [
                ("Botir Mirzayev", "Talaba", 5, "Moliyaviy savodxonlik har bir inson uchun suv va havodek zarurligini bu kursda angladim.", "Investitsiya portfeli egasi"),
                ("Ra'no opa (Ona)", "Ota-ona", 5, "Farzandim pulni qayerga sarflash va qanday tejashni mukammal o'rgandi.", "Moliya bo'yicha grant sohibi")
            ]
        },
        {
            "username": "rustam_bi",
            "first_name": "Rustam",
            "last_name": "Nazarov",
            "headline": "Lead Business Intelligence & Power BI Architect",
            "specialties": "it",
            "photo_id": "photo-1522075469751-3a6694fb2f61",
            "monthly_salary": 12000000,
            "experience_years": 8,
            "students_count": 170,
            "exam_results_summary": "Bitiruvchilarining 88% qismi yirik korxonalarda BI tahlilchi sifatida ish boshlagan",
            "bio": "Katta korxonalar uchun Power BI, DAX, Excel Power Query va Tableau orqali interaktiv analitik dashboardlar yaratish bo'yicha yetakchi ekspert.",
            "course_ids": [13],
            "group_name": "Power BI & Big Data Dashboarding",
            "room": "101-xona (Frontend & IT Lab)",
            "days": "even",
            "time": ("18:30", "20:30"),
            "reviews": [
                ("Alisher Qodirov", "Talaba", 5, "DAX formulalari va murakkab hisobotlarni juda sodda va tushunarli tushuntiradilar.", "Yirik kompaniyada BI Analyst"),
                ("Muzaffar aka (Ota)", "Ota-ona", 5, "O'g'lim xalqaro sertifikat olib, o'z sohasida nufuzli kompaniyaga kirdi.", "Microsoft Certified Data Analyst")
            ]
        },
        {
            "username": "alisher_backend",
            "first_name": "Alisher",
            "last_name": "Rustamov",
            "headline": "Head of Engineering & Algoritmik Mantiq Ustozi",
            "specialties": "it",
            "photo_id": "photo-1492562080023-ab3db95bfbce",
            "monthly_salary": 14000000,
            "experience_years": 11,
            "students_count": 310,
            "exam_results_summary": "O'quvchilari LeetCode'da 400+ masalani yechgan va xalqaro intervyulardan o'tgan",
            "bio": "Dasturlash asoslari, ma'lumotlar tuzilmalari va murakkab algoritmlarni yoshlarga interaktiv o'rgatish bo'yicha 11 yillik tajribali ustoz.",
            "course_ids": [15, 16],
            "group_name": "Algoritmlar va Mantiqiy Fikrlash (Guruh D-1)",
            "room": "103-xona (Backend & AI Laboratoriyasi)",
            "days": "odd",
            "time": ("09:00", "11:00"),
            "reviews": [
                ("Bekzod Usmonov", "Talaba", 5, "Algoritmlar fanini zerikarli deb o'ylardim, Alisher ustoz uni eng sevimli fanimga aylantirdi!", "LeetCode 500+ yechim"),
                ("Sohiba opa (Ona)", "Ota-ona", 5, "O'g'limning matematika va dasturlashga qiziqishi keskin oshdi.", "Respublika IT olimpiada 2-o'rin")
            ]
        },
        {
            "username": "azizbek_fullstack",
            "first_name": "Azizbek",
            "last_name": "Qodirov",
            "headline": "Fullstack Web & Cloud Native Developer",
            "specialties": "it",
            "photo_id": "photo-1539571696357-5a69c17a67c6",
            "monthly_salary": 13000000,
            "experience_years": 6,
            "students_count": 220,
            "exam_results_summary": "O'quvchilarining 50+ to'liq amaliy web-loyihalari ishlab chiqarishga chiqarilgan",
            "bio": "Django REST API va React/Next.js stekida to'liq veb platformalar qurish mutaxassisi. Frilans va startap jamoalari kuratori.",
            "course_ids": [17],
            "group_name": "Fullstack Web Development Intensive",
            "room": "101-xona (Frontend & IT Lab)",
            "days": "even",
            "time": ("09:00", "11:00"),
            "reviews": [
                ("Sanjarbek Shodiyev", "Talaba", 5, "Frontend va Backendni bir vaqtda mukammal bog'lashni o'rgandim.", "Middle Fullstack Developer"),
                ("Karim aka (Ota)", "Ota-ona", 5, "O'g'lim birinchi oyidayoq o'z mustaqil loyihasini taqdimot qildi.", "Zamonaviy IT startap yaratdi")
            ]
        },
        {
            "username": "malika_english",
            "first_name": "Malika",
            "last_name": "Rahimova",
            "headline": "General English & CEFR C1 Lead Trainer",
            "specialties": "languages",
            "photo_id": "photo-1517841905240-472988babdf9",
            "monthly_salary": 11000000,
            "experience_years": 7,
            "students_count": 320,
            "exam_results_summary": "94% o'quvchilari CEFR B2/C1 davlat imtihonini 1-urinishda a'lo topshirgan",
            "bio": "Kembrij CELTA sertifikatiga ega xalqaro murabbiy. Jonli muloqot, interaktiv o'yinlar va zamonaviy podkastlar orqali til o'rgatadi.",
            "course_ids": [18, 19],
            "group_name": "CEFR B2/C1 Davlat Imtihoni Tayyorgarligi",
            "room": "102-xona (IELTS & Til Markazi)",
            "days": "odd",
            "time": ("14:00", "16:00"),
            "reviews": [
                ("Zilola Qurbonova", "Talaba", 5, "CEFR C1 sertifikatini Malika ustoz yordamida 86 ball bilan oldim!", "CEFR C1 Davlat Sertifikati"),
                ("Mavjuda opa (Ona)", "Ota-ona", 5, "Qizim ingliz tilida erkin va ravon so'zlashmoqda. Rahmat sizga!", "Maktab olimpiada g'olibi")
            ]
        },
        {
            "username": "jasur_oriental",
            "first_name": "Jasur",
            "last_name": "Beknazarov",
            "headline": "Koreys Tili (TOPIK 6) & Xitoy Tili (HSK 5) Poligloti",
            "specialties": "languages",
            "photo_id": "photo-1501196354995-cbb51c65aaea",
            "monthly_salary": 12500000,
            "experience_years": 9,
            "students_count": 290,
            "exam_results_summary": "60+ shogirdi Janubiy Koreya (GKS) va Xitoy (CSC) hukumat grantlariga ega",
            "bio": "Seul Milliy Universiteti magistri. Koreys, xitoy va turk tillarini chuqur metodika va jonli madaniy kontekst orqali o'rgatadi.",
            "course_ids": [21, 23, 24],
            "group_name": "Koreys Tili TOPIK Intensive & So'zlashuv",
            "room": "202-xona (Sharq Tillari Hub - Koreys & Xitoy)",
            "days": "even",
            "time": ("14:00", "16:00"),
            "reviews": [
                ("Azizbek Norqulov", "Talaba", 5, "Jasur ustoz bilan 6 oyda TOPIK 4 darajaga yetdim va Koreyaga grant yutdim!", "GKS Koreya Granti sohibi"),
                ("Jamila opa (Ona)", "Ota-ona", 5, "Sharq tillarini o'rganish juda oson ekanligini isbotlab berdilar.", "Xitoy HSK 4 sertifikati")
            ]
        },
        {
            "username": "nilufar_russian",
            "first_name": "Nilufar",
            "last_name": "Karimova",
            "headline": "Rus Tili Filologiyasi & Erkin Muloqot Murabbiyi",
            "specialties": "languages",
            "photo_id": "photo-1524504388940-b1c1722653e1",
            "monthly_salary": 9500000,
            "experience_years": 8,
            "students_count": 260,
            "exam_results_summary": "O'quvchilarining 98% qismi 3 oy ichida rus tilidagi turg'un to'siqni (aksentni) yengib o'tgan",
            "bio": "Moskva Davlat Lingvistika Universiteti bitiruvchisi. Jonli muloqot, grammatik to'g'ri so'zlashuv va biznes rus tili ustasi.",
            "course_ids": [14, 22],
            "group_name": "Rus Tili: Erkin Muloqot & Nutq Madaniyati",
            "room": "102-xona (IELTS & Til Markazi)",
            "days": "even",
            "time": ("16:30", "18:30"),
            "reviews": [
                ("Shahrizoda Karimova", "Talaba", 5, "Rus tilida gapirishdan qo'rqardim, hozir bemalol taqdimotlar qilyapman.", "Erkin muloqot darajasi"),
                ("Olim aka (Ota)", "Ota-ona", 5, "Farzandlarim uchun ajoyib samara berdi, oilamiz nomidan minnatdormiz.", "Rus tili olimpiada sovrindori")
            ]
        },
        {
            "username": "otabek_math",
            "first_name": "Otabek",
            "last_name": "Xoliqov",
            "headline": "Oliy Toifali Matematik & DTM/Olimpiada Eksperti",
            "specialties": "school",
            "photo_id": "photo-1537368910025-700350fe46c7",
            "monthly_salary": 9000000,
            "experience_years": 12,
            "students_count": 340,
            "exam_results_summary": "O'quvchilarining 100% qismi DTM Matematika blokidan 30/30 maksimal ball to'plagan",
            "bio": "O'zbekiston Milliy Universiteti bitiruvchisi. Murakkab mantiqiy masalalarni 30 soniyada oson yechish bo'yicha maxsus mualliflik formulalari egasi.",
            "course_ids": [27],
            "group_name": "Matematika & Mantiq (DTM 30/30 & Olimpiada)",
            "room": "201-xona (Matematika & Milliy Sertifikat)",
            "days": "odd",
            "time": ("16:30", "18:30"),
            "reviews": [
                ("Mirjalol Yoqubov", "Talaba", 5, "Otabek ustozning uslubi bilan DTM imtihonida matematikadan 30/30 to'pladim!", "DTM 30/30 Maksimal Natija"),
                ("Zulayho opa (Ona)", "Ota-ona", 5, "O'g'lim Toshkent Axborot Texnologiyalari Universitetiga byudjetga kirdi!", "Davlat granti talabasi")
            ]
        },
        {
            "username": "sardor_chess",
            "first_name": "Sardor",
            "last_name": "Olimov",
            "headline": "Xalqaro Shaxmat Grossmeysteri (FIDE Trainer)",
            "specialties": "sport_arts",
            "photo_id": "photo-1544717305-2782549b5136",
            "monthly_salary": 8500000,
            "experience_years": 11,
            "students_count": 180,
            "exam_results_summary": "15+ nafar shogirdi shahar va respublika shaxmat chempioni unvoniga ega",
            "bio": "Strategik fikrlash, kombinatsion tahlil va musobaqalarga ruhiy tayyorgarlik bo'yicha nufuzli murabbiy.",
            "course_ids": [28],
            "group_name": "Shaxmat & Shashka Strategik Chempionlar To'garagi",
            "room": "Sport Majmuasi (Shaxmat, Futbol & Ping-Pong)",
            "days": "weekend",
            "time": ("10:00", "13:00"),
            "reviews": [
                ("Samandar Alimov", "Talaba", 5, "Ustoz Sardor bilan shaxmat bo'yicha 1-razryad oldim va shahar chempioni bo'ldim!", "Shahar chempioni (FIDE 1850)"),
                ("Qodir aka (Ota)", "Ota-ona", 5, "Farzandimning diqqati va mantiqiy fikrlashi shaxmat tufayli juda o'sdi.", "Respublika turniri sovrindori")
            ]
        },
        {
            "username": "gulnoza_philology",
            "first_name": "Gulnoza",
            "last_name": "Yoqubova",
            "headline": "Ona Tili va Adabiyot (Milliy Sertifikat A+ Mutaxassisi)",
            "specialties": "school",
            "photo_id": "photo-1531746020798-e6953c6e8e04",
            "monthly_salary": 8500000,
            "experience_years": 13,
            "students_count": 310,
            "exam_results_summary": "85 nafar o'quvchisi Milliy Sertifikat A+ (90+ ball) sohibi bo'lgan",
            "bio": "Filologiya fanlari nomzodi. Imlo madaniyati, badiiy tahlil va matn ustida ishlash bo'yicha davlat darsliklari mualliflaridan biri.",
            "course_ids": [25, 26],
            "group_name": "Ona Tili & Adabiyot Milliy Sertifikat A+",
            "room": "201-xona (Matematika & Milliy Sertifikat)",
            "days": "even",
            "time": ("14:00", "16:00"),
            "reviews": [
                ("Kumushbibi Rustamova", "Talaba", 5, "Ona tilidan Milliy Sertifikat imtihonida 94 ball bilan A+ darajaga erishdim!", "Milliy Sertifikat A+ (94 ball)"),
                ("Shamsiya opa (Ona)", "Ota-ona", 5, "Gulnoza opaning darslari orqali qizim adabiyotni chin dildan sevib o'qiyapti.", "O'zMU filologiya granti")
            ]
        },
        {
            "username": "farrux_football",
            "first_name": "Farrux",
            "last_name": "Zohidov",
            "headline": "UEFA 'B' Litsenziyali Futbol Murabbiyi",
            "specialties": "sport_arts",
            "photo_id": "photo-1568602471122-7832951cc4c5",
            "monthly_salary": 7500000,
            "experience_years": 10,
            "students_count": 150,
            "exam_results_summary": "Tarbiyalanuvchilari shahar o'smirlar futbol ligasida 1-o'rinni egallagan",
            "bio": "Zamonaviy futbol taktikasi, jismoniy chidamlilik va jamoaviy ruhni tarbiyalash bo'yicha tajribali murabbiy.",
            "course_ids": [29],
            "group_name": "Yakshanba Futbol Ligasi & Taktik Mashg'ulotlar",
            "room": "Sport Majmuasi (Shaxmat, Futbol & Ping-Pong)",
            "days": "weekend",
            "time": ("15:00", "18:00"),
            "reviews": [
                ("Ilhom aka (Ota)", "Ota-ona", 5, "O'g'lim har hafta yakshanba futbolini intiqib kutadi, intizomi juda yaxshilandi.", "O'smirlar ligasi eng yaxshi to'purari"),
                ("Shavkatbek Murodov", "Talaba", 5, "Taktik darslar va real o'yinlar orqali futbolni professional darajada tushuna boshladim.", "Akademiya yoshlar jamoasi a'zosi")
            ]
        },
        {
            "username": "dildora_kids",
            "first_name": "Dildora",
            "last_name": "Mahmudova",
            "headline": "Bolalar Savodxonligi & Mental Arifmetika Xalqaro Treneri",
            "specialties": "sport_arts",
            "photo_id": "photo-1567532939604-b6b5b0db2604",
            "monthly_salary": 7000000,
            "experience_years": 8,
            "students_count": 230,
            "exam_results_summary": "100+ bola 1 oyda erkin o'qish, yozish va tezkor hisoblashni o'rgangan",
            "bio": "Bolalar psixologiyasi, neyromashqlar va abakus orqali miyani ikki yarim sharini barobar rivojlantirish bo'yicha sertifikatlangan mutaxassis.",
            "course_ids": [14],
            "group_name": "Mental Arifmetika & Tezkor Savodxonlik",
            "room": "205-xona (Bolalar Savodxonligi & Mental Arifmetika)",
            "days": "odd",
            "time": ("10:00", "12:00"),
            "reviews": [
                ("Nigora opa (Ona)", "Ota-ona", 5, "6 yoshli o'g'lim 2 oyda erkin kitob o'qiy boshladi va xayolida tez hisoblayapti!", "Mental arifmetika olimpiadasi g'olibi"),
                ("Sherzod aka (Ota)", "Ota-ona", 5, "Ustoz Dildora bolalarga juda mehribon va sabrli, o'qishga mehr uyg'otdi.", "Prezident maktabiga tayyorgarlik")
            ]
        },
        {
            "username": "sanjar_pingpong",
            "first_name": "Sanjar",
            "last_name": "Qosimov",
            "headline": "Stol Tennisi Sport Ustasi & Chempionat Kuratori",
            "specialties": "sport_arts",
            "photo_id": "photo-1521119989659-a83eee488004",
            "monthly_salary": 6500000,
            "experience_years": 7,
            "students_count": 130,
            "exam_results_summary": "O'quvchilari havaskorlar ligasida doimiy sovrinli o'rinlarni qo'lga kiritmoqda",
            "bio": "Stol tennisi bo'yicha O'zbekiston sport ustasi. To'g'ri texnika, tezkor reaksiya va sog'lom turmush tarzini shakllantiradi.",
            "course_ids": [30],
            "group_name": "Stol Tennisi (Ping-Pong) Mahorat To'garagi",
            "room": "Sport Majmuasi (Shaxmat, Futbol & Ping-Pong)",
            "days": "even",
            "time": ("18:30", "20:30"),
            "reviews": [
                ("Bahrom Ergashev", "Talaba", 5, "Darslardan so'ng ping-pong o'ynab stressdan forig' bo'laman, texnikam ancha o'sdi.", "Shahar chempionati 2-o'rin"),
                ("Sobir aka (Ota)", "Ota-ona", 5, "Farzandimning chaqqonligi va ko'rish qobiliyati rivojlanmoqda.", "Havaskorlar ligasi g'olibi")
            ]
        },
        {
            "username": "madina_german",
            "first_name": "Madina",
            "last_name": "Saidova",
            "headline": "Nemis Tili (Goethe-Zertifikat C1) & DAAD Granti Murabbiyi",
            "specialties": "languages",
            "photo_id": "photo-1573497491208-6b1acb260507",
            "monthly_salary": 11500000,
            "experience_years": 7,
            "students_count": 175,
            "exam_results_summary": "40+ o'quvchisi Germaniya va Avstriya universitetlariga 100% grant yutib o'qishga ketgan",
            "bio": "Gyote Instituti akkreditatsiyasidan o'tgan mutaxassis. Nemis tili grammatikasi, TestDaF va jonli Berlin lahjasi o'qituvchisi.",
            "course_ids": [18],
            "group_name": "Nemis Tili: A1 dan B2 gacha & TestDaF",
            "room": "102-xona (IELTS & Til Markazi)",
            "days": "odd",
            "time": ("16:30", "18:30"),
            "reviews": [
                ("Shahnoza Ilhomova", "Talaba", 5, "Madina ustoz ko'magida Gyote B2 sertifikatini oldim va Myunxen universitetiga kirdim!", "Gyote B2 Zertifikat"),
                ("Ravshan aka (Ota)", "Ota-ona", 5, "Qizimning Germaniyada o'qish orzusi aynan ushbu ustoz bilan amalga oshdi.", "DAAD Granti g'olibi")
            ]
        },
        {
            "username": "jahongir_robotics",
            "first_name": "Jahongir",
            "last_name": "Mirzayev",
            "headline": "Robototexnika, IoT & Arduino Yetakchi Muhandisi",
            "specialties": "it",
            "photo_id": "photo-1548142813-c348350df52b",
            "monthly_salary": 12000000,
            "experience_years": 8,
            "students_count": 160,
            "exam_results_summary": "O'quvchilari Xalqaro Robototexnika Olimpiadasida (WRO) sovrindor bo'lgan",
            "bio": "Elektronika, mikrokontrollerlar, sensorlar va aqlli uy tizimlari muhandisi. Bolalarga va yoshlarga texnik ixtirochilikni o'rgatadi.",
            "course_ids": [1],
            "group_name": "Robototexnika & Aqlli Qurilmalar Laboratoriyasi",
            "room": "203-xona (Raqamli Dizayn & SMM Studiyasi)",
            "days": "weekend",
            "time": ("14:00", "17:00"),
            "reviews": [
                ("Javohirbek Qodirov", "Talaba", 5, "O'z qo'lim bilan aqlli robot mashinani yasadim va dasturini yozdim!", "WRO Olimpiada 3-o'rin"),
                ("Dilfuza opa (Ona)", "Ota-ona", 5, "O'g'limning texnikaga qiziqishi to'g'ri yo'naltirildi, ustoz juda professional.", "Kelajak ixtirochisi diplomi")
            ]
        }
    ]

    print(f"\n=== 2. Seeding {len(TEACHERS_CONFIG)} Unique Teachers ===")
    
    # Track used avatar URLs to ensure 100% absolute uniqueness
    used_avatars = set()

    # Clean existing non-student, non-admin duplicates if any
    for t_cfg in TEACHERS_CONFIG:
        username = t_cfg["username"]
        avatar_url = f"https://images.unsplash.com/{t_cfg['photo_id']}?w=500&auto=format&fit=crop&q=80"
        
        assert avatar_url not in used_avatars, f"Duplicate avatar URL detected: {avatar_url}"
        used_avatars.add(avatar_url)

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "first_name": t_cfg["first_name"],
                "last_name": t_cfg["last_name"],
                "role": "teacher",
                "headline": t_cfg["headline"],
                "specialties": t_cfg["specialties"],
                "avatar_url": avatar_url,
                "monthly_salary": t_cfg["monthly_salary"],
                "experience_years": t_cfg["experience_years"],
                "students_count": t_cfg["students_count"],
                "exam_results_summary": t_cfg["exam_results_summary"],
                "bio": t_cfg["bio"],
            }
        )
        if not created:
            user.first_name = t_cfg["first_name"]
            user.last_name = t_cfg["last_name"]
            user.role = "teacher"
            user.headline = t_cfg["headline"]
            user.specialties = t_cfg["specialties"]
            user.avatar_url = avatar_url
            user.monthly_salary = t_cfg["monthly_salary"]
            user.experience_years = t_cfg["experience_years"]
            user.students_count = t_cfg["students_count"]
            user.exam_results_summary = t_cfg["exam_results_summary"]
            user.bio = t_cfg["bio"]
            user.save()

        # Link Courses
        for c_id in t_cfg["course_ids"]:
            Course.objects.filter(id=c_id).update(author=user)

        # Clear old groups and reviews for clean consistency
        StudyGroup.objects.filter(teacher=user).delete()
        TeacherReview.objects.filter(teacher=user).delete()

        # Create Active StudyGroup
        room = created_rooms[t_cfg["room"]]
        c_inst = Course.objects.filter(id=t_cfg["course_ids"][0]).first() or Course.objects.first()
        StudyGroup.objects.create(
            name=t_cfg["group_name"],
            course=c_inst,
            teacher=user,
            room=room,
            days_schedule=t_cfg["days"],
            start_time=t_cfg["time"][0],
            end_time=t_cfg["time"][1],
            monthly_fee=c_inst.monthly_price if hasattr(c_inst, 'monthly_price') and c_inst.monthly_price else 450000,
            is_active=True
        )

        # Create TeacherReviews
        for author_name, author_role, rating, comment, exam_result in t_cfg["reviews"]:
            TeacherReview.objects.create(
                teacher=user,
                author_name=author_name,
                author_role=author_role,
                rating=rating,
                comment=comment,
                exam_result=exam_result
            )

        print(f"✓ Configured Teacher: {user.get_full_name()} (@{user.username}) | Avatar: {t_cfg['photo_id'][:15]}... | Salary: {user.monthly_salary:,} UZS")

    # Update admin user to be distinct (Director/Methodist)
    admin_user = User.objects.filter(username='admin').first()
    if admin_user:
        admin_user.first_name = "Akmal"
        admin_user.last_name = "Nazarov"
        admin_user.headline = "O'quv Markaz Bosh Direktori & Bosh Metodist"
        admin_user.specialties = "it"
        admin_user.avatar_url = "https://images.unsplash.com/photo-1519052537078-e6302a4968d4?w=500&auto=format&fit=crop&q=80"
        admin_user.monthly_salary = 15000000
        admin_user.experience_years = 15
        admin_user.students_count = 500
        admin_user.exam_results_summary = "Xalqaro O'quv Markazlari Assotsiatsiyasi Faxriy A'zosi"
        admin_user.bio = "15 yildan buyon xususiy ta'lim va innovatsion o'quv dasturlarini rivojlantirib kelmoqda. O'quv markazning barcha metodik standartlari va ta'lim sifatini nazorat qiladi."
        admin_user.save()
        used_avatars.add(admin_user.avatar_url)
        print("✓ Configured Director (@admin): Akmal Nazarov")

    # Remove any stray/legacy duplicate teachers that are not in our curated list and not admin
    valid_usernames = set([cfg['username'] for cfg in TEACHERS_CONFIG] + ['admin'])
    stray_teachers = User.objects.filter(role='teacher').exclude(username__in=valid_usernames)
    if stray_teachers.exists():
        print(f"Removing {stray_teachers.count()} stray/duplicate teachers...")
        stray_teachers.delete()

    print("\n=======================================================")
    print(f"SUCCESS: {User.objects.filter(role='teacher').count()} teachers seeded.")
    print(f"Unique avatar URLs verified: {len(used_avatars)}")
    print(f"Active study groups: {StudyGroup.objects.count()}")
    print(f"Teacher reviews: {TeacherReview.objects.count()}")
    print("=======================================================")

if __name__ == '__main__':
    seed_teachers()
