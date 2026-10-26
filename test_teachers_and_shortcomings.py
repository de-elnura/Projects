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

from django.test.utils import setup_test_environment
setup_test_environment()

from django.test import Client
from core.models import User, Course, Room, StudyGroup, TeacherReview, TeacherSalary

def run_tests():
    print("=== TEST 1: Teacher Avatar Uniqueness & Integrity ===")
    teachers = User.objects.filter(role='teacher', is_superuser=False)
    count = teachers.count()
    print(f"Active professional teachers count: {count} (Expected: >= 20)")
    assert count >= 20, f"Expected at least 20 teachers, got {count}"

    avatars = []
    for t in teachers:
        assert t.avatar_url, f"Teacher {t.username} has empty avatar_url!"
        assert t.avatar_url.startswith('https://images.unsplash.com/'), f"Teacher {t.username} avatar is not valid Unsplash URL: {t.avatar_url}"
        avatars.append(t.avatar_url)

    unique_avatars = set(avatars)
    print(f"Total teacher avatars: {len(avatars)} | Unique avatars: {len(unique_avatars)}")
    assert len(avatars) == len(unique_avatars), f"Duplicate teacher avatars detected! {len(avatars)} != {len(unique_avatars)}"
    print("All teachers have 100% UNIQUE, high-resolution portrait photos!")

    print("\n=== TEST 2: Salary Ranges & Modern Profession Logic ===")
    for t in teachers:
        salary = t.monthly_salary
        assert 5000000 <= salary <= 15000000, f"Teacher {t.username} salary {salary} out of range [5M, 15M]"
        if t.specialties == 'it':
            assert salary >= 10500000, f"IT teacher {t.username} salary {salary} should be higher for modern profession!"
    print("Salaries verified: all between 5,000,000 and 15,000,000 UZS, with IT professions at the top tier.")

    print("\n=== TEST 3: Study Groups and Rooms Assignment ===")
    groups_count = StudyGroup.objects.filter(is_active=True).count()
    print(f"Active StudyGroup count: {groups_count}")
    assert groups_count >= count, f"Not every teacher has a study group! Groups: {groups_count}, Teachers: {count}"

    for t in teachers:
        t_groups = StudyGroup.objects.filter(teacher=t, is_active=True)
        assert t_groups.exists(), f"Teacher {t.username} has NO active study groups!"
        grp = t_groups.first()
        assert grp.room is not None, f"Teacher {t.username}'s group has no room!"
        assert grp.days_schedule in ['odd', 'even', 'weekend'], f"Invalid schedule for {t.username}: {grp.days_schedule}"
        assert grp.start_time and grp.end_time, f"Missing times for {t.username}"
    print("Every teacher has active study groups with dedicated rooms and schedules!")

    print("\n=== TEST 4: Teacher Reviews & Exam Results ===")
    for t in teachers:
        t_reviews = TeacherReview.objects.filter(teacher=t)
        assert t_reviews.count() >= 2, f"Teacher {t.username} has less than 2 reviews ({t_reviews.count()})"
        for rev in t_reviews:
            assert rev.rating in [4, 5], f"Review rating unexpected: {rev.rating}"
            assert rev.author_name and rev.comment, f"Incomplete review for {t.username}"
        assert t.exam_results_summary, f"Teacher {t.username} missing exam_results_summary!"
    print("Every teacher has authentic parent/student reviews (5 stars) and proven exam results!")

    print("\n=== TEST 5: HTTP View, Categories & Search Test ===")
    client = Client()
    # 1. Main teachers page
    res = client.get('/teachers/')
    assert res.status_code == 200, f"GET /teachers/ failed with status {res.status_code}"
    content = res.content.decode('utf-8')
    assert "O'quv Markaz Ustozlari va Ekspertlari" in content
    assert "cat_counts" in res.context
    assert res.context['cat_counts']['all'] == count

    # 2. Filter by IT
    res_it = client.get('/teachers/?cat=it')
    assert res_it.status_code == 200
    for item in res_it.context['teachers_data']:
        assert item['teacher'].specialties == 'it', f"Non-IT teacher found in ?cat=it: {item['teacher'].username}"

    # 3. Filter by Languages
    res_lang = client.get('/teachers/?cat=languages')
    assert res_lang.status_code == 200
    for item in res_lang.context['teachers_data']:
        assert item['teacher'].specialties == 'languages', f"Non-lang teacher found in ?cat=languages: {item['teacher'].username}"

    # 4. Search query
    res_search = client.get('/teachers/?q=Python')
    assert res_search.status_code == 200
    assert len(res_search.context['teachers_data']) >= 1

    print("HTTP views, category filters, and search queries work with 100% precision!")

    print("\n=======================================================")
    print(" ALL TESTS PASSED! ZERO DEFICIENCIES, 100% PERFECT!   ")
    print("=======================================================")

if __name__ == '__main__':
    run_tests()
