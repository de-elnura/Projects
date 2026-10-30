import os
import asyncio
import logging
from asgiref.sync import sync_to_async

from aiogram import Bot, Dispatcher, F, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from django.conf import settings
from django.contrib.auth import authenticate

logger = logging.getLogger(__name__)

# FSM Holatlari: Saytdagi akkauntni Telegram bilan bog'lash
class LinkAccountStates(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()


# Asosiy Menyu Tugmalari
def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="👤 Mening Profilim / EduCoin"),
                KeyboardButton(text="📚 Mening Kurslarim")
            ],
            [
                KeyboardButton(text="🏆 Reyting (Leaderboard)"),
                KeyboardButton(text="🌐 Barcha Kurslar")
            ],
            [
                KeyboardButton(text="🔗 Akkauntni bog'lash"),
                KeyboardButton(text="📞 Qo'llab-quvvatlash")
            ]
        ],
        resize_keyboard=True
    )


def get_cancel_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
        resize_keyboard=True
    )


# =============================================================================
# Django ORM Asinxron Yordamchilari
# =============================================================================
@sync_to_async
def get_user_by_telegram_id(chat_id):
    from core.models import TelegramProfile
    try:
        profile = TelegramProfile.objects.select_related('user').get(telegram_chat_id=str(chat_id))
        return profile.user
    except TelegramProfile.DoesNotExist:
        return None


@sync_to_async
def link_telegram_account(chat_id, telegram_username, username, password):
    from core.models import TelegramProfile
    user = authenticate(username=username, password=password)
    if not user:
        return False, "Kiritilgan login yoki parol noto'g'ri."

    # Avvalgi bog'lanishlarni tozalash (1 ta telegram = 1 ta profil)
    TelegramProfile.objects.filter(telegram_chat_id=str(chat_id)).delete()
    TelegramProfile.objects.filter(user=user).delete()

    TelegramProfile.objects.create(
        user=user,
        telegram_chat_id=str(chat_id),
        telegram_username=telegram_username or ''
    )
    return True, user


@sync_to_async
def get_leaderboard_data(limit=10):
    from core.models import User
    users = User.objects.filter(role='student').order_by('-edu_coins', '-total_xp')[:limit]
    data = []
    for u in users:
        data.append({
            'name': f"{u.first_name} {u.last_name}".strip() or u.username,
            'username': u.username,
            'coins': u.edu_coins,
            'xp': u.total_xp,
            'vip': u.has_vip_badge,
        })
    return data


@sync_to_async
def get_courses_list(limit=8):
    from core.models import Course
    courses = Course.objects.all().select_related('author')[:limit]
    data = []
    for c in courses:
        data.append({
            'title': c.title,
            'author': c.author.get_full_name() if c.author else "Ustoz",
            'price': c.price,
            'is_free': c.is_free,
            'duration': c.duration_hours,
        })
    return data


@sync_to_async
def get_user_courses(user):
    from core.models import Enrollment
    enrollments = Enrollment.objects.filter(user=user).select_related('course')
    data = []
    for en in enrollments:
        data.append({
            'title': en.course.title,
            'status': en.status,
            'created_at': en.created_at.strftime('%d.%m.%Y'),
        })
    return data


# =============================================================================
# Bot Dispatcher va Handlers
# =============================================================================
dp = Dispatcher(storage=MemoryStorage())


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    full_name = html.bold(message.from_user.full_name)
    user = await get_user_by_telegram_id(message.from_user.id)
    
    extra_text = ""
    if user:
        extra_text = f"\n\n✅ <i>Sizning saytdagi profilingiz bog'langan: <b>{user.username}</b></i>"
    else:
        extra_text = "\n\n💡 <i>Saytdagi profilingizni ulash uchun <b>🔗 Akkauntni bog'lash</b> tugmasini bosing.</i>"

    await message.answer(
        f"Assalomu alaykum, {full_name}! 🎓\n\n"
        "<b>EduQuiz & LMS Ta'lim Platformasi</b> rasmiy botiga xush kelibsiz!"
        f"{extra_text}\n\n"
        "Quyidagi menyudan kerakli bo'limni tanlang:",
        reply_markup=get_main_keyboard()
    )


@dp.message(F.text == "❌ Bekor qilish")
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Amal bekor qilindi.", reply_markup=get_main_keyboard())


@dp.message(F.text == "👤 Mening Profilim / EduCoin")
@dp.message(Command("profile"))
async def profile_handler(message: Message):
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user:
        await message.answer(
            "⚠️ <b>Siz hali profilingizni Telegramga ulamagansiz!</b>\n\n"
            "EduCoin balansingiz, XP va kurslaringizni ko'rish uchun "
            "<b>🔗 Akkauntni bog'lash</b> tugmasini bosing.",
            reply_markup=get_main_keyboard()
        )
        return

    vip_badge = "🌟 Oltin VIP Profil" if user.has_vip_badge else "Oddiy a'zo"
    name = f"{user.first_name} {user.last_name}".strip() or user.username
    role_display = "Talaba" if user.role == 'student' else "O'qituvchi"
    stats = await sync_to_async(lambda: user.learning_stats)()

    text = (
        f"👤 <b>Foydalanuvchi Profili</b>\n\n"
        f"• <b>Ism-familiya:</b> {name}\n"
        f"• <b>Username:</b> @{user.username}\n"
        f"• <b>Rol:</b> {role_display}\n"
        f"• 🪙 <b>EduCoin balansi:</b> {user.edu_coins:,} 🪙\n"
        f"• ⚡ <b>Umumiy XP:</b> {user.total_xp:,} XP\n"
        f"• 📝 <b>Ishlangan savollar:</b> {stats['questions_display']} ta\n"
        f"• 📚 <b>Tugatilgan darslar:</b> {stats['lessons_display']} ta\n"
        f"• 🎖️ <b>Maqomi:</b> {vip_badge}\n"
    )
    if user.headline:
        text += f"• 💼 <b>Mutaxassislik:</b> {user.headline}\n"

    await message.answer(text, reply_markup=get_main_keyboard())


@dp.message(F.text == "📚 Mening Kurslarim")
@dp.message(Command("mycourses"))
async def my_courses_handler(message: Message):
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user:
        await message.answer(
            "⚠️ Kurslaringizni ko'rish uchun avval profilingizni botga ulang.\n"
            "Buning uchun <b>🔗 Akkauntni bog'lash</b> tugmasini bosing.",
            reply_markup=get_main_keyboard()
        )
        return

    courses = await get_user_courses(user)
    if not courses:
        await message.answer(
            "📚 Siz hozircha hech qaysi kursga a'zo emassiz.\n"
            "Saytga kirib yangi kurslarga yozilishingiz mumkin!",
            reply_markup=get_main_keyboard()
        )
        return

    text = "📚 <b>Siz a'zo bo'lgan kurslar:</b>\n\n"
    for idx, c in enumerate(courses, 1):
        status_icon = "🟢 Faol" if c['status'] == 'completed' else "📘 O'qilmoqda"
        text += f"{idx}. <b>{c['title']}</b>\n   Holati: {status_icon} (A'zolik: {c['created_at']})\n\n"

    await message.answer(text, reply_markup=get_main_keyboard())


@dp.message(F.text == "🌐 Barcha Kurslar")
@dp.message(Command("courses"))
async def all_courses_handler(message: Message):
    courses = await get_courses_list(8)
    if not courses:
        await message.answer("Hozircha kurslar topilmadi.")
        return

    text = "🌐 <b>Platformadagi eng sara kurslar:</b>\n\n"
    for idx, c in enumerate(courses, 1):
        price_str = "Bepul" if c['is_free'] else f"{c['price']:,.0f} so'm"
        text += (
            f"<b>{idx}. {c['title']}</b>\n"
            f"   👨‍🏫 Ustoz: {c['author']}\n"
            f"   ⏱ Davomiyligi: {c['duration']} soat\n"
            f"   💵 Narxi: {price_str}\n\n"
        )

    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌐 Saytda barchasini ko'rish", url="http://127.0.0.1:8000/courses/")]
        ]
    )
    await message.answer(text, reply_markup=inline_kb)


@dp.message(F.text == "🏆 Reyting (Leaderboard)")
@dp.message(Command("leaderboard"))
async def leaderboard_handler(message: Message):
    leaders = await get_leaderboard_data(10)
    if not leaders:
        await message.answer("Reyting ma'lumotlari mavjud emas.")
        return

    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    text = "🏆 <b>Eng faol talabalar reytingi (Top 10):</b>\n\n"
    for i, leader in enumerate(leaders):
        icon = medals[i] if i < len(medals) else f"{i+1}."
        vip_star = "🌟 " if leader['vip'] else ""
        text += f"{icon} {vip_star}<b>{leader['name']}</b> (@{leader['username']})\n"
        text += f"   🪙 {leader['coins']} EduCoin | ⚡ {leader['xp']} XP\n\n"

    await message.answer(text, reply_markup=get_main_keyboard())


@dp.message(F.text == "📞 Qo'llab-quvvatlash")
@dp.message(Command("help"))
async def help_handler(message: Message):
    text = (
        "📞 <b>Qo'llab-quvvatlash va Aloqa Markazi</b>\n\n"
        "Platformadan foydalanishda savollaringiz yoki texnik muammolar bo'lsa, "
        "biz bilan bog'lanishingiz mumkin:\n\n"
        "🌐 <b>Veb-sayt:</b> http://127.0.0.1:8000/\n"
        "👨‍💼 <b>Administrator:</b> @admin\n"
        "📞 <b>Aloqa telefoni:</b> +998 71 200-00-00\n"
        "⏰ <b>Ish vaqti:</b> 09:00 - 18:00 (Dush - Shanba)\n\n"
        "<i>EduQuiz & LMS jamoasi sizga muvaffaqiyatli ta'lim tilaydi!</i>"
    )
    await message.answer(text, reply_markup=get_main_keyboard())


# =============================================================================
# Akkauntni bog'lash FSM zanjiri
# =============================================================================
@dp.message(F.text == "🔗 Akkauntni bog'lash")
@dp.message(Command("link"))
async def start_linking(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    if user:
        await message.answer(
            f"ℹ️ Sizning Telegramingiz allaqachon <b>{user.username}</b> akkauntiga bog'langan.\n\n"
            "Boshqa akkauntga almashtirish uchun saytdagi yangi <b>Username (login)</b>ingizni kiriting:",
            reply_markup=get_cancel_keyboard()
        )
    else:
        await message.answer(
            "🔗 <b>Saytdagi profilingizni ulash</b>\n\n"
            "Iltimos, saytdagi <b>Foydalanuvchi nomingizni (Username)</b> kiriting:",
            reply_markup=get_cancel_keyboard()
        )
    await state.set_state(LinkAccountStates.waiting_for_username)


@dp.message(LinkAccountStates.waiting_for_username)
async def process_username(message: Message, state: FSMContext):
    username = message.text.strip()
    if not username:
        await message.answer("Iltimos, yaroqli foydalanuvchi nomini kiriting:")
        return

    await state.update_data(site_username=username)
    await message.answer(
        f"Foydalanuvchi nomi qabul qilindi: <b>{username}</b>\n\n"
        "Endi ushbu akkauntning <b>Parolini</b> kiriting:",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(LinkAccountStates.waiting_for_password)


@dp.message(LinkAccountStates.waiting_for_password)
async def process_password(message: Message, state: FSMContext):
    password = message.text.strip()
    data = await state.get_data()
    username = data.get('site_username')
    await state.clear()

    # Xavfsizlik maqsadida foydalanuvchi yuborgan parol xabarini darhol o'chirishga harakat qilamiz
    try:
        await message.delete()
    except Exception:
        pass

    success, result = await link_telegram_account(
        chat_id=message.from_user.id,
        telegram_username=message.from_user.username,
        username=username,
        password=password
    )

    if success:
        user = result
        name = f"{user.first_name} {user.last_name}".strip() or user.username
        await message.answer(
            f"🎉 <b>Tabriklaymiz, {name}!</b>\n\n"
            f"Sizning Telegramingiz <b>@{user.username}</b> profilingiz bilan muvaffaqiyatli bog'landi!\n"
            f"🪙 EduCoin balansingiz: <b>{user.edu_coins:,} 🪙</b>\n\n"
            "Endi siz bot orqali o'z profilingiz va kurslaringizni to'liq kuzatishingiz mumkin.",
            reply_markup=get_main_keyboard()
        )
    else:
        await message.answer(
            f"❌ <b>Xatolik:</b> {result}\n\n"
            "Login yoki parolni tekshirib qaytadan urinib ko'ring yoki /start bosing.",
            reply_markup=get_main_keyboard()
        )


# =============================================================================
# Botni ishga tushirish funksiyasi
# =============================================================================
async def run_telegram_bot():
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None) or os.getenv('BOT_TOKEN')
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN sozlanmagan!")
        print("Xatolik: TELEGRAM_BOT_TOKEN sozlanmagan!")
        return

    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    print(f"🤖 Telegram Bot muvaffaqiyatli ishga tushdi...")
    print(f"📡 Polling kutilmoqda. To'xtatish uchun: Ctrl + C")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
