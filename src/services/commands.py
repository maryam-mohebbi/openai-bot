import os
from adapters import telegram_adapter as bot
from adapters import openai_adapter as openai


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
    print(f'''
    ** Username: {update.message.from_user.username}
    ** Date: {update.message.date}
    ** Message id: {update.message.message_id}
    ** Message:  {update.message.text}
    ''')

    text = update.message.text
    try:
        response = openai.generate_response(text)
        await bot.reply_text(update, response, update.message.message_id)

    except Exception as e:
        print(e)
        await bot.reply_text(update, 'Error encountered while chatting.')
