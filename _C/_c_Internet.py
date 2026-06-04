##########################################################
# ---------------GENEL INTERNET İŞLEMLERİ----------------#
##########################################################

from urllib import request  # Internet İşlemleri
import _c_Format as _Format
import _c_Zaman as _Zaman


def I_Kontrol(host='http://google.com') -> bool:
    try:
        request.urlopen(host)  # Python 3.x
        return True
    except Exception as e:
        print(f"Hata tespit edildi: {str(e)}")
        return False


def Varmi(Sure: int):
    while not I_Kontrol():
        print("Şu anda internet bulunmamakta.")
        print("Sizin için " + _Format.Yazi.Yellow(str(Sure)) + " sonra tekrar deneyeceğiz.\n")
        _Zaman.Bekle(10)
