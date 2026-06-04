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
    # ANA DÖNGÜ (Menüler arası geçişi sağlar)
    while True:

        # 1. KULLANICI TÜRÜ SEÇİMİ
        # ────────────────────────────────────────────────────────────────
        while True:
            print(frmt.Yazi.White("1. Mevcut Kullanıcı"))
            print(frmt.Yazi.White("2. Yeni Kullanıcı"))
            kullaniciTuru = input(frmt.Yazi.BlueLight("Lütfen kullanıcı türünü seçin: "))
            print("")

            if kullaniciTuru in ["1", "2"]:
                break

            print(frmt.Yazi.Red("Geçersiz seçim!\n"))
        # ────────────────────────────────────────────────────────────────

        # 2. MEVCUT KULLANICI İŞLEMLERİ
        # ────────────────────────────────────────────────────────────────
        if kullaniciTuru == "1":
            tum_kullanicilar = get_all_users()
            secim = None  # Döngü dışından kontrol edebilmek için başta boş tanımlıyoruz

            # İSİM ARAMA DÖNGÜSÜ
            while True:
                aranan_isim = input(frmt.Yazi.White("Lütfen adinizi girin: "))
                aranan_isim_varmi = False

                # Kullanıcı kontrolü ve Değişken Atamaları
                for kullanici in tum_kullanicilar:
                    if kullanici.get("name") == aranan_isim:
                        aranan_isim_varmi = True

                        # İstediğin dış değişken atamaları tam burada yapılıyor:
                        conf.Gecerli_Name = aranan_isim
                        conf.Gecerli_Mail = kullanici.get("email")
                        conf.Gecerli_Telegram_ID = kullanici.get("telegram_chat_id")
                        conf.Gecerli_Aktiflik = kullanici.get("is_active")
                        break

                # EĞER İSİM BULUNDUYSA: İsim arama döngüsünü kır
                if aranan_isim_varmi:
                    print(frmt.Yazi.GreenLight(f"\nGiriş başarılı! Hoş geldiniz, {aranan_isim}.\n"))
                    break

                # EĞER İSİM BULUNAMADDIYSA: Alt Menüyü Göster
                print(frmt.Yazi.Red(f"{aranan_isim} adında bir kullanıcı bulunamadı.\n"))

                while True:
                    print(frmt.Yazi.White("1. Yeniden dene"))
                    print(frmt.Yazi.White("2. Bir Üst Menü"))
                    secim = input(frmt.Yazi.BlueLight("Lütfen yapmak istediğiniz işlemin numarasını girin: "))
                    print("")

                    if secim in ["1", "2"]:
                        break
                    print(frmt.Yazi.Red("Geçersiz seçim!\n"))

                if secim == "1":
                    continue  # İsim arama döngüsünün başına döner (Tekrar isim sorar)
                elif secim == "2":
                    break  # İsim arama döngüsünü kırar, ana menüye fırlatır

            # İsim arama döngüsünden çıkıldığında hangi sebeple çıkıldığını kontrol ediyoruz:
            if secim == "2":
                continue  # Eğer kullanıcı 'Üst Menü' dediyse, Ana Döngünün başına dön

            # Eğer 'Üst Menü' denmediyse (yani başarıyla giriş yapıldıysa) Ana Döngüyü bitir
            break

        # 3. YENİ KULLANICI İŞLEMLERİ
        # ────────────────────────────────────────────────────────────────
        elif kullaniciTuru == "2":



            print(frmt.Yazi.GreenLight("Yeni kullanıcı kayıt alanı..."))
            # Yeni kayıt kodların buraya gelecek...

            # İstediğin dış değişken atamaları tam burada yapılıyor:

            varmi: bool
            tum_kullanicilar = get_all_users()

            while True:
                y_Name = input(frmt.Yazi.BlueLight("Lütfen kullanıcı adınızı giriniz: "))
                for kullanici in tum_kullanicilar:
                    if kullanici.get("name") == y_Name:
                        varmi = True
                        break

            y_Mail = input(frmt.Yazi.BlueLight("Lütfen mail adresinizi giriniz: "))
            y_Telegram_ID = input(frmt.Yazi.BlueLight("Lütfen Telegram ıd nizi giriniz: "))



            # İstediğin dış değişken atamaları tam burada yapılıyor:
            conf.Gecerli_Name = aranan_isim




            conf.Gecerli_Mail = kullanici.get("email")
            conf.Gecerli_Telegram_ID = kullanici.get("telegram_chat_id")
            conf.Gecerli_Aktiflik = kullanici.get("is_active")

            break  # İşlem bitince ana döngüden çık