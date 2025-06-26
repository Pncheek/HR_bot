import os 
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
)
import database as db

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

REVIEW, MEETING_DATE = range(2)

BACK_BUTTON_CALLBACK = "back_to_start"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    welcome_text = (
        "Вы попали в чат-бот группы компаний VR LOGISTIC. В нашу группу компаний входит ряд организаций, "
        "чья специфика работы так или иначе связана с международной деятельностью.\n\n"
        "Что я умею:\n"
        "- Отвечаю на часто задаваемые вопросы\n"
        "- Помогу сориентироваться в компании\n"
        "- Предоставляю важную информацию быстро и удобно"
    )

    buttons = [
        [InlineKeyboardButton("Контакты", callback_data="contacts")],
        [InlineKeyboardButton("Видео", callback_data="video")],
        [InlineKeyboardButton("Презентация", callback_data="presentation")],
        [InlineKeyboardButton("Программы", callback_data="programs")],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(welcome_text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == "contacts":
        await contacts(update, context)
    elif query.data == "video":
        await send_video(update, context)
    elif query.data == "presentation":
        await send_presentation(update, context)
    elif query.data == "programs":
        await send_programs(update, context)
    elif query.data == BACK_BUTTON_CALLBACK:
        await start(update, context)

def get_back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Назад", callback_data=BACK_BUTTON_CALLBACK)]
    ])

async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    contacts_text = "Контакты HR-отдела:\n\n• Email: hr@vrlogistic.com\n• Телефон: +7 (XXX) XXX-XX-XX"
    if update.callback_query:
        await update.callback_query.edit_message_text(
            contacts_text, 
            reply_markup=get_back_keyboard()
        )
    else:
        await update.message.reply_text(
            contacts_text, 
            reply_markup=get_back_keyboard()
        )

async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        await update.callback_query.message.reply_video(
            video=open("assets/office_tour.mp4", "rb"),
            reply_markup=get_back_keyboard()
        )
    else:
        await update.message.reply_video(
            video=open("assets/office_tour.mp4", "rb"),
            reply_markup=get_back_keyboard()
        )

async def send_presentation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        await update.callback_query.message.reply_document(
            document=open("assets/presentation.pdf", "rb"),
            reply_markup=get_back_keyboard()
        )
    else:
        await update.message.reply_document(
            document=open("assets/presentation.pdf", "rb"),
            reply_markup=get_back_keyboard()
        )

async def send_programs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    programs_text = "Используемые программы:\n\n• 1C\n• SAP\n• Microsoft Teams\n• Jira"
    if update.callback_query:
        await update.callback_query.edit_message_text(
            programs_text, 
            reply_markup=get_back_keyboard()
        )
    else:
        await update.message.reply_text(
            programs_text, 
            reply_markup=get_back_keyboard()
        )

async def handle_review(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Пожалуйста, оставьте ваш отзыв:")
    return REVIEW

async def save_review(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    review_text = update.message.text
    
    db.save_review(user.id, user.username, review_text)
    await update.message.reply_text("Спасибо за ваш отзыв! 💙")
    
    return ConversationHandler.END

async def set_meeting_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("📅 Укажите дату встречи в формате ДД.ММ.ГГГГ:")
    return MEETING_DATE

async def save_meeting_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.message.chat_id
    date_str = update.message.text
    
    try:
        meeting_date = datetime.strptime(date_str, "%d.%m.%Y")
        now = datetime.now()
        
        if meeting_date < now:
            await update.message.reply_text("❌ Дата должна быть в будущем!")
            return MEETING_DATE
        
        db.save_meeting(chat_id, meeting_date)
        reminder_time = meeting_date - timedelta(days=1)
        
        context.job_queue.run_once(
            send_meeting_reminder,
            when=reminder_time,
            chat_id=chat_id,
            name=f"meeting_reminder_{chat_id}",
        )
        
        await update.message.reply_text("✅ Напоминание установлено!")
        
    except ValueError:
        await update.message.reply_text("❌ Неверный формат даты! Используйте ДД.ММ.ГГГГ")
        return MEETING_DATE
    
    return ConversationHandler.END

async def send_meeting_reminder(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    await context.bot.send_message(
        job.chat_id,
        "⏰ Напоминание: завтра у вас запланирована встреча с HR!",
    )

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("review", handle_review))
    

    application.add_handler(CallbackQueryHandler(button_handler))
    

    review_handler = ConversationHandler(
        entry_points=[CommandHandler("review", handle_review)],
        states={
            REVIEW: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_review)],
        },
        fallbacks=[],
    )
    application.add_handler(review_handler)
    

    meeting_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Напомнить о встрече$"), set_meeting_reminder)],
        states={
            MEETING_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_meeting_date)],
        },
        fallbacks=[],
    )
    application.add_handler(meeting_handler)
    
    application.run_polling()

if __name__ == "__main__":
    main()
