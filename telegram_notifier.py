from telegram import Bot

async def send_telegram_message(bot_token, chat_id, message):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)

async def main():
    bot_token = 'your_botfather_token'
    chat_id = 'your_tg_id'
    message = "Test message from Binance correlation bot"
    await send_telegram_message(bot_token, chat_id, message)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
