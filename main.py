from NLP import syntax_func
from token_1 import BOT_TOKEN

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import FSInputFile
from PIL import Image

import requests
import io
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

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


# Этот хэндлер будет срабатывать на команду "/file"
@dp.message(Command(commands=["file"]))
async def process_file_comand(message: Message):
    #chat_id = message.chat.id
    bot_file_in_id = message.document.file_id
    bot_file_in = await bot.get_file(bot_file_in_id)
    await bot.download_file(bot_file_in.file_path, "file_in.txt")
    file_in = open("file_in.txt", encoding = 'utf-8', mode = 'r')
    file_in_data = file_in.read()

    try:
        response = str()
        for i in syntax_func(file_in_data):
            response += str(i) +'\n'
        file_out = open("file_out.txt", encoding = 'utf-8', mode = 'w')
        file_out.write(response)
        file_out.close()
        file_out_obj = FSInputFile("file_out.txt", filename = "file_out.txt")
        await message.reply_document(file_out_obj)
    except:
        await message.answer(
        'Произошла какая-то ошибка, попробуйте еще раз'
    )

# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения
# кроме команд "/start" "/help" "/file"
@dp.message(F.text)
async def handle_text_message(message: Message):
    try:
        text = str()
        for i in syntax_func(message.text):
            text += str(i) +'\n'
        await message.reply(text=text)
    except:
        await message.answer(
        'Произошла какая-то ошибка, попробуйте еще раз'
    )

@dp.message(F.photo)
async def handle_photo_message(message: types.Message):
    photo = message.photo[-1]
    recognized_text = await recognize_text(photo.file_id)
    if recognized_text:
        try:
            await message.reply(f'{recognized_text}\n')
            text = str()
            for i in syntax_func(recognized_text):
                text += str(i) +'\n'
            await message.answer(text=text)
        except:
            await message.answer(
            'Произошла какая-то ошибка, попробуйте еще раз'
    )

async def recognize_text(photo_file_id):
    # Получите информацию о фотографии из Telegram
    photo = await bot.get_file(photo_file_id)
    photo_url = f'https://api.telegram.org/file/bot{TOKEN}/{photo.file_path}'

    # Скачайте фотографию
    photo_data = requests.get(photo_url).content

    # Преобразуйте фотографию в объект Image из библиотеки PIL
    image = Image.open(io.BytesIO(photo_data))

    # Используйте pytesseract для распознавания текста на фотографии
    text = pytesseract.image_to_string(image, lang = 'rus')

    return text

if __name__ == '__main__':
    dp.run_polling(bot)
