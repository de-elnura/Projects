import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from core.models import (
    User, Course, Room, StudyGroup, Attendance,
    StudentPayment, TeacherSalary, Expense, Lead, TeacherReview
)

def run_tests():
    print("=" * 60)
    print("Testing Learning Center ERP / CRM & LMS System")
    print("=" * 60)

    client = Client()

    # 1. Teachers Page (1-line compact cards & modal)
    url_teachers = reverse('teachers_list')
    print(f"1. Testing GET {url_teachers} ...")
    resp_teachers = client.get(url_teachers)
    assert resp_teachers.status_code == 200, f"Expected 200, got {resp_teachers.status_code}"
    html_teachers = resp_teachers.content.decode('utf-8')
    assert "teacher-compact-row" in html_teachers, "Missing 1-line compact teacher cards"
    assert "teacherModal" in html_teachers, "Missing pop-up teacher modal"
    assert "Erishgan Natijalari" in html_teachers, "Missing student results in modal"
    assert "Ota-onalar va Talabalar Fikrlari" in html_teachers, "Missing parent reviews"
    assert "Bepul Sinov Darsiga Yozilish" in html_teachers, "Missing trial lesson button"
    print("   [OK] 1-line compact teacher cards and detailed modal verified.")

    # 2. ERP Dashboard
    url_erp = reverse('erp_dashboard')
    print(f"2. Testing GET {url_erp} ...")
    resp_erp = client.get(url_erp)
    assert resp_erp.status_code == 200
    html_erp = resp_erp.content.decode('utf-8')
    assert "Learning Center ERP / CRM Hub" in html_erp
    assert "Faol Talabalar" in html_erp
    assert "Reja Tushum" in html_erp
    assert "Qarzdorlik" in html_erp
    assert "Sof Foyda" in html_erp
    assert "cashflowChart" in html_erp
    assert "DIQQAT: 3 kun ketma-ket dars qoldirgan talabalar" in html_erp, "Missing 3-day consecutive absence alert"
    print("   [OK] ERP Dashboard KPIs, Net Profit, and 3-day absence alerts verified.")

    # 3. Finance & Accounting Dashboard
    url_fin = reverse('finance_dashboard')
    print(f"3. Testing GET {url_fin} ...")
    resp_fin = client.get(url_fin)
    assert resp_fin.status_code == 200
    html_fin = resp_fin.content.decode('utf-8')
    assert "Talabalar Qarzdorligi" in html_fin
    assert "O'qituvchilar Maoshi Hisobi" in html_fin
    assert "Xarajatlar Daftari" in html_fin
    assert "newPaymentModal" in html_fin
    print("   [OK] Finance & Accounting Dashboard verified.")

    # 4. Timetable & Rooms Grid
    url_time = reverse('timetable')
    print(f"4. Testing GET {url_time} ...")
    resp_time = client.get(url_time)
    assert resp_time.status_code == 200
    html_time = resp_time.content.decode('utf-8')
    assert "O'quv Xonalari Bandligi" in html_time
    assert "101-xona" in html_time
    assert "Toq kunlar" in html_time
    print("   [OK] Timetable and Rooms matrix verified.")

    # 5. Attendance Tracker
    url_att = reverse('attendance')
    print(f"5. Testing GET {url_att} ...")
    resp_att = client.get(url_att)
    assert resp_att.status_code == 200
    html_att = resp_att.content.decode('utf-8')
    assert "Elektron Davomat Jurnali" in html_att
    assert "markAllPresent" in html_att
    assert "Keldi" in html_att
    assert "Sababsiz" in html_att
    print("   [OK] Attendance tracking system verified.")

    # 6. CRM Leads Management
    url_leads = reverse('leads_management')
    print(f"6. Testing GET {url_leads} ...")
    resp_leads = client.get(url_leads)
    assert resp_leads.status_code == 200
    html_leads = resp_leads.content.decode('utf-8')
    assert "Lidlar va Bepul Sinov Darsi Arizalari" in html_leads
    print("   [OK] CRM Leads board verified.")

    # 7. Submit Lead Test (POST)
    print("7. Testing POST submit_lead ...")
    post_data = {
        'full_name': 'Test Sinov Talaba',
        'phone_number': '+998 90 999-00-11',
        'interested_subject': 'IELTS Masterclass',
        'notes': 'Test arizasi'
    }
    resp_lead_post = client.post(reverse('submit_lead'), post_data, follow=True)
    assert resp_lead_post.status_code == 200
    assert Lead.objects.filter(phone_number='+998 90 999-00-11').exists()
    print("   [OK] New Lead successfully registered via trial lesson modal.")

    # 8. Add Student Payment Test (POST)
    print("8. Testing POST add_student_payment ...")
    student = User.objects.filter(role='student').first()
    group = StudyGroup.objects.first()
    assert student is not None and group is not None
    pay_data = {
        'student_id': student.id,
        'group_id': group.id,
        'amount': 650000,
        'payment_method': 'click',
        'payment_month': '2026-10',
        'notes': 'Test to\'lov'
    }
    resp_pay_post = client.post(reverse('add_student_payment'), pay_data, follow=True)
    assert resp_pay_post.status_code == 200
    assert StudentPayment.objects.filter(student=student, amount=650000).exists()
    print("   [OK] Student payment recorded and receipt created.")

    # 9. Add Expense Test (POST)
    print("9. Testing POST add_expense ...")
    exp_data = {
        'title': 'Test Reklama Flayerlari',
        'category': 'marketing',
        'amount': 450000,
        'paid_to': 'Print Express',
        'description': 'Sinov xarajati'
    }
    resp_exp_post = client.post(reverse('add_expense'), exp_data, follow=True)
    assert resp_exp_post.status_code == 200
    assert Expense.objects.filter(title='Test Reklama Flayerlari').exists()
    print("   [OK] Expense successfully added to accounting ledger.")

    print("\nALL ERP & CRM TESTS PASSED SUCCESSFULLY! [OK]")

if __name__ == '__main__':
    run_tests()
