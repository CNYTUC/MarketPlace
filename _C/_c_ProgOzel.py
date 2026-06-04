#f8vPyp7CtjiIAoJuyvvZ0uPDA2zAtm3prmzmOG2NFxXG2mhDnM5ycHyMB4Gen9SO
#Aq6aF4oOLuHa7cMLsEureCNiPYw2RaBmdKj6ZVm7wkbJDbgORJ6icEXaJpQDt52m
#wss://stream.binance.com:443/ws/
# ÖRNEK Soket SOCKET = 'wss://stream.binance.com:443/ws/ethusdt@kline_1m'

import _c_Bnnc as _Binance
import _c_Sqlite as _Sql

COIN = ""
BINANCE_KEY = ""
BINANCE_SECRET_KEY = ""
BINANCE_SOCKET = ""
ZAMAN = ""
KALDIRAC = ""
ISLEM_TUTAR = ""
ARTARAK_DEVAM = ""
ISLEM_POZISYONU = ""
ESKI_KAYIT_SAYISI = ""
# ESKI KAYITLAR VERI TABANI
VERI_TABANI_ESKI_KAYITLAR = ""

def ESKI_KAYITLARI_EKLE(VERI_TABANI_ADI: str, COIN: str):

    # Verileri Ekle
    Kayitlar = _Binance.FutureOldPrices(COIN + "USDT")

    i = 0
    liste = []
    for item in Kayitlar:

        if i == 0:  liste.extend(['OpenTime', item])
        if i == 1:  liste.extend(['OpenPrc', item])
        if i == 2:  liste.extend(['HighPrc', item])
        if i == 3:  liste.extend(['LowPrc', item])
        if i == 4:  liste.extend(['ClosePrc', item])
        if i == 5:  liste.extend(['Volume', item])

        if i == 5:
            _Sql.veri.gir.genel(VERI_TABANI_ADI, COIN, liste)
            liste.clear()
            i = 0
        else:
            i += 1



