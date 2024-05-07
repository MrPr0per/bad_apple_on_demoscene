import requests
import fake_useragent
import datetime
from colorama import Fore, Style


class Sender:
    header = {
        'User-Agent': str(fake_useragent.UserAgent().chrome),
        "Content-type": "application/x-www-form-urlencoded",
    }
    send_url = 'http://f0749945.xsph.ru/Demoscene/send.php'

    @classmethod
    def send(cls, msg, log=True, timeout=1):
        for attempt in range(6):
            try:
                r = requests.post(cls.send_url,
                                  data={"str": msg, "id": 999_999_999_999},
                                  headers=cls.header,
                                  timeout=timeout)
                break
            except Exception as e:
                print(e)
        else:
            raise Exception()
        if log:
            cls.log(msg, r)
        return r

    @classmethod
    def log(cls, msg, request=None):
        print(f'{Fore.GREEN}{datetime.datetime.now()}{Style.RESET_ALL}')
        print(msg)
        if request:
            print(request)
        print()
