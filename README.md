# 🎓 SkillUp / EduQuiz — Zamonaviy O'quv Markaz Boshqaruv Tizimi (ERP / CRM, LMS & Telegram Bot)

![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![aiogram](https://img.shields.io/badge/aiogram-3.3+-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952DE?style=for-the-badge&logo=bootstrap&logoColor=white)

---

## 📖 Loyiha Haqida

**SkillUp / EduQuiz** — bu xususiy maktablar, o'quv markazlari va IT akademiyalar uchun mo'ljallangan to'liq integratsiyalashgan **Learning Center ERP / CRM, Onlayn LMS va Telegram Bot** platformasi. 

Ushbu platforma o'quvchilarga interaktiv darslar, modulli testlar va EduCoin rag'bati orqali ta'lim olish imkonini beradi. Shu bilan birga, markaz ma'muriyati uchun moliya, o'qituvchilar maoshi, xonalar bandligi jadvali (Timetable), davomat tahlili va CRM lidlar boshqaruvini to'liq avtomatlashtiradi.

---

## ✨ Asosiy Imkoniyatlar va Modullar

### 1. 🤖 Telegram Bot Integratsiyasi (Aiogram 3.3+)
* **Admin Bildirishnomalari**: Har bir yangi talaba ro'yxatdan o'tganda, saytda CRM lid qoldirilganda, ustozga savol berilganda yoki do'kondan merch xarid qilinganda adminga bir zumda xabar boradi.
* **O'quvchi Boti**: Talaba Telegram hisobini sayt profili bilan bog'lay oladi va quyidagi buyruqlardan foydalanadi:
  - `/profile` — EduCoin balansi, XP va sertifikatlarini ko'rish;
  - `/courses` — O'quv markazdagi barcha mavjud kurslar ro'yxati;
  - `/leaderboard` — Markaz bo'yicha TOP-10 talabalar reytingi.

### 2. 📚 To'garaklar va Kurslar Katalogi (30 xil yo'nalish)
* **Keng qamrovli yo'nalishlar**: Dasturlash (Python, Django, React, AI, DevOps), Xorijiy tillar (IELTS 8.0+, CEFR, Nemis, Koreys, Rus), Maktab fanlari (Matematika, Ona tili va adabiyot) va Sport to'garaklari (Shaxmat, Futbol, Stol tennisi).
* **Interaktiv Darslik va Modulli Testlar**: Har bir modul so'ngida test imtihonlari va anti-farming (ballarni suiiste'mol qilishdan) himoyasi.
* **Paketli Chegirma Tizimi**: Bir vaqtning o'zida bir nechta kursga a'zo bo'lganda avtomatik chegirma.

### 3. 🪙 EduCoin Gamifikatsiyasi va Reyting (Leaderboard)
* **160+ Talabalar Bazasi**: Haqiqiy o'zbekcha ismlar, XP reytingi va Oltin/Kumush/Bronza shohsupasi.
* **Oshib Boruvchi Kunlik Tashrif (Streak Multiplier)**:
  - 1-kun: `+15 🪙`, 2-kun: `+20 🪙`, 3-kun: `+25 🪙`, 7-kun: `+50 🪙 Mega-bonus`!
* **EduCoin Do'koni**: To'plangan tangalarni kurs uchun -50% chegirma kuponlariga, Oltin VIP nishoniga, murabbiy bilan 1-ga-1 konsultatsiyaga yoki markaz sovg'alariga almashtirish.

### 4. 🏢 O'quv Markazi ERP va Moliyaviy Boshqaruv
* **Davomat Tizimi (`Attendance`)**:
  - Har bir guruh talabalari uchun 1 klik bilan oson davomat qilish;
  - Davomat jadvalida har bir o'quvchi yonida **oylik to'lov indikatori** (🟢 To'langan / 🟡 Qisman / 🔴 Qarzdor);
  - Ketma-ket 3 kun dars qoldirgan o'quvchilar bo'yicha adminga tezkor Telegram ogohlantirish.
* **Moliya & Maosh Kalkulyatori (`Finance`)**: Talabalar oylik to'lovlari (Click, Payme, Uzum, Naqd), o'qituvchilar maoshi, sof foyda va xarajatlar tahlili.
* **Dars Jadvali va Xonalar Bandligi (`Timetable`)**: Xonalar va soatlar kesimidagi aniq jadval.
* **CRM Lidlar Boshqaruvi (`Leads`)**: Sinov darsiga yozilgan mijozlar oqimi va statuslar voronkasi.

---

## ⚡ Tezkor Ishga Tushirish (Windows)

Loyiha ildiz papkasidagi tayyor `start_all.bat` fayli orqali Django serveri va Telegram botni bir vaqtning o'zida ishga tushirish mumkin:

1. **`start_all.bat` faylini ikki marta bosing.**
2. Veb-sayt: **http://127.0.0.1:8000**
3. Telegram Bot va Django server ikkita alohida konsolda parallel ishlaydi.

---

## 🚀 Standart O'rnatish va Ishga Tushirish

### 1. Repozitoriyni klon qilish:
```bash
git clone https://github.com/de-elnura/Projects.git
cd Projects
```

### 2. Virtual muhit yaratish va faollashtirish:
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate
```

### 3. Kutubxonalarni o'rnatish:
```bash
pip install -r requirements.txt
```

### 4. Muhit o'zgaruvchilarini sozlash:
`.env.example` faylidan nusxa olib `.env` yarating va Telegram bot sozlamalarini kiriting:
```bash
copy .env.example .env
```

### 5. Server va Botni ishga tushirish:
```bash
# Veb-serverni ishga tushirish:
python manage.py runserver

# Alohida terminalda Telegram botni ishga tushirish:
python manage.py run_bot
```

---

## 🔑 Asosiy Foydalanuvchi Hisoblari (Test Uchun)

| Rol | Foydalanuvchi nomi | Ism-familiya |
| :--- | :--- | :--- |
| **Administrator** | `admin` | Elnura Ibragimova |
| **Talaba** | `akbar` | Akbar Xolmatov |
| **Talaba** | `ismoil` | Ismoil Qodirov |
| **Talaba** | `yahyo` | Yahyo Nurullayev |
| **Talaba** | `elnura` | Elnura Ibragimova |

---

## 🧪 Avtomatlashtirilgan Testlar

Tizim barqarorligini tekshirish uchun:
```bash
python manage.py check
```

---

## 👩‍💻 Muallif
* **GitHub**: [@de-elnura](https://github.com/de-elnura)
* **Email**: elnuraibragimova2014@gmail.com
