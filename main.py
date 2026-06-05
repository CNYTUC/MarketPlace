from modules.user import create_user, get_all_users
import modules.user as user

print("🚀 MarketPlace Test Uygulaması Başlatıldı!")

# Kullanıcı işlemleri
# ==================================================================================
if user.kullanici_atama():
    print(frmt.Yazi.Red(f"başarılı\n"))








# #İnternet Kontrol
#
# for i in range(1, 5):
#     try:
#         # İnternet bağlantısını test etmek için örnek bir istek
#         response = requests.get("https://httpbin.org", timeout=5)
#         if response.status_code == 200:
#             print(f"⏱️ Kontrol {i}: İnternet bağlantısı aktif, borsa sunucusu erişilebilir.")
#             break
#
#     except Exception as e:
#         print(f"❌ Kontrol {i} Başarısız: Bağlantı hatası! {e}")
#
#     time.sleep(2)  # 2 saniye bekle

