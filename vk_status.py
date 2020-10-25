import time
import datetime
import vk_api

from getpass import getpass

print('Итак, мне нужна небольшая настройка, уделите одну минуту...')
time.sleep(2)
log = input('Введите логин: ')
passwd = getpass('Введите пароль (скрыт, для обеспечения конфендициальности): ')
hours = int(input('Часовой пояс (в UTC-формате и только цифры): '))
text = input('Введите текст статуса: ')
times = int(input('Раз в сколько минут обновлять статус: '))


def auth_handler(): #если есть двухфакторная аутентификция, то вызывается эта функция
    key = input('Введите код двухфакторной аутентификации: ') #код аутентификации
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
        print('Авторизация прошла успешно! Наслаждайтесь Вашим статусом.')
        def countdown(stop):
            while True:
                vk_session.auth()
                delta = datetime.timedelta(hours = hours)
                t = (datetime.datetime.now(datetime.timezone.utc) + delta)
                nowtime = t.strftime("%H:%M") #текущее время
                nowdate = t.strftime("%d.%m.%Y") #текущая дата
                on = vk_session.method("friends.getOnline") 
                counted = len(on) #количество друзей в онлайне
                vk_session.method("status.set", {"text": f'{text} {nowtime}'})
                time.sleep(times * 60) #время в минутах для автообновления статуса (без капчи - от двух-трёх минут и выше)

        end_time = datetime.datetime(9999, 9, 1, 0, 0, 0)
        countdown(end_time)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
main()
