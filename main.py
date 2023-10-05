from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from NLP import syntax_func
from token_1 import BOT_TOKEN

TOKEN = BOT_TOKEN()

# Создаем объекты бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Синтакс-бот!\nНапиши мне что-нибудь')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю синтаксический разбор твоего предложения'
    )

# Этот хэндлер будет срабатывать на команду "/contacts"
@dp.message(Command(commands=['contacts']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши автору для предоставления комментариев, замечаний и донатов @alesk_777 '
    )

# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    try:
        text = str()
        for i in syntax_func(message.text):
            text += str(i) +'\n'
        await message.reply(text=text)
    except:
        await message.answer(
        'Произошла какая-то ошибка, попробуйте еще раз'
    )


if __name__ == '__main__':
    dp.run_polling(bot)