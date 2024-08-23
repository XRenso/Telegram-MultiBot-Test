from aiogram import Router
from aiogram.types import Message

from aiogram.enums.content_type import ContentType
from aiogram.enums.dice_emoji import DiceEmoji
import asyncio
from aiogram.filters import Command

router = Router()


@router.message(Command('start'))
async def start(message:Message):
    await message.answer("Добро пожаловать в телеграм бот, чтобы бросать кости!")

@router.message()
async def dice_game(message:Message):





    if message.content_type == ContentType.DICE:
            m1 = await message.answer_dice(emoji=message.dice.emoji)
            m2 = message.dice.value
            print(f'Результат бота - {m1.dice.value} \nРезультат игрока - {m2}')
            await asyncio.sleep(3.5)
            if message.dice.emoji != DiceEmoji.SLOT_MACHINE:
                winner = 'Победитель: Компьютер' if m1.dice.value > m2 else 'Победитель: Игрок' if m2 > m1.dice.value else 'Ничья'
            else:
                slot = [1,22,43,64]
                if m1.dice.value in slot and m2 not in slot:
                    winner = 'Победитель: Компьютер'
                elif m2 in slot and m1.dice.value not in slot:
                    winner = 'Победитель: Игрок'
                else:
                    winner = 'Ничья'
            if message.dice.emoji != DiceEmoji.SLOT_MACHINE:
                await message.answer(f'Ваш результат - {m2}\nРезультат компьютера - {m1.dice.value}\n\nИтог:\n{winner}')
            else:
                await message.answer(f'Итог:\n{winner}')
