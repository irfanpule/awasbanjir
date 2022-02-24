from telethon.sync import TelegramClient
from django.conf import settings


async def send_telegram_personal(user_entity, message="Awas Banjir!"):
    client = TelegramClient(
        settings.TELEGRAM_PHONE,
        settings.TELEGRAM_API_ID,
        settings.TELEGRAM_API_HASH
    )
    async with client:
        receiver = await client.get_input_entity(user_entity)
        await client.send_message(receiver, message)


def send_telegram_bot(user_entity, message="Awas Banjir!"):
    bot = TelegramClient('bot', settings.TELEGRAM_API_ID,
                         settings.TELEGRAM_API_HASH).start(bot_token=settings.TELEGRAM_BOT_TOKEN)
    with bot:
        bot.send_message(user_entity, message)
