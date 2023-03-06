from aiogram import Bot, Dispatcher, types

from config import config
from api_requests import ApiRequests


bot = Bot(token=config['BOT_TOKEN'])
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    api = ApiRequests()
    company = await api.subsite('https://vc.ru/softlex')
    message = f"Пользователь опубликовал материалов: {company}"
    bot.send_message(message.chat.id, )
