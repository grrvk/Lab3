from src.scheme import User
import time


vika = User('vika')
#margo = User('margo')
vika.connect()
#margo.connect()
time.sleep(3)
vika.send_message('hi')
time.sleep(3)
vika.disconnect()
#time.sleep(4)
#margo.disconnect()
