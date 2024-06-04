from algo.aes import encrypt
from src.scheme import User
import time

from algo.shrek import exit_handler
import atexit

atexit.register(exit_handler)

"""change user name"""

your_user = User('your_user')
your_user.connect()
time.sleep(30)
message = "hi"

enc_message = encrypt(message, str(your_user.private_key))
your_user.send_message(str(enc_message))
time.sleep(30)
your_user.disconnect()
