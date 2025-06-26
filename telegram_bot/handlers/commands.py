from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from .base import BaseHandler

class CommandHandler(BaseHandler):
    def __init__(self, db, scheduler):
        super().__init__(db, scheduler) 
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        welcome_text = (
            "Вы попали в чат-бот группы компаний VR LOGISTIC. В нашу группу компаний входит ряд организаций, "
            "чья специфика работы так или иначе связана с международной деятельностью.\n\n"
            "Что я умею:\n"
            "- Отвечаю на часто задаваемые вопросы\n"
            "- Помогу сориентироваться в компании\n"
            "- Предоставляю важную информацию быстро и удобно"
        )

        self.db.set_user_first_message_date(user.id, user.username)

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
    
    async def contacts(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        contacts_text = "Контакты HR-отдела:\n\n• Email: hr@vrlogistic.com\n• Телефон: +7 (XXX) XXX-XX-XX"
        if update.callback_query:
            await update.callback_query.edit_message_text(
                contacts_text, 
                reply_markup=self.get_back_keyboard()
            )
        else:
            await update.message.reply_text(
                contacts_text, 
                reply_markup=self.get_back_keyboard()
            )
    
    async def send_programs(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        programs_text = "Используемые программы:\n\n• 1C\n• SAP\n• Microsoft Teams\n• Jira"
        if update.callback_query:
            await update.callback_query.edit_message_text(
                programs_text, 
                reply_markup=self.get_back_keyboard()
            )
        else:
            await update.message.reply_text(
                programs_text, 
                reply_markup=self.get_back_keyboard()
            )
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        
        if query.data == "contacts":
            await self.contacts(update, context)
        elif query.data == "programs":
            await self.send_programs(update, context)
        elif query.data == self.BACK_BUTTON_CALLBACK:
            await self.start(update, context)