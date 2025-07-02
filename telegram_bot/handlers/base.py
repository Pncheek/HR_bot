from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class BaseHandler:
    # BACK_BUTTON_CALLBACK = "back_to_start"

    ALLOWED_USER_IDS = {562442831, 354135340, 222459211, 2028809889}  

    # def get_back_keyboard(self):
    #     keyboard = [
    #         [InlineKeyboardButton("Назад", callback_data=self.BACK_BUTTON_CALLBACK)]
    #     ]
    #     return InlineKeyboardMarkup(keyboard)


    def is_user_allowed(self, user_id: int) -> bool:
        return user_id in self.ALLOWED_USER_IDS
    
    def __init__(self, db, scheduler=None):  
        self.db = db
        self.scheduler = scheduler
    