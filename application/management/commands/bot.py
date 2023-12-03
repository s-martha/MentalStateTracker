from django.core.management.base import BaseCommand
#from django.conf import settings
from telebot import TeleBot


# Объявление переменной бота
bot = TeleBot("6499145833:AAGtf5zr6HHIHGWAXF_tRMac6UsW1uvMq8M", threaded=False)


# Название класса обязательно - "Command"
class Command(BaseCommand):
  	# Используется как описание команды обычно
    help = 'Just a command for launching a Telegram bot.'

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2) # Сохранение обработчиков
        bot.load_next_step_handlers()				# Загрузка обработчиков
        bot.infinity_polling()						# Бесконечный цикл бота