### CONVERTING THE DATE ###
class Convert(): 
	def __init__(self, dateAndTime):

		dateAndTime = dateAndTime.split(" ")
		date = dateAndTime[0].split("-")
		time = dateAndTime[1].split(":")	

		if(date[1] == "01"):
			self.month = "January"
		elif(date[1] == "02"):
			self.month = "February"
		elif(date[1] == "03"):
			self.month = "March"
		elif(date[1] == "04"):
			self.month = "April"
		elif(date[1] == "05"):
			self.month = "May"
		elif(date[1] == "06"):
			self.month = "June"
		elif(date[1] == "07"):
			self.month = "July"
		elif(date[1] == "08"):
			self.month = "August"
		elif(date[1] == "09"):
			self.month = "September"
		elif(date[1] == "10"):
			self.month = "October"
		elif(date[1] == "11"):
			self.month = "November"
		elif(date[1] == "12"):
			self.month = "December"

		if (int(time[0]) > 12):
			self.hour = str(int(time[0]) - 12) + " p.m."	
		elif (int(time[0]) < 12):
			self.hour = time[0] + " a.m."

		self.year = date[0]
		self.day = date[2]
		self.minute = time[1]
		self.second = time[2]
		self.newDate = self.day + " of " + self.month + " " + self.year
	
