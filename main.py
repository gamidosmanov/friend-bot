import os
import json
import pandas as pd
import random
import aiohttp
from telebot.async_telebot import AsyncTeleBot
import asyncio
import time
import sqlite3 as sql

bot = AsyncTeleBot(os.environ['SEMEN_BOT_TOKEN'])

with open('data.json', encoding='utf-8') as json_file:
    data = json.load(json_file)

exit()

semen = []
semen_date = []

for i in data['messages']:
    if (
        i['type'] == 'message' 
        and isinstance(i['text'], str) == True
    ):
        if (
            i['from_id'] == 'user116680789' 
            and i['text'].upper() not in semen 
            and len(i['text']) > 14 
            and len(i['text']) < 125
        ):
            semen.append(i['text'].upper())
            semen_date.append(i['date'][0:10])

df = pd.DataFrame()

df['Message'] = semen
df['Date'] = semen_date

df1 = df.reindex(df.Message.str.len().sort_values().index)
df1 = df1.reset_index(drop=True)
df = df1

@bot.message_handler(commands=['dispense_wisdom'])
async def dispense(message):
    cid = message.chat.id
    x = random.randrange(3378)
    mes = df['Message'][x] + ' (' + df['Date'][x][8:10] + '.' + df['Date'][x][5:7] + '.' + df['Date'][x][0:4] + ')'
    await bot.send_message(cid, text=mes)

asyncio.run(bot.polling())