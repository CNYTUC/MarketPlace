import pandas as pd
import yfinance as yf

# Hisse senedi listesi çekerken mesajları gizler
# import logging
# logging.getLogger("yfinance").setLevel(logging.CRITICAL)

def squeeze(s):
    if hasattr(s, "squeeze"):
        s = s.squeeze()

    if hasattr(s, "iloc") and getattr(s, "ndim", 1) == 2:
        s = s.iloc[:, 0]
    return s


def hisse_kodlarini_temizle(hisse):
    """
    Supabase'den gelen hisse bilgisini temizler.
    Virgülle ayrılmış kodları ayırır.
    """

    if isinstance(hisse, str):
        ham = hisse

    elif isinstance(hisse, dict):
        ham = hisse.get("Kod")

    elif isinstance(hisse, (list, tuple)):
        ham = hisse[0]

    else:
        ham = str(hisse)

    if not ham:
        return []

    ham = str(ham).replace(".IS", "")
    parcalar = ham.split(",")

    kodlar = []

    for kod in parcalar:
        kod = kod.strip().upper()

        if kod:
            kodlar.append(kod)

    return kodlar


def veri_cek(kod, gun=300):
    """
    Tek bir hisse için Yahoo Finance üzerinden veri çeker.
    Örnek:
        THYAO -> THYAO.IS
    """

    kod = str(kod).strip().upper().replace(".IS", "")

    if not kod:
        return None

    try:
        df = yf.download(
            kod + ".IS",
            period=f"{gun}d",
            interval="1d",
            progress=False,
            auto_adjust=True,
            threads=False
        )

        if df.empty or len(df) < 60:
            return None

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df[["Open", "High", "Low", "Close", "Volume"]].dropna()

        for col in df.columns:
            df[col] = squeeze(df[col])

        return df

    except Exception:
        return None


def tum_hisselerin_verisini_cek(hisse_listesi, gun=300):
    """
    Supabase'den gelen tüm hisse listesi için veri çeker.

    Dönen değerler:
        veri_dict:
            Başarılı hisselerin DataFrame verileri

        durum_listesi:
            Her hissenin başarılı/başarısız durumu

        basarili_hisseler:
            Verisi çekilen hisseler

        hatali_hisseler:
            Verisi çekilemeyen hisseler
    """

    veri_dict = {}
    durum_listesi = []
    basarili_hisseler = []
    hatali_hisseler = []

    for hisse in hisse_listesi:
        kodlar = hisse_kodlarini_temizle(hisse)

        for kod in kodlar:
            df = veri_cek(kod, gun=gun)

            if df is None:
                hatali_hisseler.append(kod)

                durum_listesi.append({
                    "Kod": kod,
                    "Durum": "❌"
                })

            else:
                veri_dict[kod] = df
                basarili_hisseler.append(kod)

                durum_listesi.append({
                    "Kod": kod,
                    "Durum": "✅"
                })

    return veri_dict, durum_listesi, basarili_hisseler, hatali_hisseler


def veri_durumlarini_yazdir(durum_listesi):
    """
    Tüm hisseleri başarılı/başarısız olarak ekrana yazar.
    """

    print("\nHİSSE VERİ DURUMLARI")
    print("-" * 30)

    for sonuc in durum_listesi:
        print(f"{sonuc['Kod']:10} {sonuc['Durum']}")