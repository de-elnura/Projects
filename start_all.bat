@echo off
chcp 65001 >nul
title SkillUp / EduQuiz LMS - Ishga Tushirish
color 0b

echo ======================================================================
echo    🎓 SkillUp / EduQuiz LMS - Boshqaruv Markazi
echo ======================================================================
echo.
echo [1/2] Django Veb-Serveri ishga tushirilmoqda (http://127.0.0.1:8000)...
start "SkillUp LMS Web Server" cmd /k "python manage.py runserver"

echo [2/2] Telegram Bot xizmati ishga tushirilmoqda...
start "SkillUp Telegram Bot" cmd /k "python manage.py run_bot"

echo.
echo ======================================================================
echo  [OK] Ikkala xizmat alohida konsollarda muvaffaqiyatli ishga tushdi!
echo  Brauzerda http://127.0.0.1:8000 manziliga kirishingiz mumkin.
echo ======================================================================
echo.
pause
