import _c_DosyaKlasor as _Dk
import _c_Zaman as _Zaman

def LogYeni(Ad:str):

    if _Dk.Dosya_Klasor.Varmi.Dosya(Ad):
        _Dk.Dosya_Klasor.sil.Dosya(Ad)

    with open(Ad, 'w') as log:

        SATIR = _Zaman.GunSaat() + " / " + Ad + " adlı dosya oluşturuldu."

        log.write(SATIR)
        log.write("\n")
        log.close()


def LogGuncelle(Ad:str, Msj:str):

    with open(Ad, 'a+') as log:
        zmn = _Zaman.GunSaat()
        Msj = zmn + " " + Msj
        log.write(Msj)
        log.write("\n")
        log.close()
