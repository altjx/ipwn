#!/usr/bin/env python

import smtplib
import string
import sys
import getopt

helpMessages = [
	'-r: Recipient to send an email to.',
	'-u: Gmail username (include @gmail.com)',
        '-p: Password to login to gmail with.',
	'-m: Message to send to user.',
	'-s: Subject for the email.',
	'-n: How many times you want to send this email.'
]

class bcolors:
	OKBLUE = '\033[1;34m'
	ENDC = '\033[0m'

	def disable(self):
		self.OKBLUE = '' 
		self.ENDC = ''

print '\n' + '=' * 51
print bcolors.OKBLUE + ' SMSpam v1.0 created by Alton (alton.jx@gmail.com)' + bcolors.ENDC
print '=' * 51 + '\n'

def usage():
	space = '\t' * 2
	for msg in helpMessages:
		print space + msg
	print '\n'  # Newline after all of the messages

def start(argv):
	if len(sys.argv) < 4:
		usage()
		sys.exit()
	try:
		opts, args = getopt.getopt(argv, "r:p:u:s:m:n:")
	except getopt.GetoptError:
		usage()
		sys.exit()
	for opt, arg in opts:
		if opt == '-r':
			rcpt = arg
		elif opt == '-u':
			username = arg
		elif opt == '-m':
			content = arg
		elif opt == '-s':
			subject = arg
		elif opt == '-p':
			passwd = arg
		elif opt == '-n':
			counts = int(arg)
	try:
		attempts = 0
		smtpserver = smtplib.SMTP('smtp.gmail.com',587)
		smtpserver.ehlo()
		smtpserver.starttls()
		smtpserver.ehlo()
		smtpserver.login(username, passwd)
		header = "To: " + rcpt + '\n' + 'From: ' + username + '\n' + 'Subject: ' + subject + '\n\n'
		msg = header + content
		print msg + '\n'
		while attempts != counts:
			smtpserver.sendmail(username, rcpt, msg)
			attempts+=1
			print bcolors.OKBLUE +  'Successfully sent message: ' + str(attempts)
		smtpserver.close()
	except Exception, err:
		print err

if __name__ == '__main__':
	try:
		start(sys.argv[1:])
	except:
		sys.exit()
