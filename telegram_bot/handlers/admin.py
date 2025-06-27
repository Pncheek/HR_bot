from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from .base import BaseHandler

class AdminHandler(BaseHandler):
    async def show_feedback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        
        if not self.is_user_allowed(user.id):
            await update.message.reply_text("⚠️ У вас нет доступа к этой команде")
            return
        
        feedbacks = self.db.get_all_feedbacks()
        survey_responses = self.db.get_all_survey_responses()
        
        
        response = "📝 Отзывы:\n\n"
        for fb in feedbacks:
            response += f"👤 {fb['username']} ({fb['date']}):\n{fb['text']}\n\n"
        
        response += "\n📊 Ответы на опросы:\n\n"
        for sr in survey_responses:
            response += f"🔹 {sr['survey_type']} - {sr['username']} ({sr['date']}):\n{sr['response']}\n\n"
        
        await update.message.reply_text(response[:4000])

    def get_admin_handlers(self):
        return [CommandHandler("show_data", self.show_feedback)]