import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler, JobQueue
from config import Config
from database import Database
from handlers.commands import CommandHandler as CustomCommandHandler
from handlers.conversations import ReviewConversationHandler, NotificationConversationHandler
from handlers.admin import AdminHandler
from services.scheduler import SurveyScheduler
from alembic.config import Config
from alembic import command

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    run_migrations()
    db = Database()
    config = Config()
    
    application = (
        Application.builder()
        .token(config.TOKEN)
        .job_queue(JobQueue())  # Явно указываем JobQueue
        .build()
    )
    
    survey_scheduler = SurveyScheduler(db)
    
    command_handler = CustomCommandHandler(db, survey_scheduler)
    review_handler = ReviewConversationHandler(db)  
    notification_handler = NotificationConversationHandler(db)  
    
    application.add_handler(CommandHandler("start", command_handler.start))
    application.add_handler(review_handler.get_conversation_handler())
    application.add_handler(notification_handler.get_conversation_handler())
    application.add_handler(CallbackQueryHandler(command_handler.button_handler))
    admin_handler = AdminHandler(db)
    for handler in admin_handler.get_admin_handlers():
        application.add_handler(handler)
    
    application.run_polling()

if __name__ == "__main__":
    main()
