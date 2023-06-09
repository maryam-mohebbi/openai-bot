from adapters import telegram_adapter as bot
from adapters import openai_adapter as openai
from adapters import mysql_adapter as mysql


async def start(update, context):
    start_message = 'Welcome to the OpenAI bot! Use /help to see the available commands.'
    await bot.reply_text(update, start_message)


async def help(update, context):
    help_message = f'''Available commands:
    /start - Start the Bot
    /help - See all commands
    /chat - Start a chat with the bot and ask it any question.'''
    await bot.reply_text(update, help_message)


async def chat(update, context):
    await bot.reply_text(update, 'Ask me anything!')
    return


async def handle_text(update, context):

    print(
        f'''
        ** chat_id : {update.message.chat.id},
        ** username : {update.message.chat.username},
        ** datetime : {update.message.date},
        ** message_id : {update.message.message_id},
        ** reply_message_id : {update.message.reply_to_message.message_id if update.message.reply_to_message is not None else None}'''
    )

    if mysql.does_user_exist(update.message.chat.username) == False:
        await bot.reply_text(update, 'Oh, Sorry! You do not have access')
        return

    if mysql.tokens_count(update.message.chat.username) == False:
        await bot.reply_text(update, 'Sorry, The sum of tokens has exceeded.')
        return

    mysql.insert_message(chat_id=update.message.chat.id,
                         username=update.message.chat.username,
                         datetime=update.message.date,
                         message_id=update.message.message_id,
                         text=update.message.text,
                         reply_message_id=update.message.reply_to_message.message_id if update.message.reply_to_message is not None else None)

    text = update.message.text

    previous_messages = mysql.find_previous_messages(update.message.message_id)

    try:
        response = openai.generate_response(text, previous_messages)
        mysql.update_message_tokens(update.message.message_id,
                                    response['tokens']['completion_tokens'],
                                    response['tokens']['prompt_tokens'])

        reply_message = await bot.reply_text(update, response['content'], update.message.message_id)

        mysql.insert_message(chat_id=reply_message.chat.id,
                             username='OpenAi-Bot',
                             datetime=reply_message.date,
                             message_id=reply_message.message_id,
                             text=reply_message.text,
                             reply_message_id=reply_message.reply_to_message.message_id if reply_message.reply_to_message is not None else None)

    except Exception as e:
        print(e)
        await bot.reply_text(update, 'Error encountered while chatting.')
