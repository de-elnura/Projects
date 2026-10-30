import json
import logging
import urllib.request
import urllib.parse
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


def send_telegram_message(chat_id=None, text="", parse_mode="HTML"):
    """
    Telegram bot orqali ko'rsatilgan chat_id ga xabar yuborish.
    Tarmoq xatolari Django veb-so'rovini to'xtatib qo'ymasligi uchun
    barcha istisnolar xavfsiz tarzda ushlab qolinadi.
    """
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    if not token or not text:
        logger.warning("Telegram xabari yuborilmadi: TOKEN yoki matn mavjud emas.")
        return False

    target_chat_id = chat_id or getattr(settings, 'TELEGRAM_ADMIN_ID', None)
    if not target_chat_id:
        logger.warning("Telegram xabari yuborilmadi: CHAT_ID belgilanmagan.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": target_chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True,
    }

    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status == 200
    except Exception as e:
        logger.error(f"Telegram botga xabar yuborishda xatolik: {e}")
        return False


def send_admin_alert(text):
    """Platforma administratoriga tezkor xabarnoma yuborish."""
    admin_id = getattr(settings, 'TELEGRAM_ADMIN_ID', None)
    return send_telegram_message(chat_id=admin_id, text=text)


def notify_admin_new_user(user):
    """Yangi foydalanuvchi ro'yxatdan o'tganda adminga xabar berish."""
    full_name = f"{user.first_name} {user.last_name}".strip() or user.username
    now_str = timezone.now().strftime("%Y-%m-%d %H:%M")
    
    msg = (
        "🎉 <b>Yangi talaba ro'yxatdan o'tdi!</b>\n\n"
        f"👤 <b>Ism-familiya:</b> {full_name}\n"
        f"🆔 <b>Username:</b> @{user.username}\n"
        f"📧 <b>Email:</b> {user.email or 'Kiritilmagan'}\n"
        f"🎭 <b>Roli:</b> {user.get_role_display()}\n"
        f"🪙 <b>Xush kelibsiz bonusi:</b> +100 EduCoin\n"
        f"⏰ <b>Vaqt:</b> {now_str}\n\n"
        "🔗 <i>Boshqaruv panelida ko'rish: /admin</i>"
    )
    return send_admin_alert(msg)


def notify_admin_new_lead(lead):
    """Yangi mijoz / lid qoldirilganda adminga xabar berish."""
    subject = getattr(lead, 'interested_subject', None) or (lead.course.title if getattr(lead, 'course', None) else "Umumiy ta'lim")
    phone = getattr(lead, 'phone_number', None) or getattr(lead, 'phone', 'Noma\'lum')
    now_str = timezone.now().strftime("%Y-%m-%d %H:%M")
    
    msg = (
        "📥 <b>Yangi murojaat (Lid) qabul qilindi!</b>\n\n"
        f"👤 <b>Mijoz:</b> {lead.full_name}\n"
        f"📞 <b>Telefon:</b> <code>{phone}</code>\n"
        f"📚 <b>Fan/Kurs:</b> {subject}\n"
        f"💬 <b>Izoh:</b> {lead.notes or 'Mavjud emas'}\n"
        f"⏰ <b>Vaqt:</b> {now_str}\n"
    )
    return send_admin_alert(msg)


def notify_admin_new_payment(payment):
    """Talaba to'lov qilganda adminga xabar berish."""
    student_name = payment.student.get_full_name() if getattr(payment, 'student', None) else "Talaba"
    group_name = payment.group.name if getattr(payment, 'group', None) else "Guruhsiz"
    
    msg = (
        "💰 <b>Yangi to'lov tasdiqlandi!</b>\n\n"
        f"👤 <b>Talaba:</b> {student_name}\n"
        f"👥 <b>Guruh:</b> {group_name}\n"
        f"💵 <b>Miqdor:</b> {payment.amount:,.0f} so'm\n"
        f"💳 <b>To'lov turi:</b> {payment.get_payment_type_display() if hasattr(payment, 'get_payment_type_display') else payment.payment_type}\n"
        f"📅 <b>Sana:</b> {payment.payment_date}\n"
    )
    return send_admin_alert(msg)


def notify_admin_teacher_inquiry(inquiry):
    """Ustozga yangi savol yo'llanganda adminga bildirishnoma yuborish."""
    teacher_name = inquiry.teacher.get_full_name() if inquiry.teacher else "Ustoz"
    now_str = timezone.now().strftime("%Y-%m-%d %H:%M")
    
    msg = (
        "❓ <b>Ustozga yangi savol kelib tushdi!</b>\n\n"
        f"👨‍🏫 <b>Qabul qiluvchi ustoz:</b> {teacher_name}\n"
        f"👤 <b>O'quvchi:</b> {inquiry.full_name}\n"
        f"📞 <b>Bog'lanish:</b> <code>{inquiry.phone_number}</code>\n"
        f"📚 <b>Fan:</b> {inquiry.subject}\n"
        f"💬 <b>Savol matni:</b>\n<i>{inquiry.question_text}</i>\n\n"
        f"⏰ <b>Vaqt:</b> {now_str}"
    )
    return send_admin_alert(msg)


def notify_admin_shop_purchase(user, item):
    """EduCoin do'konidan sovg'a yoki xizmat xarid qilinganda adminga bildirishnoma."""
    full_name = f"{user.first_name} {user.last_name}".strip() or user.username
    now_str = timezone.now().strftime("%Y-%m-%d %H:%M")

    msg = (
        "🎁 <b>EduCoin Do'konidan Yangi Xarid!</b>\n\n"
        f"👤 <b>Talaba:</b> {full_name} (@{user.username})\n"
        f"📧 <b>Email:</b> {user.email or 'Kiritilmagan'}\n"
        f"🛍 <b>Mahsulot:</b> {item.title}\n"
        f"🪙 <b>Sarflangan tanga:</b> {item.price_coins} EduCoin\n"
        f"⏰ <b>Vaqt:</b> {now_str}\n\n"
        "ℹ️ <i>Agar xarid murabbiy suhbati yoki merch sovg'asi bo'lsa, talaba bilan tezkor bog'laning.</i>"
    )
    return send_admin_alert(msg)


def notify_admin_attendance_danger(student, group, absence_count=3):
    """Talaba ketma-ket dars qoldirganda adminga tezkor xabar."""
    full_name = f"{student.first_name} {student.last_name}".strip() or student.username
    teacher_name = group.teacher.get_full_name() if group.teacher else "Ustoz"
    now_str = timezone.now().strftime("%Y-%m-%d %H:%M")

    msg = (
        "⚠️ <b>DIQQAT: Ketma-ket dars qoldirish!</b>\n\n"
        f"👤 <b>O'quvchi:</b> {full_name} (@{student.username})\n"
        f"👥 <b>Guruh:</b> {group.name}\n"
        f"👨‍🏫 <b>Ustoz:</b> {teacher_name}\n"
        f"❌ <b>Holat:</b> Ketma-ket {absence_count} ta darsga kelmadi!\n"
        f"⏰ <b>Qayd sanasi:</b> {now_str}\n\n"
        "📞 <i>Iltimos, o'quvchi yoki ota-onasi bilan bog'lanib sababini aniqlang.</i>"
    )
    return send_admin_alert(msg)


