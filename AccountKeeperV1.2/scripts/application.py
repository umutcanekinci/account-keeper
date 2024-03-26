#!/usr/bin/env python3
try:

	### IMPORT THE PACKAGES ###
	from scripts.rainbowText import RainbowText, PrintInColor, ColorizeText, bcolors, Fore	
	from tabulate import tabulate
	from time import ctime
	from scripts.database import Database

except ImportError as e:
	
	print("==> You need the install requirements to use this application.\n==> Use 'pip install -r requirements.txt' command to download and install this packages in the terminal.")
	exit()

class Application:

	def __init__(self) -> None:
		
		self.database = Database()
		self.database.Connect()
		self.CreateTable()

	def CreateTable(self) -> None:

			sql = '''
			CREATE TABLE IF NOT EXISTS accounts(
			account_id INTEGER PRIMARY KEY,
			account_type VARCHAR(100) NOT NULL,		
			account_username VARCHAR(100) NOT NULL,
			account_password VARCHAR(100) NOT NULL,
			account_email VARCHAR(50) NOT NULL,
			account_date TEXT
			)
			'''
			self.database.Execute(sql)
			self.database.Commit()

	### LISTING ALL ACCOUNTS ###
	def List(self) -> None:

		accounts = self.database.Execute('SELECT * FROM accounts').fetchall()
		print("\n"+Fore.GREEN+tabulate(accounts, headers=['ID', 'Type', 'Username', 'Password', 'Email', 'Creation Time'], tablefmt="fancy_grid")+"\n")			

	### ADDING AN ACCOUNT ###
	def Add(self) -> None:
		
		#-# Taking the Account Variables #-#
		accType = input(bcolors.UNDERLINE+Fore.GREEN+"Account Type"+bcolors.ENDC+Fore.GREEN+" ==> ")	
		accUsername = input(bcolors.UNDERLINE+Fore.GREEN+"Account Username"+bcolors.ENDC+Fore.GREEN+" ==> ")	
		accPass = input(bcolors.UNDERLINE+Fore.GREEN+"Account Password"+bcolors.ENDC+Fore.GREEN+" ==> ")	
		accEmail = input(bcolors.UNDERLINE+Fore.GREEN+"Account Email"+bcolors.ENDC+Fore.GREEN+" ==> ")
		accDate = ctime()
		print("\n")

		#-# Checking the Account Variables #-#
		if accType and accUsername and accEmail and accPass:

			#-# Checking the database If Account Exists #-#
			exist = self.database.Execute("SELECT * FROM accounts WHERE account_type == '"+accType+"' AND account_username == '"+accUsername+"' AND account_password == '"+accPass+"' AND account_email == '"+accEmail+"'").fetchone()                 

			if exist:

				PrintInColor("==> This account already exists!", Fore.YELLOW)
				
			else:

				#-# Adding Account to the Database #-#
				add = self.database.Execute("INSERT INTO accounts(account_type, account_username, account_password, account_email, account_date) VALUES ('"+accType+"', '"+accUsername+"', '"+accPass+"', '"+accEmail+"', '"+accDate+"')")   

				if add:

					self.database.Commit()
					PrintInColor("==> Added to the database successfully!", Fore.GREEN)

				else:

					PrintInColor("==> There was an error when adding to the account database. Please try again later.", Fore.RED)
					self.Exit()	
		else:

			PrintInColor("==> Please complete all questions!.", Fore.RED)
			self.Add()

	### EDITING AN ACCOUNT ##
	def Edit(self) -> None:

		#-# Taking Account ID for Edit #-#
		upAccID = input(bcolors.UNDERLINE+Fore.GREEN+"Account ID"+bcolors.ENDC+Fore.GREEN+" ==> ")	
		
		#-# Checking the Database for Account #-#
		doesExist = self.database.Execute("SELECT * FROM accounts WHERE account_id == '"+upAccID+"'").fetchone()
		
		if doesExist:
		
			#-# Taking the Account Variables #-#
			upAccType = input(bcolors.UNDERLINE + Fore.GREEN + "Account Type" + bcolors.ENDC + Fore.GREEN+" ==> ")	
			upAccUsername = input(bcolors.UNDERLINE + Fore.GREEN + "Account Username" + bcolors.ENDC+Fore.GREEN+" ==> ")	
			upAccPass = input(bcolors.UNDERLINE + Fore.GREEN + "Account Password" + bcolors.ENDC + Fore.GREEN+" ==> ")
			upAccEmail = input(bcolors.UNDERLINE + Fore.GREEN + "Account Email" + bcolors.ENDC + Fore.GREEN + " ==> ")

			#-# Uploading Account Veriables #-#			
			edit = self.database.Execute("UPDATE accounts SET account_type = '"+upAccType+"', account_username = '"+upAccUsername+"', account_password = '"+upAccPass+"', account_email = '"+upAccEmail+"' WHERE account_id == '"+upAccID+"'")                 

			if edit:

				self.database.Commit()		
				PrintInColor("==> Edited successfully!", Fore.GREEN)

			else:

				PrintInColor("==> There was an error when editing account from the database. Please try again later.", Fore.RED)
				self.Exit()

		else:

			PrintInColor("==> No account matching the ID you entered was found!", Fore.RED)
			self.Edit()
						
	### DELETING AN ACCOUNT ###
	def Delete(self) -> None:

		accID = input(bcolors.UNDERLINE+Fore.GREEN+"Account ID"+bcolors.ENDC+Fore.GREEN+" ==> ")	
		
		#-# Check the Database for Account #-#
		doesExist = self.database.Execute("SELECT * FROM accounts WHERE account_id == '"+accID+"'").fetchone()

		if doesExist:

			delete = self.database.Execute("DELETE FROM accounts WHERE account_id == '"+accID+"'")
			
			if delete:

				self.database.Commit()
				PrintInColor("==> Account had been deleted successfully!", Fore.GREEN)

			else:

				PrintInColor("==> There was an error when deleting account from the database. Please try again later.", Fore.RED)
				self.Exit()
		else:

			PrintInColor("==> No account matching the ID you entered was found!", Fore.RED)
					
			self.Delete()

	def GetInput(self) -> None:

		PrintInColor(bcolors.UNDERLINE+"\nWHAT DO YOU WANT?"+bcolors.ENDC, bold=True)
		
		isThereAnyAccount = self.database.Execute("SELECT * FROM accounts").fetchone()
		
		#region printing options

		if isThereAnyAccount:
			
			PrintInColor("A) List Accounts", Fore.GREEN)
			
		else:

			PrintInColor("A) List Accounts", Fore.BLACK)

		PrintInColor("B) Add Account", Fore.GREEN)

		if isThereAnyAccount:
			
			PrintInColor("C) Edit Account", Fore.GREEN)
			PrintInColor("D) Delete Acount", Fore.RED)

		else:

			PrintInColor("C) Edit Account\nD) Delete Acount", Fore.BLACK)
			
		PrintInColor("E) Exit", Fore.RED)
			
		if isThereAnyAccount:

			PrintInColor("R) Reset (Delete All Accounts)\n", Fore.RED)

		else:

			PrintInColor("R) Reset (Delete All Accounts)\n", Fore.BLACK)

		#endregion

		value = input(ColorizeText("==> ")).upper()

		if not isThereAnyAccount and (value == "A" or value == "C" or value == "D" or value == "R"):
			
			PrintInColor("==> There is no account! Please add an account before doing an operation!", Fore.RED)
			return

		if value == "A":

			self.List()

		elif value == "B":

			print("\n")
			self.Add()

		elif value == "C":
			
			print("\n")
			self.Edit()

		elif value == "D":	

			print("\n")
			self.Delete()
			
		elif value == "E":

			self.Exit()
			
		elif value == "R":

			self.database.Delete()
			PrintInColor("==> Database had been reseted successfully!", Fore.GREEN)

	def Intro(self) -> None:

		print(RainbowText('''
##############################################################
#                                                            #
#              ACCOUNT KEEPER v1.2                           #
#                   Made by Umutcan Ekinci                   #
#                                                            #	
##############################################################
#                                                            #
#    Python Version ==> 3.12                                 #
#    Mail ==> umutcannekinci@gmail.com                       #
#    Instagram ==> https://instagram.com/umut_ekinci_        #
#    Github ==> https://github.com/umutcanekinci             #
#                                                            #
##############################################################
		'''))

	def Run(self) -> None:

		self.isRunning = True

		self.Intro()

		while self.isRunning:

			self.GetInput()

	def Exit(self) -> None:

		self.isRunning = False
		exit()