import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
# Подключаем типы кнопок
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# === НАСТРОЙКИ ===
TOKEN = "8590170777:AAEYYCoapqN6WRlqhOvhj_93GYEAeGWGlgo"
MANAGER_ID = 984929835
# СЮДА ВСТАВЬ ССЫЛКУ НА ТВОЙ GITHUB (где лежит index.html)
# Например: https://alex.github.io/dress-rent/
WEB_APP_URL = "https://ТВОЙ_НИК.github.io/РЕПОЗИТОРИЙ/" 
# =================

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    # Создаем кнопку, которая открывает сайт
    web_app_info = WebAppInfo(url=WEB_APP_URL)
    
    # Кладем кнопку в клавиатуру
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👗 Открыть каталог", web_app=web_app_info)]
        ],
        resize_keyboard=True # Делаем кнопку компактной
    )
    
    await message.answer(
        "Привет! Нажми на кнопку ниже, чтобы выбрать платье 👇", 
        reply_markup=keyboard
    )

@dp.message(F.content_type == types.ContentType.WEB_APP_DATA)
async def web_app_data_handler(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        
        text = f"👗 <b>НОВЫЙ ЗАКАЗ!</b>\n"
        text += f"От: @{message.from_user.username}\n"
        text += "--------------------\n"
        if 'items' in data:
            for item in data['items']:
                text += f"• {item}\n"
        text += "--------------------\n"
        text += f"💰 <b>Итого: {data.get('total', 0)} руб.</b>"

        await bot.send_message(MANAGER_ID, text, parse_mode="HTML")
        await message.answer(f"Заказ на {data.get('total', 0)}₽ принят!")
    
    except Exception as e:
        logging.error(f"Ошибка: {e}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())