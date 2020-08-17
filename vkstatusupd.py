import time
import datetime
import vk_api


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция.
    """

    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def main():
    """ Пример обработки двухфакторной аутентификации """

    login, password = 'логин', 'пароль'
    vk_session = vk_api.VkApi(
        login, password,
        # функция для обработки двухфакторной аутентификации
        auth_handler=auth_handler
    )

    try:
        def countdown(stop):
            while True:
                vk_session.auth()
                delta = datetime.timedelta(hours=3, minutes=0)
                t = (datetime.datetime.now(datetime.timezone.utc) + delta)
                nowtime = t.strftime("%H:%M")
                nowdate = t.strftime("%d.%m.%Y")
                on = vk_session.method("friends.getOnline")
                counted = len(on)
                vk_session.method("status.set", {"text": "Сейчас в Москве: " + nowtime})
                time.sleep(2*60)

        end_time = datetime.datetime(9999, 9, 1, 0, 0, 0)
        countdown(end_time)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
main()
