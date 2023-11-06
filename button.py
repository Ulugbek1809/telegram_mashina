from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from img import color

import database

tel = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Telefon raqamni yuborish", request_contact=True)]
], resize_keyboard=True)

menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.row("🚗 Mashinalar", "🛒 Xaridlar")
menu.row("👤 Account", "👥 Bot foydalanuvchilari")


def kom() -> InlineKeyboardMarkup:
    k = InlineKeyboardMarkup(row_width=2)
    for i in database.car.kom():
        s = InlineKeyboardButton(text=i, callback_data=i)
        k.insert(s)
    return k


def typ(kom0: str) -> InlineKeyboardMarkup:
    t = InlineKeyboardMarkup(row_width=2)
    for i in database.car.typ(kom0):
        s = InlineKeyboardButton(text=i, callback_data=i)
        t.insert(s)
    s = InlineKeyboardButton(text="🔙 ortga", callback_data="or1")
    t.insert(s)
    return t


def mashinalar(kom1, ty) -> InlineKeyboardMarkup:
    k = InlineKeyboardMarkup(row_width=2)
    for i in database.car.mashina(kom1, ty):
        s = InlineKeyboardButton(text=i, callback_data=i)
        k.insert(s)
    s = InlineKeyboardButton(text="🔙 ortga", callback_data="or2")
    k.insert(s)
    return k


def mashina_col(kom2, ty, mash) -> InlineKeyboardMarkup:
    k = InlineKeyboardMarkup(row_width=2)
    for i in database.car.mashina_color(kom2, ty, mash):
        s = InlineKeyboardButton(text=color(i), callback_data=i)
        k.insert(s)
    s = InlineKeyboardButton(text="🔙 ortga", callback_data="or3")
    k.insert(s)
    return k


def number() -> InlineKeyboardMarkup:
    k = InlineKeyboardMarkup(row_width=3)
    for i in range(1, 10):
        s = InlineKeyboardButton(text=str(i), callback_data=str(i))
        k.insert(s)
    s = InlineKeyboardButton(text="🔙 ortga", callback_data="or4")
    k.insert(s)
    return k


def final() -> InlineKeyboardMarkup:
    k = InlineKeyboardMarkup(row_width=2)
    s1 = InlineKeyboardButton(text="🔙 ortga", callback_data="or5")
    s2 = InlineKeyboardButton(text="🚗 Mashinalar", callback_data="or6")
    k.insert(s1)
    k.insert(s2)
    return k


account = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Ism ni o'zgartirish", callback_data="ism")],
    [InlineKeyboardButton(text="Familiyani o`zgartirish", callback_data="fam")],
    [InlineKeyboardButton(text="📧 Email ni o'zgartirish", callback_data="email")],
    [InlineKeyboardButton(text="📞 Telefon raqamni o'zgartirish", callback_data="tel", request_contact=True)]
])

bekor = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
bekor.row("❌ bekor qilish")

delet = InlineKeyboardMarkup()
de = InlineKeyboardButton(text="❌ Xaridni bekor qilish", callback_data="delete")
delet.insert(de)
