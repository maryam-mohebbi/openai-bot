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
        ** text : {update.message.text},
        ** reply_message_id : {update.message.reply_to_message.message_id if update.message.reply_to_message is not None else None})'''
    )

    mysql.insert_message(chat_id=update.message.chat.id,
                         username=update.message.chat.username,
                         datetime=update.message.date,
                         message_id=update.message.message_id,
                         text=update.message.text,
                         reply_message_id=update.message.reply_to_message.message_id if update.message.reply_to_message is not None else None)

    text = update.message.text
    try:
        response = openai.generate_response(text)
        await bot.reply_text(update, response, update.message.message_id)

    except Exception as e:
        print(e)
        await bot.reply_text(update, 'Error encountered while chatting.')
