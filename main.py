

import os
import asyncio
import pandas as pd
import keyboard as kb
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
   await message.answer("Задача этого бота заключается в отображении запроса из excel базы данных.", reply_markup=kb.main)

   
@dp.message(F.text == "Выполнение запроса")
async def answer1(message: Message):
   LastRow = data.shape[0]
   skore = data['Группа'].str.contains('ПИ101').sum()
   stud_PI101 = len(data[data['Группа'] == 'ПИ101']['Личный номер студента'].unique())
   pi101 = data.loc[data['Группа']== 'ПИ101' , 'Личный номер студента'].unique()
   pi101q = ', '.join(map(str, pi101))
   control = data['Уровень контроля'].unique()
   controlq = ', '.join(map(str, control))
   years = sorted(data['Год'].unique())
   yearsq = ', '.join(map(str, years))
   await message.answer(f'Количество оценок {LastRow}, оценок из них {skore} относятся к ПИ101')
   await message.answer(f'В датасете находятся оценки , {stud_PI101}, студентов со следующими личными номерами: , {pi101q}')
   await message.answer(f'Используемые формы контроля: {controlq}')
   await message.answer(f'Данные представлены по следующим учебным годам: {yearsq}')

async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

