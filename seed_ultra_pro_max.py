import os
import sys
import django

# Windows UTF-8 terminal xatoliklarini oldini olish
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

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


def seed_ultra_pro_max():
    print("🚀 'Ultra Pro Max' ma'lumotlarini yuklash boshlandi...")

    # =========================================================================
    # 1. 7 TA PROFESSIONAL O'QITUVCHI VA TALABALARNI YARATISH
    # =========================================================================

    teachers_info = [
        {
            'username': 'ustoz_anvar',
            'first_name': 'Anvar',
            'last_name': 'Qodirov',
            'email': 'anvar.backend@skillup.uz',
            'headline': 'Senior Backend Architect & Python Guru',
            'bio': "10+ yillik xalqaro tajribaga ega Backend me'mori. Yuqori yuklamali (High-Load) tizimlar, mikroservislar va Python arxitekturasi bo'yicha ekspert.",
            'avatar_url': 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=250&q=80',
            'total_xp': 850
        },
        {
            'username': 'malika_frontend',
            'first_name': 'Malika',
            'last_name': 'Rustamova',
            'email': 'malika.frontend@skillup.uz',
            'headline': 'Lead Frontend Engineer & UI/UX Architect',
            'bio': "React, Next.js, TypeScript va Design Systems bo'yicha xalqaro IT kompaniyalarda ishlagan yetakchi frontend dasturchi.",
            'avatar_url': 'https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=250&q=80',
            'total_xp': 790
        },
        {
            'username': 'bobur_ai',
            'first_name': 'Bobur',
            'last_name': 'Mirzayev',
            'email': 'bobur.ai@skillup.uz',
            'headline': 'AI & Machine Learning Researcher, PhD',
            'bio': "Sun'iy intellekt, katta til modellari (LLM), neyron tarmoqlar va PyTorch bo'yicha ilmiy izlanuvchi va amaliyotchi mutaxassis.",
            'avatar_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=250&q=80',
            'total_xp': 910
        },
        {
            'username': 'jamshid_devops',
            'first_name': 'Jamshid',
            'last_name': 'Alimov',
            'email': 'jamshid.devops@skillup.uz',
            'headline': 'Certified Kubernetes Administrator & Cloud Lead',
            'bio': "Bulutli infratuzilma (AWS/GCP), Docker konteynerlashtirish va uzluksiz CI/CD integratsiyasi bo'yicha tajribali DevOps muhandisi.",
            'avatar_url': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=250&q=80',
            'total_xp': 720
        },
        {
            'username': 'nigora_cyber',
            'first_name': 'Nigora',
            'last_name': 'Karimova',
            'email': 'nigora.security@skillup.uz',
            'headline': 'Ethical Hacker & Information Security Consultant',
            'bio': "OSCP va CEH sertifikatlariga ega kiberxavfsizlik mutaxassisi. Tizimlarni zaifliklarga tekshirish va axborot himoyasi auditini o'tkazadi.",
            'avatar_url': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=250&q=80',
            'total_xp': 830
        },
        {
            'username': 'sardor_mobile',
            'first_name': 'Sardor',
            'last_name': 'Toshmatov',
            'email': 'sardor.mobile@skillup.uz',
            'headline': 'Mobile Tech Lead (Flutter, iOS & Android)',
            'bio': "15 dan ortiq yirik mobil ilovalar muallifi. Dart va Flutter platformasida zamonaviy mobil servislar yaratish bo'yicha ekspert.",
            'avatar_url': 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=250&q=80',
            'total_xp': 680
        },
        {
            'username': 'dilshod_db',
            'first_name': 'Dilshodbek',
            'last_name': 'Yusupov',
            'email': 'dilshod.db@skillup.uz',
            'headline': 'Principal Database Architect (PostgreSQL & Redis)',
            'bio': "Milliardlab yozuvlarga ega relatsion bazalarni optimallashtirish, indekslash va keshlashtirish bo'yicha katta amaliy tajriba egasi.",
            'avatar_url': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=250&q=80',
            'total_xp': 760
        }
    ]

    teacher_objects = {}
    for t_data in teachers_info:
        user, _ = User.objects.get_or_create(
            username=t_data['username'],
            defaults={
                'first_name': t_data['first_name'],
                'last_name': t_data['last_name'],
                'email': t_data['email'],
                'role': 'teacher',
                'headline': t_data['headline'],
                'bio': t_data['bio'],
                'avatar_url': t_data['avatar_url'],
                'total_xp': t_data['total_xp'],
            }
        )
        user.set_password('parol123')
        user.headline = t_data['headline']
        user.bio = t_data['bio']
        user.avatar_url = t_data['avatar_url']
        user.save()
        teacher_objects[t_data['username']] = user

    print(f"✅ {len(teacher_objects)} ta professional o'qituvchi muvaffaqiyatli saqlandi.")

    # Talabalar
    student1, _ = User.objects.get_or_create(
        username='talaba',
        defaults={'first_name': 'Sanjar', 'last_name': 'Aliyev', 'email': 'sanjar@student.uz', 'role': 'student', 'total_xp': 180}
    )
    student1.set_password('parol123')
    student1.save()

    student2, _ = User.objects.get_or_create(
        username='jasur',
        defaults={'first_name': 'Jasur', 'last_name': 'Mahmudov', 'email': 'jasur@student.uz', 'role': 'student', 'total_xp': 640}
    )
    student2.set_password('parol123')
    student2.save()

    # =========================================================================
    # 2. 7 TA CHUQURLASHTIRILGAN KURS, MODULLAR VA TESTLARNI YARATISH
    # =========================================================================

    courses_blueprint = [
        # 1-KURS: PYTHON BACKEND
        {
            'author_key': 'ustoz_anvar',
            'title': "Python Backend Masterclass: Noldan Katta Loyihalargacha",
            'category': "Backend",
            'level': "O'rta / Murakkab",
            'duration_hours': 36,
            'description': "Katta hajmli veb-ilovalarni professional darajada ishlab chiqish. Python sintaksisi, OOP tamoyillari, Clean Code, asinxron dasturlash va REST API yaratish bo'yicha amaliy masterclass.",
            'modules': [
                {
                    'title': "Python Sintaksisi, Algoritmlar va Ma'lumotlar Tuzilmasi",
                    'lessons': [
                        ("Python 3.12 yangiliklari va Muhitni sozlash", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Python zamonaviy sintaksisi va virtual muhit bilan ishlash asoslari."),
                        ("List, Dict, Set va Generator Expressions", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Xotiradan unumli foydalanish va tejamkor generatorlar yaratish."),
                        ("Algoritmik Murakkablik (Big-O Notatsiyasi)", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Kodni optimallashtirish va vaqt sarfini hisoblash mezonlari.")
                    ],
                    'quiz_title': "1-Modul: Sintaksis va Algoritmlar Imtihoni",
                    'questions': [
                        ("Generatordan qiymat olish uchun qaysi kalit so'z ishlatiladi?", [("yield", True), ("return", False), ("give", False), ("send", False)]),
                        ("Lug'atda (dict) kalit bo'yicha qidirishning o'rtacha murakkabligi qanday?", [("O(1)", True), ("O(N)", False), ("O(N^2)", False), ("O(log N)", False)])
                    ]
                },
                {
                    'title': "OOP Tamoyillari, Design Patternlar va Clean Architecture",
                    'lessons': [
                        ("Klasslar, Vorislik va Multiple Inheritance", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Klass tuzilmasi, super() funksiyasi va MRO (Method Resolution Order)."),
                        ("SOLID Tamoyillarining Amaliy Qo'llanilishi", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Clean Code yozish va arxitekturaviy xatolardan saqlanish."),
                        ("Factory, Singleton va Repository Patternlari", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Ishlab chiqarish darajasidagi loyihalarda patternlarni to'g'ri tanlash.")
                    ],
                    'quiz_title': "2-Modul: OOP va Clean Architecture Imtihoni",
                    'questions': [
                        ("SOLID qoidalaridagi 'S' nimani anglatadi?", [("Single Responsibility Principle", True), ("Simple Code", False), ("Speed", False), ("Structure", False)]),
                        ("Faqat bitta obyekt nusxasini yaratishga kafolat beruvchi pattern qaysi?", [("Singleton", True), ("Factory", False), ("Observer", False), ("Adapter", False)])
                    ]
                },
                {
                    'title': "Asinxron Dasturlash (Asyncio) va Mikroservislar",
                    'lessons': [
                        ("Asyncio Event Loop va Coroutines", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "I/O operatsiyalarini bloklamasdan parallel bajarish texnikasi."),
                        ("FastAPI va Pydantic bilan Yuqori Tezlikdagi API", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Avtomatik Swagger hujjatlari va qat'iy ma'lumotlar validatsiyasi.")
                    ],
                    'quiz_title': "Yakuniy Bitiruv Imtihoni: Backend Arxitektura",
                    'questions': [
                        ("Asinxron funksiyani kutish uchun qaysi operator ishlatiladi?", [("await", True), ("wait", False), ("async", False), ("defer", False)]),
                        ("Pydantic kutubxonasining asosiy vazifasi nima?", [("Ma'lumotlar validatsiyasi va parsing", True), ("Baza boshqaruvi", False), ("Frontend render", False), ("Keshlashtirish", False)])
                    ]
                }
            ]
        },

        # 2-KURS: FRONTEND & REACT
        {
            'author_key': 'malika_frontend',
            'title': "Zamonaviy Frontend va UI/UX: HTML5, CSS3, JS & React",
            'category': "Frontend",
            'level': "Boshlang'ich / O'rta",
            'duration_hours': 28,
            'description': "Interaktiv, chiroyli va tez ishlaydigan foydalanuvchi interfeyslarini yarating. Flexbox, CSS Grid, Tailwind CSS, JavaScript ES6+ va React Hooks bo'yicha to'liq amaliyot.",
            'modules': [
                {
                    'title': "Zamonaviy CSS, Flexbox, Grid va Tailwind CSS",
                    'lessons': [
                        ("Semantik HTML5 va Web Accessibility (a11y)", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "To'g'ri teglar tanlash va qidiruv tizimlari (SEO) uchun optimallashtirish."),
                        ("Flexbox va CSS Grid orqali Responsiv UI Qadash", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Mobil va planshet ekranlarga 100% moslashuvchan maketlar yaratish.")
                    ],
                    'quiz_title': "1-Modul: CSS Maketlash va Tailwind Imtihoni",
                    'questions': [
                        ("CSS Flexbox-da elementlarni asosiy o'q bo'ylab markazlash uchun nima ishlatiladi?", [("justify-content: center", True), ("align-items: center", False), ("text-align: center", False), ("display: center", False)]),
                        ("Tailwind CSS da 'flex justify-between' nima qiladi?", [("Elementlarni ikki chekkaga suradi", True), ("Markazga yig'adi", False), ("Ustun qiladi", False), ("Yashiradi", False)])
                    ]
                },
                {
                    'title': "JavaScript ES6+, DOM va Asinxronlik (Fetch API)",
                    'lessons': [
                        ("ES6+ Destructuring, Spread va Arrow Functions", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Qisqa, aniq va zamonaviy JavaScript sintaksisidan foydalanish."),
                        ("Promises, Async/Await va REST API bilan Aloqa", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Serverdan JSON ma'lumotlarni qabul qilish va ekranga chiqarish.")
                    ],
                    'quiz_title': "2-Modul: JavaScript Dasturlash Imtihoni",
                    'questions': [
                        ("Qaysi kalit so'z o'zgarmas qiymatli o'zgaruvchi e'lon qiladi?", [("const", True), ("let", False), ("var", False), ("val", False)]),
                        ("JSON ma'lumotni JavaScript obyektiga o'girish funksiyasi qaysi?", [("JSON.parse()", True), ("JSON.stringify()", False), ("JSON.toObject()", False), ("JSON.decode()", False)])
                    ]
                },
                {
                    'title': "React.js: Komponentlar, Hooks va State Management",
                    'lessons': [
                        ("React Komponentlar, Props va JSX sintaksisi", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Kodni mayda, qayta ishlatiluvchi bo'laklarga ajratish san'ati."),
                        ("useState, useEffect va Custom Hooks", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Dinamik ma'lumotlar bilan ishlash va komponent hayot sikli.")
                    ],
                    'quiz_title': "Yakuniy Bitiruv Imtihoni: React Frontend",
                    'questions': [
                        ("React da holatni (state) saqlash uchun qaysi hook ishlatiladi?", [("useState", True), ("useEffect", False), ("useRef", False), ("useMemo", False)]),
                        ("useEffect ikkinchi parametri bo'sh massiv `[]` bo'lsa nima sodir bo'ladi?", [("Faqat 1 marta komponent yuklanganda ishlaydi", True), ("Har doim ishlaydi", False), ("Hech qachon ishlamaydi", False), ("Xatolik beradi", False)])
                    ]
                }
            ]
        },

        # 3-KURS: AI & MACHINE LEARNING
        {
            'author_key': 'bobur_ai',
            'title': "Amaliy Sun'iy Intellekt va Machine Learning Asoslari",
            'category': "Sun'iy Intellekt",
            'level': "O'rta / Ilg'or",
            'duration_hours': 32,
            'description': "Matematik modellashtirishdan tortib amaliy neyron tarmoqlar va LLM agentlargacha. NumPy, Pandas, Scikit-Learn va PyTorch yordamida haqiqiy AI modellarini yarating.",
            'modules': [
                {
                    'title': "Data Science: NumPy, Pandas va Ma'lumotlarni Tozalash",
                    'lessons': [
                        ("NumPy Matritsalari va Vektorlashtirilgan Amallar", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Ko'p o'lchamli massivlar va tezkor matematik hisob-kitoblar."),
                        ("Pandas DataFrame: Ma'lumotlarni tahlil qilish va tozalash", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Bo'sh qiymatlarni to'ldirish, filtrlash va statistik ko'rsatkichlar.")
                    ],
                    'quiz_title': "1-Modul: Data Science Asoslari Imtihoni",
                    'questions': [
                        ("Pandas kutubxonasida asosiy 2 o'lchamli jadval tuzilmasi nima deyiladi?", [("DataFrame", True), ("Series", False), ("Table", False), ("Matrix", False)]),
                        ("NumPy massivlari nima sababdan standart Python ro'yxatlaridan ancha tezroq?", [("C tilida yozilgan va xotirada ketma-ket joylashadi", True), ("Kichikroq", False), ("Interpretatsiya qilinmaydi", False), ("Faqat sonlar uchun", False)])
                    ]
                },
                {
                    'title': "Klassik Machine Learning: Regressiya va Klassifikatsiya",
                    'lessons': [
                        ("Chiziqli Regressiya va Logistik Regressiya Modeli", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Narxlarni bashorat qilish va toifalarga ajratish usullari."),
                        ("Random Forest va Decision Trees Algoritmlari", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Ansambl metodlari orqali model aniqligini oshirish.")
                    ],
                    'quiz_title': "2-Modul: Machine Learning Modellari Imtihoni",
                    'questions': [
                        ("Modelni o'qitish va test qilishga ajratishning odatiy nisbati qanday?", [("80% train, 20% test", True), ("50% train, 50% test", False), ("100% train", False), ("10% train, 90% test", False)]),
                        ("Klassifikatsiya modelining aniqligini baholovchi asosiy ko'rsatkich qaysi?", [("Accuracy / F1-Score", True), ("Mean Squared Error", False), ("R-squared", False), ("Loss faqat", False)])
                    ]
                },
                {
                    'title': "Chuqur O'rganish (Deep Learning) va PyTorch Asoslari",
                    'lessons': [
                        ("Neyron Tarmoqlari: Forward & Backward Propagation", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Gradient descent va og'irlik koeffitsiyentlarini sozlash."),
                        ("PyTorch orqali Rasmlarni Tanuvchi CNN Tarmog'i", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Konvolyutsion qatlamlar va kompyuter ko'rishi (Computer Vision).")
                    ],
                    'quiz_title': "Yakuniy Bitiruv Imtihoni: Sun'iy Intellekt",
                    'questions': [
                        ("Neyron tarmoqlarda nochiziqlikni ta'minlovchi funksiya qanday ataladi?", [("Activation Function (ReLU, Sigmoid)", True), ("Loss Function", False), ("Optimizer", False), ("Weight", False)]),
                        ("PyTorch da tensorni GPU xotirasiga o'tkazish uchun nima chaqiriladi?", [(".to('cuda')", True), (".gpu()", False), (".accelerate()", False), (".cuda_now()", False)])
                    ]
                }
            ]
        },

        # 4-KURS: DEVOPS & KUBERNETES
        {
            'author_key': 'jamshid_devops',
            'title': "DevOps, Docker va Kubernetes: Ishlab Chiqarish Muhiti",
            'category': "DevOps",
            'level': "O'rta / Murakkab",
            'duration_hours': 30,
            'description': "Dasturiy ta'minotni ishlab chiqishdan serverga joylashgacha bo'lgan to'liq jarayon. Linux boshqaruvi, Docker, Docker Compose, CI/CD pipeline va Kubernetes klasterlari.",
            'modules': [
                {
                    'title': "Linux Server Boshqaruvi va Bash Skriptlar",
                    'lessons': [
                        ("Linux Buyruqlar Satri va Ruxsatlar Tizimi (chmod, chown)", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Fayllar xavfsizligi, jarayonlarni kuzatish (top, ps, kill)."),
                        ("Nginx Veb-Serverini Sozlash va Reverse Proxy", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Statik fayllarni tarqatish va SSL sertifikatlarini o'rnatish.")
                    ],
                    'quiz_title': "1-Modul: Linux va Server Boshqaruvi Imtihoni",
                    'questions': [
                        ("Faylga barcha ruxsatlarni (o'qish, yozish, bajarish) berish kodi qaysi?", [("chmod 777", True), ("chmod 644", False), ("chmod 700", False), ("chmod 111", False)]),
                        ("Nginx da so'rovni ichki backend portga yo'naltirish direktivasi qaysi?", [("proxy_pass", True), ("forward_to", False), ("redirect", False), ("backend_route", False)])
                    ]
                },
                {
                    'title': "Docker va Ko'p Konteynerli Tizimlar (Compose)",
                    'lessons': [
                        ("Dockerfile Yozish va Image Optimallashtirish", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Multi-stage build orqali image hajmini 10 barobarga qisqartirish."),
                        ("Docker Compose: Django, PostgreSQL va Redisni Birgalikda Ishlatish", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Tarmoqlar (networks) va ma'lumot saqlovchilar (volumes) bilan ishlash.")
                    ],
                    'quiz_title': "2-Modul: Docker Konteynerlashtirish Imtihoni",
                    'questions': [
                        ("Ishga tushgan konteyner ichiga terminal orqali kirish buyrug'i qaysi?", [("docker exec -it <id> bash", True), ("docker run -it", False), ("docker enter", False), ("docker connect", False)]),
                        ("Dockerfile da eng birinchi yoziladigan direktiva qaysi?", [("FROM", True), ("RUN", False), ("WORKDIR", False), ("CMD", False)])
                    ]
                },
                {
                    'title': "Kubernetes (K8s) Klasterlari va Avtomatlashgan CI/CD",
                    'lessons': [
                        ("Kubernetes Pod, Deployment va Service Tushunchalari", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Ilovalarni klasterda taqsimlash va avtomatik tiklanish mexanizmi."),
                        ("GitHub Actions orqali Avtomatik Test va Deploy", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Har bir git push qilinganda avtomatik test va serverga yuklash.")
                    ],
                    'quiz_title': "Yakuniy Bitiruv Imtihoni: DevOps & K8s",
                    'questions': [
                        ("Kubernetes-da eng kichik hisoblash birligi nima?", [("Pod", True), ("Node", False), ("Cluster", False), ("Service", False)]),
                        ("CI/CD qisqartmasi nimani bildiradi?", [("Continuous Integration / Continuous Deployment", True), ("Cloud Internet / Central Data", False), ("Computer Interface", False), ("Code Inspector", False)])
                    ]
                }
            ]
        },

        # 5-KURS: CYBERSECURITY
        {
            'author_key': 'nigora_cyber',
            'title': "Ethical Hacking va Kiberxavfsizlik Asoslari",
            'category': "Kiberxavfsizlik",
            'level': "Boshlang'ich / O'rta",
            'duration_hours': 26,
            'description': "Axborot tizimlarini buzg'unchilardan himoya qilish san'ati. Tarmoq xavfsizligi, penetratsion testlar, SQL Injection, XSS, CSRF zaifliklarini topish va bartaraf qilish.",
            'modules': [
                {
                    'title': "Tarmoq Xavfsizligi, OSI Modeli va Skanerlash",
                    'lessons': [
                        ("TCP/IP, OSI Modeli va Tarmoq Paketlari Anatomiyasi", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Wireshark orqali tarmoq trafigini tahlil qilish asoslari."),
                        ("Nmap yordamida Portlar va Servislarni Skanerlash", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Ochiq portlar va zaif servis versiyalarini aniqlash usullari.")
                    ],
                    'quiz_title': "1-Modul: Tarmoq Tahlili Imtihoni",
                    'questions': [
                        ("HTTPS protokoli standart qaysi port orqali ishlaydi?", [("443", True), ("80", False), ("8080", False), ("22", False)]),
                        ("TCP 3-bosqichli bog'lanish (3-way handshake) ketma-ketligi qanday?", [("SYN -> SYN-ACK -> ACK", True), ("ACK -> SYN -> FIN", False), ("HELLO -> OK", False), ("CONNECT -> READY", False)])
                    ]
                },
                {
                    'title': "Web Ilovalar Zaifliklari (OWASP Top 10)",
                    'lessons': [
                        ("SQL Injection va Xom SQL So'rovlar Xavfi", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "ORM parametrli so'rovlar orqali bazani to'liq himoyalash."),
                        ("XSS (Cross-Site Scripting) va CSRF Hujumlari", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Foydalanuvchi ma'lumotlarini qochirish va himoya tokenlari.")
                    ],
                    'quiz_title': "2-Modul: Web Zaifliklar Imtihoni",
                    'questions': [
                        ("SQL Injection hujumidan eng samarali himoya nima?", [("Parametrlangan so'rovlar (Prepared Statements / ORM)", True), ("Parolni shifrlash", False), ("Faqat GET so'rov ishlatish", False), ("Firewall o'rnatish", False)]),
                        ("CSRF hujumidan himoyalanish uchun Django nimadan foydalanadi?", [("CSRF Token (csrf_token)", True), ("JWT", False), ("Cookie", False), ("Basic Auth", False)])
                    ]
                },
                {
                    'title': "Kriptografiya, Parollar Himoyasi va Audit",
                    'lessons': [
                        ("Hashing (Bcrypt, Argon2) va Shifrlash (AES, RSA)", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Parollarni xom holda saqlamaslik va asimmetrik shifrlash."),
                        ("Xavfsizlik Auditi va Xodimlarni Phishing'dan Saqlash", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Ijtimoiy muhandislik hujumlariga qarshi korporativ himoya choralari.")
                    ],
                    'quiz_title': "Yakuniy Bitiruv Imtihoni: Kiberxavfsizlik",
                    'questions': [
                        ("Bir tomonlama qaytarib bo'lmaydigan matematik o'zgartirish nima?", [("Hashing (Heshlash)", True), ("Encryption (Shifrlash)", False), ("Encoding", False), ("Compression", False)]),
                        ("Parollarni heshlashda 'Tuz' (Salt) nimaga kerak?", [("Kamalak jadvallari (Rainbow tables) orqali parolni topishni qiyinlashtirish", True), ("Parolni qisqartirish", False), ("Bazani tezlashtirish", False), ("Shunchaki format", False)])
                    ]
                }
            ]
        },

        # 6-KURS: FLUTTER & MOBILE
        {
            'author_key': 'sardor_mobile',
            'title': "Flutter orqali iOS va Android Mobil Ilovalar Yaratish",
            'category': "Mobil Dasturlash",
            'level': "Boshlang'ich / O'rta",
            'duration_hours': 24,
            'description': "Yagona kod bazasi bilan ham iPhone, ham Android smartfonlari uchun ajoyib ilovalar dasturlash. Dart tili asoslari, Widgetlar, Navigatsiya, REST API integratsiyasi va BLoC/Provider.",
            'modules': [
                {
                    'title': "Dart Dasturlash Tili va Flutter Asoslari",
                    'lessons': [
                        ("Dart O'zgaruvchilari, Null-Safety va Funksiyalar", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Dart tili xususiyatlari va xatoliksiz kod yozish qoidalari."),
                        ("Stateless va Stateful Widgetlar Tafovuti", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Ekran elementlarini yaratish va dinamik yangilanish.")
                    ],
                    'quiz_title': "1-Modul: Dart va Widgetlar Imtihoni",
                    'questions': [
                        ("Flutter-da hamma narsa nima hisoblanadi?", [("Widget", True), ("Component", False), ("View", False), ("Div", False)]),
                        ("Dart-da o'zgaruvchi null bo'lishi mumkinligini bildirish belgisi qaysi?", [("?", True), ("!", False), ("*", False), ("#", False)])
                    ]
                },
                {
                    'title': "Mobil UI Dizayn va Navigatsiya Tizimi",
                    'lessons': [
                        ("Scaffold, AppBar, ListView va GridView", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Cheksiz ro'yxatlar va kartochkalar dizayni."),
                        ("Sahifalararo O'tish (Navigator 2.0 va GoRouter)", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Parametrlar uzatish va orqaga qaytish mantig'i.")
                    ],
                    'quiz_title': "2-Modul: Mobil UI Dizayn Imtihoni",
                    'questions': [
                        ("Material Design standart ekran qobig'ini beruvchi asosiy widget qaysi?", [("Scaffold", True), ("Container", False), ("Center", False), ("Screen", False)]),
                        ("Yangi ekranga o'tish uchun nima chaqiriladi?", [("Navigator.push()", True), ("Navigator.next()", False), ("Router.go()", False), ("Page.open()", False)])
                    ]
                },
                {
                    'title': "REST API Integratsiyasi va Holat Boshqaruvi",
                    'lessons': [
                        ("Http paketi orqali Backend bilan Bog'lanish", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "JSON ma'lumotlarni parse qilish va yuklanish animatsiyalari."),
                        ("Provider / BLoC orqali Global State Boshqaruvi", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Ilova holatini toza va modulli boshqarish.")
                    ],
                    'quiz_title': "Yakuniy Bitiruv Imtihoni: Flutter Mobile",
                    'questions': [
                        ("Asinxron ma'lumotlarni kutib ekranda render qiluvchi widget qaysi?", [("FutureBuilder", True), ("AsyncWidget", False), ("DataLoader", False), ("WaitBuilder", False)]),
                        ("Flutter qaysi dasturlash tilida yoziladi?", [("Dart", True), ("JavaScript", False), ("Kotlin", False), ("Swift", False)])
                    ]
                }
            ]
        },

        # 7-KURS: DATABASE & SQL
        {
            'author_key': 'dilshod_db',
            'title': "Ma'lumotlar Bazalari va SQL Chuqurlashtirilgan Kurs",
            'category': "Ma'lumotlar Bazasi",
            'level': "O'rta / Murakkab",
            'duration_hours': 22,
            'description': "Murakkab SQL so'rovlar, ma'lumotlar bazasi normalizatsiyasi, B-Tree indekslar, tranzaksiyalar (ACID), PostgreSQL optimizatsiyasi va Redis keshlashtirish.",
            'modules': [
                {
                    'title': "Relatsion Modellar, Joins va Murakkab SQL",
                    'lessons': [
                        ("SELECT, INNER JOIN, LEFT JOIN va Agregat Funksiyalar", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Bir nechta jadvallardan tezkor va to'g'ri ma'lumot yig'ish."),
                        ("Subqueries (Ichki So'rovlar) va Window Functions", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "ROW_NUMBER(), RANK() va qismlarga bo'lingan analitika.")
                    ],
                    'quiz_title': "1-Modul: SQL So'rovlar Imtihoni",
                    'questions': [
                        ("Ikki jadvaldan faqat bir-biriga mos keluvchi yozuvlarni oluvchi join turi qaysi?", [("INNER JOIN", True), ("LEFT JOIN", False), ("FULL JOIN", False), ("CROSS JOIN", False)]),
                        ("Guruhlangan ma'lumotlarni filtrlash uchun WHERE o'rniga nima ishlatiladi?", [("HAVING", True), ("FILTER", False), ("GROUP BY", False), ("ORDER", False)])
                    ]
                },
                {
                    'title': "Tranzaksiyalar, ACID va Indekslar Optimizatsiyasi",
                    'lessons': [
                        ("ACID Tamoyillari va Tranzaksiya Izolyatsiya Darajalari", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Bank o'tkazmalari va pul operatsiyalarida xatoliklarni oldini olish."),
                        ("B-Tree va Hash Indekslar: EXPLAIN ANALYZE orqali tezlashtirish", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "So'rov bajarilish vaqtini soniyalardan millisoniyalarga tushirish.")
                    ],
                    'quiz_title': "2-Modul: Tranzaksiyalar va Indekslar Imtihoni",
                    'questions': [
                        ("ACID qisqartmasidagi 'A' harfi nimani anglatadi?", [("Atomicity (Atomlilik - yo hammasi bajariladi, yo hech biri)", True), ("Accuracy", False), ("Availability", False), ("Action", False)]),
                        ("SQL so'rovning qanday indekslardan foydalanayotganini tahlil qilish buyrug'i qaysi?", [("EXPLAIN ANALYZE", True), ("CHECK QUERY", False), ("SPEED TEST", False), ("SHOW PERFORMANCE", False)])
                    ]
                },
                {
                    'title': "Replikatsiya, Sharding va Redis bilan Keshlashtirish",
                    'lessons': [
                        ("Master-Slave Replikatsiya va Read Replicas", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "O'qish so'rovlarini bir nechta serverlarga taqsimlash uslubi."),
                        ("Redis In-Memory Kesh: Tezkor ma'lumotlar ombori", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Tez-tez so'raladigan ma'lumotlarni xotirada saqlash.")
                    ],
                    'quiz_title': "Yakuniy Bitiruv Imtihoni: Katta Hajmli Bazalar",
                    'questions': [
                        ("Redis ma'lumotlarni qayerda saqlaydi?", [("RAM (Operativ Xotira)da", True), ("Faqat qattiq diskda", False), ("Fayllarda", False), ("Tarmoqda", False)]),
                        ("Jadvalni gorizontal ravishda bir nechta serverlarga bo'lish qanday ataladi?", [("Sharding", True), ("Indexing", False), ("Normalization", False), ("Backup", False)])
                    ]
                }
            ]
        }
    ]

    total_created_courses = 0
    total_created_lessons = 0
    total_created_quizzes = 0

    for c_data in courses_blueprint:
        author = teacher_objects[c_data['author_key']]
        course, created = Course.objects.get_or_create(
            title=c_data['title'],
            defaults={
                'author': author,
                'category': c_data['category'],
                'level': c_data['level'],
                'duration_hours': c_data['duration_hours'],
                'description': c_data['description'],
            }
        )
        course.category = c_data['category']
        course.level = c_data['level']
        course.duration_hours = c_data['duration_hours']
        course.author = author
        course.description = c_data['description']
        course.save()

        total_created_courses += 1

        for m_idx, m_info in enumerate(c_data['modules'], start=1):
            module, _ = Module.objects.get_or_create(
                course=course,
                order=m_idx,
                defaults={'title': m_info['title']}
            )
            module.title = m_info['title']
            module.save()

            # Darslarni yaratish
            for l_idx, l_tuple in enumerate(m_info['lessons'], start=1):
                les_title, les_video, les_content = l_tuple
                lesson, _ = Lesson.objects.get_or_create(
                    module=module,
                    order=l_idx,
                    defaults={
                        'title': les_title,
                        'video_url': les_video,
                        'content': f"# 📌 {les_title}\n\n{les_content}\n\n### Amaliy Maslahat:\nUshbu mavzuni to'liq tushunib bo'lgach, pastdagi **'Darsni tugatdim (+15 XP)'** tugmasini bosing va o'z bilimingizni mustahkamlang!"
                    }
                )
                total_created_lessons += 1

            # Modul Testini yaratish
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
            total_created_quizzes += 1

            # Savollar va variantlar
            for q_text, choices_list in m_info['questions']:
                q_obj, _ = Question.objects.get_or_create(
                    quiz=quiz,
                    text=q_text
                )
                for ch_text, is_corr in choices_list:
                    Choice.objects.get_or_create(
                        question=q_obj,
                        text=ch_text,
                        defaults={'is_correct': is_corr}
                    )

    print(f"✅ {total_created_courses} ta amaliy kurs yaratildi.")
    print(f"✅ {total_created_lessons} ta interaktiv dars yaratildi.")
    print(f"✅ {total_created_quizzes} ta modul imtihonlari va yuzlab test savollari muvaffaqiyatli saqlandi.")

    # =========================================================================
    # 3. TALABALAR PROGRESSI VA SERTIFIKATLARINI O'RNATISH
    # =========================================================================

    first_course = Course.objects.filter(author=teacher_objects['ustoz_anvar']).first()
    if first_course:
        mod1 = first_course.modules.filter(order=1).first()
        if mod1:
            for l in mod1.lessons.all():
                UserLessonProgress.objects.get_or_create(user=student1, lesson=l, defaults={'is_completed': True, 'completed_at': timezone.now()})
            if hasattr(mod1, 'quiz'):
                QuizResult.objects.get_or_create(user=student1, quiz=mod1.quiz, defaults={'score': 100.0, 'is_passed': True})

        # A'lochi talaba (Jasur) uchun barcha darslar va sertifikat
        for mod in first_course.modules.all():
            for l in mod.lessons.all():
                UserLessonProgress.objects.get_or_create(user=student2, lesson=l, defaults={'is_completed': True, 'completed_at': timezone.now()})
            if hasattr(mod, 'quiz'):
                QuizResult.objects.get_or_create(user=student2, quiz=mod.quiz, defaults={'score': 95.0, 'is_passed': True})

        Certificate.objects.get_or_create(
            user=student2,
            course=first_course,
            defaults={'certificate_code': Certificate.generate_code(first_course.id, student2.id)}
        )

    print("🎉 'Ultra Pro Max' platforma ma'lumotlari 100% muvaffaqiyatli yuklandi!")


if __name__ == '__main__':
    seed_ultra_pro_max()
