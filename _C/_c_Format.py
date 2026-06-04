##########################################################
# --------------------GENEL FORMAT İŞLEMLERİ-------------#
##########################################################
class Yazi:

    @staticmethod
    def Default(Metin: str): return colors.Default + Metin + colors.ResetAll

    @staticmethod
    def White(Metin: str): return colors.White + Metin + colors.ResetAll

    @staticmethod
    def Black(Metin: str): return colors.Black + Metin + colors.ResetAll

    @staticmethod
    def GrayLight(Metin: str): return colors.LightGray + Metin + colors.ResetAll

    @staticmethod
    def GrayDark(Metin: str): return colors.DarkGray + Metin + colors.ResetAll

    @staticmethod
    def Red(Metin: str): return colors.Red + Metin + colors.ResetAll

    @staticmethod
    def RedLight(Metin: str): return colors.LightRed + Metin + colors.ResetAll

    @staticmethod
    def Green(Metin: str): return colors.Green + Metin + colors.ResetAll

    @staticmethod
    def GreenLight(Metin: str): return colors.LightGreen + Metin + colors.ResetAll

    @staticmethod
    def Yellow(Metin: str): return colors.Yellow + Metin + colors.ResetAll

    @staticmethod
    def YellowLight(Metin: str): return colors.LightYellow + Metin + colors.ResetAll

    @staticmethod
    def Blue(Metin: str): return colors.Blue + Metin + colors.ResetAll

    @staticmethod
    def BlueLight(Metin: str): return colors.LightBlue + Metin + colors.ResetAll

    @staticmethod
    def Magenta(Metin: str): return colors.Magenta + Metin + colors.ResetAll

    @staticmethod
    def MagentaLight(Metin: str): return colors.LightMagenta + Metin + colors.ResetAll

    @staticmethod
    def Cyan(Metin: str): return colors.Cyan + Metin + colors.ResetAll

    @staticmethod
    def CyanLight(Metin: str): return colors.LightCyan + Metin + colors.ResetAll


class YaziArkaPlan:

    @staticmethod
    def Default(Metin: str): return colors.BackgroundDefault + Metin + colors.ResetAll

    @staticmethod
    def White(Metin: str): return colors.BackgroundWhite + Metin + colors.ResetAll

    @staticmethod
    def Black(Metin: str): return colors.BackgroundBlack + Metin + colors.ResetAll

    @staticmethod
    def GrayDark(Metin: str): return colors.BackgroundDarkGray + Metin + colors.ResetAll

    @staticmethod
    def GrayLight(Metin: str): return colors.BackgroundLightGray + Metin + colors.ResetAll

    @staticmethod
    def Red(Metin: str): return colors.BackgroundRed + Metin + colors.ResetAll

    @staticmethod
    def RedLight(Metin: str): return colors.BackgroundLightRed + Metin + colors.ResetAll

    @staticmethod
    def Green(Metin: str): return colors.BackgroundGreen + Metin + colors.ResetAll

    @staticmethod
    def GreenLight(Metin: str): return colors.BackgroundLightGreen + Metin + colors.ResetAll

    @staticmethod
    def Yellow(Metin: str): return colors.BackgroundYellow + Metin + colors.ResetAll

    @staticmethod
    def YellowLight(Metin: str): return colors.BackgroundLightYellow + Metin + colors.ResetAll

    @staticmethod
    def Blue(Metin: str): return colors.BackgroundBlue + Metin + colors.ResetAll

    @staticmethod
    def BlueLight(Metin: str): return colors.BackgroundLightBlue + Metin + colors.ResetAll

    @staticmethod
    def Magenta(Metin: str): return colors.BackgroundMagenta + Metin + colors.ResetAll

    @staticmethod
    def MagentaLight(Metin: str): return colors.BackgroundLightMagenta + Metin + colors.ResetAll

    @staticmethod
    def Cyan(Metin: str): return colors.BackgroundCyan + Metin + colors.ResetAll

    @staticmethod
    def CyanLight(Metin: str): return colors.BackgroundLightCyan + Metin + colors.ResetAll


class YaziFormat:
    @staticmethod
    def ResetAll(Metin: str): return colors.ResetAll + Metin + colors.ResetAll

    @staticmethod
    def Bold(Metin: str): return colors.Bold + Metin + colors.ResetAll

    @staticmethod
    def Dim(Metin: str): return colors.Dim + Metin + colors.ResetAll

    @staticmethod
    def Underlined(Metin: str): return colors.Underlined + Metin + colors.ResetAll

    @staticmethod
    def Blink(Metin: str): return colors.Blink + Metin + colors.ResetAll

    @staticmethod
    def Reverse(Metin: str): return colors.Reverse + Metin + colors.ResetAll

    @staticmethod
    def Hidden(Metin: str): return colors.Hidden + Metin + colors.ResetAll


class colors:
    ResetAll = "\033[0m"
    Bold = "\033[1m"
    BoldReset = "\033[21m"
    Dim = "\033[2m"
    DimReset = "\033[22m"
    Underlined = "\033[4m"
    UnderlinedReset = "\033[24m"
    Blink = "\033[5m"
    BlinkReset = "\033[25m"
    Reverse = "\033[7m"
    ReverseReset = "\033[27m"
    Hidden = "\033[8m"
    HiddenReset = "\033[28m"

    Default = "\033[39m"
    Black = "\033[30m"
    Red = "\033[31m"
    Green = "\033[32m"
    Yellow = "\033[33m"
    Blue = "\033[34m"
    Magenta = "\033[35m"
    Cyan = "\033[36m"
    LightGray = "\033[37m"
    DarkGray = "\033[90m"
    LightRed = "\033[91m"
    LightGreen = "\033[92m"
    LightYellow = "\033[93m"
    LightBlue = "\033[94m"
    LightMagenta = "\033[95m"
    LightCyan = "\033[96m"
    White = "\033[97m"

    BackgroundDefault = "\033[49m"
    BackgroundBlack = "\033[40m"
    BackgroundRed = "\033[41m"
    BackgroundGreen = "\033[42m"
    BackgroundYellow = "\033[43m"
    BackgroundBlue = "\033[44m"
    BackgroundMagenta = "\033[45m"
    BackgroundCyan = "\033[46m"
    BackgroundLightGray = "\033[47m"
    BackgroundDarkGray = "\033[100m"
    BackgroundLightRed = "\033[101m"
    BackgroundLightGreen = "\033[102m"
    BackgroundLightYellow = "\033[103m"
    BackgroundLightBlue = "\033[104m"
    BackgroundLightMagenta = "\033[105m"
    BackgroundLightCyan = "\033[106m"
    BackgroundWhite = "\033[107m"
