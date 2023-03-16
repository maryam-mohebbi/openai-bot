from bot import run
import os


def get_config(config_name):
    return os.environ.get(config_name)


if __name__ == '__main__':
    BOT_TOKEN = get_config('BOT_TOKEN')
    OPENAI_API_KEY = get_config('OPENAI_API_KEY')
    HOST = get_config('HOST')
    PORT = get_config('PORT')
    USER = get_config('USER')
    PASSWORD = get_config('PASSWORD')
    DATABASE = get_config('DATABASE')

    run(BOT_TOKEN, OPENAI_API_KEY, HOST, PORT, USER, PASSWORD, DATABASE)
