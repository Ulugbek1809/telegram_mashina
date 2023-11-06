import logging
import re
from aiogram import Bot, Dispatcher, executor, types
import button
import database
from tok import Token
from aiogram.types import ReplyKeyboardRemove

logging.basicConfig(level=logging.INFO)
bot = Bot(token=Token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.message):
    try:
        d = str(message.from_user.id)
        nal = database.ac.get_mal(d)
        if not (database.ac.mal_uzunlik(d) == 4):
            database.ac.user_name(message.from_user.id, message.from_user.username)
            await message.answer(
                f"Assalomu alaykum {message.from_user.first_name} botga xush kelibsiz !\nBotdan foydalanish uchun ro`yhatdan o`ting")
            await message.answer("Isminginzni kiriting")
        else:
            await message.answer(f"Assalomu alaykum {nal[1]} {nal[0]} botga xush kelibsiz")
            await message.answer("Bot dan foydalanishinggiz mumkin", reply_markup=button.menu)
    except Exception:
        print("ERROR")
        database.ac.user_name(message.from_user.id, message.from_user.first_name)
        await message.answer(
            f"Assalomu alaykum {message.from_user.first_name} botga xush kelibsiz !\nBotdan foydalanish uchun ro`yhatdan o`ting")
        await message.answer("Isminginzni kiriting:")


@dp.message_handler(state="*")
async def malumotlarni_kiritish(message: types.Message):
    andoza = "[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+"
    d = str(message.from_user.id)
    mal = database.ac.get_mal(d)
    call = str(message.text)
    if database.ac.mal_uzunlik(d) == 0 and database.ac.keyboard_get(d) == False:
        mal.append(call)
        database.ac.set_mal(d, mal)
        await message.answer("Familiyanggizni kiriting:")
    elif database.ac.mal_uzunlik(d) == 1 and database.ac.keyboard_get(d) == False:
        mal.append(call)
        database.ac.set_mal(d, mal)
        await message.answer("📧 Elektron pochtanggizni kiriting:")
    elif database.ac.mal_uzunlik(d) == 2 and database.ac.keyboard_get(d) == False:
        if re.match(andoza, call):
            mal.append(call)
            database.ac.set_mal(d, mal)
            await message.answer("📞 Telefon raqaminggizni yuboring:", reply_markup=button.tel)
        else:
            await message.answer("❌ Email xato kiritildi !")
            await message.answer("📧 Elektron pochtanggizni kiriting:")
    elif call == "🚗 Mashinalar" and database.ac.mal_uzunlik(d) == 4:
        database.ac.hozir(message.from_user.id, [])
        await message.answer("Mashina ishlab chiqaruvchi kompaniyani tanlang:", reply_markup=button.kom())
    elif call == "🛒 Xaridlar" and database.ac.mal_uzunlik(d) == 4:
        if database.ac.Barcha_xaridlar(d) != "😥 Siz hech narsa sotib olmadingiz !":
            await message.answer(database.ac.Barcha_xaridlar(str(message.from_user.id)), reply_markup=button.delet)
        else:
            await message.answer(database.ac.Barcha_xaridlar(str(message.from_user.id)))
    elif call == "👥 Bot foydalanuvchilari" and database.ac.mal_uzunlik(d) == 4:
        await message.answer("Bot dan " + str(database.ac.foydalanuvchilar()) + " ta odam foydalanyapti")
    elif call == "👤 Account" and database.ac.mal_uzunlik(d) == 4:
        await message.answer(f"{database.ac.account_data(d, str(message.from_user.username))}",
                             reply_markup=button.account)
    elif call == "❌ bekor qilish":
        database.ac.hozir(d, [])
        await message.answer("❌ bekor qilindi", reply_markup=button.menu)
    elif database.ac.set_hozir(d) == ["ism"]:
        a = database.ac.get_mal(d)
        a = a[1:]
        a.copy()
        a.insert(0, call)
        database.ac.set_mal(d, a)
        await message.answer("ism muaffaqiyatli o'zgartirildi !", reply_markup=button.menu)
    elif database.ac.set_hozir(d) == ["fam"]:
        a = database.ac.get_mal(d)
        del a[1]
        a.insert(1, call)
        await message.answer("Familiya muaffaqiyatli o'zgartirildi !", reply_markup=button.menu)
    elif database.ac.set_hozir(d) == ["email"]:
        a = database.ac.get_mal(d)
        if re.match(andoza, str(call)):
            del a[2]
            a.insert(2, call)
            await message.answer("Email muaffaqiyatli o'zgartirildi !", reply_markup=button.menu)
        else:
            await message.answer("❌ Email xato kiritildi !")
            await message.answer("Yangi Email kiriting !")
    elif database.ac.set_hozir(d) == ["delete"]:
        try:
            if database.ac.delete(d, int(call)):
                await message.answer(f"❌ muaffaqiyatli bekor qilindi", reply_markup=button.menu)
            else:
                await message.answer(f"{call}-xarid mavjud emas !")
        except Exception:
            await message.answer("Xato qiymat kiritdingiz !")
    else:
        if database.ac.keyboard_get(d) == True and database.ac.mal_uzunlik(d) != 4:
            r = ReplyKeyboardRemove()
            await message.answer("Bot yangilandi  👉 /start ni bosing !", reply_markup=r)


@dp.message_handler(content_types=["contact"])
async def tel(message: types):
    num = message.contact["phone_number"]
    if database.ac.set_hozir(str(message.from_user.id)) == ["tel"]:
        a = database.ac.get_mal(str(message.from_user.id))
        del a[3]
        a.insert(3, str(num))
        database.ac.set_mal(str(message.from_user.id), a)
        await message.answer("Telefon raqam muafaqiyatli o'zgartirildi !", reply_markup=button.menu)
    else:
        a = database.ac.get_mal(str(message.from_user.id))
        a.append(num)
        database.ac.set_mal(str(message.from_user.id), a)
        database.ac.keyboard_set(str(message.from_user.id), True)
        await message.answer("Siz bot dan muaffaqiyatli ro'yihatdan o'tdingiz !")
        await message.answer("Bot dan foydalanishingiz mumkin", reply_markup=button.menu)


@dp.callback_query_handler()
async def umum(call: types.CallbackQuery):
    cal = str(call.data)
    d = str(call.from_user.id)
    ho = database.ac.set_hozir(d)
    am = ""
    await call.answer(cache_time=10)
    try:
        if cal in ["ism", "fam", "email", "tel", "delete"]:
            am = "ac"
            if cal == "ism":
                ho = ["ism"]
                await call.message.answer("Yangi ism kiriting :", reply_markup=button.bekor)
            elif cal == "fam":
                ho = ["fam"]
                await call.message.answer("Yangi familiya kiriting :", reply_markup=button.bekor)
            elif cal == "email":
                ho = ["email"]
                await call.message.answer("Yangi email kiriting :", reply_markup=button.bekor)
            elif cal == "tel":
                ho = ["tel"]
                await call.message.answer("Telefon raqamingizni yuboring", reply_markup=button.tel)
            elif cal == "delete":
                ho = ["delete"]
                await call.message.answer("Xaridning tartib raqamni yuboring !", reply_markup=button.bekor)
        if not (cal in ["or1", "or2", "or3", "or4", "or5", "or6"]) and database.ac.mal_uzunlik(d) == 4 and am != "ac":
            if len(ho) == 0:
                ho.append(cal)
                ho = ho[:1]
                await call.message.answer_photo(photo=open(database.car.img_kom(ho[0]), "rb"),
                                                caption=f"{cal} mashina turini tanlang",
                                                reply_markup=button.typ(cal))
            elif len(ho) == 1:
                ho.append(cal)
                ho = ho[:2]
                await call.message.answer_photo(photo=open(database.car.img_kom(ho[0]), "rb"),
                                                caption=f"{cal} mashinalarini tanlang:",
                                                reply_markup=button.mashinalar(ho[0], ho[1]))
            elif len(ho) == 2:
                ho.append(cal)
                ho = ho[:3]
                await call.message.answer_photo(
                    photo=open(database.car.mashina_color_img(ho[0], ho[1], ho[2], "oq"), "rb"),
                    caption=f"{cal} mashina rangini tanlang:",
                    reply_markup=button.mashina_col(ho[0], ho[1], ho[2]))
            elif len(ho) == 3:
                ho.append(cal)
                ho = ho[:4]
                await  call.message.answer_photo(
                    photo=open(database.car.mashina_color_img(ho[0], ho[1], ho[2], ho[3]), "rb"),
                    caption=f"Qancha {ho[3]} {ho[2]} sotib olmoqchisiz? \nNarxi: {database.Formmat(database.car.money(ho[0], ho[1], ho[2]))} so'm",
                    reply_markup=button.number())
            elif len(ho) == 4:
                ho.append(cal)
                ho = ho[:5]
                database.ac.xarid(d, ho[2], ho[3], ho[4], database.car.money(ho[0], ho[1], ho[2]) * int(ho[4]))
                await call.message.answer_photo(
                    photo=open(database.car.mashina_color_img(ho[0], ho[1], ho[2], ho[3]), "rb"),
                    caption=f"Siz {ho[4]} ta {ho[3]} {ho[2]} sotib oldinggiz ! \nNarxi: {database.Formmat(database.car.money(ho[0], ho[1], ho[2]) * int(ho[4]))} so'm",
                    reply_markup=button.final())
        else:
            if cal == "or1" and database.ac.mal_uzunlik(d) == 4:
                ho = []
                await call.message.answer("Mashina ishlab chiqaruvchi kompaniyani tanlang:", reply_markup=button.kom())
            elif cal == "or2" and database.ac.mal_uzunlik(d) == 4:
                ho = ho[:1]
                await call.message.answer_photo(photo=open(database.car.img_kom(ho[0]), "rb"),
                                                caption=f"{ho[0]} mashina turini tanlang",
                                                reply_markup=button.typ(ho[0]))
            elif cal == "or3" and database.ac.mal_uzunlik(d) == 4:
                ho = ho[:2]
                await call.message.answer_photo(photo=open(database.car.img_kom(ho[0]), "rb"),
                                                caption=f"{ho[1]} mashinalarini tanlang:",
                                                reply_markup=button.mashinalar(ho[0], ho[1]))
            elif cal == "or4" and database.ac.mal_uzunlik(d) == 4:
                ho = ho[:3]
                await call.message.answer_photo(
                    photo=open(database.car.mashina_color_img(ho[0], ho[1], ho[2], "oq"), "rb"),
                    caption=f"{ho[2]} mashina rangini tanlang:",
                    reply_markup=button.mashina_col(ho[0], ho[1], ho[2]))
            elif cal == "or5" and database.ac.mal_uzunlik(d) == 4:
                ho = ho[:2]
                print(len(ho))
                await call.message.answer_photo(
                    photo=open(database.car.img_kom(ho[0]), "rb"),
                    caption=f"{ho[1]} mashinalarini tanlang:",
                    reply_markup=button.mashinalar(ho[0], ho[1]))
            elif cal == "or6" and database.ac.mal_uzunlik(d) == 4:
                ho = []
                await call.message.answer("Mashina ishlab chiqaruvchi kompaniyani tanlang:", reply_markup=button.kom())
            else:
                if am != "ac":
                    rem = types.ReplyKeyboardRemove()
                    await call.message.answer("Bot yangilandi  👉 /start ni bosing !", reply_markup=rem)
        database.ac.hozir(d, ho)
        await call.message.delete()
    except Exception as e:
        await call.message.answer("Botda xatolik 👉 /start ni bosing !")
        print(e)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
