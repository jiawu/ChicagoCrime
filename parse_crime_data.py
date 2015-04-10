import csv
import pdb
import re
import calendar

#generate the data for the python workshop

"""
Every line is in the following format:
'ID,Case Number,Date,Block,IUCR,Primary Type,Description,Location Description,Arrest,Domestic,Beat,District,Ward,Community Area,FBI Code,X Coordinate,Y Coordinate,Year,Updated On,Latitude,Longitude,Location\n'
Here's the line with indices:
'ID [0],Case Number [1],Date [2],Block [3],IUCR [4],Primary Type [5],Description [6],Location Description[7],Arrest [8],Domestic[9],Beat[10],District[11],Ward[12],Community Area[13],FBI Code[14],X Coordinate[15],Y Coordinate[16],Year[17],Updated On[18],Latitude[19],Longitude[20],Location[21]\n'
"""


PATTERN = re.compile(r''',(?=(?:[^'"]|'[^']*'|"[^"]*")*$)''')

""""
file_object = open('/Users/jjw036/ChicagoCrime/Crimes_2001_to_present.csv', 'r')
with open('/Users/jjw036/ChicagoCrime/crimes_2001_to_present_parsed.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=',')
	counter = 0
	for line in file_object:	
		if line:
			#get rid of \n newspace
			new_line = line.strip()	
			#they used commas in one of the fields... yes the dataset is supposed to be COMMA SEPARATED!! ARG!
			#regex below to ignore all the commas in between quotes
			new_line = PATTERN.split(new_line)
			
			#replace commas with space so the dataset won't break
			for index,term in enumerate(new_line):
				if "," in term:
					new_line[index] = term.replace(',', ' ')

			
			try:
				date = new_line[2]
				#date format is 03/03/2014
				if counter != 0:
					month_name = calendar.month_name[int(date[0:2].lstrip('0'))]
					year = new_line[17]
					if int(year) > 2009:
						writer.writerow([new_line[0], new_line[1],new_line[2], new_line[3], new_line[5], new_line[6], new_line[7], new_line[12], new_line[17], month_name, new_line[19], new_line[20]])
				else:
					writer.writerow([new_line[0], new_line[1],new_line[2], new_line[3], new_line[5], new_line[6], new_line[7], new_line[12], new_line[17], "Month", new_line[19], new_line[20]])
			except IndexError:
				print("Found line with incomplete entry.")
			counter += 1
			if counter % 100000 == 0:
				print(counter)
"""
file_object = open('/Users/jjw036/ChicagoCrime/512021.csv', 'r')
with open('/Users/jjw036/ChicagoCrime/weather_parsed.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=',')
	counter = 0
	for line in file_object:	
		if line:
			#get rid of \n newspace
			new_line = line.strip()	
			new_line = PATTERN.split(new_line)
			if counter == 0:
				writer.writerow([new_line[0], new_line[1],new_line[2], new_line[22], "Year","Month"])
			else:
				if "OHARE" in new_line[1]:
					#get only o'hare, get the months and write in a new section
					date = new_line[2]
					#sample date = 20140420
					year = date[0:4]
					month_name = calendar.month_name[int(date[4:6].lstrip('0'))]
					if int(year) > 2009:
						writer.writerow([new_line[0], new_line[1],new_line[2], new_line[22], year,month_name])
				
			counter += 1
			if counter % 100000 == 0:
				print(counter)
