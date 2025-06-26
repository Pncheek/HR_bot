from telegram import Update, ReplyKeyboardRemove
from datetime import datetime, timedelta
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters
)
from .base import BaseHandler

# Состояния для диалога отзыва
REVIEW = 1

class ReviewConversationHandler(BaseHandler):
    def get_conversation_handler(self):
        return ConversationHandler(
            entry_points=[CommandHandler('review', self.review)],
            states={
                REVIEW: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.save_review)],
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
        )

    async def review(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text('Пожалуйста, оставьте ваш отзыв о компании одним сообщением:')
        return REVIEW

    async def save_review(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user = update.effective_user
        review_text = update.message.text
        
        self.db.add_review(user.id, user.username, review_text)
        await update.message.reply_text('Спасибо за ваш отзыв!')
        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text('Операция отменена.', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


# Состояния для диалога напоминания
NOTIFICATION_DATE, NOTIFICATION_TEXT = range(2)

class NotificationConversationHandler(BaseHandler):
    def get_conversation_handler(self):
        return ConversationHandler(
            entry_points=[CommandHandler('notification', self.notification)],
            states={
                NOTIFICATION_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_notification_date)],
                NOTIFICATION_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.save_notification)],
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
        )

    async def notification(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text('Пожалуйста, укажите дату, на которую надо поставить напоминание о встрече в формате ДД.ММ.ГГГГ')
        return NOTIFICATION_DATE

    async def get_notification_date(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user = update.effective_user
        date_text = update.message.text
        
        try:
            notification_date = datetime.strptime(date_text, '%d.%m.%Y').date()
            context.user_data['notification_date'] = notification_date
            
            await update.message.reply_text('Теперь введите текст напоминания:')
            return NOTIFICATION_TEXT
        except ValueError:
            await update.message.reply_text('Неправильный формат даты. Пожалуйста, укажите дату в формате ДД.ММ.ГГГГ')
            return NOTIFICATION_DATE

    async def save_notification(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user = update.effective_user
        notification_text = update.message.text
        notification_date = context.user_data['notification_date']
        
        self.db.add_notification(
            user.id,
            user.username,
            notification_date.strftime('%Y-%m-%d'),
            notification_text,
            update.effective_chat.id
        )

        reminder_date = notification_date - timedelta(days=1)
        delay = (reminder_date - datetime.now().date()).total_seconds()
        
        if delay > 0:
            context.job_queue.run_once(
                self.send_reminder,
                delay,
                chat_id=update.effective_chat.id,
                data={
                    'text': notification_text,
                    'date': notification_date.strftime('%d.%m.%Y')
                },
                name=f"reminder_{user.id}_{notification_date}"
            )
        
        await update.message.reply_text(
            f'Напоминание установлено на {notification_date.strftime("%d.%m.%Y")}. '
            'Вы получите уведомление за день до этой даты.'
        )
        return ConversationHandler.END

    async def send_reminder(self, context: ContextTypes.DEFAULT_TYPE):
        job = context.job
        await context.bot.send_message(
            job.chat_id,
            f'🔔 Напоминание: {job.data["text"]} (завтра, {job.data["date"]})'
        )

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text('Операция отменена.', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END