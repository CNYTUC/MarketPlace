import conf
import modules.user as user
import modules.fonksiyonlar as fnks

internet_kontrolcu = fnks.Internet()
yazi_frmt = fnks.YaziFormat()

#Hoşgeldiniz

print("🚀 MarketPlace Test Uygulaması Başlatıldı!")

# 1) INTERNET SIVISINI BAŞLAT
# fnks modülü içindeki Internet sınıfından bir nesne oluşturuyoruz

while True:
    # Nesne üzerinden çağırıyoruz ve 'i' parametresi için 1 değerini gönderiyoruz
    if internet_kontrolcu.Ikontrol(i=1):
        break
    print(yazi_frmt.Yazi.Red(f"İnternet bağlantısı Kurulamadı. Lütfen Tekrar deneyiniz!!!"))


# 2) Kullanıcı işlemleri
# ==================================================================================
if user.kullanici_atama():

    if conf.Gecerli_Aktiflik == "1":

        print(yazi_frmt.Yazi.Green(f"Giriş Başarılı\nKullanıcı Adı: {conf.Gecerli_Name}")
        )

# 3) Hisse Senedi Listesini Çek










