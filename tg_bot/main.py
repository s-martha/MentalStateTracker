from aiogram import Bot, Dispatcher, executor, types
#from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '6499145833:AAGtf5zr6HHIHGWAXF_tRMac6UsW1uvMq8M'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
 

urlkb = InlineKeyboardMarkup(row_width=1)
urlButton = InlineKeyboardButton(text='Заполнить Яндекс.форму', url='https://forms.yandex.ru/u/6527f17069387285ff106e0f/')
urlButton2 = InlineKeyboardButton(text='Анализировать динамику изменения настроения', url='https://www.google.com/search?q=%D1%80%D0%B0%D0%B4%D0%BE%D1%81%D1%82%D1%8C&tbm=isch&ved=2ahUKEwirt6KJ0_CBAxX3HBAIHf92A5gQ2-cCegQIABAA&oq=%D1%80%D0%B0%D0%B4%D0%BE%D1%81%D1%82%D1%8C&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB46BAgjECc6BwgAEBMQgARQiRNYyxtguyJoAHAAeACAAcUEiAHDD5IBCzIuMS4zLjEuMC4xmAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=IfknZeuiA_e5wPAP_-2NwAk&bih=667&biw=1280&hl=en')
urlkb.add(urlButton,urlButton2)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
   await message.answer("Привет!\nЯ бот, позволяющий отслеживать психическое самочувствие!\n")
   await message.answer('Выбери, с чего начнём:', reply_markup=urlkb)
 
 
# @dp.message_handler(commands='ссылки')
# async def url_command(message: types.Message):
#    await message.answer('Полезные ссылки:', reply_markup=urlkb)

# @dp.message_handler()
# async def echo(message: types.Message):
#    await message.answer("Извини, отвечу, когда придумаю что-нибудь умное :D")
 
if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)








