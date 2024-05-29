from src.scheme import User
import time


vika = User('vika')
margo = User('margo')
vika.connect()
margo.connect()
vika.send_message('hi')
vika.disconnect()
#time.sleep(4)
margo.disconnect()
