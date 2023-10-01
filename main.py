
import os
import asyncio
import logging
import sys
import pandas as pd
import keyboard as kb
from dotenv import load_dotenv
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart

   
load_dotenv()
data = pd.read_excel("lab_pi_101.xlsx")


TOKEN = os.getenv("TOKEN")
dp = Dispatcher()

form_router = Router()


class Form(StatesGroup):
   name = State()
   

@form_router.message(CommandStart())
async def command_start(message: Message):
   await message.answer("Добро пожаловать!")
   await message.answer("Задача этого бота заключается в отображении запроса из excel базы данных.", reply_markup=kb.main)

   
   
@form_router.message(F.text == 'Получить отчет')
async def report(message: Message, state: FSMContext) -> None:
   await state.set_state(Form.name)
   await message.answer(
        "Введите номер группы: ",
        reply_markup=ReplyKeyboardRemove())

   
@form_router.message(Form.name)
async def process_name(message: Message, state: FSMContext) -> None:
   await state.update_data(name=message.text)
   await message.answer(f"Номер вашей группы:  {html.quote(message.text)}")
   skore = data['Группа'].str.contains(str(Form.name)).sum()
   if skore == 0:
      await message.answer('К сожалению группы с таким номером не существует.', reply_markup=kb.main)
   else:
      await message.answer('Выберите отчет какого типа Вы хотите получить:', reply_markup=kb.report)
   

@dp.callback_query(F.data == 'quantity')
async def cbquantity(callback: CallbackQuery):
   LastRow = data.shape[0]
   skore = data['Группа'].str.contains(str(Form.name)).sum()
   years = sorted(data['Год'].unique())
   yearsq = ', '.join(map(str, years))
   await callback.message.answer(f'Количество оценок {LastRow}, оценок из них {skore} относятся к ПИ101')
   await callback.message.answer(f'Данные представлены по следующим учебным годам: {yearsq}')

@dp.callback_query(F.data == 'number')
async def cbquantity(callback: CallbackQuery):
   stud_PI101 = len(data[data['Группа'] == str(Form.name)]['Личный номер студента'].unique())
   pi101 = data.loc[data['Группа']== str(Form.name) , 'Личный номер студента'].unique()
   pi101q = ', '.join(map(str, pi101))
   years = sorted(data['Год'].unique())
   yearsq = ', '.join(map(str, years))
   await callback.message.answer(f'В датасете находятся оценки , {stud_PI101}, студентов со следующими личными номерами: , {pi101q}')
   await callback.message.answer(f'Данные представлены по следующим учебным годам: {yearsq}')

@dp.callback_query(F.data == 'forms')
async def cbquantity(callback: CallbackQuery):
   control = data['Уровень контроля'].unique()
   controlq = ', '.join(map(str, control))
   years = sorted(data['Год'].unique())
   yearsq = ', '.join(map(str, years))
   await callback.message.answer(f'Используемые формы контроля: {controlq}')
   await callback.message.answer(f'Данные представлены по следующим учебным годам: {yearsq}')


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())