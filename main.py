import os
from telebot.async_telebot import AsyncTeleBot
import asyncio
import aiohttp
import sqlite3 as sql
from datetime import datetime

conn = sql.connect('messages.db')
cur = conn.cursor()

def get_message(cur):
    query = (
        "SELECT timestamp, text "
        "FROM messages "
        "WHERE from_id = ? "
        "ORDER BY RANDOM() "
        "LIMIT 1;"
    )
    cur.execute(query, [os.environ['FRIEND_BOT_USER']])
    row = cur.fetchone()
    return "{} ({})".format(
        row[1], 
        datetime.fromtimestamp(row[0])
    )

bot = AsyncTeleBot(os.environ['FRIEND_BOT_TOKEN'])

@bot.message_handler(commands=['dispense_wisdom'])
async def dispense(message):
    await bot.send_message(
        message.chat.id, text=get_message(cur)
    )

asyncio.run(bot.polling())