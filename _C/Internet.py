##########################################################
# ---------------GENEL INTERNET İŞLEMLERİ----------------#
##########################################################

from urllib import request  # Internet İşlemleri
from _C import _c_Format as _Format
import _c_Zaman as _Zaman


def I_Kontrol(host='http://google.com') -> bool:
    try:
        request.urlopen(host)  # Python 3.x
        return True
    except Exception as e:
        print(f"Hata tespit edildi: {str(e)}")
        return False

#İnternet Kontrol
def Ikontrol2():
    try:
        # İnternet bağlantısını test etmek için örnek bir istek
        response = requests.get("https://httpbin.org", timeout=5)
        if response.status_code == 200:
            print(f"⏱️ Kontrol {i}: İnternet bağlantısı aktif, borsa sunucusu erişilebilir.")
            return True

    except Exception as e:
        print(f"❌ Kontrol {i} Başarısız: Bağlantı hatası! {e}")
        return False


def Varmi(Sure: int):
    while not I_Kontrol():
        print("Şu anda internet bulunmamakta.")
        print("Sizin için " + _Format.Yazi.Yellow(str(Sure)) + " sonra tekrar deneyeceğiz.\n")
        _Zaman.Bekle(10)
