# 🎓 EduQuiz / SkillUp — Ultra Pro Max Onlayn LMS Ta'lim & Gamifikatsiya Platformasi

Professional darajada ishlab chiqilgan onlayn ta'lim, interaktiv imtihon, xavfsiz demo to'lovlar hamda **8 xil EduCoin (🪙)** mukofotlash iqtisodiyoti tizimi.

---

## 🌟 Ultra Pro Max Asosiy Imkoniyatlar va Arxitektura

### 1. 🪙 EduCoin 8 Xil Rag'batlantirish Tizimi (Gamification Economy)
Talabalarni faollikka undovchi 8 xil amaliy harakat uchun maxsus tangalar:
1. **Xush kelibsiz bonusi (`welcome_bonus`):** `+100 🪙` — Yangi talaba ro'yxatdan o'tganda.
2. **Darsni yakunlash (`lesson_completed`):** `+10 🪙` & `+15 XP` — Har bir dars to'liq o'rganganda.
3. **Modul testidan o'tish (`quiz_passed` >= 70%):** `+25 🪙` — Modul yakunidagi imtihondan o'tganda.
4. **Testda 100% a'lo natija (`quiz_perfect`):** `+50 🪙` — Birorta ham xatosiz maksimal natija ko'rsatganda.
5. **Kursni tamomlash & Sertifikat (`course_completed`):** `+150 🪙` — Kurs to'liq bitirilganda.
6. **Yangi kursga yozilish (`course_enrolled`):** `+40 🪙` — Yangi yo'nalishdagi kursga a'zo bo'lganda.
7. **Profilni to'ldirish (`profile_completed`):** `+30 🪙` — Kasb, bio va avatar rasmini to'ldirganda.
8. **Kunlik faollik (`daily_streak`):** `+15 🪙` — Har 24 soatda platformaga kirib bir marta olinadigan bonus.

---

### 2. 🏪 EduCoin Sovg'alar Do'koni (`/coin-shop/`)
Yig'ilgan tangalarni real imtiyozlarga almashtirish:
- **-50% Chegirma Kuponi (`120 🪙`):** Shaxsiy bir martalik promokod generatsiya qilinadi.
- **Oltin VIP Profil Nishoni (`200 🪙`):** Ism yonida jilvalanuvchi Oltin Toj va profil nishoni.
- **Katta Dasturchi bilan 1-ga-1 Mentorlik (`300 🪙`):** 45 daqiqalik shaxsiy video-konsultatsiya.
- **SkillUp Brendli Premium Xudi & Stikerlar (`450 🪙`):** Yetkazib beriladigan sifatli IT-merch.
- **AI Prompt Muhandisligi Kutubxonasi (`100 🪙`):** ChatGPT & Claude uchun 500+ sinalgan promptlar.
- **Qattiq Muqovali Oltin Muhrli Sertifikat (`250 🪙`):** A4 qattiq muqovali diplom.

---

### 3. 💳 Xavfsiz Demo To'lov Tizimi va Promokodlar
- Haqiqiy pul yechilmaydigan, to'liq xavfsiz **Click, Payme, Uzum** to'lov simulyatsiyasi.
- **Promokodlar:**
  - `PROMO50` — 50% chegirma
  - `SKILLUP30` — 30% chegirma
  - `BEPUL100` — 100% mutlaqo bepul vaucher
- Har bir to'lov uchun avtomatik unikal kvitansiya generatsiyasi (`TXN-...`).

---

### 4. 👨‍👩‍👦 Ota-onalar Uchun Rasmiy O'zlashtirish Ma'lumotnomasi (`/parent-report/`)
- A4 va PDF formatida chop etishga tayyor rasmiy hujjat.
- O'quvchining davomati, topshirgan testlari, o'rtacha balli va respublika reytingi.
- O'qituvchilar va platforma ma'muriyati muhri.

---

### 5. 📚 Ko'p Tarmoqli Kurslar (Multidisciplinary Catalog)
- **Backend:** Python, Django, REST API, PostgreSQL.
- **Frontend:** React, Next.js, TypeScript, Tailwind.
- **Sun'iy Intellekt:** Machine Learning, Deep Learning, Prompt Engineering.
- **DevOps:** Docker, Kubernetes, CI/CD, Linux.
- **Kiberxavfsizlik:** Ethical Hacking, Network Defense.
- **Mobil Dasturlash:** Flutter, Android & iOS.
- **Grafik Dizayn:** UI/UX, Figma, Web Design.
- **SMM & Marketing:** Target, Content, Raqamli Marketing.
- **IELTS & Til:** IELTS 7.5+, Akademik Ingliz tili.
- **Biznes & Moliya:** Startup menejmenti, Moliyaviy savodxonlik.

---

## 👥 Sinov Akkauntlari

| Rol | Login | Parol | Ta'rif |
|---|---|---|---|
| **A'lochi Talaba (VIP)** | `jasur` | `parol123` | Sertifikatlari va 240+ EduCoin balansi bor |
| **Talaba** | `talaba` | `parol123` | Boshlang'ich talaba, 100 EduCoin |
| **Bosh Ustoz** | `ustoz` | `parol123` | Python & AI katta o'qituvchisi |
| **Frontend O'qituvchi** | `malika` | `parol123` | React & UI mutaxassisi |
| **Admin** | `admin` | `admin123` | Markaziy Boshqaruv Paneli |

---

## 🚀 Serverni Ishga Tushirish

```bash
# Virtual muhit orqali serverni yoqish:
python manage.py runserver
```

Brauzerda oching:
`http://127.0.0.1:8000/`
