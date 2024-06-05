from src.scheme import User
import time

"""change user name"""

your_user = User('vika')
your_user.connect()
time.sleep(15)
message = "hi"
your_user.send_message(message, 'vika')
time.sleep(15)
your_user.disconnect()
