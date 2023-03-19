import mysql.connector

cnx = ''


def sql_setup(host, port, user, password, database):
    global cnx
    cnx = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    return cnx


def insert_message(chat_id, username, datetime, message_id, text, reply_message_id):
    global cnx
    cursor = cnx.cursor()
    sql = 'INSERT INTO MESSAGES (CHAT_ID, USERNAME, DATETIME, MESSAGE_ID, TEXT, REPLY_MESSAGE_ID) VALUES (%s, %s, %s, %s, %s, %s)'
    val = (chat_id, username, datetime, message_id, text, reply_message_id)
    cursor.execute(sql, val)
    cnx.commit()


def does_user_exist(username):
    global cnx
    cursor = cnx.cursor()
    sql = 'SELECT USERNAME FROM USERS WHERE USERNAME = %s'
    val = (username,)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    cnx.commit()
    if result is not None:
        return True
    else:
        return False


def update_message_tokens(message_id, completion_tokens, prompt_tokens):
    global cnx
    cursor = cnx.cursor()
    sql = 'UPDATE MESSAGES SET COMPLETION_TOKENS=%s, PROMPT_TOKENS=%s WHERE MESSAGE_ID = %s'
    val = (completion_tokens, prompt_tokens, message_id)
    cursor.execute(sql, val)
    cnx.commit()
