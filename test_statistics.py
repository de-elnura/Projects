import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from core.models import User, Course, Module, Lesson, Quiz, QuizResult, Certificate, Enrollment, BundleEnrollment

def run_tests():
    print("=" * 60)
    print("Testing EduQuiz / SkillUp Statistics & Analytics System")
    print("=" * 60)

    client = Client()

    # 1. Test URL resolution and response code
    url = reverse('statistics')
    print(f"1. Testing GET {url} ...")
    response = client.get(url)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("   [OK] HTTP 200 returned successfully.")

    # 2. Check HTML content
    content = response.content.decode('utf-8')
    assert "EduQuiz / SkillUp Statistikasi" in content, "Missing title in HTML"
    assert "categoryChart" in content, "Missing categoryChart in HTML"
    assert "scheduleChart" in content, "Missing scheduleChart in HTML"
    assert "teacherSalaryChart" in content, "Missing teacherSalaryChart in HTML"
    assert "quizDistributionChart" in content, "Missing quizDistributionChart in HTML"
    assert "O'qituvchilarning To'liq Statistikasi" in content, "Missing teachers table in HTML"
    assert "Oylik Jami Maosh Fondi" in content, "Missing total payroll in HTML"
    assert "5 Asosiy Ta'lim Yo'nalishlari" in content, "Missing clusters in HTML"
    print("   [OK] All 4 Chart.js charts and teacher statistics table rendered properly.")

    # 3. Direct view call with RequestFactory to check context
    from django.test import RequestFactory
    from core import views
    factory = RequestFactory()
    req = factory.get('/statistics/')
    resp = views.statistics_view(req)
    assert resp.status_code == 200
    print("   [OK] views.statistics_view executed directly with HTTP 200.")

    # 4. Check navbar link in home page
    home_resp = client.get(reverse('home'))
    assert home_resp.status_code == 200
    home_html = home_resp.content.decode('utf-8')
    assert url in home_html, "Statistics URL not found in Navbar"
    print("   [OK] Navbar link to /statistics/ confirmed on homepage.")

    print("\nALL STATISTICS TESTS PASSED SUCCESSFULLY! [OK]")

if __name__ == '__main__':
    run_tests()
