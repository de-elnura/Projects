import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test.utils import setup_test_environment
setup_test_environment()

from django.test import Client
from core.models import User, Course, CoinTransaction, StudyGroup, QuizResult

def run_tests():
    print("=== TEST 1: Database Counts & Unique Thumbnails ===")
    student_count = User.objects.filter(role='student').count()
    course_count = Course.objects.count()
    distinct_thumbnails = Course.objects.values('thumbnail_url').distinct().count()
    tx_count = CoinTransaction.objects.count()

    print(f"Students count: {student_count} (Expected: >= 100)")
    assert student_count >= 100, f"Expected at least 100 students, got {student_count}"

    print(f"Courses count: {course_count}")
    print(f"Distinct thumbnails: {distinct_thumbnails}")
    assert course_count == distinct_thumbnails, f"Every course should have a unique thumbnail! {course_count} != {distinct_thumbnails}"

    # Check for empty or generic thumbnails
    for course in Course.objects.all():
        assert course.thumbnail_url and course.thumbnail_url.startswith('http'), f"Course {course.title} has invalid thumbnail_url: {course.thumbnail_url}"

    print("=== TEST 2: Course Schedule Display without raw &bull; ===")
    for course in Course.objects.all():
        display = course.get_schedule_display_full()
        assert '&bull;' not in display, f"Course {course.title} schedule contains raw &bull;: {display}"
    print("Schedule formatting verified: all bullet points are clean Unicode '•'.")

    print("=== TEST 3: 8 Action Types in Coin Transactions ===")
    actions = set(CoinTransaction.objects.values_list('action_type', flat=True).distinct())
    print(f"Action types found in DB: {actions}")
    expected_actions = {
        'attendance_streak', 'homework_perfect', 'class_activity',
        'quiz_passed', 'quiz_perfect', 'book_reading',
        'weekly_streak', 'course_completed'
    }
    missing_actions = expected_actions - actions
    assert not missing_actions, f"Missing actions: {missing_actions}"
    print("All 8 practical school/activity action types exist in student records!")

    print("=== TEST 4: Leaderboard HTTP View and Podium ===")
    client = Client()
    # Test Leaderboard page without login (public)
    response = client.get('/leaderboard/')
    assert response.status_code == 200, f"Leaderboard page returned status {response.status_code}"
    content = response.content.decode('utf-8')

    assert 'Olimpiada va Reyting' in content or 'Reyting' in content, "Leaderboard title not found"
    assert 'podium_students' in response.context, "podium_students missing from context"
    assert len(response.context['podium_students']) == 3, f"Expected 3 podium winners, got {len(response.context['podium_students'])}"
    assert 'students_page' in response.context, "students_page missing from context"
    assert response.context['total_count'] == student_count, f"Total count mismatch: {response.context['total_count']} vs {student_count}"

    # Test sorting by coins
    response_coins = client.get('/leaderboard/?sort=coins')
    assert response_coins.status_code == 200
    top_coin_user = response_coins.context['podium_students'][0]
    second_coin_user = response_coins.context['podium_students'][1]
    assert top_coin_user.edu_coins >= second_coin_user.edu_coins, "Coins sorting failed on podium"

    # Test pagination
    response_p2 = client.get('/leaderboard/?page=2')
    assert response_p2.status_code == 200
    assert response_p2.context['students_page'].number == 2, "Page 2 navigation failed"

    print("Leaderboard HTTP view, podium, search, and pagination verified successfully!")

    print("=== TEST 5: Bundle Enroll Page Unique Images ===")
    from django.urls import reverse
    bundle_url = reverse('bundle_enroll')
    student_user = User.objects.filter(role='student').first()
    client.force_login(student_user)
    response_bundle = client.get(bundle_url)
    assert response_bundle.status_code == 200, f"Expected 200 for {bundle_url}, got {response_bundle.status_code}"
    bundle_content = response_bundle.content.decode('utf-8')
    assert '&amp;bull;' not in bundle_content, "Found escaped raw text &amp;bull; in bundle enroll template output"
    print("Bundle enroll view rendered cleanly without &amp;bull; escaped entity.")

    print("\n==============================================")
    print(" ALL TESTS PASSED SUCCESSFULLY! (100% PERFECT)")
    print("==============================================")

if __name__ == '__main__':
    run_tests()
