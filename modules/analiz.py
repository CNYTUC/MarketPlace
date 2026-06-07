import pandas as pd

def squeeze(s):
    if hasattr(s, "squeeze"):
        s = s.squeeze()

    if hasattr(s, "iloc") and getattr(s, "ndim", 1) == 2:
        s = s.iloc[:, 0]

    return s


def ema(seri, periyot):
    return squeeze(seri).ewm(span=periyot, adjust=False).mean()


def atr_hesapla(df, periyot=14):
    close = squeeze(df["Close"])
    high = squeeze(df["High"])
    low = squeeze(df["Low"])

    hl = high - low
    hc = (high - close.shift(1)).abs()
    lc = (low - close.shift(1)).abs()

    tr = pd.concat([hl, hc, lc], axis=1).max(axis=1)

    return tr.ewm(span=periyot, adjust=False).mean()


def macd_hesapla(close, hizli=12, yavas=26, sinyal=9):
    close = squeeze(close)

    ema_h = close.ewm(span=hizli, adjust=False).mean()
    ema_y = close.ewm(span=yavas, adjust=False).mean()

    macd = ema_h - ema_y
    macd_sig = macd.ewm(span=sinyal, adjust=False).mean()
    macd_his = macd - macd_sig

    return macd, macd_sig, macd_his


def rsi_hesapla(close, periyot=14):
    close = squeeze(close)

    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = (-delta).clip(lower=0)

    avg_gain = gain.ewm(span=periyot, adjust=False).mean()
    avg_loss = loss.ewm(span=periyot, adjust=False).mean()

    rs = avg_gain / (avg_loss + 1e-10)
    rsi = 100 - (100 / (1 + rs))

    return rsi


def hacim_ort(df, periyot=20):
    return squeeze(df["Volume"]).rolling(periyot).mean()


def konsolidasyon_tespit(df, lookback=20, max_bant=0.10):
    closes = squeeze(df["Close"]).iloc[-lookback:]

    if len(closes) < lookback:
        return False, 0, 0

    bant = (closes.max() - closes.min()) / closes.mean()

    ust_bant = float(closes.max())
    alt_bant = float(closes.min())

    return bant <= max_bant, ust_bant, alt_bant


def hacim_patlama_mi(df, kat=1.5, lookback=20):
    volume = squeeze(df["Volume"])

    if len(volume) < lookback + 1:
        return False, 0

    ort = float(volume.iloc[-lookback - 1:-1].mean())
    son = float(volume.iloc[-1])

    if ort <= 0:
        return False, 0

    oran = son / ort

    return oran >= kat, round(oran, 2)


def elli_iki_hafta_zirve_mi(df, tolerans=0.05):
    closes = squeeze(df["Close"])

    if len(closes) < 20:
        return False

    zirve = float(closes.rolling(min(252, len(closes))).max().iloc[-1])
    son = float(closes.iloc[-1])

    return son >= zirve * (1 - tolerans)


def yukselen_trend_mi(df):
    ema20 = float(df["EMA20"].iloc[-1])
    ema50 = float(df["EMA50"].iloc[-1])
    ema100 = float(df["EMA100"].iloc[-1])

    guclu = ema20 > ema50 > ema100
    zayif = ema20 > ema50

    return guclu, zayif


def yalanci_kirilim_var_mi(df, direnc, lookback=10):
    closes = squeeze(df["Close"]).iloc[-lookback - 1:-1]

    kiri = (closes > direnc).any()

    return bool(kiri)


def varsayilan_parametreler():
    return {
        "konsol_lookback": 20,
        "konsol_bant": 0.10,
        "kirilim_tolerans": 0.005,
        "hacim_kat": 1.5,
        "rsi_min": 50,
        "rsi_max": 75,
        "atr_kat": 1.5,
        "rr_kat": 2.0,
        "zayif_trend_izin": False,
    }


def tek_hisse_analiz_et(hisse, df, params=None):
    if params is None:
        params = varsayilan_parametreler()

    try:
        df = df.copy()

        for col in ["Open", "High", "Low", "Close", "Volume"]:
            if col in df.columns:
                df[col] = squeeze(df[col])

        close = df["Close"]

        df["EMA20"] = ema(close, 20)
        df["EMA50"] = ema(close, 50)
        df["EMA100"] = ema(close, 100)
        df["EMA200"] = ema(close, 200)
        df["ATR"] = atr_hesapla(df, 14)
        df["RSI"] = rsi_hesapla(close, 14)
        df["MACD"], df["MACD_SIG"], df["MACD_HIS"] = macd_hesapla(close)
        df["VOL_ORT"] = hacim_ort(df, 20)

        df.dropna(
            subset=["EMA200", "ATR", "RSI", "MACD", "MACD_SIG", "VOL_ORT"],
            inplace=True
        )

        if len(df) < 5:
            return None, "veri_yetersiz"

        son = df.iloc[-1]
        onceki = df.iloc[-2]

        guclu_trend, zayif_trend = yukselen_trend_mi(df)

        if not params["zayif_trend_izin"] and not guclu_trend:
            return None, "trend"

        if params["zayif_trend_izin"] and not zayif_trend:
            return None, "trend"

        rsi_val = float(son["RSI"])

        if rsi_val > params["rsi_max"]:
            return None, "rsi_asiri_alim"

        if rsi_val < params["rsi_min"]:
            return None, "rsi_zayif"

        macd_val = float(son["MACD"])
        macd_sig_val = float(son["MACD_SIG"])

        macd_pozitif = macd_val > 0
        macd_kesiyor = (
            float(onceki["MACD"]) < float(onceki["MACD_SIG"])
            and macd_val > macd_sig_val
        )

        if not (macd_pozitif or macd_kesiyor):
            return None, "macd"

        konsol_var, ust_bant, alt_bant = konsolidasyon_tespit(
            df.iloc[:-1],
            lookback=params["konsol_lookback"],
            max_bant=params["konsol_bant"]
        )

        if not konsol_var:
            return None, "konsolidasyon"

        son_kapanis = float(son["Close"])

        kirilim_var = son_kapanis > ust_bant * (1 + params["kirilim_tolerans"])

        if not kirilim_var:
            return None, "kirilim_yok"

        kirilim_yesil = float(son["Close"]) > float(son["Open"])

        if not kirilim_yesil:
            return None, "kirilim_kirmizi"

        hacim_var, hacim_oran = hacim_patlama_mi(
            df,
            kat=params["hacim_kat"],
            lookback=20
        )

        if not hacim_var:
            return None, "hacim_yetersiz"

        uyarilar = []

        if yalanci_kirilim_var_mi(df, ust_bant, lookback=15):
            uyarilar.append("Daha önce kırılmış")

        if rsi_val > 65:
            uyarilar.append("RSI yüksek")

        if not guclu_trend:
            uyarilar.append("Zayıf trend")

        kalite = 0
        kalite_detay = []

        if elli_iki_hafta_zirve_mi(df, tolerans=0.03):
            kalite += 1
            kalite_detay.append("52H Zirve")

        if hacim_oran >= 2.0:
            kalite += 1
            kalite_detay.append(f"Güçlü Hacim {hacim_oran:.1f}x")

        if params["konsol_lookback"] >= 25:
            konsol_uzun, _, _ = konsolidasyon_tespit(
                df.iloc[:-1],
                lookback=30,
                max_bant=params["konsol_bant"]
            )

            if konsol_uzun:
                kalite += 1
                kalite_detay.append("Uzun Konsol")

        if guclu_trend:
            kalite += 1
            kalite_detay.append("Güçlü Trend")

        if macd_kesiyor:
            kalite += 1
            kalite_detay.append("MACD Kesiyor")

        atr_val = float(son["ATR"])
        giris = float(son["Close"])

        stop_konsol = round(ust_bant * (1 - 0.005), 2)
        stop_atr = round(giris - params["atr_kat"] * atr_val, 2)

        stop = max(stop_konsol, stop_atr)

        bir_r = giris - stop

        if bir_r <= 0:
            return None, "stop_hatasi"

        hedef_r = params["rr_kat"]

        if len(uyarilar) > 0:
            hedef_r = hedef_r * 0.8

        hedef_r = round(max(1.0, hedef_r), 1)
        hedef = round(giris + hedef_r * bir_r, 2)

        sonuc = {
            "Hisse": hisse,
            "Kapanis": round(giris, 2),
            "Giris": round(giris, 2),
            "KonsolUst": round(ust_bant, 2),
            "KonsolAlt": round(alt_bant, 2),
            "Stop": stop,
            "StopYuzde": round((giris - stop) / giris * 100, 2),
            "Hedef": hedef,
            "HedefYuzde": round((hedef - giris) / giris * 100, 2),
            "HedefR": hedef_r,
            "RiskTL": round(bir_r, 2),
            "ATR": round(atr_val, 2),
            "RSI": round(rsi_val, 2),
            "MACD": round(macd_val, 4),
            "HacimOran": hacim_oran,
            "Kalite": kalite,
            "KaliteDetay": ", ".join(kalite_detay) if kalite_detay else "-",
            "Uyarilar": " | ".join(uyarilar) if uyarilar else "-",
            "GucluTrend": guclu_trend,
            "Sebep": "ok",
        }

        return sonuc, "ok"

    except Exception as e:
        return None, f"hata: {e}"


def tum_hisseleri_analiz_et(hisse_verileri, params=None):
    if params is None:
        params = varsayilan_parametreler()

    olumlu_sonuclar = []
    elenenler = {}
    hatalar = []

    for hisse, df in hisse_verileri.items():
        sonuc, sebep = tek_hisse_analiz_et(
            hisse=hisse,
            df=df,
            params=params
        )

        if sonuc is None:
            elenenler[sebep] = elenenler.get(sebep, 0) + 1

            if str(sebep).startswith("hata"):
                hatalar.append({
                    "Hisse": hisse,
                    "Hata": sebep
                })

            continue

        olumlu_sonuclar.append(sonuc)

    olumlu_sonuclar = sorted(
        olumlu_sonuclar,
        key=lambda x: (
            x["Kalite"],
            x["HacimOran"],
            x["RSI"]
        ),
        reverse=True
    )

    return olumlu_sonuclar, elenenler, hatalar


def analiz_sonuclarini_yazdir(sonuclar):
    print("\nANALİZ SONUÇLARI")
    print("-" * 80)

    if len(sonuclar) == 0:
        print("Bugün kriterlere uyan hisse bulunamadı.")
        return

    for s in sonuclar:
        print(
            f"{s['Hisse']:8} ✅ "
            f"Kapanış: {s['Kapanis']:8.2f} | "
            f"Giriş: {s['Giris']:8.2f} | "
            f"Stop: {s['Stop']:8.2f} | "
            f"Hedef: {s['Hedef']:8.2f} | "
            f"RSI: {s['RSI']:6.2f} | "
            f"Hacim: {s['HacimOran']:4.1f}x | "
            f"Kalite: {s['Kalite']}"
        )