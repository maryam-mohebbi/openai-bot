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


def tokens_count(username):
    global cnx
    cursor = cnx.cursor()
    val = (username,)

    # Check if the user exists in the MESSAGES table
    sql_check_user = 'SELECT COUNT(*) FROM MESSAGES WHERE USERNAME = %s;'
    cursor.execute(sql_check_user, val)
    user_count = cursor.fetchone()[0]

    if user_count == 0:
        return True

    sql_token = 'SELECT SUM(COMPLETION_TOKENS) as TOTAL_COMPLETION_TOKENS , SUM(PROMPT_TOKENS) as TOTAL_PROMPT_TOKENS FROM MESSAGES WHERE USERNAME =%s;'
    sql_limitation = 'SELECT TOKEN_LIMITATION FROM USERS WHERE USERNAME =%s;'

    cursor.execute(sql_token, val)
    result_token = cursor.fetchone()

    cursor.execute(sql_limitation, val)
    result_limitation = cursor.fetchone()

    cnx.commit()

    print(f'Result Token: {result_token}')
    print(f'Result limitation: {result_limitation}')

    total_tokens = result_token[0] + result_token[1]

    if total_tokens < result_limitation[0]:
        return True
    else:
        return False


def find_previous_messages(message_id, depth=0, max_depth=10):
    messages = []

    if depth >= max_depth:
        return messages

    cursor = cnx.cursor()
    sql = "SELECT MESSAGE_ID,REPLY_MESSAGE_ID,TEXT FROM MESSAGES WHERE MESSAGE_ID = %s"
    cursor.execute(sql, (message_id,))
    message = cursor.fetchone()

    if message:
        # Convert the message to a dictionary
        column_names = [desc[0] for desc in cursor.description]
        message_dict = dict(zip(column_names, message))

        messages.append(message_dict)

        if message_dict['REPLY_MESSAGE_ID'] is not None:
            previous_messages = find_previous_messages(
                message_dict['REPLY_MESSAGE_ID'], depth=depth + 1, max_depth=max_depth)
            messages = messages + previous_messages

    return messages
