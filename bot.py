import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.filters.command import CommandObject
from aiogram import F
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
import aioschedule
import os
import settings  # settings.py
import db  # db.py
from plot import PlotParse  # plot.py

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
# Диспетчер
dp = Dispatcher()
dp = Dispatcher()
user_time = {}  # словарь юзер - время автополучения формы
users_weekly_stats = set()  # список юзеров, которым каждую неделю присылаем статистику за неделю
new_form = True
kb = [
    [types.KeyboardButton(text="Статистика за неделю")],
    [types.KeyboardButton(text="Статистика за месяц")],
    [types.KeyboardButton(text="Статистика за всё время")],
    [types.KeyboardButton(text="Изменить время отправки формы")],
    [types.KeyboardButton(text="Отправить форму")],
]
keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True,
)


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # print("/start", message.from_user.id)

    global user_time
    asyncio.create_task(scheduler(message))
    user_time[message.from_user.id] = '12:00'
    db.AddUserTime(message.from_user.id, '12:00')

    await message.answer(
        'Привет!\nЯ бот, позволяющий отслеживать психическое самочувствие!',
        reply_markup=keyboard,
    )
    await message.answer(
        'Каждый день я буду присылать Вам анкету, \nв которой Вы можете отметить своё настроение, \nа в конце каждой недели я отправлю статистику.'
    )
    await message.answer(
        'В какое время Вам удобно получать форму? \nОтправьте время в формате "/time чч:мм" (например "/time 08:15")'
    )


@dp.message(F.text == "Изменить время отправки формы")
async def time_change(message: types.Message):
    if user_time[message.from_user.id] == "12:00":
        print("time_change:", "new time", message.from_user.id)
        await message.answer(
            'В какое время Вам удобно получать форму? \nОтправьте время в формате "/time чч:мм" (например "/time 08:15")'
        )
    else:
        print("time_change:", "change time", message.from_user.id)
        await message.answer(
            f'Текущее время - {user_time[message.from_user.id]}\nОтправьте новое время в формате "/time чч:мм" (например "/time 08:15")'
        )


@dp.message(Command("time"))
async def get_time(message: types.Message, command: CommandObject):
    print("get_time:", message.from_user.id)
    global user_time
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
        if (
                0 <= int(hour) <= 23
                and 0 <= int(minutes) <= 59
                and len(hour) == len(minutes) == 2
        ):
            await message.answer(f"Добавлено время: {command.args}")
            user_time[message.from_user.id] = command.args
            db.AddUserTime(message.from_user.id, command.args)

        else:
            await message.answer("Ошибка: неправильный формат времени")
    except:
        await message.answer("Ошибка: неправильный формат времени")


poll_res = {
    0: "очень плохое",
    1: "плохое",
    2: "удовлетворительное",
    3: "хорошее",
    4: "очень хорошее",
}


def get_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="1 - очень плохое", callback_data="mood_0")],
        [types.InlineKeyboardButton(text="2 - плохое", callback_data="mood_1")],
        [
            types.InlineKeyboardButton(
                text="3 - удовлетворительное", callback_data="mood_2"
            )
        ],
        [types.InlineKeyboardButton(text="4 - хорошее", callback_data="mood_3")],
        [types.InlineKeyboardButton(text="5 - очень хорошее", callback_data="mood_4")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


@dp.message(F.text == "Отправить форму")
async def send_form(message: types.Message):
    print("send_form:", message.from_user.id)
    global new_form
    if new_form:
        await message.answer("Отметьте своё настроение:", reply_markup=get_keyboard())
        new_form = False


@dp.callback_query(F.data.startswith("mood_"))
async def callbacks_mood(callback: types.CallbackQuery):
    print("callbacks_mood:", callback.from_user.id)
    global new_form
    action = callback.data.split("_")[1]

    db.AddMood(callback.from_user.id, int(action) + 1)  # запись настроения пользователя в бд

    await callback.message.answer(f'Вы отметили "{poll_res[int(action)]}"')
    await callback.message.delete()
    new_form = True


@dp.message(F.text == "Статистика за неделю")  # month stats
async def week_stats(message: types.Message):
    print("week_stats:", message.from_user.id)
    await message.answer("Ваша статистика за неделю:")
    dates, values = db.GetMoodDatesAndValues(message.from_user.id, 7)
    print("week_stats:", dates, values)
    PlotParse(
        dates, values, message.from_user.id, message.from_user.username, "on this week"
    )
    image_from_pc = FSInputFile(f"userplots/{message.from_user.id}_plot.png")
    result = await message.answer_photo(image_from_pc, caption="Статистика за неделю")
    os.remove(f"userplots/{message.from_user.id}_plot.png")


@dp.message(F.text == "Статистика за месяц")  # month stats
async def month_stats(message: types.Message):
    print("month_stats:", message.from_user.id)
    await message.answer("Ваша статистика за месяц:")
    dates, values = db.GetMoodDatesAndValues(message.from_user.id, 30)
    print("month_stats:", dates, values)
    PlotParse(
        dates, values, message.from_user.id, message.from_user.username, "in this month"
    )
    image_from_pc = FSInputFile(f"userplots/{message.from_user.id}_plot.png")
    result = await message.answer_photo(image_from_pc, caption="Статистика за месяц")
    os.remove(f"userplots/{message.from_user.id}_plot.png")


@dp.message(F.text == "Статистика за всё время")  # all time stats
async def all_stats(message: types.Message):
    print("all_stats:", message.from_user.id)
    await message.answer("Ваша статистика за всё время:")
    dates, values = db.GetMoodDatesAndValues(message.from_user.id, 'all_time')
    # print("all_stats:", dates, values)
    PlotParse(
        dates,
        values,
        message.from_user.id,
        message.from_user.username,
        "for all time",
    )
    image_from_pc = FSInputFile(f"userplots/{message.from_user.id}_plot.png")
    result = await message.answer_photo(
        image_from_pc, caption="Статистика за всё время"
    )
    os.remove(f"userplots/{message.from_user.id}_plot.png")


@dp.message()
async def dont_understand(message: types.Message):
    print("dont_understand:", message.from_user.id)
    await message.answer("Я Вас не понимаю")


async def sched_mess(mes: types.Message):
    print("sched_mess")
    await send_form(mes)


async def scheduler(mess: types.Message):
    aioschedule.every().day.at(user_time[mess.from_user.id]).do(sched_mess, mes=mess)
    # aioschedule.every().minute.do(sched_mess, mes=mess) #for testing
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def main():
    global user_time
    db.GetAllUsersInfo(user_time, users_weekly_stats)
    # Перед запуском бота скачаем в себя время юзеров и информацию, подписаны ли они на еженедельное получение статистики
    print(user_time)
    print(users_weekly_stats)

    await dp.start_polling(bot)  # Запуск процесса поллинга новых апдейтов


if __name__ == "__main__":
    asyncio.run(main())
