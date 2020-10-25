import time
import datetime
import vk_api

from getpass import getpass

log = input('Введите логин: ')
passwd = getpass('Введи пароль: ')

def auth_handler(): #если есть двухфакторная аутентификция, то вызывается эта функция
    key = input("Введи код двухфакторной аутентификации: ") #код аутентификации
    remember_device = True # если: True - сохранить, False - не сохранять
    return key, remember_device


def main():
    login, password = log, passwd
    vk_session = vk_api.VkApi(
        login, password,
        # функция для обработки двухфакторной аутентификации
        auth_handler = auth_handler
    )

    try:
        def countdown(stop):
            while True:
                vk_session.auth()
                delta = datetime.timedelta(hours = 3)
                t = (datetime.datetime.now(datetime.timezone.utc) + delta)
                nowtime = t.strftime("%H:%M") #текущее время
                nowdate = t.strftime("%d.%m.%Y") #текущая дата
                on = vk_session.method("friends.getOnline") 
                counted = len(on) #количество друзей в онлайне
                vk_session.method("status.set", {"text": "Сейчас в Москве: " + nowtime})
                time.sleep(2 * 60) #время в минутах для автообновления статуса (без капчи - от двух-трёх минут и выше

        end_time = datetime.datetime(9999, 9, 1, 0, 0, 0)
        countdown(end_time)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
main()
