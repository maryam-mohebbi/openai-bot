from adapters import telegram_adapter as bot
from adapters import openai_adapter as ai
from services import commands


def setup_bot(token):
    builder = bot.setup(token)
    bot.add_command_handler(builder, 'start', commands.start)
    bot.add_command_handler(builder, 'help', commands.help)
    bot.add_command_handler(builder, 'chat', commands.chat)
    bot.add_message_handler(builder, commands.handle_text)
    return builder


def setup_ai(key):
    ai.setup(key)


def start_bot(builder):
    bot.start(builder)


def run(BOT_TOKEN, OPENAI_API_KEY):
    setup_ai(OPENAI_API_KEY)

    builder = setup_bot(BOT_TOKEN)
    start_bot(builder)
