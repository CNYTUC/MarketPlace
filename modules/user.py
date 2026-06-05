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



# ── YARDIMCILAR────────────────────────────────────────────────────────────────

def kullanici_atama():

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
            conf.Gecerli_Name = bulunan.get("name")
            conf.Gecerli_Mail = bulunan.get("email")
            conf.Gecerli_Telegram_ID = bulunan.get("telegram_chat_id")
            conf.Gecerli_Aktiflik = bulunan.get("is_active")
            print(frmt.Yazi.GreenLight(f"\nGiriş başarılı! Hoş geldiniz, {aranan_isim}.\n"))
            break  # Başarılı giriş → ana döngüden çık
            return True

        print(frmt.Yazi.Red(f"{aranan_isim} adında kullanıcı bulunamadı.\n"))

