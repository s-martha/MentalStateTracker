import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.filters.command import CommandObject
from aiogram import F
import matplotlib.pyplot as plt
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="6499145833:AAGtf5zr6HHIHGWAXF_tRMac6UsW1uvMq8M")
# Диспетчер
dp = Dispatcher()
user_data = {}
kb = [
    [types.KeyboardButton(text="Статистика за месяц")],
    [types.KeyboardButton(text="Статистика за всё время")],
    [types.KeyboardButton(text="Изменить время отправки формы")],
    [types.KeyboardButton(text="Отправить форму")]
]
keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True,
)

def PlotParse(dates, values, chat_id, username): # len(dates) == len(values)
    #plt.plot(dates, values, 'ro', dates, values, 'r--') #dots and punktir
    plt.bar(dates, values)
    plt.axis((0.5, 31.5, 0, 5.5))
    plt.ylabel('mood')
    plt.title(f"{username}'s mood in this month")
    plt.xlabel(f'dates')
    #plt.show()
    plt.savefig(f'userplots/{chat_id}_plot.png')

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    global user_data
    user_data[message.from_user.id] = []
    await message.answer("Привет!\nЯ бот, позволяющий отслеживать психическое самочувствие!", reply_markup=keyboard)
    await message.answer('Каждый день я буду присылать Вам анкету, \nв которой Вы можете отметить своё настроение, \nа в конце каждой недели я отправлю статистику.')
    await message.answer('В какое время Вам удобно получать форму? \nОтправьте время в формате "/time чч:мм" (например "/time 17:50")')


@dp.message(F.text == "Статистика за месяц")
async def month_stats(message: types.Message):
    await message.answer("Ваша статистика за месяц:")
    dates = range(31)
    values = user_data[message.from_user.id] + [0 for i in range(31 - len(user_data[message.from_user.id]))]
    PlotParse(dates, values, message.from_user.id, message.from_user.username)
    image_from_pc = FSInputFile(f'userplots/{message.from_user.id}_plot.png')
    result = await message.answer_photo(
        image_from_pc,
        caption="Статистика за месяц"
    )

@dp.message(F.text == "Статистика за всё время")
async def all_stats(message: types.Message):
    await message.answer("Ваша статистика за всё время:")

@dp.message(F.text == "Изменить время отправки формы")
async def time_change(message: types.Message):
    await message.answer('Отправьте время в формате "/time чч:мм" (например "/time 17:50")')

@dp.message(Command('time'))
async def get_time(message: types.Message, command: CommandObject):
    if command.args is None:
        await message.answer("Ошибка: не переданы аргументы")
        return
    try:
        hour, minutes = command.args.split(":", maxsplit=1)
    # Если получилось меньше двух частей, вылетит ValueError
    except ValueError:
        await message.answer("Ошибка: неправильный формат времени")
        return
    try:
        if 0 <= int(hour) <= 23 and 0 <= int(minutes) <= 59 and len(hour) == len(minutes) == 2:
            await message.answer(f"Добавлено время:\n{hour}:{minutes}")
        else:
            await message.answer("Ошибка: неправильный формат времени")
    except:
        await message.answer("Ошибка: неправильный формат времени")

poll_res = {0: 'очень плохое',
            1: 'плохое',
            2: 'удовлетворительное',
            3: 'хорошее',
            4: 'очень хорошее'}

def get_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="1 - очень плохое", callback_data="mood_0")],
        [types.InlineKeyboardButton(text="2 - плохое", callback_data="mood_1")],
        [types.InlineKeyboardButton(text="3 - удовлетворительное", callback_data="mood_2")],
        [types.InlineKeyboardButton(text="4 - хорошее", callback_data="mood_3")],
        [types.InlineKeyboardButton(text="5 - очень хорошее", callback_data="mood_4")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


@dp.message(F.text == "Отправить форму")
async def send_form(message: types.Message):
    await message.answer("Отметьте своё настроение:", reply_markup=get_keyboard())


@dp.callback_query(F.data.startswith("mood_"))
async def callbacks_mood(callback: types.CallbackQuery):
    global user_data
    action = callback.data.split("_")[1]
    user_data[callback.from_user.id].append(int(action) + 1)
    await callback.message.answer(f'Вы отметили "{poll_res[int(action)]}"')
    await callback.message.delete()


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())