from aiogram import Bot, Dispatcher, types

import messages
from config import config
from api_requests import ApiRequests


bot = Bot(token=config['BOT_TOKEN'])
dp = Dispatcher(bot)
api = ApiRequests()


async def blog_stats_handler(message: types.Message, located: dict):
    blog, subsite_id = await api.subsite(located)
    if not blog:
        await bot.send_message(message.chat.id, 'Блог не найден')
        return

    check_message = f"Проверяю блог {blog['result']['name']}\n" \
                    f"Это может занять какое-то время"
    await bot.send_message(message.chat.id, check_message)

    blog_stats = await messages.get_blog_stats(blog)

    await bot.send_message(message.chat.id, blog_stats)

    stats = await api.subsite_timeline(subsite_id)
    if not stats:
        await bot.send_message(message.chat.id, 'Статей не найдено')
        return

    total_stats = await messages.get_entries_total_count(stats['result'])
    await bot.send_message(message.chat.id, total_stats, parse_mode='markdown')

    entries_stats = await messages.get_entries_stats(stats)

    await bot.send_message(message.chat.id, entries_stats, parse_mode='markdown', disable_web_page_preview=True)


async def user_stats_handler(message: types.Message, located: dict):
    user, user_id = await api.user(located)

    if not user:
        await bot.send_message(message.chat.id, 'Пользователь не найден')
        return

    check_message = f"Проверяю пользователя {user['result']['name']}\n" \
                    f"Это может занять какое-то время"
    await bot.send_message(message.chat.id, check_message)

    users_stats = await messages.get_user_stats(user)

    await bot.send_message(message.chat.id, users_stats)

    stats = await api.user_entries(user_id)
    if not stats:
        await bot.send_message(message.chat.id, 'Статей не найдено')
        return

    total_stats = await messages.get_entries_total_count(stats['result'])
    await bot.send_message(message.chat.id, total_stats, parse_mode='markdown')

    entries_stats = await messages.get_entries_stats(stats)

    await bot.send_message(message.chat.id, entries_stats, parse_mode='markdown', disable_web_page_preview=True)


async def is_user_url(url: str):
    pattern = 'https://vc.ru/u/'
    return url.startswith(pattern)


@dp.message_handler(content_types=['text'])
async def url_handler(message: types.Message):
    located = await api.locate(message.text)

    if not located:
        await bot.send_message(message.chat.id, 'По вашему запросу данных не найдено')

    if await is_user_url(message.text):
        await user_stats_handler(message, located)
    else:
        await blog_stats_handler(message, located)

