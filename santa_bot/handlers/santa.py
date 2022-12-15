from aiogram import types, executor
from dispatcher import dp
from bot import BotDB
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
import aiogram.utils.markdown as md
import random
import logging

logging.basicConfig(
    level=logging.INFO,
    filename = "mylog.log",
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
    )
DATA_LIST = []

        
# создаём форму и указываем поля
class Form(StatesGroup):
    addres = State() 
    number = State() 
    comment = State()
    fio = State()

@dp.message_handler(commands = "start")
async def start(message: types.Message):
    if(not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id, message.from_user.first_name)
    await message.bot.send_message(message.from_user.id, "Добро пожаловать! Для начала регистрации введите команду: /registration. Узнать количество учатников можно командой: /count")
    #await distribution_of_participants(message)

@dp.message_handler(commands = "add_data")
async def add_data(message: types.Message):
    user_id = message.from_user.id
    addres = DATA_LIST[0]
    number = DATA_LIST[1]
    comment = DATA_LIST[2]
    fio = DATA_LIST[3]
    logging.info(f"Добавлены данные:{user_id, addres, number, comment, fio}")
    print(type(user_id), type(addres), type(number), type(comment), type(fio))
    BotDB.add_data_users(user_id, addres, number, comment, fio)

@dp.message_handler(commands = "registration")
async def registration(message: types.Message):
    await Form.addres.set()
    await message.reply("Введите ваш адрес! Формат ввода: Страна, регион, город, улица")
            
@dp.message_handler(state=Form.addres)
async def process_addres(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['addres'] = message.text
    logging.info(f"{data['addres']}")
    await Form.next()
    await message.reply("Давай обменяемся номерами? Введите номер в формате: +7...")

@dp.message_handler(state=Form.number)
async def process_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number'] = message.text
    logging.info(f"{data['number']}")
    await Form.next()
    await message.reply("Какие есть пожелания(присутствует аалергия, непереносимость чего либо?)? . Если нет пожеланий, то введите слово: 'Нет")

@dp.message_handler(state=Form.comment)
async def process_comment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['comment'] = message.text
    logging.info(f"{data['comment']}")
    await Form.next()
    await message.reply("Забыл спросить, а как вас зовут? Введите вашу Фамилию, Имя")

# Сохраняем пол, выводим анкету
@dp.message_handler(state=Form.fio)
async def process_fio(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fio'] = message.text
        logging.info(f"{data['fio']}")
        markup = types.ReplyKeyboardRemove()
        await message.bot.send_message(
        message.chat.id,
            md.text(
                md.text('Рад с тобой познакомиться', md.bold(data['fio'])),
                md.text('Ты живешь:', data['addres']),
                md.text('Твой номер:', data['number']),
                md.text('Твое пожелание:', data['comment']),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )
        DATA_LIST.clear()
        for value in data.values():
            if value not in data.values():
                await message.bot.send_message(message.from_user.id, f"Значения поля {value} не были найдены. Повторите регистрацию. Введите команду /registration")
                break
            else:
                DATA_LIST.append(value)
    await state.finish()
    await message.bot.send_message(message.from_user.id, "Если все данные введены верно, введите команду: /add_data")

@dp.message_handler(commands = "count")
async def send_message_on_time(message: types.Message):
    await message.bot.send_message(message.from_user.id, f"Всего участников: {len(BotDB.number_of_users())}")

@dp.message_handler(commands = "start_random")  
async def distribution_of_participants(message: types.Message):
    sender = BotDB.info_of_participants()
    recipient = BotDB.info_of_participants()
    for i in sender:
        recipient_random = random.choice(recipient)
        if i == recipient_random:
            while i == recipient_random:
                recipient_random = random.choice(recipient)
                logging.info(f"i = {i}, recipient_random = {recipient_random}")
        await message.bot.send_message(i[1], f'Поздравляю! Тебе достался пользователь с ником: {recipient_random[5]}. Он живет по адресу: {recipient_random[2]}. Его предпочтения: {recipient_random[4]}. Контактный номер телефона / id в телеграм: {recipient_random[3]}, {recipient_random[1]}')
        logging.info(f"{i[1]}, 'Поздравляю! Тебе достался пользователь с ником: {recipient_random[5]}. Он живет по адресу: {recipient_random[2]}. Его предпочтения: {recipient_random[4]}. Контактный номер телефона / id в телеграм: {recipient_random[3]}, {recipient_random[1]}'")
        recipient.remove(recipient_random)
