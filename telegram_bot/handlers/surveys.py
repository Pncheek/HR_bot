from datetime import timedelta
from telegram import Update
from telegram.ext import ContextTypes, CallbackContext
from .base import BaseHandler

class SurveyHandler(BaseHandler):
    def __init__(self, db, scheduler):
        super().__init__(db)
        self.scheduler = scheduler
    
    async def handle_survey_response(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        response_text = update.message.text
        survey_type = context.user_data.get('survey_type', 'unknown')
        
       
        self.db.add_survey_response(
            user.id,
            user.username,
            survey_type,
            response_text
        )
        
        await update.message.reply_text('Спасибо за ваш ответ!')
    
    def schedule_user_surveys(self, user_id: int, username: str, context: ContextTypes.DEFAULT_TYPE):
        """Планирует опросы для нового пользователя"""
        self.scheduler.schedule_surveys(user_id, username, context)
