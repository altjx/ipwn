#!/usr/bin/python
import sqlite3, commands, getopt
from prettytable import *
from sys import argv

banner = "\n " + "-" * 64
banner += "\n\t iOS 7 Parser, Alton Johnson (alton.jx@gmail.com)\n"
banner += " " + "-" * 64 + "\n"

def help():
	print banner
	print "\n Usage: %s <OPTIONS>" % argv[0]
	print "\n -n \t\t Extract numbers from iOS 7 backup."
	print " -d <directory>\t Provide directory containing iOS 7 backup files."
	print
	exit()

def start(argv):
	if len(argv) < 2:
		help()
	try:
		opts, args = getopt.getopt(argv, "nd:")
	except getopt.GetoptError:
		help()
	
	directory = ""
	numbers = False

	for opt, arg in opts:
		if opt == "-d":
			directory = arg
		elif opt == "-n":
			numbers = True

	if directory == "":
		print "\n Error: No directory provided."
		help()
	if not numbers:
		print "\n Error: No options are selected."
		help()
	print banner
	begin = parser(directory)
	if numbers:
		begin.grab_numbers()

class parser:
	def __init__(self, directory):
		self.directory = directory
	
	def parse_dbs(self):
		db_list = commands.getoutput("file %s/* | grep -i sqlite" % self.directory).split("\n")
		dbs = []
		for i in db_list:
			dbs.append(i[:i.find(":")])
		return dbs
	
	def parse_num(self, number):
		return "(" + number[1:4] + ") " + number[4:7] + "-" + number[7:]

	def grab_numbers(self):
		print " [*] Extracting phone numbers...\n"
		contact = PrettyTable(["Name","Number"])
		contact.align["Name"] = "l"
		contacts = []
		for db in self.parse_dbs():
			conn = sqlite3.connect(db)
			c = conn.cursor()
			c.execute("SELECT name FROM sqlite_master WHERE type='table' ;")
			for table in c.fetchall():
				try:
					c.execute("SELECT * FROM %s;" % table[0])
					for row in c.fetchall():
						if "None, None, u'(" in str(row):
							if str(row[1]) != "None":
								name = str(row[1])
								if str(row[2]) != "None":
									name += " " + str(row[2])
								if name in contacts:
									continue
								number = " " + str(row[16][:15])
								contacts.append(name)
								contact.add_row([name, number])
						elif "+" in str(row) and "None)" in str(row) and "http" not in str(row) \
						and "\\" not in str(row):
							if str(row[1]) != "None":
								name = row[1]
								if str(row[2]) != "None":
									name += " " + row[2]
								if "(" in str(row)[1:]:
									temp = str(row)[1:]
									number = temp[temp.find("("):temp.find("(")+14]
								elif "(" not in str(row)[1:] and "+" in str(row):
									temp = str(row)
									number = self.parse_num(temp[temp.find("+")+1:temp.find("+")+12])
								if name in contacts or "'" in number:
									continue
								contacts.append(name)
								contact.add_row([name, number])
				except Exception, err:
					pass
		print contact.get_string(sortby="Name")
		print "\n Total contacts: %s" % str(len(contacts))

if __name__ == "__main__":
	try:
		start(argv[1:])
	except KeyboardInterrupt:
		print "\n Exiting. Closed by user (ctrl-c)."
	except Exception, err:
		print err
		exit()
print
