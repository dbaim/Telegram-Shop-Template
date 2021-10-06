#!/usr/bin/python
# -*- coding: utf8 -*-


from aiogram.types import message, message_auto_delete_timer_changed, message_entity
from config import TOKEN
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from sqlite3 import Error

import re
import markups as nav
import sqlite3

allCart: list = []
finalPrice: list = []

executes_pos1: dict = {}
executes_pos2: dict = {}


def listToString(s):
    str1 = ","
    return (str1.join(s))


class Position:
    type: int
    quantity: int
    color: int
    price: int

    def __init__(self, type, quantity, color):
        self.type = type
        self.quantity = quantity
        self.color = color
        if self.type == 800:
            self.price = 2100 * self.quantity
        else:
            self.price = 2500 * self.quantity

    def ReturnPosition(self):
        return str(self.color) + " " + str(self.type) + " " + str(self.quantity) + " pieces."


class Client:
    phone: str
    address: str
    zakaz: str

    def __init__(self, phone, addres, zakaz) -> None:
        self.phone = phone
        self.address = addres
        self.zakaz = zakaz

    def ReturnAll(self):
        return self.phone + " " + self.address + " " + self.zakaz


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def Avaliable_type1(conn, type):
    sql = '''SELECT kolvo FROM tovary1500 WHERE color = (?)'''
    cur = conn.cursor()
    cur.execute(sql, [type])
    if int(cur.fetchone()[0]) == 0:
        return False
    return True


def QuantityMoreThanN(conn, type, quantity):
    sql = '''SELECT kolvo FROM tovary1500 WHERE color = (?)'''
    cur = conn.cursor()
    cur.execute(sql, [type])
    if int(cur.fetchone()[0]) - quantity < 0:
        return True
    return False


def Avaliable_type2(conn, type):
    sql = '''SELECT kolvo FROM tovary800 WHERE color = (?)'''
    cur = conn.cursor()
    cur.execute(sql, [type])
    if int(cur.fetchone()[0]) == 0:
        return False
    return True


def QuantityMoreThanKolvo800(conn, type, quantity):
    sql = '''SELECT kolvo FROM tovary800 WHERE color = (?)'''
    cur = conn.cursor()
    cur.execute(sql, [type])
    if int(cur.fetchone()[0]) - quantity < 0:
        return True
    return False


def create_client(conn, task):
    sql = ''' INSERT INTO client (tg_user, phone, address, zakaz)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid


database = r"Shop.db"  # Your DB path
conn = create_connection(database)

# Bot initialization
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# Commands
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "Hi, {0.first_name}!\nThis telegram bot for ordering some goods. Below you will find a catalog of the products that are in stock. Thank you for choosing us. \nHappy shopping!".format(
                               message.from_user), reply_markup=nav.mainMenu)


# Навигация
@dp.message_handler(text="⬅️ Main Menu")
async def cmd_random(message: types.Message):
    await bot.send_message(message.from_user.id, 'Main menu', reply_markup=nav.mainMenu)


@dp.message_handler(text="Catalog")
async def cmd_random(message: types.Message):
    await bot.send_message(message.from_user.id, 'Choose a product', reply_markup=nav.CatMenu)


@dp.message_handler(text="Cart")
async def cmd_random(message: types.Message):
    await bot.send_message(message.from_user.id, 'You are in the cart', reply_markup=nav.KorzMenu)
    global finalPrice
    if not allCart:
        await bot.send_message(message.from_user.id, 'Cart is empty', reply_markup=nav.mainMenu)
    else:
        await bot.send_message(message.from_user.id,
                               f"Your cart: " + listToString(allCart) + " Overall price: " + str(sum(
                                   finalPrice)) + " $")


# Catalog
@dp.message_handler(text="Shop Item Type 1")
async def send_1(message: types.Message):
    global AllTs
    AllTs = open("all ts.jpg", 'rb')
    await bot.send_photo(message.from_user.id, AllTs,
                         caption="Price: 2100 \nDescription: ...",
                         reply_markup=nav.MainPropMenu)
    global position
    position = Position(800, 0, "default")


@dp.message_handler(text="Shop Item Type 2")
async def send_2(message: types.Message):
    global AllTs
    AllTs = open("all ts.jpg", 'rb')
    await bot.send_photo(message.from_user.id, AllTs,
                         caption="Price: 2500 \nDescription: ...",
                         reply_markup=nav.MainPropMenu)
    global position
    position = Position(1500, 0, "default")


# Color or other properties
@dp.message_handler(text="Shop Item Properties")
async def cmd_random(message: types.Message):
    await message.reply("All colors are below", reply_markup=nav.ColMenu)


@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    global red
    red = open("red t.jpg", 'rb')
    await bot.send_photo(callback_query.from_user.id, red, caption="Red is chosen",
                         reply_markup=nav.MainQMenu)
    global position
    position.color = "Red"


@dp.callback_query_handler(lambda c: c.data == 'button2')
async def process_callback_button1(callback_query: types.CallbackQuery):
    global blue
    blue = open("blue t.jpg", 'rb')
    await bot.send_photo(callback_query.from_user.id, blue, caption="Blue is chosen", reply_markup=nav.MainQMenu)
    global position
    position.color = "Blue"


@dp.callback_query_handler(lambda c: c.data == 'button3')
async def process_callback_button1(callback_query: types.CallbackQuery):
    global green
    green = open("green t.jpg", 'rb')
    await bot.send_photo(callback_query.from_user.id, green, caption="Green is chosen",
                         reply_markup=nav.MainQMenu)
    global position
    position.color = "Green"


# Quantity
@dp.message_handler(text="Choose a quantity")
async def cmd_random(message: types.Message):
    await message.reply("Type in an amount of this product that you want: ")

    @dp.message_handler(regexp='^([1-9][0-9]{0,2}|1000)$')
    async def take_quantity(message: types.Message):
        global position
        global allCart
        position.quantity = int(message.text)
        if position.type == 1500:
            position.price = 2500 * position.quantity
        if position.type == 800:
            position.price = 2100 * position.quantity
        await message.reply(
            "If you want to continue ordering and empty the cart, click the 'Continue order' button \nTo add an order to the cart, click 'Add to cart'",
            reply_markup=nav.DecMenu)


# Navigation
@dp.message_handler(text="Continue Shopping")
async def cmd_random(message: types.Message):
    global allCart
    allCart.clear()
    await bot.send_message(message.from_user.id, 'Main Menu', reply_markup=nav.mainMenu)


@dp.message_handler(text="Add to Cart")
async def cmd_random(message: types.Message):
    global position
    if position.type == 1500:
        with conn:
            if QuantityMoreThanN(conn, position.color, position.quantity):
                await bot.send_message(message.from_user.id,
                                       f"Sorry, the product of color {position.color} is out of stock in that quantity ",
                                       reply_markup=nav.mainMenu)
            elif Avaliable_type1(conn, position.color):
                cur = conn.cursor()
                sql = '''SELECT kolvo FROM tovary1500 WHERE color = (?)'''
                cur.execute(sql, [position.color])
                new_kolvo = int(cur.fetchone()[0]) - position.quantity
                sql1 = f'''UPDATE tovary1500 SET kolvo = {new_kolvo} WHERE color = (?)'''
                executes_pos1[sql1] = [position.color]
                allCart.append(position.ReturnPosition())
                finalPrice.append(position.price)
                await bot.send_message(message.from_user.id, f"Your order: " + listToString(allCart),
                                       reply_markup=nav.DecMenu1)


            else:
                await bot.send_message(message.from_user.id, f"Sorry, the product of color {position.color} is out of stock in that quantity ",
                                       reply_markup=nav.mainMenu)

    if position.type == 800:
        with conn:
            if QuantityMoreThanKolvo800(conn, position.color, position.quantity):
                await bot.send_message(message.from_user.id,
                                       f"Sorry, the product of color {position.color} is out of stock in that quantity ",
                                       reply_markup=nav.mainMenu)
            elif Avaliable_type2(conn, position.color):
                cur = conn.cursor()
                sql = '''SELECT kolvo FROM tovary800 WHERE color = (?)'''
                cur.execute(sql, [position.color])
                new_kolvo = int(cur.fetchone()[0]) - position.quantity
                sql1 = f'''UPDATE tovary800 SET kolvo = {new_kolvo} WHERE color = (?)'''
                executes_pos2[sql1] = [position.color]
                allCart.append(position.ReturnPosition())
                finalPrice.append(position.price)
                await bot.send_message(message.from_user.id, f"Your order: " + listToString(allCart),
                                       reply_markup=nav.DecMenu1)


            else:
                await bot.send_message(message.from_user.id, f"Sorry, the product of color {position.color} is out of stock in that quantity ",
                                       reply_markup=nav.mainMenu)


@dp.message_handler(text="No")
async def cmd_random(message: types.Message):
    allCart.clear()
    await bot.send_message(message.from_user.id, 'Main menu', reply_markup=nav.mainMenu)


# Формирование клиента
@dp.message_handler(text="Yes")
async def take_phone(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'The item has been added to the cart! To place an order, go to the shopping cart. You can continue shopping ',
                           reply_markup=nav.mainMenu)


# Корзина
@dp.message_handler(text="Clear cart")
async def clean(message: types.Message):
    global allCart
    allCart.clear()
    await bot.send_message(message.from_user.id, "Cart is empty")


@dp.message_handler(text="Form an order")
async def take_phone(message: types.Message):
    global clien
    global position
    zakaz = position.ReturnPosition()
    clien = Client('none', 'none', zakaz)
    await bot.send_message(message.from_user.id,
                           f"Overall price: {position.price} $. Enter your phone number starting with 8 to continue shopping ")

    @dp.message_handler(regexp='^[8][0-9]{10}$')
    async def take_phone(message: types.Message):
        global clien
        clien.phone = message.text
        print(clien.ReturnAll())
        await bot.send_message(message.from_user.id, "Enter your address info")

        @dp.message_handler()
        async def take_address(message: types.Message):
            tg_user: str = message.from_user.id
            clien.address = message.text
            print(clien.ReturnAll())
            with conn:
                task_2 = (tg_user, clien.phone, clien.address, listToString(allCart))
                create_client(conn, task_2)
                conn.commit()
            await bot.send_message(message.from_user.id,
                                   'Done! Your order has been accepted and is already being prepared for assembly. Please wait to contact you shortly to discuss delivery or pickup details.',
                                   reply_markup=nav.mainMenu)
            if executes_pos1:
                with conn:
                    cur = conn.cursor()
                    for i in executes_pos1:
                        cur.execute(i, executes_pos1[i])

            if executes_pos2:
                with conn:
                    cur = conn.cursor()
                    for i in executes_pos2:
                        cur.execute(i, executes_pos2[i])

            allCart.clear()


if __name__ == '__main__':
    executor.start_polling(dp)