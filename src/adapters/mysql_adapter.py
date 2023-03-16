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
    sql = "INSERT INTO MESSAGES (CHAT_ID, USERNAME, DATETIME, MESSAGE_ID, TEXT, REPLY_MESSAGE_ID) VALUES ( %s, %s, %s, %s, %s, %s)"
    val = (chat_id, username, datetime, message_id, text, reply_message_id)
    cursor.execute(sql, val)
    cnx.commit()

    print(f'''
    {sql}
    {val}
    ''')
