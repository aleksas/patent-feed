
from typing import List, Dict, Tuple, Iterable
import mysql.connector

def get_connection():
    config = {
        'user': 'root',
        'password': None,
        'host': 'mysql',
        'port': '3306',
        'database': 'knights'
    }
    return mysql.connector.connect(**config)

def get_channels() -> Iterable[Dict]:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT id, title, link, description FROM channels')
    for channel_id, title, link, description in cursor:
        yield {'channel_id':channel_id, 'link':link, 'title':title, 'description':description}
    cursor.close()
    connection.close()

def get_channel(channel_id) -> Iterable[Dict]:
    connection = get_connection()
    cursor = connection.cursor(prepared=True)
    cursor.execute('SELECT title, link, description FROM channels WHERE id=?', (channel_id,))
    title, link, description = cursor.fetchone()
    data = {'channel_id':channel_id, 'title':title, 'link':link, 'description':description}
    cursor.close()
    connection.close()
    return data

def get_channel_entries(channel_id, logger=None) -> Iterable[Dict]:
    if logger:
        logger(channel_id)
    connection = get_connection()
    cursor = connection.cursor(prepared=True)
    cursor.execute('SELECT id, channel_id, title, link, description FROM channel_entries WHERE channel_id=?', (channel_id,))
    for entry_id, channel_id, title, link, description in cursor:
        yield {'entry_id':entry_id, 'channel_id':channel_id, 'title':title.decode('utf8'), 'link':link.decode('utf8'), 'description':description.decode('utf8')}
    cursor.close()
    connection.close()

def get_channel_entries_with_datetime(channel_id) -> Iterable[Dict]:
    query = '''
    SELECT channel_entries.id, channel_id, title, link, description, datetime FROM channel_entries
    JOIN channel_entries_datetimes ON channel_entries.id = channel_entries_datetimes.id
    WHERE channel_id=?
    ORDER BY datetime DESC
    '''

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query, (channel_id,))
    for entry_id, channel_id, title, link, description, datetime in cursor:
        yield {'entry_id':entry_id, 'channel_id':channel_id, 'title':title, 'link':link, 'description':description, 'datetime':datetime}
    cursor.close()
    connection.close()

def insert_channel(title, link, description, channel_id=None, logger=None):
    connection = get_connection()
    cursor = connection.cursor(prepared=True)
    if channel_id == None:
        cursor.execute('INSERT INTO channels (title, link, description) VALUES (?,?,?)', (title, link, description))
        channel_id = cursor.lastrowid
    else:
        query = 'INSERT INTO channels (id, title, link, description) VALUES (?,?,?,?) ON DUPLICATE KEY UPDATE title=?, link=?, description=?'
        cursor.execute(query, (channel_id, title, link, description, title, link, description))

    if logger:
        logger(channel_id)
    connection.commit()
    connection.close()
    return channel_id

def insert_channel_entry(channel_id, title, link, description, entry_id=None, datetime=None, logger=None):
    connection = get_connection()
    cursor = connection.cursor(prepared=True)
    if entry_id == None:
        cursor.execute('INSERT INTO channel_entries (channel_id, title, link, description) VALUES (?,?,?,?)', (channel_id, title, link, description))
    else:
        query = '''
            INSERT INTO channel_entries (id, channel_id, title, link, description) VALUES (?,?,?,?,?)
            ON DUPLICATE KEY UPDATE channel_id=?, title=?, link=?, description=?'''
        cursor.execute(query, (entry_id, channel_id, title, link, description, channel_id, title, link, description))

    entry_id = cursor.lastrowid
    if logger:
        logger(entry_id)
    if datetime != None:
        cursor.execute('INSERT INTO channel_entries_datetimes (id, datetime) VALUES (?,?)', (entry_id, datetime))

    connection.commit()
    connection.close()
    return entry_id