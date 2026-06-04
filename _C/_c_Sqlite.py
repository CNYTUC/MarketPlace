##########################################################
# ------------------GENEL SQL LITE İŞLEMLERİ-------------#
##########################################################

import _sqlite3 as sql
import os


class VeriTabani:

    @staticmethod
    def olustur(AD: str):
        con = sql.connect(AD)
        con.close()

    @staticmethod
    def sil(AD: str): os.remove(AD)

    @staticmethod
    def yoklama(AD: str) -> bool: return os.path.isfile(AD)

    @staticmethod
    def sema_al(VT: str) -> list:
        sqlMetin = 'SELECT name FROM sqlite_schema WHERE type ="table" AND name NOT LIKE "sqlite_%";'

        con = sql.connect(str(VT))
        cur = con.cursor()
        cur.execute(sqlMetin)
        con.commit()
        data = cur.fetchall()
        con.close()

        return data[:]

class Tablo:

    @staticmethod
    def olustur(VT: str, TABLO: str):
        sqlMetin = 'CREATE TABLE IF NOT EXISTS ' + TABLO + ' (id INTEGER Not NULL PRIMARY KEY autoincrement);'

        con = sql.connect(str(VT))
        cur = con.cursor()
        cur.execute(sqlMetin)
        con.commit()
        con.close()

    @staticmethod
    def yeniden_adlandir(VT: str, TABLO_AD: str, TABLO_YENI_AD: str):
        sqlMetin = 'ALTER TABLE "' + TABLO_AD + '" RENAME TO "' + TABLO_YENI_AD + '";'

        con = sql.connect(str(VT))
        cur = con.cursor()
        cur.execute(sqlMetin)
        con.commit()
        con.close()

    @staticmethod
    def sil(VT: str, TABLO: str):
        sqlMetin = 'DROP TABLE ' + str(TABLO)

        con = sql.connect(str(VT))
        cur = con.cursor()
        cur.execute(sqlMetin)
        con.commit()
        con.close()

class Kolon:

    @staticmethod
    def olustur(VT: str, TABLO: str, KOLON: str, OZELLIK: str):
        sqlMetin = 'ALTER TABLE ' + TABLO + ' ADD COLUMN "' + KOLON + '" ' + OZELLIK
        con = sql.connect(str(VT))
        cur = con.cursor()
        cur.execute(sqlMetin)
        con.commit()
        con.close()

class veri:

    class gir:

        @staticmethod
        def genel(VT:str, TABLO:str, LISTE:list):
            sqlMetin = 'INSERT INTO ' + TABLO

            Kolonlar = '"'
            Degerler = '"'
            i = True

            for deger in LISTE:
                if i:
                    Kolonlar = str(Kolonlar) + str(deger) + '", "'
                    i = False
                else:
                    Degerler = str(Degerler) + str(deger) + '", "'
                    i = True
            Kolonlar = Kolonlar[:len(Kolonlar) - 3]
            Degerler = Degerler[:len(Degerler) - 3]
            sqlMetin = sqlMetin + ' (' + Kolonlar + ') VALUES (' + Degerler + '); '

            con = sql.connect(str(VT))
            cur = con.cursor()
            cur.execute(sqlMetin)
            con.commit()
            con.close()

        @staticmethod
        def Kontrollu(VT:str, TABLO:str, LISTE:list):
            sqlMetin = ''

            Kolonmu = True

            for x in LISTE:
                if Kolonmu:
                    Kolon = str(x)
                    Kolonmu = False
                    continue
                else:
                    Deger = str(x)
                    Kolonmu = True

                sqlMetin = 'INSERT INTO ' + TABLO + ' ("' + Kolon + '") VALUES ("' + Deger + '"); '

                # Kontrol ET
                if int(veri.say.kolon_kontrollu(str(VT), TABLO, Kolon, Deger)) == 0:
                    con = sql.connect(str(VT))
                    cur = con.cursor()
                    cur.execute(sqlMetin)
                    con.commit()
                    con.close()

    class guncelle:

        @staticmethod
        def genel(VT: str, TABLO: str, liste:list):
            Anahtar = str(liste[0])
            AnahtarDeger = str(liste[1])
            Kolon = str(liste[2])
            Deger = str(liste[3])

            sqlMetin = 'UPDATE ' + TABLO + ' SET ' + Kolon + ' = "' + Deger + '" WHERE ' + Anahtar + ' = "' + AnahtarDeger + '";'

            con = sql.connect(str(VT))
            cur = con.cursor()
            cur.execute(sqlMetin)
            con.commit()
            con.close()

    class sil:

        @staticmethod
        def tum_tablo(vt, tablo_adi):  # tabloda ki tüm veriler
            sqlMetin = 'DELETE FROM ' + tablo_adi + ';'

            con = sql.connect(str(vt))
            cur = con.cursor()
            cur.execute(sqlMetin)
            con.commit()
            con.close()

        @staticmethod
        def Kontrollu(vt, tablo_adi, KolonAdi, Deger):  # tabloda ki değerle eşleşen tüm veriler
            sqlMetin = 'DELETE FROM ' + tablo_adi + ' WHERE ' + KolonAdi + ' = "' + Deger + '";'

            con = sql.connect(str(vt))
            cur = con.cursor()
            cur.execute(sqlMetin)
            con.commit()
            con.close()

    class cek:

        @staticmethod
        def hersey(VT:str, TABLO:str):
            sqlMetin = 'SELECT * FROM ' + TABLO + ';'

            con = sql.connect(str(VT))
            cur = con.cursor()
            cur.execute(sqlMetin)
            con.commit()
            data = cur.fetchall()
            con.close()

            return data[:]

        @staticmethod
        def tum_kolon(VT:str, TABLO:str, KOLON:str):
            sqlMetin = 'SELECT ' + KOLON + ' FROM ' + TABLO + ';'

            con = sql.connect(str(VT))
            cur = con.cursor()
            cur.execute(sqlMetin)
            con.commit()
            data = cur.fetchall()
            con.close()

            return data[:]

        @staticmethod
        def tum_kolon_kontrollu(VT: str, TABLO: str, LISTE:list):
            Anahtar = str(LISTE[0])
            AnahtarDeger = str(LISTE[1])
            CekilecekDeger = str(LISTE[2])

            sqlMetin = 'SELECT ' + CekilecekDeger + ' FROM ' + TABLO + ' WHERE ' + Anahtar + ' = "' + AnahtarDeger + '";'

            con = sql.connect(str(VT))
            cur = con.cursor()
            cur.execute(sqlMetin)
            con.commit()
            data = cur.fetchall()
            con.close()

            return data[0]

    class say:

        @staticmethod
        def genel(vt, tablo_adi):
            sqlMetin = 'SELECT COUNT(*) FROM ' + tablo_adi

            con = sql.connect(str(vt))
            cur = con.cursor()
            cur.execute(sqlMetin)
            con.commit()
            data = cur.fetchone()
            con.close()

            return data[0]

        @staticmethod
        def kolon_kontrollu(VT, TABLO, KOLON, DEGER):
            sqlMetin = 'SELECT COUNT(*) FROM ' + TABLO + ' WHERE ' + KOLON + ' = "' + DEGER + '";'

            con = sql.connect(str(VT))
            cur = con.cursor()
            cur.execute(sqlMetin)
            con.commit()
            data = cur.fetchone()
            con.close()

            return data[0]

    class yoklama:

        @staticmethod
        def kosulsuz(VT: str, TABLO: str, KOLON: str, DEGER: str):
            sqlMetin = 'SELECT * FROM ' + TABLO + ' WHERE ("' + KOLON + '"  =  "' + DEGER + '");'

            con = sql.connect(str(VT))
            cur = con.cursor()
            cur.execute(sqlMetin)
            con.commit()
            data = cur.fetchall()
            con.close()

            return data[:]

