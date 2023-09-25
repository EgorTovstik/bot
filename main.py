

import os
import asyncio
import pandas as pd
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart

   
load_dotenv()
data = pd.read_excel("lab_pi_101.xlsx")


bot = Bot(token = os.getenv("TOKEN"))
dp = Dispatcher()


@dp.message(CommandStart()) 
async def send_welcome(message: Message):
   await message.answer("Добро пожаловать!")
   await message.answer("Задача этого бота заключается в отображении запроса из excel базы данных.")
   
@dp.message(F.text == "/info")
async def answer1(message: Message):
   LastRow = data.shape[0]
   await message.answer('Количество оценок', LastRow)

async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

