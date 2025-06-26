from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class BaseHandler:
    BACK_BUTTON_CALLBACK = "back_to_start"
    
    def __init__(self, db, scheduler=None):  
        self.db = db
        self.scheduler = scheduler
    
    def get_back_keyboard(self):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("Назад", callback_data=self.BACK_BUTTON_CALLBACK)]
        ])
