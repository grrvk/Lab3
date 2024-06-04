from random import randint
from src.config import settings
import requests
import threading
import time
from datetime import datetime


class TestThreading(object):
    def __init__(self, interval=1):
        self.interval = interval
        self.stop = False
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        while True:
            if self.stop:
                break
            payload = {'command': "status"}
            response = requests.get(settings.url, params=payload)
            print(f"{response.text}")
            time.sleep(self.interval)


def get_recalculation_status(stop_arg):
    while True:
        if stop_arg:
            break
        payload = {'command': "status"}
        response = requests.get(settings.url, params=payload)
        print(f"{response.text}")
        time.sleep(1)


class KeyGen:
    def __init__(self, generator, primary, users, index):
        self.generator = generator
        self.primary = primary
        self.users = users
        self.index = index

    def get_base_public_shared(self, private):
        return self.generator ** private % self.primary

    def get_part_public_shared(self, base, private):
        return base ** private % self.primary


def seconds_count():
    time_count = datetime.utcnow().timestamp()
    while time_count % 10 != 0:
        time_count = int(datetime.utcnow().timestamp())
    print(time_count)
    return time_count


class User:
    def __init__(self, name, interval=1):
        self.name = name
        self.private_key = randint(16, 32)
        self.public_private_shared_key = None
        self.recalculation_status = False
        self.key = None

        #thread data
        self.interval_thread = interval
        self.stop_thread = False
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True

    def run(self):
        while True:
            if self.stop_thread:
                break
            if self.recalculation_status:
                recalculating = threading.Thread(target=self.recalculate_client, args=())
                recalculating.start()
                recalculating.join()
                self.recalculation_status = True
            response = requests.get(settings.url, params={'command': "status", 'user': self.name})
            #print(f"{response.text}")
            self.recalculation_status = False if response.text == "false" else True
            #print(f"{self.name}: recalc {self.recalculation_status}")
            time.sleep(self.interval_thread)

    def connect(self):
        payload = {'command': "connect", 'user': self.name}
        response = requests.get(settings.url, params=payload)
        print(f"{self.name}: {response.text}")
        #self.recalculation_status = True
        self.thread.start()
        time.sleep(1)
        print(f"{self.name} is thread alive connect: {self.thread.is_alive()}")

    def disconnect(self):
        self.stop_thread = True
        payload = {'command': "disconnect", 'user': self.name}
        response = requests.get(settings.url, params=payload)
        print(response.text)
        time.sleep(1)
        print(f"{self.name} is thread alive disconnect: {self.thread.is_alive()}")

    def send_message(self, message):
        payload = {'command': "send_message", 'user': self.name, 'message': message}
        response = requests.get(settings.url, params=payload)
        print(response.text)
        print(f"{self.name} is thread alive message: {self.thread.is_alive()}")

    def wait(self):
        seconds = threading.Thread(target=seconds_count, args=())
        seconds.start()
        seconds.join()

    def recalculate_client(self):
        seconds = threading.Thread(target=seconds_count, args=())
        seconds.start()
        seconds.join()

        response = requests.get(settings.url, params={'command': "get_data", 'user': self.name})

        members = response.json()['chat_users'].split()
        self.key = KeyGen(response.json()['gen'], response.json()['primary'],
                          members, members.index(self.name))
        r = requests.get(settings.url, params={'command': "upd_shared", 'user': self.name,
                                               'value': self.key.get_base_public_shared(self.private_key)})
        seconds = threading.Thread(target=seconds_count, args=())
        seconds.start()
        seconds.join()

        print(f"{self.name}: begin - gen {response.json()['gen']}, pr - {response.json()['primary']}, "
              f"index - {members.index(self.name)}, start_val: {self.key.get_base_public_shared(self.private_key)}")

        for i in range(len(members) - 2):
            seconds = threading.Thread(target=seconds_count, args=())
            seconds.start()
            seconds.join()

            payload = {'command': "current_shared", 'user': self.name,
                       'index': (self.key.index + i + 1) % len(members), "process": "process"}
            print(payload)
            response = int(requests.get(settings.url, params=payload).text)
            requests.get(settings.url,
                         params={'command': "upd_shared", 'user': self.name,
                                 'value': self.key.get_part_public_shared(response, self.private_key)})
            print(f"user {self.name}: asked index - {(self.key.index + i + 1) % len(members)}, "
                  f"got val - {response}, sent_upd - {self.key.get_part_public_shared(response, self.private_key)}")

        payload = {'command': "current_shared", 'user': self.name,
                   'index': (self.key.index + 1) % len(members), "process": "fin"}
        print(requests.get(settings.url, params=payload).text)

        number = int(requests.get(settings.url, params=payload).text)
        self.public_private_shared_key = self.key.get_part_public_shared(number, self.private_key)

        print(f"{self.name} finished with {self.public_private_shared_key}")
        time.sleep(1)
