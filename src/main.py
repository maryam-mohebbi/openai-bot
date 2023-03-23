from bot import run
from dotenv import load_dotenv
import os


def get_config(config_name):
    return os.environ.get(config_name)


if __name__ == '__main__':
    load_dotenv('src/config/.env')
    BOT_TOKEN = get_config('BOT_TOKEN')
    OPENAI_API_KEY = get_config('OPENAI_API_KEY')
    HOST = get_config('HOST')
    PORT = get_config('PORT')
    DB_USER = get_config('DB_USER')
    PASSWORD = get_config('PASSWORD')
    DATABASE = get_config('DATABASE')

    run(BOT_TOKEN, OPENAI_API_KEY, HOST, PORT, DB_USER, PASSWORD, DATABASE)
