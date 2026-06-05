import conf
import modules.user as user
import fonksiyonlar.f_str as f_str
import fonksiyonlar.f_internet as f_int
import fonksiyonlar.f_zaman as f_zaman

# 0) Hoşgeldiniz

print("🚀 MC Test Başlatıldı!\n")

# 1) INTERNET SINAMASI

while True:

    if f_int.kontrol():

        Msj = f"⏱️ İnternet bağlantısı aktif, borsa sunucusuna erişilebilir."
        print(f_str.MsjBasari(Msj))

        break

    Msj: str = f"❌ Başarısız: Bağlantı hatası! 5 sn içinde tekrar denenecek!!!"
    print(f_str.MsjIkaz(Msj))

    x = f_zaman.Bekle(5)

# 2) Adına işlem yapılacak Kullanıcı Sayısını Al

conf.tum_kullanicilar = user.get_all_users()
i = 0
for kullanici in conf.tum_kullanicilar:
    i = i + 1

if i == 0:
    Msj: str = f"❌ Başarısız: Adına işlem yapılacak kullanıcı bulunamadı!!!"
    print(f_str.MsjHata(Msj))
else:
    Msj = f"{i} kullanıcı için işlem başlatılıyor."
    print(f_str.MsjBasari(Msj))


# 3) Hisse Senedi Listesini Çek










