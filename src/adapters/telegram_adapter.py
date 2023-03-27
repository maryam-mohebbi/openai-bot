from telegram.ext import ApplicationBuilder, CommandHandler, filters, MessageHandler


def setup(token):
    builder = ApplicationBuilder().token(token).build()
    return builder


def add_command_handler(builder, command, fn):
    builder.add_handler(CommandHandler(command, fn))


def add_message_handler(builder, fn):
    builder.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fn))


async def reply_text(update, text, message_id=None):
    await update.message.reply_text(text=text, reply_to_message_id=message_id)


def start(builder):
    builder.run_polling()
