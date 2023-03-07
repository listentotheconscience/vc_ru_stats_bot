import emoji


ON_PAGE_COUNT = 3


async def get_blog_stats(response: dict) -> str:
    karma = response['result']['karma']
    subscribers_count = response['result']['subscribers_count']
    entries_count = response['result']['entries_count']

    blog_stats = f"- Рейтинг блога: {karma}\n" \
                 f"- Подписчиков: {subscribers_count}\n" \
                 f"- Статей: {entries_count}"

    return blog_stats


async def get_entries_top_by_views(entries: list) -> str:
    top_by_views = sorted(entries, key=lambda x: x['hitsCount'], reverse=True)[:ON_PAGE_COUNT]

    text = f"{emoji.emojize(':eyes:')} Топ по просмотрам\n"

    for item in top_by_views:
        text += f"- [{item['title']}]({item['url']}) (Просмотров: {item['hitsCount']})\n"
    text += "\n"

    return text


async def get_entries_top_by_favorites(entries: list) -> str:
    top_by_favorites = sorted(entries, key=lambda x: x['favoritesCount'], reverse=True)[:ON_PAGE_COUNT]

    text = f"{emoji.emojize(':floppy_disk:')} Топ по закладкам\n"

    for item in top_by_favorites:
        text += f"- [{item['title']}]({item['url']}) (Добавлений в закладки: {item['favoritesCount']})\n"
    text += "\n"

    return text


async def get_entries_top_by_comments(entries: list) -> str:
    top_by_comments = sorted(entries, key=lambda x: x['commentsCount'], reverse=True)[:ON_PAGE_COUNT]

    text = f"{emoji.emojize(':speech_balloon:')} Топ по комментариям\n"

    for item in top_by_comments:
        text += f"- [{item['title']}]({item['url']}) (Комментариев: {item['commentsCount']})\n"
    text += "\n"

    return text


async def get_entries_top_by_rating(entries: list) -> str:
    top_by_comments = sorted(entries, key=lambda x: x['likes']['summ'], reverse=True)[:ON_PAGE_COUNT]

    text = f"{emoji.emojize(':thumbs_up:')} Топ по рейтингу\n"

    for item in top_by_comments:
        text += f"- [{item['title']}]({item['url']}) (Рейтинг: {item['likes']['summ']})\n"
    text += "\n"

    return text


async def get_entries_total_count(entries: list) -> str:
    entries_count = len(entries)
    views_count = 0
    favorite_count = 0
    comments_count = 0
    rating = 0

    for entry in entries:
        views_count += entry['hitsCount']
        favorite_count += entry['favoritesCount']
        comments_count += entry['commentsCount']
        rating += entry['likes']['summ']

    message = f"Всего материалов: {entries_count}\n\n" \
              f"*У этих материалов совокупно:*\n\n" \
              f"- Просмотров: {views_count}\n" \
              f"- Добавлений в закладки: {favorite_count}\n" \
              f"- Комметариев: {comments_count}\n" \
              f"- Рейтинг: {rating}"

    return message


async def get_entries_stats(response: dict) -> str:
    entries = response['result']

    message = f"{emoji.emojize(':fire:')} Топ по материалам\n\n"
    message += await get_entries_top_by_views(entries)
    message += await get_entries_top_by_favorites(entries)
    message += await get_entries_top_by_comments(entries)
    message += await get_entries_top_by_rating(entries)

    return message


async def get_user_stats(response: dict) -> str:
    karma = response['result']['karma']
    subscribers_count = response['result']['subscribers_count']
    entries_count = response['result']['counters']['entries']
    comments_count = response['result']['counters']['comments']

    user_stats = f"Рейтинг пользователя: {karma}\n" \
                 f"Подписчиков: {subscribers_count}\n" \
                 f"Статей: {entries_count}\n" \
                 f"Комметариев: {comments_count}"

    return user_stats
