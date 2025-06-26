from datetime import timedelta
from telegram.ext import CallbackContext

class SurveyScheduler:
    def __init__(self, db):
        self.db = db
    
    def schedule_surveys(self, user_id: int, username: str, context: CallbackContext):
        first_message_date = self.db.get_user_first_message_date(user_id)
        if not first_message_date:
            return
        
        surveys = [
            {"days": 1, "name": "1 день", "job_name": f"{user_id}_survey_1day"},
            {"weeks": 1, "name": "1 неделя", "job_name": f"{user_id}_survey_1week"},
            {"days": 30, "name": "1 месяц", "job_name": f"{user_id}_survey_1month"},
            {"days": 90, "name": "3 месяца", "job_name": f"{user_id}_survey_3months"},
        ]
        
        for survey in surveys:
            context.job_queue.run_once(
                callback=self.send_survey_callback,
                when=timedelta(**{k: v for k, v in survey.items() if k in ["days", "weeks"]}),
                chat_id=user_id,
                data={"survey_type": survey["name"]},
                name=survey["job_name"]
            )
    
    async def send_survey_callback(self, context: CallbackContext):
        job = context.job
        user_id = job.chat_id
        survey_type = job.data["survey_type"]

        questions = {
            "1 день": "Как ваше впечатление после первого дня работы с нами?",
            "1 неделя": "Как ваше впечатление после недели работы с нами?",
            "1 месяц": "Как ваше впечатление после месяца работы с нами?",
            "3 месяца": "Как ваше впечатление после трех месяцев работы с нами?",
        }

        question = questions.get(survey_type, "Пожалуйста, оцените нашу работу:")
        
        await context.bot.send_message(
            chat_id=user_id,
            text=f"{question}\nПожалуйста, ответьте одним сообщением."
        )