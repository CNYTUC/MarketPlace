import time  # Zaman
from datetime import datetime
from datetime import date

def Bekle(Sure: int):
    time.sleep(Sure)

def Saat():
    now = datetime.now()
    return now.strftime("%H:%M:%S")

def Gun():
    today = date.today()
    return today.strftime("%d/%m/%Y")

def GunSaat():
    return Gun() + " " + Saat()

def TimeStamp_GunFormat(timeStamp): return datetime.fromtimestamp(int(timeStamp) / 1000)