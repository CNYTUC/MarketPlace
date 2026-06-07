import conf
import modules.supabaseFnks as sbase
import fonksiyonlar.f_str as f_str
import fonksiyonlar.f_internet as f_int
import fonksiyonlar.f_zaman as f_zaman
from modules.veri import tum_hisselerin_verisini_cek
from modules.veri import veri_durumlarini_yazdir

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

conf.tum_kullanicilar = sbase.get_all_users()
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

conf.tum_hisseler = sbase.get_all_bist()

# 4) Hisse Senedi verilerini

i = 0

for x in conf.tum_hisseler:
    i += 1

if i == 0:
    Msj = "❌ Başarısız: İşlem yapılacak hisse bulunamadı!!!"
    print(f_str.MsjHata(Msj))

else:
    Msj = f"{i} Hisse Senedi bulundu."
    print(f_str.MsjBasari(Msj))

    (
        conf.hisse_verileri,
        conf.veri_durumlari,
        conf.basarili_hisseler,
        conf.veri_hatalari
    ) = tum_hisselerin_verisini_cek(
        conf.tum_hisseler,
        gun=300
    )

    veri_durumlarini_yazdir(conf.veri_durumlari)

    print()
    print(f_str.MsjBasari(
        f"{len(conf.basarili_hisseler)} hissenin verisi çekildi."
    ))

    print(f_str.MsjIkaz(
        f"{len(conf.basarisiz_hisseler)} hissede veri alınamadı."
    ))





