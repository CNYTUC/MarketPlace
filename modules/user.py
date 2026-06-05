from ast import Str, While

from supabase import create_client, Client
from dotenv import load_dotenv
import os

import _C._c_Format as frmt
import conf

load_dotenv()
TableName = "MC_User"

def get_client() -> Client:
    url  = os.getenv("SUPABASE_URL")
    key  = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise EnvironmentError("SUPABASE_URL veya SUPABASE_KEY eksik.")
    return create_client(url, key)


# ── CREATE ────────────────────────────────────────────────────────────────────

def create_user(name: str, email: str,
                telegram_chat_id: str = None,
                is_active: bool = True) -> dict:
    """Yeni kullanıcı oluşturur. Email zaten varsa hata fırlatır."""
    client = get_client()
    payload = {
        "name"            : name,
        "email"           : email,
        "telegram_chat_id": telegram_chat_id,
        "is_active"       : is_active,
    }
    result = client.table(TableName).insert(payload).execute()
    return result.data[0]

# ── READ ──────────────────────────────────────────────────────────────────────

def get_all_users() -> list[dict]:
    """Tüm kullanıcıları döndürür."""
    client = get_client()
    result = client.table(TableName).select("*").order("id").execute()
    return result.data

def get_user_by_id(user_id: str) -> dict | None:
    """UUID ile kullanıcı getirir. Bulunamazsa None döner."""
    client = get_client()
    result = (
        client.table(TableName)
        .select("*")
        .eq("id", user_id)
        .maybe_single()
        .execute()
    )
    return result.data

def get_user_by_email(email: str) -> dict | None:
    """Email ile kullanıcı getirir. Bulunamazsa None döner."""
    client = get_client()
    result = (
        client.table(TableName)
        .select("*")
        .eq("email", email)
        .maybe_single()
        .execute()
    )
    return result.data

def get_active_users() -> list[dict]:
    """Sadece is_active=True olan kullanıcıları döndürür."""
    client = get_client()
    result = (
        client.table(TableName)
        .select("*")
        .eq("is_active", True)
        .order("id")
        .execute()
    )
    return result.data


# ── UPDATE ────────────────────────────────────────────────────────────────────

def update_user(user_id: str, **fields) -> dict:
    """
    Verilen alanları günceller.
    Kullanım: update_user(id, name="Ali", telegram_chat_id="123")
    """
    if not fields:
        raise ValueError("En az bir alan belirtilmeli.")
    client = get_client()
    result = (
        client.table(TableName)
        .update(fields)
        .eq("id", user_id)
        .execute()
    )
    return result.data[0]

def deactivate_user(user_id: str) -> dict:
    """Kullanıcıyı pasif yapar (silmez)."""
    return update_user(user_id, is_active=False)

def activate_user(user_id: str) -> dict:
    """Pasif kullanıcıyı tekrar aktif yapar."""
    return update_user(user_id, is_active=True)


# ── DELETE ────────────────────────────────────────────────────────────────────

def delete_user(user_id: str) -> bool:
    """
    Kullanıcıyı kalıcı olarak siler.
    Genellikle deactivate_user() tercih edilmeli.
    """
    client = get_client()
    result = (
        client.table(TableName)
        .delete()
        .eq("id", user_id)
        .execute()
    )
    return len(result.data) > 0

# ── YARDIMCILAR────────────────────────────────────────────────────────────────

def kullanici_atama():

    while True:

        # 1. KULLANICI TÜRÜ SEÇİMİ
        while True:
            print(frmt.Yazi.White("1. Mevcut Kullanıcı"))
            print(frmt.Yazi.White("2. Yeni Kullanıcı"))
            kullaniciTuru = input(frmt.Yazi.BlueLight("Lütfen kullanıcı türünü seçin: "))
            print("")
            if kullaniciTuru in ["1", "2"]:
                break
            print(frmt.Yazi.Red("Geçersiz seçim!\n"))

        # 2. MEVCUT KULLANICI
        if kullaniciTuru == "1":
            tum_kullanicilar = get_all_users()
            secim = None

            while True:
                aranan_isim = input(frmt.Yazi.White("Lütfen adınızı girin: "))
                bulunan = None

                for kullanici in tum_kullanicilar:
                    if kullanici.get("name") == aranan_isim:
                        bulunan = kullanici
                        break

                if bulunan:
                    conf.Gecerli_Name         = bulunan.get("name")
                    conf.Gecerli_Mail         = bulunan.get("email")
                    conf.Gecerli_Telegram_ID  = bulunan.get("telegram_chat_id")
                    conf.Gecerli_Aktiflik     = bulunan.get("is_active")
                    print(frmt.Yazi.GreenLight(f"\nGiriş başarılı! Hoş geldiniz, {aranan_isim}.\n"))
                    break

                print(frmt.Yazi.Red(f"{aranan_isim} adında kullanıcı bulunamadı.\n"))

                while True:
                    print(frmt.Yazi.White("1. Yeniden dene"))
                    print(frmt.Yazi.White("2. Bir Üst Menü"))
                    secim = input(frmt.Yazi.BlueLight("Seçiminiz: "))
                    print("")
                    if secim in ["1", "2"]:
                        break
                    print(frmt.Yazi.Red("Geçersiz seçim!\n"))

                if secim == "2":
                    break

            if secim == "2":
                continue

            break  # Başarılı giriş → ana döngüden çık

        # 3. YENİ KULLANICI
        elif kullaniciTuru == "2":
            tum_kullanicilar = get_all_users()
            mevcut_isimler = [k.get("name") for k in tum_kullanicilar]
            mevcut_mailler = [k.get("email") for k in tum_kullanicilar]

            # İsim al — mükerrer kontrolü
            while True:
                y_Name = input(frmt.Yazi.BlueLight("Kullanıcı adı: "))
                if y_Name in mevcut_isimler:
                    print(frmt.Yazi.Red(f"'{y_Name}' adı zaten kayıtlı. Farklı bir ad girin.\n"))
                else:
                    break

            # Mail al — mükerrer kontrolü
            while True:
                y_Mail = input(frmt.Yazi.BlueLight("Mail adresi: "))
                if y_Mail in mevcut_mailler:
                    print(frmt.Yazi.Red(f"'{y_Mail}' zaten kayıtlı. Farklı bir mail girin.\n"))
                else:
                    break

            # Telegram ID al
            y_Telegram_ID = input(frmt.Yazi.BlueLight("Telegram Chat ID: "))

            # Veritabanına kaydet
            yeni = create_user(
                name=y_Name,
                email=y_Mail,
                telegram_chat_id=y_Telegram_ID
            )

            # conf'a ata
            conf.Gecerli_Name        = yeni.get("name")
            conf.Gecerli_Mail        = yeni.get("email")
            conf.Gecerli_Telegram_ID = yeni.get("telegram_chat_id")
            conf.Gecerli_Aktiflik    = yeni.get("is_active")

            print(frmt.Yazi.GreenLight(f"\nKayıt başarılı! Hoş geldiniz, {y_Name}.\n"))
            break
