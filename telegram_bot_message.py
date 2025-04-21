import telegram
import json
import asyncio

with open('realconfig.json') as jason: # format in fakeconfig.json
    config = json.load(jason)

BOT_TOKEN = config['TG_BOT_KEY']
CHAT_ID = config['TG_USERID_tom']

def tgram_message(message, BOT_TOKEN = BOT_TOKEN, CHAT_ID = CHAT_ID):
    async def send_message(message):
        bot = telegram.Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=message)
    asyncio.run(send_message(message))

if __name__=="__main__":
    tgram_message('hi hi hi')