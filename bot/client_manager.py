from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode

from data import *

app = Client(bot_name,
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token)


with app:
    pass



if __name__ == "__main__":
    print("+---------------------+\n"
          "| ManagerBot Iniciado |\n"
          "+---------------------+\n")

    app.run()