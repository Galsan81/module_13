from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext



api = ""
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())



class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

key1 = InlineKeyboardMarkup(resize_keyboard=True)
but1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
but2 = InlineKeyboardButton(text='Формула расчета', callback_data='formulas')
key1.add(but1)
key1.add(but2)

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=key1)

@dp.callback_query_handler(text='formulas') #связь с кнопкой but2
async def get_formulas(call): 
    await call.message.answer('Норма калорий для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer() # чтобы кнопка не залипла, и стала доступной после нажатия

@dp.callback_query_handler(text='calories') #связь с кнопкой but1
async def set_age(call):
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight) # реагирует на переданное состояние User.State.weight
async def send_calories(message, state):
    await state.update_data(weight=message.text) # обновляет данные в состоянии weight на message.text
    data = await state.get_data() # запоминает все введенные раннее состояния
    await message.answer(f"Ваша норма калорий {10*float(data['weight'])+6.25*float(data['growth'])-5*float(data['age'])+5}")

    await state.finish()
# для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;

@dp.message_handler(commands=['start'])
async def start(message):
    #стартовое меню клавиатур
    start_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Рассчитать')],
                                               [KeyboardButton(text='Информация')]], resize_keyboard=True)

    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = start_menu)

@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)