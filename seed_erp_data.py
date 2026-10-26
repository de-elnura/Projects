import os
import sys
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from core.models import (
    User, Course, Room, StudyGroup, Attendance,
    StudentPayment, TeacherSalary, Expense, Lead, TeacherReview
)

def seed_erp():
    print("=" * 60)
    print("Seeding Learning Center ERP & CRM Data...")
    print("=" * 60)

    # 1. Rooms
    rooms_data = [
        {"name": "101-xona (Frontend & IT Lab)", "capacity": 18, "floor": "1-qavat", "equipment": "18 ta iMac, Proyektor, Konditsioner", "color_code": "#4f46e5"},
        {"name": "102-xona (IELTS & CEFR Hub)", "capacity": 20, "floor": "1-qavat", "equipment": "Akustik audio tizim, Smart doska", "color_code": "#0ea5e9"},
        {"name": "201-xona (Matematika & Milliy)", "capacity": 25, "floor": "2-qavat", "equipment": "Keng auditoriya doskasi, Konditsioner", "color_code": "#10b981"},
        {"name": "202-xona (Sharq Tillari Hub)", "capacity": 16, "floor": "2-qavat", "equipment": "Interaktiv sensor doska, Qulay partalar", "color_code": "#f59e0b"},
        {"name": "Sport zali (Shaxmat & Stol tennisi)", "capacity": 24, "floor": "1-qavat", "equipment": "Professional shaxmat soatlari, 4 ta Tennis stoli", "color_code": "#ef4444"},
    ]

    rooms = {}
    for r_data in rooms_data:
        room, _ = Room.objects.get_or_create(name=r_data["name"], defaults=r_data)
        rooms[r_data["name"]] = room
    print(f"[OK] {len(rooms)} xonalar yaratildi yoki yangilandi.")

    # Get teachers and students
    teachers = list(User.objects.filter(role='teacher'))
    students = list(User.objects.filter(role='student'))

    if not teachers:
        print("Hech bo'lmasa 1 ta o'qituvchi bo'lishi kerak!")
        return

    # 2. Groups
    groups_data = [
        {
            "name": "Frontend React Bootcamp #1",
            "teacher": teachers[0],
            "room": rooms["101-xona (Frontend & IT Lab)"],
            "days_schedule": "toq",
            "start_time": "14:00",
            "end_time": "16:00",
            "monthly_fee": 700000,
        },
        {
            "name": "Backend Python Django #3",
            "teacher": teachers[1] if len(teachers) > 1 else teachers[0],
            "room": rooms["101-xona (Frontend & IT Lab)"],
            "days_schedule": "juft",
            "start_time": "16:30",
            "end_time": "18:30",
            "monthly_fee": 750000,
        },
        {
            "name": "IELTS 7.5+ Intensive Masterclass",
            "teacher": teachers[2] if len(teachers) > 2 else teachers[0],
            "room": rooms["102-xona (IELTS & CEFR Hub)"],
            "days_schedule": "toq",
            "start_time": "09:00",
            "end_time": "11:00",
            "monthly_fee": 650000,
        },
        {
            "name": "Ona tili va Adabiyot Milliy Sertifikat-A",
            "teacher": teachers[3] if len(teachers) > 3 else teachers[0],
            "room": rooms["201-xona (Matematika & Milliy)"],
            "days_schedule": "juft",
            "start_time": "14:00",
            "end_time": "16:00",
            "monthly_fee": 500000,
        },
        {
            "name": "Matematika DTM va Milliy Sertifikat Pro",
            "teacher": teachers[4] if len(teachers) > 4 else teachers[0],
            "room": rooms["201-xona (Matematika & Milliy)"],
            "days_schedule": "toq",
            "start_time": "16:30",
            "end_time": "18:30",
            "monthly_fee": 550000,
        },
        {
            "name": "Koreys tili TOPIK Level 3-4",
            "teacher": teachers[5] if len(teachers) > 5 else teachers[0],
            "room": rooms["202-xona (Sharq Tillari Hub)"],
            "days_schedule": "hafta_oxiri",
            "start_time": "10:00",
            "end_time": "13:00",
            "monthly_fee": 600000,
        },
        {
            "name": "Shaxmat va Mantiq Junior Grandmasters",
            "teacher": teachers[6] if len(teachers) > 6 else teachers[0],
            "room": rooms["Sport zali (Shaxmat & Stol tennisi)"],
            "days_schedule": "hafta_oxiri",
            "start_time": "14:00",
            "end_time": "16:30",
            "monthly_fee": 400000,
        },
    ]

    created_groups = []
    for g_info in groups_data:
        grp, _ = StudyGroup.objects.get_or_create(
            name=g_info["name"],
            defaults=g_info
        )
        # Assign some students to each group
        if students:
            import random
            selected_students = random.sample(students, min(len(students), 6))
            grp.students.set(selected_students)
        created_groups.append(grp)
    print(f"[OK] {len(created_groups)} o'quv guruhlari yaratildi va talabalar biriktirildi.")

    # 3. Attendance records
    today = date.today()
    past_dates = [today - timedelta(days=6), today - timedelta(days=4), today - timedelta(days=2), today]

    for grp in created_groups:
        grp_students = list(grp.students.all())
        for idx, st in enumerate(grp_students):
            # Let the first student in the first group have 3 consecutive absences to test alerts
            if grp == created_groups[0] and idx == 0:
                for d in past_dates[-3:]:
                    Attendance.objects.update_or_create(
                        group=grp,
                        student=st,
                        date=d,
                        defaults={"status": "absent", "notes": "Qo'ng'iroqqa javob bermadi", "recorded_by": grp.teacher}
                    )
            else:
                for d in past_dates:
                    Attendance.objects.update_or_create(
                        group=grp,
                        student=st,
                        date=d,
                        defaults={"status": "present" if (idx + d.day) % 5 != 0 else "excused", "recorded_by": grp.teacher}
                    )
    print("[OK] Davomat yozuvlari kiritildi (3 kun ketma-ket qoldirgan talaba ham sinov uchun kiritildi).")

    # 4. Student Payments (Finance)
    current_month = "2026-10"
    for grp in created_groups:
        grp_students = list(grp.students.all())
        for idx, st in enumerate(grp_students):
            # some paid full, some partial, some debt
            if idx % 3 == 0:
                # Full paid
                StudentPayment.objects.get_or_create(
                    receipt_number=f"REC-202610-U{st.id}-G{grp.id}-FULL",
                    defaults={
                        "student": st,
                        "group": grp,
                        "amount": grp.monthly_fee,
                        "payment_method": "click",
                        "payment_month": current_month,
                        "payment_date": today - timedelta(days=10),
                        "status": "paid",
                        "notes": "Oylik to'liq to'landi"
                    }
                )
            elif idx % 3 == 1:
                # Partial paid
                half_amount = grp.monthly_fee // 2
                StudentPayment.objects.get_or_create(
                    receipt_number=f"REC-202610-U{st.id}-G{grp.id}-PART",
                    defaults={
                        "student": st,
                        "group": grp,
                        "amount": half_amount,
                        "payment_method": "payme",
                        "payment_month": current_month,
                        "payment_date": today - timedelta(days=5),
                        "status": "partial",
                        "notes": "Qolgan qismi oy o'rtasida to'lanadi"
                    }
                )
    print("[OK] Talabalar to'lovlari kiritildi.")

    # 5. Teacher Salaries
    for t in teachers[:8]:
        # calculate revenue from their groups
        t_groups = StudyGroup.objects.filter(teacher=t)
        total_rev = sum(g.students.count() * g.monthly_fee for g in t_groups) or 15000000
        salary_rec, _ = TeacherSalary.objects.get_or_create(
            teacher=t,
            month=current_month,
            defaults={
                "calculation_type": "percentage",
                "percentage": 45,
                "fixed_amount": t.monthly_salary,
                "total_student_revenue": total_rev,
                "calculated_salary": int(total_rev * 0.45),
                "bonus": 500000,
                "final_salary": int(total_rev * 0.45) + 500000,
                "is_paid": True,
                "paid_date": today - timedelta(days=2),
                "notes": "O'quvchilar yuqori ko'rsatkichlari uchun +500 000 bonus berildi"
            }
        )
    print("[OK] O'qituvchilar maoshi kalkulyatori qaydlari shakllantirildi.")

    # 6. Expenses
    expenses_data = [
        {"title": "Bino va xonalar oylik ijarasi (Oktyabr)", "category": "rent", "amount": 12000000, "paid_to": "'City Center Plaza' MCHJ"},
        {"title": "Kommunal xizmatlar (Elektr, issiqlik, sovitish, tozalik)", "category": "utilities", "amount": 2350000, "paid_to": "Hududiy Elektr & Kommunal"},
        {"title": "Yuqori tezlikdagi Optik Internet (1 Gbit/s)", "category": "utilities", "amount": 650000, "paid_to": "Sarkor Telecom"},
        {"title": "Instagram va Telegram maqsadli reklama (Targeting)", "category": "marketing", "amount": 4200000, "paid_to": "Digital Agency Pro"},
        {"title": "Ofis qog'ozlari, ruchkalar va doska markerlari", "category": "office", "amount": 950000, "paid_to": "Gross Kantselyariya"},
        {"title": "Talabalar va mehmonlar uchun bepul choy/qahva, suv", "category": "office", "amount": 850000, "paid_to": "Family Market"},
        {"title": "2 ta yangi proyektor lampasi va HDMI kabellar", "category": "equipment", "amount": 1400000, "paid_to": "Techno Pro Service"},
    ]
    for exp in expenses_data:
        Expense.objects.get_or_create(
            title=exp["title"],
            defaults={
                "category": exp["category"],
                "amount": exp["amount"],
                "date": today - timedelta(days=8),
                "paid_to": exp["paid_to"],
                "description": f"Rasmiy to'lov qabul qilindi. {exp['title']}"
            }
        )
    print(f"[OK] {len(expenses_data)} ta xarajatlar daftari kiritildi.")

    # 7. Leads (CRM)
    leads_data = [
        {"full_name": "Sardorbek Rahimov", "phone_number": "+998 90 123-45-67", "interested_subject": "Frontend Dasturlash (React/JS)", "preferred_teacher": teachers[0], "status": "new", "notes": "Saytdan sinov darsiga yozildi. Kechki guruhni so'ramoqda."},
        {"full_name": "Nilufar Karimova", "phone_number": "+998 93 987-65-43", "interested_subject": "IELTS 7.5 Intensive", "preferred_teacher": teachers[2] if len(teachers)>2 else teachers[0], "status": "trial", "notes": "Sinov darsiga ertaga soat 14:00 da keladi."},
        {"full_name": "Javohir Aliyev", "phone_number": "+998 94 456-78-90", "interested_subject": "Matematika va Milliy Sertifikat", "preferred_teacher": teachers[4] if len(teachers)>4 else teachers[0], "status": "enrolled", "notes": "Sinov darsiga keldi, to'lov qilib guruhga qo'shildi."},
        {"full_name": "Madinabonu Usmonova", "phone_number": "+998 97 777-88-99", "interested_subject": "Koreys tili TOPIK", "preferred_teacher": teachers[5] if len(teachers)>5 else teachers[0], "status": "contacted", "notes": "Qo'ng'iroq qilindi, ota-onasi bilan maslahatlashib qayta bog'lanadi."},
        {"full_name": "Bobur Mirzayev", "phone_number": "+998 91 333-22-11", "interested_subject": "Shaxmat va Mantiq", "preferred_teacher": teachers[6] if len(teachers)>6 else teachers[0], "status": "new", "notes": "Farzandi 9 yoshda, shanba kungi guruhga yozilmoqchi."},
    ]
    for ld in leads_data:
        Lead.objects.get_or_create(
            full_name=ld["full_name"],
            phone_number=ld["phone_number"],
            defaults=ld
        )
    print(f"[OK] {len(leads_data)} ta CRM lidlar kiritildi.")

    # 8. Teacher Reviews from Parents
    reviews_data = [
        {"author_name": "Dilnoza Olimova (Ona)", "author_role": "Ota-ona", "rating": 5, "comment": "O'g'lim ushbu ustozning darslariga qatnashib, 3 oyda IELTS dan 7.5 ball oldi! O'qituvchining individual yondashuvi uchun katta rahmat!", "exam_result": "IELTS 7.5 Natija"},
        {"author_name": "Rustam Qodirov (Ota)", "author_role": "Ota-ona", "rating": 5, "comment": "Qizim Ona tili va adabiyotidan Milliy Sertifikat A darajasini 96% bilan qo'lga kiritdi. O'qituvchining tajribasi juda yuqori!", "exam_result": "Milliy Sertifikat A (96%)"},
        {"author_name": "Ziyoda Xolmatova (Ona)", "author_role": "Ota-ona", "rating": 5, "comment": "Farzandim noldan Frontend dasturlashni o'rganib, hozirda portfolio loyihalarini mustaqil qilyapti. O'qituvchi o'z ishining haqiqiy ustasi!", "exam_result": "Frontend Junior Portfolio"},
        {"author_name": "Shohruh Mirzayev (Talaba)", "author_role": "Talaba", "rating": 5, "comment": "Matematika darslari shunchalik qiziqarli o'tiladiki, murakkab masalalar ham oson yechiladi. DTM testlarida 100% natija qildim!", "exam_result": "Matematika DTM 100%"},
        {"author_name": "Nargiza Mahmudova (Ona)", "author_role": "Ota-ona", "rating": 5, "comment": "Farzandim shaxmat to'garagida shahar chempionatida 2-o'rinni oldi. Murabbiyga cheksiz minnatdormiz!", "exam_result": "Shahar Chempionati 2-o'rin"},
    ]
    for idx, t in enumerate(teachers[:5]):
        rev = reviews_data[idx % len(reviews_data)]
        TeacherReview.objects.get_or_create(
            teacher=t,
            author_name=rev["author_name"],
            defaults={
                "author_role": rev["author_role"],
                "rating": rev["rating"],
                "comment": rev["comment"],
                "exam_result": rev["exam_result"]
            }
        )
    print(f"[OK] Ota-onalar va talabalar sharhlari kiritildi.")
    print("\nERP & CRM SEEDING COMPLETED SUCCESSFULLY!")

if __name__ == '__main__':
    seed_erp()
