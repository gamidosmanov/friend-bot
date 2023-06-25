import json
import sqlite3 as sql
import re
from datetime import datetime

def ifnull(x):
    if x == None:
        return ''
    return x

# Database initial setup
query_init = (
    "BEGIN; "
    "PRAGMA foreign_keys = ON;"
    "DROP TABLE IF EXISTS users; "
    "DROP TABLE IF EXISTS messages; "
    "CREATE TABLE users("
        "id INTEGER NOT NULL, "
        "name TEXT NOT NULL, "
        "PRIMARY KEY (id)"
    ");"
    "CREATE TABLE messages("
        "id INTEGER NOT NULL, "
        "timestamp INTEGER NOT NULL, "
        "from_id INTEGER NOT NULL, "
        "text TEXT NOT NULL, "
        "PRIMARY KEY (id), "
        "FOREIGN KEY (from_id) "
            "REFERENCES users(id) "
            "ON DELETE CASCADE "
            "ON UPDATE NO ACTION"
    ");"
    "COMMIT;"
)

conn = sql.connect('messages.db')
cur = conn.cursor()
cur.executescript(query_init)

# Data file opening
with open('data.json', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Inserting data
users = []
messages = []
users_dict = {}
date_format = '%Y-%m-%dT%H:%M:%S'

for msg in data['messages']:
    if (
        msg['type'] == 'message' 
        and isinstance(msg['text'], str) == True
        and 'photo' not in msg
        and 'media_type' not in msg
        and 'file' not in msg
        and 'from' != None
    ):
        if msg['from_id'] not in users_dict:
            users_dict[msg['from_id']] = 1
            users.append(
                (
                    int(re.sub(r'[a-z]', '', msg['from_id'])),
                    ifnull(msg['from'])
                )
            )
        messages.append(
            (
                msg['id'],
                int(datetime.strptime(msg['date'], date_format).timestamp()),
                int(re.sub(r'[a-z]', '', msg['from_id'])),
                msg['text']
            )
        )

query_users = "REPLACE INTO users (id, name) VALUES (?, ?);"
cur.executemany(query_users, users)
    
query_messages = (
    "REPLACE INTO messages "
    "(id, timestamp, from_id, text) "
    "VALUES (?, ?, ?, ?)"
)
cur.executemany(query_messages, messages)

conn.commit()
conn.close()