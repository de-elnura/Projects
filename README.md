# 🎓 SkillUp / EduQuiz — Zamonaviy O'quv Markaz Boshqaruv Tizimi (ERP / CRM & Mini-LMS)

![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952DE?style=for-the-badge&logo=bootstrap&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

---

## 📌 Loyiha Haqida

**SkillUp / EduQuiz** — bu xususiy maktablar, o'quv markazlari va IT akademiyalar uchun mo'ljallangan to'liq integratsiyalashgan **Learning Center ERP / CRM & Onlayn LMS** platformasi. Platforma o'quvchilarga onlayn bilim olish va test topshirish imkonini berish bilan bir qatorda, o'quv markaz ma'muriyati uchun moliya, xodimlar maoshi, xonalar bandligi, davomat va lidlarni (CRM) to'liq avtomatlashtiradi.

---

## 🚀 Asosiy Imkoniyatlar va Modullar

### 1. 📚 To'garaklar va Kurslar Katalogi (30 xil yo'nalish)
* **Ko'p tarmoqli kurslar**: Dasturlash (Python, Backend, Frontend, React), AI, Kiberxavfsizlik, Xorijiy tillar (IELTS, CEFR, Koreys, Xitoy, Rus, Nemis, Turk), Maktab fanlari (Ona tili, Adabiyot, Matematika), Sport va musobaqalar (Shaxmat, Futbol, Stol tennisi, Mental arifmetika).
* **1 Qatorli (1 Yo'lli) Ixcham Format**: Sahifada ko'p joy egallamaydigan, zamonaviy SaaS uslubidagi gorizontal qatorlar.
* **To'liq Ma'lumotli Pop-up Modal**: Har qanday to'garak bosilganda dars jadvallari, o'qituvchi oyligi, batafsil tavsif va qatnashish oynasi chiqadi.
* **Paket Chegirmasi**: 2 ta to'garak uchun — 50 000 so'm, 3 tasiga — 100 000 so'm avtomatik chegirma tizimi.

### 2. 👨‍🏫 O'qituvchilar Tarkibi (25 nafar Katta Murabbiy)
* **100% Unikal HD Portretlar**: Har bir o'qituvchi uchun alohida, takrorlanmas professional suratlar.
* **Maoshlar Ierarxiyasi**: Oylik maoshlar 5,000,000 dan 15,000,000 so'mgacha (zamonaviy IT va AI mutaxassislari yuqori stavkada).
* **O'quv Guruhlari va Dars Xonalari**: Har bir ustozga biriktirilgan maxsus auditoriyalar va haftalik dars jadvallari.
* **Ota-onalar Baholari va Yutuqlar**: 5 yulduzli sharhlar hamda o'quvchilarining haqiqiy imtihon ko'rsatkichlari (IELTS 8.0+, Milliy sertifikat A+, DTM 30/30).
* **Tezkor Filtr & Qidiruv**: Sohalar bo'yicha saralash va jonli qidiruv tizimi.

### 3. 🪙 EduCoin Gamifikatsiyasi va Reyting (Leaderboard)
* **159 nafar talabalar bazasi**: O'zbekcha ism-familiyali haqiqiy talabalar reytingi.
* **Shohsupa (Podium - TOP 3)**: Oltin 👑, Kumush 🥈 va Bronza 🥉 shohsupasi.
* **8 Xil Amaliy Faoliyat orqali Rag'batlantirish**:
  1. Darsga o'z vaqtida kelish (Davomat) — `+15 EduCoin`, `+20 XP`
  2. Uy vazifasini 100% a'lo bajarish — `+25 EduCoin`, `+35 XP`
  3. Darsda faollik (Savol-javob & amaliyot) — `+20 EduCoin`, `+30 XP`
  4. Modul testidan o'tish (70%+) — `+30 EduCoin`, `+50 XP`
  5. Imtihondan 100% a'lo natija — `+50 EduCoin`, `+100 XP`
  6. Badiiy kitob mutolaasi — `+35 EduCoin`, `+45 XP`
  7. Haftalik intizom va uzluksiz streak — `+40 EduCoin`, `+60 XP`
  8. Kursni tamomlab Sertifikat olish — `+150 EduCoin`, `+200 XP`
* **EduCoin Do'koni (Coin Shop)**: To'plangan tangalarga chegirma vaucherlari, kitoblar va sovg'alar xarid qilish.

### 4. 💼 O'quv Markaz Moliya va Boshqaruv Tizimi (ERP / CRM)
* **Talabalar To'lovlari (`StudentPayment`)**: Click, Payme, Uzum va Naqd to'lovlar monitoringi, qarzdorliklar hisob-kitobi.
* **O'qituvchilar Maoshi (`TeacherSalary`)**: Oylik maoshlar, bonuslar va to'lov holatlari.
* **Xarajatlar Daftari (`Expense`)**: Ijara, marketing, kommunal to'lovlar va markazning oylik sof foyda kalkulyatori.
* **CRM Bepul Sinov Darsi (`Lead`)**: Yangi tashrif buyuruvchilar arizalari va statuslar voronkasi.
* **Davomat Tizimi (`Attendance`)**: Bir klik bilan butun guruhga davomat qilish.

---

## 🛠 O'rnatish va Ishga Tushirish

### 1. Repozitoriyni yuklab olish:
```bash
git clone https://github.com/de-elnura/Projects.git
cd Projects
```

### 2. Virtual muhitni faollashtirish:
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3. Zarur kutubxonalarni o'rnatish:
```bash
pip install -r requirements.txt
```

### 4. Ma'lumotlar bazasini yangilash (yoki tayyor db.sqlite3 ishlatish):
```bash
python manage.py migrate
# O'qituvchilar va to'garaklarni qayta to'ldirish (ixtiyoriy):
python seed_teachers_complete.py
python seed_students_and_activities.py
```

### 5. Serverni ishga tushirish:
```bash
python manage.py runserver
```

Brauzerda oching:
* **Asosiy sahifa / Kurslar**: `http://127.0.0.1:8000/courses/`
* **O'qituvchilar**: `http://127.0.0.1:8000/teachers/`
* **Olimpiada va Reyting**: `http://127.0.0.1:8000/leaderboard/`
* **Paketli a'zo bo'lish**: `http://127.0.0.1:8000/bundle-enroll/`
* **ERP / Moliya Boshqaruv Paneli**: `http://127.0.0.1:8000/erp/`
* **Admin panel**: `http://127.0.0.1:8000/admin/`

---

## 🧪 Avtomatik Tekshiruv Testlari

Loyiha sifatini tekshirish uchun maxsus avtotestlar kiritilgan:
```bash
python test_teachers_and_shortcomings.py
python test_leaderboard_and_courses.py
python manage.py check
```

---

## 👤 Muallif
* **GitHub**: [@de-elnura](https://github.com/de-elnura)
* **Email**: elnuraibragimova2014@gmail.com
