### IMPORT ##
from colorama import *
from random import sample

### TEXT FONT ###
class bcolors:
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

## COLORFUL TEXT FUNCTION ##
def Colorful(text, bold = True, turn = sample(["red", "blue", "yellow", "green", "cyan", "purple"], k = 1)[0]):
	i = 0
	newText = ""

	while i < len(text):
		if(text[i] != " "):
			if(turn == "red"):
				turn = "blue"			
				t = Fore.RED + text[i]				
			elif(turn == "blue"):
				turn = "yellow"
				t =Fore.YELLOW + text[i]
			elif(turn == "yellow"):
				turn = "green"
				t = Fore.BLUE + text[i]
			elif(turn == "green"):
				turn = "cyan"
				t = Fore.GREEN + text[i]
			elif(turn == "cyan"):
				turn = "purple"
				t = Fore.CYAN + text[i]
			elif(turn == "purple"):
				turn = "red"
				t = Fore.BLACK + text[i]
	
			newText = newText + t

		else:

			newText = newText + " "

		i = i + 1

	if(bold == True):
		return bcolors.BOLD + newText + bcolors.ENDC
	else:
		return newText

