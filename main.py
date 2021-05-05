import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.utils.callback_data  import CallbackData

API_TOKEN = '1712583828:AAHdBNR4tIS2rA4KXMXTAM8k-15QZlSusd0'

#@stud_prof_bot

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
callback_data = CallbackData("login", "type", "level")

#start
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Приветствую, {message.from_user.full_name}!\n'
                         f'Для продолжения работы войдите или зарегестрируйтесь:', reply_markup=login_menu)

login_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text = "Вход", callback_data = callback_data.new(type = "lg", level = 0))
        ],
        [
            InlineKeyboardButton(text = "Регестрация", callback_data = callback_data.new(type = "reg", level = 0))
        ],
    ],
    resize_keyboard=True
)

#для логин кнопок:
@dp.callback_query_handler(text_contains="lg")
async def enter(call: CallbackQuery):
    await call.answer(cache_time=15)
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    await call.message.answer("Вы успешно вошли!", reply_markup = main_menu)
    await call.message.edit_reply_markup()

@dp.callback_query_handler(text_contains="reg")
async def reg(call: CallbackQuery):
    await call.answer(cache_time=15)
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    await call.message.answer("Вы успешно зарегестрировались!", reply_markup = main_menu)
    await call.message.edit_reply_markup()


main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text = "Профиль", callback_data = callback_data.new(type = "prof", level = 1))
        ],
        [
            InlineKeyboardButton(text = "Расписание", callback_data = callback_data.new(type = "shed", level = 1))
        ],
        [
            InlineKeyboardButton(text = "Личные записи", callback_data = callback_data.new(type = "pers", level = 1))
        ],
        [
            InlineKeyboardButton(text = "Список группы", callback_data = callback_data.new(type = "group", level = 1))
        ],
        [
            InlineKeyboardButton(text = "Выход", callback_data = callback_data.new(type = "exit", level = 1))
        ]
    ],
    resize_keyboard=True
)

#выход из основной менюшки
@dp.callback_query_handler(text_contains="exit")
async def cancel(call: CallbackQuery):
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    await call.answer("Вы вышли", show_alert=True)
    await call.message.edit_reply_markup()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

