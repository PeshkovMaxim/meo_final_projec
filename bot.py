import asyncio
import logging
from aiogram import Bot, Dispatcher, types, html
from dialogflow_handler import df_text_handler
import DAO
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"путь к файлу json"

# отладочное логирование
# logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token='', parse_mode="HTML")

# Диспетчер
dp = Dispatcher()

bot_dont_know = 'к сожалению, бот не знает ответ на вопрос, отправили его на тренировку!'

# Хэндлер на команду /star
@dp.message(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Привет, я бот-консультант МЭО")


@dp.message(content_types="text")
async def get_text(message: types.Message):
    with open('resources/request_log.txt', 'a+') as log:
        log.write("\n" + message.text)
    df_answer = df_text_handler(message.text)
    if df_answer:
        await message.answer(df_answer)
    else:
        await message.answer(bot_dont_know)
        DAO.save_data(message.text, message.chat.id)

@dp.message(content_types="photo")
async def download_photo(message: types.Message):
    await message.reply_photo(message.photo[-1].file_id)



# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())