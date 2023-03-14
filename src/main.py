from bot import run
import os


def get_config(config_name):
    return os.environ.get(config_name)


if __name__ == '__main__':
    BOT_TOKEN = get_config('BOT_TOKEN')
    OPENAI_API_KEY = get_config('OPENAI_API_KEY')

    run(BOT_TOKEN, OPENAI_API_KEY)
