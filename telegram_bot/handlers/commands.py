from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, Application
import logging
from .base import BaseHandler

logger = logging.getLogger(__name__)

class CommandHandler(BaseHandler):
    def __init__(self, db, scheduler):
        super().__init__(db, scheduler)  


    async def test_keyboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Простейшая клавиатура с одной кнопкой
        await update.message.reply_text(
            "Тест кнопки Назад",
            reply_markup=self.get_back_keyboard()
        )
        print(f"Generated keyboard: {self.get_back_keyboard()}")

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        welcome_text = (
            "Вы попали в чат-бот группы компаний VR LOGISTIC. В нашу группу компаний входит ряд организаций, "
            "чья специфика работы так или иначе связана с международной деятельностью.\n\n"
            "Что я умею:\n"
            "- Отвечаю на часто задаваемые вопросы\n"
            "- Помогу сориентироваться в компании\n"
            "- Предоставляю важную информацию быстро и удобно\n"
            'чтобы в последствии вернуться на это сообщение напиши мне "/back"'
        )

        self.db.set_user_first_message_date(user.id, user.username)
        
        # Используем планировщик для настройки опросов
        if self.scheduler:
            self.scheduler.schedule_surveys(user.id, user.username, context)

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

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        logger.info(f"Received callback: {query.data}")
        await query.answer()
        
        if query.data == "contacts":
            await self.contacts(update, context)
        elif query.data == "programs":
            await self.send_programs(update, context)
        elif query.data == "Назад":
            await self.start(update, context)
    
    async def contacts(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                "Контакты HR-отдела:\n\n• Email: hr@vrlogistic.com\n• Телефон: +7 (XXX) XXX-XX-XX"
            )
        else:
            await update.message.reply_text(
                "Контакты HR-отдела:\n\n• Email: hr@vrlogistic.com\n• Телефон: +7 (XXX) XXX-XX-XX" 
            )
    
    async def send_programs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        "this is program we are working with."
        if update.callback_query:
            await update.callback_query.edit_message_text(
                "this is program we are working with."
                
            )
        else:
            await update.message.reply_text(
                "this is program we are working with."
                
            )
    async def get_back(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        welcome_text = (
            "Вы попали в чат-бот группы компаний VR LOGISTIC. В нашу группу компаний входит ряд организаций, "
            "чья специфика работы так или иначе связана с международной деятельностью.\n\n"
            "Что я умею:\n"
            "- Отвечаю на часто задаваемые вопросы\n"
            "- Помогу сориентироваться в компании\n"
            "- Предоставляю важную информацию быстро и удобно\n"
            'чтобы в последствии вернуться на это сообщение напиши мне "/back"'

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
