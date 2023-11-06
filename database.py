import json
import datetime


class account:
    __data = {}

    def __init__(self, file):
        self.file = file
        with open(file, "r") as f:
            self.__data = json.load(f)

    def user_name(self, di, user):
        self.__data["account"][str(di)] = {
            "user": user,
            "mal": [],
            "mashinalar": [],
            "rangi": [],
            "soni": [],
            "narxi": [],
            "vaqti": [],
            "Hozir": [],
        }
        self.__save()

    def hozir(self, di, ho):
        self.__data["account"][str(di)]["Hozir"] = ho
        self.__save()

    def set_hozir(self, di) -> list:
        return self.__data["account"][str(di)]["Hozir"]

    def xarid(self, ID, mashina, rangi, soni, na):
        m = self.__data["account"][ID]["mashinalar"]
        r = self.__data["account"][ID]["rangi"]
        s = self.__data["account"][ID]["soni"]
        n = self.__data["account"][ID]["narxi"]
        v = self.__data["account"][ID]["vaqti"]
        m.append(mashina)
        r.append(rangi)
        s.append(soni)
        n.append(na)
        v.append(datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
        self.__data["account"][ID]["mashinalar"] = m
        self.__data["account"][ID]["rangi"] = r
        self.__data["account"][ID]["soni"] = s
        self.__data["account"][ID]["narxi"] = n
        self.__data["account"][ID]["vaqti"] = v
        self.__save()

    def get_mal(self, ID) -> list:
        try:
            return self.__data["account"][ID]["mal"]
        except Exception:
            return []

    def set_mal(self, ID: str, mal: list):
        self.__data["account"][ID]["mal"] = mal
        self.__save()

    def Barcha_xaridlar(self, ID) -> str:
        mal = "🛒 Sizning barcha xaridlaringiz :\n"
        try:
            m = self.__data["account"][ID]["mashinalar"]
            r = self.__data["account"][ID]["rangi"]
            s = self.__data["account"][ID]["soni"]
            n = self.__data["account"][ID]["narxi"]
            v = self.__data["account"][ID]["vaqti"]
            bar = len(m) - 1
            uch = 0
            if bar >= 0:
                while bar >= 0:
                    uch += 1
                    mal += f"\n\n{str(uch)}.{m[bar]} {str(r[bar])} rangli: \n\t\t🛍 xaridlar soni: {s[bar]} \n\t\t💰 Narxi: {Formmat(n[bar])} so'm \n\t\t📅 Sotib olingan vaqti: {v[bar]}"
                    bar -= 1
                mal += f"\n\n\n💰 Jami: {Formmat(sum(n))} so'm"
                return mal
            else:
                return "😥 Siz hech narsa sotib olmadingiz !"
        except Exception:
            return "😥 Siz hech narsa sotib olmadingiz !"

    def mal_uzunlik(self, ID) -> int:
        try:
            return len(self.__data["account"][ID]["mal"])
        except Exception:
            return 0

    def foydalanuvchilar(self) -> int:
        s = 0
        for i in self.__data["account"]:
            try:
                if len(self.__data["account"][i]["mal"]) == 4:
                    s += 1
            except Exception:
                return s
        return s

    def account_data(self, ID, pr) -> str:
        r = ""
        mal = self.__data["account"][ID]["mal"]
        r += f"👤Bot foydalanuvchi: {mal[1]} {mal[0]}\n"
        r += f"Profil :@" + pr
        r += f"\nID: {ID}"
        r += f"\n📞 Telefon raqami: {mal[3]}"
        r += f"\n📧 Elektron pochtasi: {mal[2]}"
        return r

    def keyboard_set(self, ID: str, value: bool):
        self.__data["account"][ID]["key"] = value
        self.__save()

    def keyboard_get(self, ID) -> bool:
        try:
            return self.__data["account"][ID]["key"]
        except Exception:
            return False

    def delete(self, ID, number: int) -> bool:
        try:
            m = self.__data["account"][ID]["mashinalar"]
            r = self.__data["account"][ID]["rangi"]
            s = self.__data["account"][ID]["soni"]
            n = self.__data["account"][ID]["narxi"]
            v = self.__data["account"][ID]["vaqti"]
            m.reverse()
            r.reverse()
            s.reverse()
            n.reverse()
            v.reverse()
            if number <= len(m):
                del m[number - 1]
                del r[number - 1]
                del s[number - 1]
                del n[number - 1]
                del v[number - 1]
                m.reverse()
                r.reverse()
                s.reverse()
                n.reverse()
                v.reverse()
                self.__data["account"][ID]["mashinalar"] = m
                self.__data["account"][ID]["rangi"] = r
                self.__data["account"][ID]["soni"] = s
                self.__data["account"][ID]["narxi"] = n
                self.__data["account"][ID]["vaqti"] = v
                return True
                self.__save()
            else:
                return False
        except Exception:
            return False

    def __save(self):
        with open(self.file, "w") as f:
            json.dump(self.__data, f)


class car_database:
    __data = {}

    def __init__(self, file):
        self.file = file
        with open(self.file, "r") as f:
            self.__data = json.load(f)

    def kom(self) -> list:
        l = []
        for i in self.__data["car"]:
            l.append(i)
        return l

    def typ(self, ty):
        l = []
        for i in self.__data["car"][ty]:
            if i != "img":
                l.append(i)
        return l

    def mashina(self, km, ty):
        l = []
        for i in self.__data["car"][km][ty]:
            l.append(i)
        return l

    def mashina_color(self, km, ty, ma):
        l = []
        for i in self.__data["car"][km][ty][ma]["rangi"]:
            l.append(i)
        return l

    def money(self, km, ty, ma) -> int:
        return self.__data["car"][km][ty][ma]["narxi"]

    def img_kom(self, km):
        return self.__data["car"][km]["img"]

    def mashina_color_img(self, km, ty, ma, im):
        return self.__data["car"][km][ty][ma]["rangi"][im]


ac = account("Account.json")
car = car_database("Car.json")


def Formmat(v: int):
    v_revers = str(v)[::-1]
    c = 0
    res = ""
    for i in v_revers:
        c += 1
        if c != 3:
            res += i
            c += 0
        else:
            c = 0
            res += i
            res += " "
    return res[::-1]
