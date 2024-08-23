import logging
import sys
from os import getenv
from dotenv import load_dotenv
from aiohttp import web
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher, Router
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.filters import Command, CommandObject
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    TokenBasedRequestHandler,
    setup_application,
)
from handlers.dice import router as dice_game_router

load_dotenv()
main_router = Router()

BASE_URL = getenv("NGROK_URL")

MAINBOT_TOKEN = getenv("TOKEN")

MAINBOT_PATH = f'/bot/{MAINBOT_TOKEN}'
OTHER_PATH = '/other_bots/{bot_token}'
MAINBOT_URL = f'{getenv("NGROK_URL")}/bot/{getenv("TOKEN")}'
OTHER_URL = f'{BASE_URL}{OTHER_PATH}'

WEBHOOK_HOST = f'{getenv("HOST")}'
WEBHOOK_PORT = f'{getenv("PORT")}'


@main_router.message(Command('start'))
async def start(message:Message):
    await message.answer('Отправь мне комманду /add вместе с токеном бота, и я его добавлю')

@main_router.message(Command("add"))
async def command_add_bot(message: Message, command: CommandObject):
    try:
        new_bot = Bot(token=command.args, default=DefaultBotProperties(parse_mode='HTML'))
        bot_user = await new_bot.get_me()
    except TelegramUnauthorizedError:
        return message.answer("Неверный токен")
    await new_bot.delete_webhook(drop_pending_updates=True)
    await new_bot.set_webhook(OTHER_URL.format(bot_token=command.args))
    return await message.answer(f"Бот @{bot_user.username} теперь работает!")


async def on_startup(bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(url=MAINBOT_URL)




def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    storage = MemoryStorage()


    dp = Dispatcher(storage=storage)
    dp.include_router(main_router)
    dp.startup.register(on_startup)
    app = web.Application()
    bot = Bot(token=MAINBOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    webhook = SimpleRequestHandler(dispatcher=dp,bot=bot)
    webhook.register(app,path=MAINBOT_PATH)


    other_dp = Dispatcher(storage=storage)
    other_dp.include_router(dice_game_router)
    other_webhook = TokenBasedRequestHandler(dispatcher=other_dp)
    other_webhook.register(app, path=OTHER_PATH)

    setup_application(app,dp,bot=bot)
    setup_application(app,other_dp)

    web.run_app(app,host=WEBHOOK_HOST,port=int(WEBHOOK_PORT))


if __name__ == "__main__":
    main()