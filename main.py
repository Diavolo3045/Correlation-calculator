import asyncio
import schedule
import time
from binance_data import main as download_data
from correlation_calculator import main as calculate_correlation
from telegram_notifier import send_telegram_message

async def process():
    # Download data
    download_data()

    # Calculate correlation
    correlation_results = calculate_correlation()

    # Prepare and send Telegram message
    bot_token = 'your-bot-token from Botfather' # https://t.me/BotFather
    chat_id = 'your-telegram-chat-id' # https://t.me/getmy_idbot
    message = "Correlation Results:\n"
    for result in correlation_results:
        message += (f"{result['symbol']} - {result['timeframe']}: "
                    f"Correlation with BTC-PERP: {result['correlation']:.4f} "
                    f"({result['relationship']}) - Data points: {result['data_points']}\n")

    await send_telegram_message(bot_token, chat_id, message)

def run_process():
    asyncio.run(process())

def main():
    # Run immediately on start
    run_process()

    # Schedule to run every hour
    schedule.every().hour.do(run_process)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
~                 
