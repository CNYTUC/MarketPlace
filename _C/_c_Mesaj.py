class Mesaj:
    def eminmisin(MSJ: str):
        if MSJ == "":
            MSJ = "Bu işlemi gerçekleştirmek istediğinizden Emin misiniz?"

        Cvp = ""
        while not Cvp == "E" or not Cvp == "e" or not Cvp == "H" or not Cvp == "h":
            print(bgcolors.Bold + bgcolors.Red + MSJ + bgcolors.ResetAll)
            cvp = str.upper(input('E: Evet / H: Hayır : '))

            if cvp == 'E':
                return True
            elif cvp == 'H':
                return False


class bgcolors:
    ResetAll = "\033[0m"
    Bold = "\033[1m"
    Red = "\033[31m"