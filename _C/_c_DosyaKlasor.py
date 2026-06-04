##########################################################
# ---------------GENEL FILE/KLASOR İŞLEMLERİ-------------#
##########################################################

import shutil  # Dosya İşlemleri
import os  # Dosya İşlemleri


class Dosya_Klasor:

    class Varmi:

        @staticmethod
        def Dosya(Dosya_x: str) -> bool:
            try:
                return os.path.isfile(Dosya_x)
            except Exception as e:
                print(f"Hata tespit edildi: {str(e)}")
                return False

        @staticmethod
        def Klasor(Klasor_x: str) -> bool:
            try:
                return os.path.isdir(Klasor_x)
            except Exception as e:
                print(f"Hata tespit edildi: {str(e)}")
                return False

    class Olustur:

        @staticmethod
        def Klasor(path: str):
            os.mkdir(path)

    class sil:

        @staticmethod
        def Dosya(dosya: str):
            os.remove(dosya)

        @staticmethod
        def Klasor_Bos(yol: str):
            os.rmdir(yol)

        @staticmethod
        def Klasor_icindekilerle(yol: str):
            shutil.rmtree(yol)
