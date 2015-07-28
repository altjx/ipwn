#!/usr/bin/env python
#
#################################################################################################################
#	                                                                                    													#
#	 This script was designed to be seemingly easy if you're used to ispoof by Stone.		                        	#
#	 This script supports a variety of things that we typically test for during an external pentest.            	#
#	 Overall, you can automate the process of SMTP User Enumeration, SMTP Spoofing, and/or SMTP relay.	          #
#	 Any combination of the techniques can be used -- in other words, it's as flexible as you need it to be.      #
#														                                                                                    #
#	 Author: Alton Johnson 											                                                                  #
#	 Contact: alton.jx@gmail.com                                                              										#
#	 Updated: 05-24-2013								                                                                     			#
#	 Version: 1.6												                                                                          #
#														                                                                                    #
#	 While this tool supports a variety of options, there is still a lot of room for improvement.		              #
#	 Please report any bugs and/or suggestions to me.							                                                #
#														                                                                                     #
#################################################################################################################

from sys import argv
import time, smtplib, getopt, socket, os

class colors:
	lightblue = "\033[1;36m"
	blue = "\033[1;34m"
	normal = "\033[0;00m"
	red = "\033[1;31m"
	white = "\033[1;37m"
	green = "\033[1;32m"

start_time = time.time()
banner = "\n " + "-" * 69 + "\n " + colors.white + " iSMTP v1.6 - SMTP Server Tester, Alton Johnson (alton.jx@gmail.com)\n " + colors.normal + "-" * 69 + "\n "
split_service = "\n " + colors.white + "-" * 10 + " starting next test " + "-" * 10 + colors.normal + "\n"
split_target = "\n " + colors.white + "=" * 23 + " starting next target " + "=" * 23 + colors.normal + "\n"

def help():
	print banner
	print " Usage: ./iSMTP.py <OPTIONS>\n"
	print colors.red + " Required:\n" + colors.normal
	print "\t-f <import file>\tImports a list of SMTP servers for testing.\n\t\t\t\t(Cannot use with '-h'.)"
	print "\t-h <host>\t\tThe target IP and port (IP:port).\n\t\t\t\t(Cannot use with '-f'.)"
	print colors.green + "\n Spoofing:\n" + colors.normal
	print "\t-i <consultant email>\tThe consultant's email address."
	print "\t-s <sndr email>\t\tThe sender's email address."
	print "\t-r <rcpt email>\t\tThe recipient's email address."
	print "\t   --sr <email>\t\tSpecifies both the sender's and recipient's email address."
	print "\t-S <sndr name>\t\tThe sender's first and last name."
	print "\t-R <rcpt name>\t\tThe recipient's first and last name."
	print "\t   --SR <name>\t\tSpecifies both the sender's and recipient's first and last name."
	print "\t-m\t\t\tEnables SMTP spoof testing."
	print "\t-a\t\t\tIncludes .txt attachment with spoofed email."
	print colors.green + "\n SMTP enumeration:\n" + colors.normal
	print "\t-e <file>\tEnable SMTP user enumeration testing and imports email list."
	print "\t-l <1|2|3>\tSpecifies enumeration type (1 = VRFY, 2 = RCPT TO, 3 = all).\n\t\t\t(Default is 3.)"
	print colors.green + "\n SMTP relay:\n" + colors.normal
	print "\t-i <consultant email>\tThe consultant's email address."
	print "\t-x\t\t\tEnables SMTP external relay testing."
	print colors.green + "\n Misc:\n" + colors.normal
	print "\t-t <secs>\tThe timeout value. (Default is 10.)"
	print "\t-o\t\tCreates \"ismtp-results\" directory and writes output to\n\t\t\tismtp-results/smtp_<service>_<ip>(port).txt\n"
	print " Note: Any combination of options is supported (e.g., enumeration, relay, both, all, etc.).\n"

def output_write(smtp_host,smtp_port,data,output,smtp_test):
	if output:
		if not os.path.exists('ismtp-results'):
			os.makedirs('ismtp-results')
		output_file = open('ismtp-results/%s_%s(%s).txt' % (smtp_test,smtp_host,smtp_port), 'w')
		output_file.write(data)
		output_file.write("%s" % ("-" * 5)) 
		output_file.write("\nCompleted in: %.1fs\n" % (time.time() - start_time))
		output_file.close()
		print " Output file created."

def smtp_relay(smtp_host,smtp_port,consultant_email):
	print " Testing SMTP server [external relay]: %s:%s\n" % (smtp_host, smtp_port)
	smtp_rlog = "\n Testing SMTP server [external relay]: %s:%s\n" % (smtp_host, smtp_port)

	#grabs the domain name from consultant email
	consultant_domain = consultant_email[consultant_email.rfind("@")+1:]
	
	try:
		server = smtplib.SMTP(smtp_host, smtp_port)
		# server.docmd returns ['status code','message']
		response = server.docmd("helo",consultant_domain)
		print " - Submitted 'helo %s' : %s" % (consultant_domain,str(response[0]))
		smtp_rlog += "\n - Submitted 'helo example.com' : %s" % str(response[0])
		response = server.docmd("mail from:","<%s>" % consultant_email)
		print " - Submitted 'mail from: <%s>' : %s" % (consultant_email, str(response[0]))
		smtp_rlog += "\n - Submitted 'mail from: <%s>' : %s" % (consultant_email, str(response[0]))
		response = server.docmd("rcpt to:","<%s>" % consultant_email)
		print " - Submitted 'rcpt to: <%s>' : %s" % (consultant_email, response[0])
		smtp_rlog += "\n - Submitted 'rcpt to: <%s>' : %s" % (consultant_email, response[0])
		if response[0] != 250:
			print colors.red + "\n External SMTP relay access denied." + colors.normal
			smtp_rlog += colors.red + "\n\n External SMTP relay access denied." + colors.normal
		else:
			print colors.blue + "\n External SMTP relay enabled." + colors.normal
			smtp_rlog += colors.blue + "\n\n External SMTP relay enabled." + colors.normal
		server.quit()
	except smtplib.SMTPException, err:
		if "421" in str(err):
			print colors.red + " Error: Service rejected connection attempt." + colors.normal
			smtp_rlog = colors.red + "\n Error: Service rejected connection attempt." + colors.normal
		else:
			print colors.red + str(err) + colors.normal
			smtp_rlog += "\n" + colors.red + str(err) + colors.normal
	except socket.timeout:
		print colors.red + " Error: The system timed out while trying to connect to the SMTP server." + colors.normal
		smtp_rlog += colors.red + "\n Error: The system while timed out trying to connect to the SMTP server." + colors.normal
	except Exception, err:
		print colors.red + str(err) + colors.normal
		smtp_rlog += "\n" + colors.red + str(err) + colors.normal

	print "\n Completed external SMTP relay test."
	smtp_rlog += "\n\n Completed external SMTP relay test.\n\n"
	
	#return log in case output is enabled
	return smtp_rlog

def smtp_spoof(smtp_host,smtp_port,consultant_email,sndr_email,rcpt_email,sndr_name,rcpt_name,spoof_attach):
	print " Testing SMTP server [internal spoof]: %s:%s\n" % (smtp_host, smtp_port)
	smtp_slog = "\n Testing SMTP server [internal spoof]: %s:%s\n" % (smtp_host, smtp_port)
	
	# grab domain from target mail server's banner
	try:
		s = socket.socket()
		s.connect((smtp_host,smtp_port))
		response = s.recv(1024)
		domain = response.split(' ')[1].split('.')[-2] + "." + response.split(' ')[1].split('.')[-1]
		s.close()
	except socket.timeout:
		print colors.red + " Error: The system timed out while trying to connect to the SMTP server." + colors.normal
		smtp_slog += "\n" + colors.red + " Error: The system timed out while trying to connect to the SMTP server." + colors.normal
		print "\n Completed SMTP internal spoof test."
		smtp_slog += "\n\n Completed SMTP internal spoof test.\n\n"
		return smtp_slog
	except Exception, err:
		if "range" in str(err):
			domain = 'example.com'
		else:
			print colors.red + " Please check the SMTP server for typos: %s" % smtp_host + colors.normal
			smtp_slog += colors.red + "\n Error: Please check the SMTP server for typos: %s" % smtp_host + colors.normal
			print colors.red + " If your SMTP servers do not contain a typo, please report this error to Alton." + colors.normal
			print "\n Completed SMTP internal spoof test."
			smtp_slog += "\n\n Completed SMTP internal spoof test.\n\n"
			return smtp_slog

	try: 
		smtp_subj = "SMTP Server Test"
		smtp_msg = "\r\n%s:\r\n\r\nThis message is part of a security assessment.  If this message is received, \nplease take a screenshot and forward it \nto %s.\r\n\r\nThis message was delivered through %s:%s." % (rcpt_name, consultant_email, smtp_host, str(smtp_port))
		if spoof_attach:
			smtp_data = "From: %s <%s>\r\nTo: %s <%s>\r\nSubject: %s\r\nMIME-Version: 1.0\r\nContent-Type: multipart/mixed; boundary=\"000Message000\"\r\n\r\n--000Message000\r\n%s\r\n\r\n--000Message000\r\nContent-Type: application/octet-stream; name=\"Attachment.txt\"\r\n\r\nSecurity Assessment (with attachment).\r\n\r\n--000Message000--\r\n." % (sndr_name, sndr_email, rcpt_name, rcpt_email, smtp_subj,smtp_msg)
		else:
			smtp_data = "From: %s <%s>\r\nTo: %s <%s>\r\nSubject: %s\r\n%s\r\n." % (sndr_name, sndr_email, rcpt_name, rcpt_email, smtp_subj,smtp_msg)
		server = smtplib.SMTP(smtp_host, smtp_port)
		# server.docmd returns ['status code','message']
		response = server.docmd("helo",domain)
		print " - Submitted 'helo %s' : %s" % (domain,str(response[0]))
		smtp_slog += "\n - Submitted 'helo %s' : %s" % (domain, str(response[0]))
		response = server.docmd("mail from:", "<%s>" % sndr_email)
		print " - Submitted 'mail from' : %s" % str(response[0])
		smtp_slog += "\n - Submitted 'mail from' : %s" % str(response[0])
		response = server.docmd("rcpt to:", "<%s>" % rcpt_email)
		print " - Submitted 'rcpt to' : %s" % str(response[0])
		smtp_slog += "\n - Submitted 'rcpt to' : %s" % str(response[0])
		if str(response[0])[0] == '5':
			print colors.red + "\n Error providing recipient email address: %s" % response[1] + colors.normal
			smtp_slog += colors.red + "\n\n Error providing recipient email address: %s" % response[1] + colors.normal
			server.quit()
			print "\n Completed SMTP internal spoof test."
			smtp_slog += "\n\n Completed SMTP internal spoof test.\n\n"
			return smtp_slog
		response = server.docmd("data")
		print " - Submitted 'data' : %s" % str(response[0])
		smtp_slog += "\n - Submitted 'data' : %s" % str(response[0])
		if spoof_attach:
			print " - Adding attachment..."
			smtp_slog += "\n - Adding attachment..."
		print " - Submitting message...\n"
		smtp_slog += "\n - Submitting message...\n"
		response = server.docmd("%s" % smtp_data)
		if str(response[0]) != '250':
			print colors.red + "\n Error submitting message: %s" % response[1] + colors.normal
			smtp_slog += colors.red + "\n\n Error submitting message: %s" % response[1] + colors.normal
			server.quit()
			print "\n Completed SMTP internal spoof test."
			smtp_slog += "\n\n Completed SMTP internal spoof test.\n\n"
			return smtp_slog
		if spoof_attach:
			modded_data = smtp_data.split('\n')
			del modded_data[3:7]
			del modded_data[12:]
			modded_data.insert(3, "Attachment: Attachment.txt")
			for i in modded_data:
				print colors.blue + "   | " + i + colors.normal
				smtp_slog += colors.blue + "\n   | " + i + colors.normal
			smtp_slog += "\n"
			print
		else:
			print colors.blue + "   | " + smtp_data.replace("\n", "\n   | ")[:-3] + colors.normal
			smtp_slog += colors.blue + "\n   | " + smtp_data.replace("\n", "\n   | ")[:-3] + colors.normal
		print " - Message complete"
		smtp_slog += "\n - Message complete"
		print " - Successfully submitted message: %s" % str(response[0])
		smtp_slog += "\n - Successfully submitted message: %s" % str(response[0])
		server.quit()
	except socket.timeout:
		pass
	except Exception, err:
		if "421" in str(err):
			print colors.red + " Error: Service rejected connection attempt." + colors.normal
			smtp_slog = colors.red + "\n Error: Service rejected connection attempt." + colors.normal
		else:
			print colors.red + " Error: " +  str(err) + colors.normal
			smtp_slog += colors.red + "\n Error: " + str(err) + colors.normal

	print "\n Completed SMTP internal spoof test."
	smtp_slog += "\n\n Completed SMTP internal spoof test.\n\n"
	
	#return log in case output is enabled
	return smtp_slog
	
def smtp_enumeration(smtp_host,smtp_port,email_list,enum_level):
	print " Testing SMTP server [user enumeration]: %s:%s" % (smtp_host,smtp_port)
	print " Emails provided for testing: %s\n" % str(len(email_list))
	smtp_elog = "\n Testing SMTP server [user enumeration]: %s:%s" % (smtp_host,smtp_port)
	smtp_elog += "\n Emails provided for testing: %s\n" % str(len(email_list))
	validc = 0

	#grab domain from target mail server's banner
	try:
		s = socket.socket()
		s.connect((smtp_host,smtp_port))
		response = s.recv(1024)
		domain = response.split(' ')[1].split('.')[-2] + "." + response.split(' ')[1].split('.')[-1]
		s.close()
	except socket.timeout:
		print colors.red + " Error: The system timed out while trying to connect to the SMTP server." + colors.normal
		smtp_elog += "\n" + colors.red + " Error: The system timed out while trying to connect to the SMTP server." + colors.normal
		print "\n Completed SMTP user enumeration test."
		smtp_elog += "\n\n Completed SMTP user enumeration test.\n\n"
		return smtp_elog
	except Exception, err:
		if "list index" in str(err):
			domain = 'example.com'
		else:
			print colors.red + " Please check the SMTP server for typos: %s" % smtp_host + colors.normal
			smtp_elog += colors.red + "\n Error: Please check the SMTP server for typos: %s" % smtp_host + colors.normal
			print colors.red + " If your SMTP servers do not contain a typo, please report this error to Alton." + colors.normal
			print "\n Completed SMTP user enumeration test."
			smtp_elog += "\n\n Completed SMTP user enumeration test.\n\n"
			return smtp_elog
	try:
		server = smtplib.SMTP(smtp_host,smtp_port)
		response = server.docmd('helo',domain)
	except Exception, err:
		if "421" in str(err):
			print colors.red + " Error: Service rejected connection attempt." + colors.normal
			smtp_elog = colors.red + "\n Error: Service rejected connection attempt." + colors.normal
		else:
			print colors.red + " Error: " + str(err) + colors.normal
			smtp_elog += colors.red + "\n Error: " + str(err) + colors.normal
		return smtp_elog
	
	# set spaces to format output
	offset = 0
	for line in email_list:
		if len(line) > offset:
			offset = len(line) + 3

	# begin testing via SMTP VRFY
	# server.docmd returns ['status code','message']
	if enum_level == 1 or enum_level == 3:
		print " Performing SMTP VRFY test...\n"
		smtp_elog += "\n Performing SMTP VRFY test...\n"
		fail = 0
		for i in email_list:
			try:
				if "@" in i:
					response = server.docmd('VRFY', '%s' % i[:i.find("@")])
				else:
					response = server.docmd('VRFY', i)
				if response[0] == 502 or response[0] == 252 or (response[0] == 550 and "user unknown" not in response[1].lower()):
					if "disabled" in str(response[1]) or "Cannot VRFY user" in str(response[1]):
						print colors.red + " Server is not vulnerable to SMTP VRFY user enumeration." + colors.normal
						smtp_elog +=   colors.red + "\n Server is not vulnerable to SMTP VRFY user enumeration." + colors.normal
					else:
						print colors.red + " Error: %s." % response[1] + colors.normal
						smtp_elog += colors.red + "\n Error: %s." % response[1] + "\n" + colors.normal
					break
				elif response[0] == 250:
					print colors.blue + " [+] %s " % i + "-" * (offset-len(i)) + " [ success ]" + colors.normal
					smtp_elog +=  colors.blue + "\n [+] %s " % i + "-" * (offset-len(i)) + " [ success ]" + colors.normal
					fail = 0
				else:
					if fail == 15:
						print colors.red + "\n Error: Too many consistent failures. Probably not vulnerable to SMTP VRFY. Skipping... " + colors.normal
						smtp_elog += colors.red + "\n\n Error: Too many consistent failures. Probably not vulnerable to SMTP VRFY. Skipping... \n" + colors.normal
						break
					print colors.red + " [-] %s " % i + "-" * (offset-len(i)) + " [ invalid ]" + colors.normal
					smtp_elog += colors.red + "\n [-] %s " % i + "-" * (offset-len(i)) + " [ invalid ]" + colors.normal
					fail+= 1
#					print colors.red + " Error: %s:%s" % (response[0],response[1]) + colors.normal
#					smtp_elog += colors.red + "\n Error: %s:%s" % (response[0],response[1]) + colors.normal
			except Exception, err:
				if "unexpectedly closed" in str(err):
					print colors.red + " Error: Attempting to reconnect..." + colors.normal
					smtp_elog += colors.red + "\n Error: Attempting to reconnect..." + colors.normal
					try:
						server = smtplib.SMTP(smtp_host,smtp_port)
						response = server.docmd('helo',domain)
						continue
					except Exception:
						print colors.red + " Error: Cannot reconnect. Quitting..." + colors.normal
						smtp_elog += colors.red + "\n Error: Cannot reconnect. Quitting...\n" + colors.normal
						break
				else:
					print colors.red + " Error: " + colors.red + str(err) + "\n" + colors.normal
					smtp_elog += colors.red + "\n Error: " + colors.red + str(err) + "\n\n"  + colors.normal
		print	
	# begin testing via SMTP RCPT TO
	# server.docmd returns ['status code','message']
	if enum_level == 2 or enum_level == 3:
		print " Performing SMTP RCPT TO test...\n"
		smtp_elog += "\n Performing SMTP RCPT TO test...\n"
		
		try: 
			response = server.docmd('mail from:', '<pentest@company.com>')
			if str(response[0])[0] == '5':
				print colors.red + " Error: %s" % response[1] + colors.normal
				smtp_elog += colors.red +"\n\n Error: %s" % response[1] + colors.normal
				server.quit()
				print "\n Completed SMTP user enumeration test."
				smtp_elog += "\n\n Completed SMTP user enumeration test.\n\n"
				return smtp_elog
			email_domain = email_list[1][email_list[1].find("@"):]
			response = server.docmd("rcpt to:", "<invalidemail34598374%s>" % email_domain)
			if str(response[0])[0] == '2' or response[0] == 554:
				print colors.red + " Server is not vulnerable to SMTP RCPT TO user enumeration." + colors.normal
				smtp_elog += colors.red + "\n Sever is not vulnerable to SMTP RCPT TO user enumeration." + colors.normal
				server.quit()
				print "\n Completed SMTP user enumeration test."
				smtp_elog += "\n\n Completed SMTP user enumeration test.\n\n"
				return smtp_elog
			for n in email_list:
				if "@" not in n:
					print colors.red + " [-] %s " % n + "-" * (offset-len(n)) + " skipped (invalid email format)" + colors.normal
					smtp_elog += colors.red +  "\n [-] %s " % n + "-" * (offset-len(n)) + " skipped (invalid email format)" + colors.normal
					continue
				try:
					response = server.docmd('rcpt to:', '<%s>' % n)
				except socket.timeout:
					print colors.red + " [-] %s " % n + "-" * (offset-len(n)) + " timeout" + colors.normal                                    
					smtp_elog += colors.red + " [-] %s " % n + "-" * (offset-len(n)) + " timeout" + colors.normal
					continue
				except Exception:
					print colors.red + " Error: Attempting to reconnect..." + colors.normal
					smtp_elog += colors.red + "\n Error: Attempting to reconnect..." + colors.normal
					try:
						server = smtplib.SMTP(smtp_host,smtp_port)
						response = server.docmd('helo',domain)
						response = server.docmd('mail from:', '<pentest@company.com>')
						continue
					except Exception:
						print colors.red + " Error: Cannot reconnect. Quitting..." + colors.normal
						smtp_elog += colors.red + "\n Error: Cannot reconnect. Quitting..." + colors.normal
						break
				if response[0] == 250:
					print colors.blue + " [+] %s " % n + "-" * (offset-len(n)) + " [ valid ]" + colors.normal
					smtp_elog += colors.blue + "\n [+] %s " % n + "-" * (offset-len(n)) + " [ valid ]" + colors.normal
				else:
					print colors.red + " [-] %s " % n + "-" * (offset-len(n)) + " [ invalid ]" + colors.normal
					smtp_elog += colors.red + "\n [-] %s " % n + "-" * (offset-len(n)) + " [ invalid ]" + colors.normal
					validc = 0
			print 
		except Exception, err:
			if "timed out" in str(err):
				print colors.red + " Error: Timed out. Try increasing the default timeout value to 10+ secs.\n" + colors.normal
				smtp_elog += colors.red + "\n Error: Timed out. Try increasing the default timeout value to 10+ secs.\n\n" + colors.normal
			else:
				print colors.red + " Error: \n" +  str(err) + colors.normal
				smtp_elog += colors.red + "\n Error: \n\n" + str(err) + colors.normal
	print " Completed SMTP user enumeration test."
	smtp_elog += "\n Completed SMTP user enumeration test.\n\n"
	
	try:
		server.quit()
	except Exception, err:
		pass
	return smtp_elog

def start(argv):
	if len(argv) < 1:
		help()
		exit()
	try:
		opts, args = getopt.getopt(argv, "h:i:s:r:S:R:moxe:l:f:t:a", ['sr=','SR='])
	except getopt.GetoptError, err:
		print colors.red + "\n Error: %s" % err + colors.normal
		help()
		exit()

	# set default variables (needed in case if statement isn't met)
	smtp_host = ''
	smtp_port = 25
	consultant_email = ''
	sndr_email = ''
	rcpt_email = ''
	sndr_name = ''
	rcpt_name = ''
	smtp_enum = False
	smtp_list = False
	email_list = ''
	socket.setdefaulttimeout(10)
	relay_test = False
	output = False
	enum_level = 3
	spoof_test = False
	spoof_attach = False

	# for loop stdin to determine what arguments are provided
	for opt, arg in opts:
		if opt == "-i":
			consultant_email = arg
		elif opt == "-s":
			sndr_email = arg
		elif opt == "-r":
			rcpt_email = arg
		elif opt == "-S":
			sndr_name = arg
		elif opt == "-R":
			rcpt_name = arg
		elif opt == "-f":
			if smtp_host != "":
				print colors.blue + "\n Error: You cannot use '-f' with '-h'!" + colors.normal
				help()
				exit()
			try: 
				smtpfile = open(arg)
				smtp_file = smtpfile.read().split()
			except Exception, err:
				print colors.red + "\n Error: %s\n" % err + colors.normal
				exit()
			smtp_list = True
		elif opt == "-h":
			if ":" in arg:
				smtp_host = arg.split(":")[0]
				smtp_port = int(arg.split(":")[1])
			else:
				smtp_host = arg
			if smtp_list:
				smtpfile.close()
				print colors.red +  "\n Error: You cannot use '-h' with '-f'!" + colors.normal
				help()
				exit()
		elif opt == "-t":
			socket.setdefaulttimeout(float(arg))
		elif opt == "-e":
			smtp_enum = True
			try:
				email_file = open(arg)
				email_list = email_file.read().split()
			except Exception, err:
				print colors.red + "\n Error: %s\n" % err + colors.normal
				exit()
		elif opt == "-x":
			relay_test = True
		elif opt == "-o":
			output = True
		elif opt == "-l":
			enum_level = int(arg)
		elif opt == "--SR":
			sndr_name = arg
			rcpt_name = arg
		elif opt == "--sr":
			sndr_email = arg
			rcpt_email = arg
		elif opt == "-m":
			spoof_test = True
		elif opt == "-a":
			spoof_attach = True

	#assign required parameters depending on the test being conducted (for error checking as well)
	spoof_options = {'SMTP Port':smtp_port,'consultant email address':consultant_email,'sender email address':sndr_email,'recipient email address':rcpt_email,'sender name':sndr_name,'recipient name':rcpt_name}
	enum_options = {'email list':email_list,'SMTP port':smtp_port}
	relay_options = {'consultant email address':consultant_email,'SMTP port':smtp_port}

	# checks for errors before processing arguments
	if smtp_host == "" and smtp_list == False:
		print colors.red + "\n Error: You must provide either an SMTP server or an imported list of SMTP servers." + colors.normal
		help()
		exit()
	if smtp_enum == False and spoof_test == False and relay_test == False:
		print colors.red + "\n Error: You didn't enable any options such as spoof (-m), relay (-x), and/or enumeration (-e <list>)." + colors.normal
		help()
		exit()
	if smtp_enum == True:
		for b in enum_options:
			if enum_options[b] == "":
				print colors.red + "\n Error: While providing SMTP enumeration arguments, you forgot to provide the %s." % b + colors.normal
				help()
				exit()
	if relay_test == True:
		for y in relay_options:
			if relay_options[y] == "":
				print colors.red + "\n Error: While providing SMTP relay arguments, you forgot to provide the %s." % y + colors.normal
				help()
				exit()
	if spoof_test == True:
		for x in spoof_options:
			if spoof_options[x] == "":
				print colors.red + "\n Error: While providing SMTP spoofing arguments, you forgot to provide the %s." % x + colors.normal
				help()
				exit()

	#banner will print (only one time throughout entire execution) if all looks well
	print banner

	# performs either SMTP enumeration, SMTP spoofing, SMTP relay, or whatever combination requested
	if smtp_list:
		for i in smtp_file:
			if smtp_file.index(i) > 0:
				print split_target
			if spoof_test:
				output_write(i,smtp_port,smtp_spoof(i,smtp_port,consultant_email,sndr_email,rcpt_email,sndr_name,rcpt_name,spoof_attach),output,'smtp_spoof')
			if relay_test:
				if spoof_test:
					print split_service
				output_write(i,smtp_port,smtp_relay(i,smtp_port,consultant_email),output,'smtp_relay')
			if smtp_enum:
				if spoof_test or relay_test:
					print split_service
				output_write(i,smtp_port,smtp_enumeration(i,smtp_port,email_list,enum_level),output,'smtp_enum')
		smtpfile.close()
		if smtp_enum:
			email_file.close()
	else:
		if spoof_test:
			output_write(smtp_host,smtp_port,smtp_spoof(smtp_host,smtp_port,consultant_email,sndr_email,rcpt_email,sndr_name,rcpt_name,spoof_attach),output,'smtp_spoof')
		if relay_test:
			if spoof_test:
				print split_service
			output_write(smtp_host,smtp_port,smtp_relay(smtp_host,smtp_port,consultant_email),output,'smtp_relay')
		if smtp_enum:
			if spoof_test or relay_test:
				print split_service
			output_write(smtp_host,smtp_port,smtp_enumeration(smtp_host,smtp_port,email_list,enum_level),output,'smtp_enum')
			email_file.close()
		
if __name__ == "__main__":
	try:
		start(argv[1:])
	except KeyboardInterrupt:
		print "\nExiting. Closed by user (ctrl-c)"
		exit()

print "\n" + "-" * 5
print "Completed in: %.1fs\n" % (time.time() - start_time)
