### IMPORT ##
from colorama import Fore

COLORS = [Fore.RED, Fore.BLUE, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.MAGENTA]

class bcolors:
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def ColorizeText(text, color=Fore.YELLOW, bold=False):

	if bold:

		return color + bcolors.BOLD + text + bcolors.ENDC + bcolors.ENDC

	return color + text + bcolors.ENDC

def PrintInColor(text, color=Fore.YELLOW, bold=False):

	print(ColorizeText(text, color, bold))

def RainbowText(text, bold = False):

	return "".join([ColorizeText(char, COLORS[index%len(COLORS)], bold) for index, char in enumerate(text)])

