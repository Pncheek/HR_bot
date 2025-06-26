from datetime import datetime, timedelta
from telegram.ext import CallbackContext

class NotificationService:
    def __init__(self, db):
        self.db = db
    
    async def create_notification(self, user_id: int, username: str, date_text: str, notification_text: str, chat_id: int, context: CallbackContext):
        """Создает напоминание и планирует его отправку"""
        try:
            notification_date = datetime.strptime(date_text, '%d.%m.%Y').date()
            
            self.db.add_notification(
                user_id,
                username,
                notification_date.strftime('%Y-%m-%d'),
                notification_text,
                chat_id
            )

            self.schedule_reminder(notification_date, notification_text, chat_id, context)
            return True, notification_date
        except ValueError:
            return False, None
    
    def schedule_reminder(self, notification_date, notification_text, chat_id, context):
        """Планирует отправку напоминания"""
        reminder_date = notification_date - timedelta(days=1)
        delay = (reminder_date - datetime.now().date()).total_seconds()
        
        if delay > 0:
            context.job_queue.run_once(
                self.send_reminder,
                delay,
                chat_id=chat_id,
                data={
                    'text': notification_text,
                    'date': notification_date.strftime('%d.%m.%Y')
                },
                name=f"reminder_{chat_id}_{notification_date}"
            )
    
    async def send_reminder(self, context: CallbackContext):
        """Отправляет напоминание пользователю"""
        job = context.job
        await context.bot.send_message(
            job.chat_id,
            f'🔔 Напоминание: {job.data["text"]} (завтра, {job.data["date"]})'
        )