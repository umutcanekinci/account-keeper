#!/usr/bin/env python3
### IMPORT THE PACKAGES ###
try:
	from os import remove
	from sqlite3 import *	
	from convertDate import *
	from rainbowText import *	
	from tabulate import tabulate

except ImportError as e:
	print(Fore.YELLOW+bcolors.BOLD+"==> You need the install 'tabulate' package to use this application.\n==> Use 'sudo apt-get install python3-pip && pip3 download tabulate && pip3 install tabulate' command to download and install this packages in the terminal."+bcolors.ENDC)
	exit()

### CONNECTING TO THE DATABASE ###
def Connect():
	global connectdb	
	connectdb = connect('database.db')	
	if(connectdb):
		#print(Fore.CYAN+"==> Connected to the database successfully!")   
		global db
		db = connectdb.cursor()

		#-# Creating Table #-#
		db.execute('''
		CREATE TABLE IF NOT EXISTS accounts(
		account_id INTEGER PRIMARY KEY,
		account_type VARCHAR(100) NOT NULL,		
		account_username VARCHAR(100) NOT NULL,
		account_password VARCHAR(100) NOT NULL,
		account_email VARCHAR(50) NOT NULL,
		account_date TEXT
		)
		''')
	else:
	    print(Fore.RED+"==> Failed to connect to database!")
	    exit()

### DISCONNECTING TO THE DATABASE ###
def Disconnect():
	connectdb.commit()
	connectdb.close()

### LISTING THE ACCOUNTS ###
def List():

	#-# Connecting to the Datababe #-#
	Connect()

	#-# Reading Database #-#
	read = db.execute('SELECT * FROM accounts')

	#-# Checking the Database #-#
	if(read.fetchall() == []):
		print(Fore.YELLOW+"==> There is no account! Please add more account!")
		Add()
	else:

		#-# Printing Accounts to the Table #-#
		read = db.execute('SELECT * FROM accounts')
		accounts = []	

		#-# Converting the Date #-#
		for account in read.fetchall():
			date = Convert(account[5])
			account = list(account)			
			account.remove(account[5])
			account.append(date.newDate)
			account.append(date.hour)
			account = tuple(account)
			accounts.append(account)

		print("\n"+Fore.GREEN+tabulate(accounts, headers=['ID', 'Type', 'Username', 'Password', 'Email', 'Creation Date', 'Creation Time'], tablefmt="fancy_grid")+"\n")			
		Ask()
	
	#-# Disconnecting to the Datababe #-#
	Disconnect()

### ADDING A ACCOUNT ###
def Add():
	
	#-# Taking the Account Variables #-#
	accType = input(bcolors.UNDERLINE+Fore.GREEN+"Account Type"+bcolors.ENDC+Fore.GREEN+" ==> ")	
	accUsername = input(bcolors.UNDERLINE+Fore.GREEN+"Account Username"+bcolors.ENDC+Fore.GREEN+" ==> ")	
	accPass = input(bcolors.UNDERLINE+Fore.GREEN+"Account Password"+bcolors.ENDC+Fore.GREEN+" ==> ")	
	accEmail = input(bcolors.UNDERLINE+Fore.GREEN+"Account Email"+bcolors.ENDC+Fore.GREEN+" ==> ")
	print("\n")
	#-# Checking the Account Variables #-#
	if(accType and accUsername and accEmail and accPass):
		
		#-# Connecting to the Database #-#		
		Connect()

		#-# Checking the database If Account Exists #-#
		check = db.execute("SELECT * FROM accounts WHERE account_type == '"+accType+"' AND account_username == '"+accUsername+"' AND account_password == '"+accPass+"' AND account_email == '"+accEmail+"'")                            

		if (len(check.fetchall()) > 0):
			print(Fore.YELLOW+"==> This account is already available!")
			Add()
			
		else:

			#-# Adding Account to the Database #-#
			add = db.execute("INSERT INTO accounts(account_type, account_username, account_password, account_email, account_date) VALUES ('"+accType+"', '"+accUsername+"', '"+accPass+"', '"+accEmail+"', datetime('now'))")   
			
			#-# Disconnecting to the Datababe #-#
			Disconnect()	
			
			if(add):
				print(Fore.CYAN+"==> Added to the database successfully!")
				Ask()
			else:
				print(Fore.RED+"==> There was an error when adding to the account database. Please try again later.")
				exit()	
	else:
		print(Fore.RED+"==> Please complete all questions!.")
		Add()

### EDITING THE ACCOUNT ##
def Edit():
	
	#-# Connecting to the Database #-#	
	Connect()

	#-# Checking the Database #-#	
	read = db.execute('SELECT * FROM accounts')
	if(read.fetchall() == []):
		print(Fore.YELLOW+"==> There is no account! Please add more account!")
		Add()
	else:
		
		#-# Taking Account ID for Edit #-#
		upAccID = input(bcolors.UNDERLINE+Fore.GREEN+"Account ID"+bcolors.ENDC+Fore.GREEN+" ==> ")	
		
		#-# Checking the Database for Account #-#
		check = db.execute("SELECT * FROM accounts WHERE account_id == '"+upAccID+"'")
		if(len(check.fetchall()) > 0):
		
			#-# Taking the Account Variables #-#
			upAccType = input(bcolors.UNDERLINE + Fore.GREEN + "Account Type" + bcolors.ENDC + Fore.GREEN+" ==> ")	
			upAccUsername = input(bcolors.UNDERLINE + Fore.GREEN + "Account Username" + bcolors.ENDC+Fore.GREEN+" ==> ")	
			upAccPass = input(bcolors.UNDERLINE + Fore.GREEN + "Account Password" + bcolors.ENDC + Fore.GREEN+" ==> ")
			upAccEmail = input(bcolors.UNDERLINE + Fore.GREEN + "Account Email" + bcolors.ENDC + Fore.GREEN + " ==> ")
			
			#-# Uploading Account Veriables #-#			
			edit = db.execute("UPDATE accounts SET account_type = '"+upAccType+"', account_username = '"+upAccUsername+"', account_password = '"+upAccPass+"', account_email = '"+upAccEmail+"' WHERE account_id == '"+upAccID+"'")                 
			Disconnect()
			if(edit):		
				print(Fore.CYAN+"==> Edited successfully!")
				Ask()
			else:
				print(Fore.RED+"==> There was an error when editing account from the database. Please try again later.")
				exit()
		else:
			print(Fore.RED+"==> No account matching the ID you entered was found!")
			Edit()
		Ask()			

### DELETING THE ACCOUNT ###
def Delete():
	
	#-# Connecting to the Database #-#	
	Connect()

	#-# Checking the Database #-#
	read = db.execute('SELECT * FROM accounts')
	if(read.fetchall() == []):
		print(Fore.YELLOW+"==> There is no account! Please add more account!")
		Add()
	else:
		accID = input(bcolors.UNDERLINE+Fore.GREEN+"Account ID"+bcolors.ENDC+Fore.GREEN+" ==> ")	
		
		#-# Check the Database for Account #-#
		check = db.execute("SELECT * FROM accounts WHERE account_id == '"+accID+"'")
		if(len(check.fetchall()) > 0):
			delete = db.execute("DELETE FROM accounts WHERE account_id == '"+accID+"'")
			Disconnect()
			if(delete):		
				print(Fore.CYAN+"==> Deleted successfully!")
				Ask()
			else:
				print(Fore.RED+"==> There was an error when deleting account from the database. Please try again later.")
				exit()
		else:
			print(Fore.RED+"==> No account matching the ID you entered was found!")
			Disconnect()			
			Delete()
		
		Ask()

### WHAT SHOULD I DO :) ###
def Ask():
	value = input(Fore.CYAN+"==> ")
	if(value == "A"):
		List()
	elif(value == "B"):
		print("\n")
		Add()
	elif(value == "C"):	
		print("\n")
		Edit()
	elif(value == "D"):	
		print("\n")
		Delete()
	elif(value == "E"):
		exit()
	elif(value == "R"):
		#-# Deleting Database #-#
		remove("database.db")
		print(Fore.CYAN+"==> Reseted successfully!")		
		Ask()		
	else:	
		Ask()

#-# Main Function #-#
def Main():
	print(Colorful('''
##############################################################
#                                                            #
#              ACCOUNT KEEPER v1.0                           #
#                   Maked by Lord Ch4os                      #
#                                                            #	
##############################################################
#                                                            #
#    Python Version ==> 3.7.5                                #
#    Mail ==> muetnmuetn@gmail.com                           #
#    Facebook ==> https://facebook.com/muetnmuetn            #
#    Instagram ==> https://instagram.com/umut_ekinci_        #
#    Github ==> https://github.com/LordCh4os/Python          #
#                                                            #
##############################################################
	''', True))

	print(Fore.RED+bcolors.BOLD+bcolors.UNDERLINE+"\nWHAT DO YOU WANT ?"+bcolors.ENDC+Fore.GREEN+"\nA) List Accounts\nB) Add Account\nC) Edit Account\nD) Delete Acount\nE) Exit\nR) Reset (Delete All Accounts)\n")
	Ask()

Main()
