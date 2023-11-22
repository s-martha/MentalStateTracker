from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .. import db_init

API_TOKEN = '6499145833:AAGtf5zr6HHIHGWAXF_tRMac6UsW1uvMq8M'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
 
button_week = KeyboardButton("/Статистика_за_неделю")
button_2weeks = KeyboardButton("/Статистика_за_2_недели")
button_month = KeyboardButton("/Статистика_за_месяц")
button_all = KeyboardButton("/Статистика_за_всё_время")
button_change = KeyboardButton("/Изменить_время_отправления_формы")
keyboard = types.ReplyKeyboardMarkup().row(button_week, button_2weeks, button_month).add(button_all).insert(button_change)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
   await message.answer("Привет!\nЯ бот, позволяющий отслеживать психическое самочувствие!\n", reply_markup=keyboard)
   await message.answer('Каждый день я буду присылать тебе анкету, \nв которой ты можешь отметить своё самочувствие, \nа в конце каждой недели и каждого месяца я покажу статистику\n')
   await message.answer('В какое время тебе удобно получать формы? \nОтправь мне время в формате "/time чч:мм" (например "/time 17:50")\n')
 
 
@dp.message_handler(commands='time')
async def get_time(message: types.Message):
   try:
      if 0 <= int(message.text[6:8]) <= 23 and message.text[8] == ':' and 0 <= int(message.text[9:11]) <= 59 and len(message.text) == 11:
         e = db_init.MentalState(time=message.text[6:])
         e.save()
         await message.answer(f'Вы ввели время: {message.text[6:]}')
      else:
         await message.answer(f'Вы ввели некорректное время. Просьба прислать время в указанном формате.')
   except:
         await message.answer(f'Вы ввели некорректное время. Просьба прислать время в указанном формате.')

@dp.message_handler(commands='Статистика_за_неделю')
async def get_time(message: types.Message):
   await message.answer(f'Вы запрашиваете статистику за неделю\n')

@dp.message_handler(commands='Статистика_за_2_недели')
async def get_time(message: types.Message):
   await message.answer(f'Вы запрашиваете статистику за 2 недели\n')

@dp.message_handler(commands='Статистика_за_месяц')
async def get_time(message: types.Message):
   await message.answer(f'Вы запрашиваете статистику за месяц\n')

@dp.message_handler(commands='Статистика_за_всё_время')
async def get_time(message: types.Message):
   await message.answer(f'Вы запрашиваете статистику за всё время\n')


@dp.message_handler(commands='Изменить_время_отправления_формы')
async def get_time(message: types.Message):
   await message.answer(f'Введите новое время в формате: /time чч:мм\n')

@dp.message_handler()
async def get_time(message: types.Message):
   await message.answer(f'Я Вас не понимаю.\n')
 
if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)








