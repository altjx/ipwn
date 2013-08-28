#!/usr/bin/python
#
###############################################################################
#																										#
# This script can be used to spider remote systems during post-exploitation.	#
# It is extremely beneficial when you need to spider numerous systems			#
# to identify  for "sensitive" and/or "confidential" data. A great way to use	#
# this script is to redir stdout to a file and grep for suspicious files such	#
# as "assw", "member", "visa", "salary", etc.											#
# 																										#
# Thanks to Josh Stone (www.josho.org) for allowing me to rewrite and expand	#
# on his idea																						#
#																										#
# Author: Alton Johnson																			#
# Contact: alton.jx@gmail.com																	#
# Version: 1.0																						#
#																										#
###############################################################################

import commands, time, getopt, re
from sys import argv

start_time = time.time()

class colors:
	red = "\033[1;31m"
	blue = "\033[1;34m"
	norm = "\033[0;00m"
	green = "\033[1;32m"

banner = "\n " + "-" * 68 + "\n"
banner += "\t SMB Spider v1.0, Alton Johnson (alton.jx@gmail.com)" + "\n"
banner += " " + "-" * 68 + "\n"

def help():
	print banner
	print " Usage: %s <OPTIONS>" % argv[0]
	print colors.red + "\n Credentials (required): \n" + colors.norm
	print "\t -u <user>\t Specify a valid username to authenticate to the system(s)."
	print "\t -p <pass>\t Specify the password which goes with the username."
	print "\t -d <domain>\t If using a domain account, provide domain name."
	print colors.red + "\n Target(s) (required): \n" + colors.norm
	print "\t -h <host>\t Provide IP address or a text file containing IPs."
	print colors.green + "\n Shares:\n" + colors.norm
	print "\t -s <share>\t Specify shares (separate by comma) or specify \"profile\" to spider profiles."
	print "\t -f <file>\t Specify a list of shares from a file."
	print
	exit()

def start(argv):
	if len(argv) < 1:
		help()
	try:
		opts, args = getopt.getopt(argv, "u:p:d:h:s:f:")
	except getopt.GetoptError, err:
		print colors.red + "\n Error: " + err + colors.normal
	
	# set default variables to prevent errors later in script
	smb_user = ""
	smb_pass = ""
	smb_domain = ""
	smb_host = []
	smb_share = ["profile"]

	#parse through arguments
	for opt, arg in opts:
		if opt == "-u":
			smb_user = arg
		elif opt == "-p":
			smb_pass = arg
		elif opt == "-d":
			smb_domain = arg
		elif opt == "-h":
			try:
				smb_host = open(arg).read().split()
			except:
				smb_host.append(arg)
		elif opt == "-f":
			smb_share = open(arg).read().split()
		elif opt == "-s":
			smb_share = arg.split(',')

	#check options before proceeding
	if (not smb_user or not smb_pass or not smb_host):
		print colors.red + "\n Error: Please check to ensure that all required options are provided." + colors.norm
		help()

	#make smb_domain, smb_user, and smb_pass one variable
	if smb_domain:
		credentials = smb_domain + "\\\\" + smb_user + " " + smb_pass
	else:
		credentials = smb_user + " " + smb_pass
	
	#check credentials to avoid locking this account out.
	if smb_share[0] == "profile":
		result = commands.getoutput("smbclient -c ls //%s/C$ -U %s" % (smb_host[0], credentials))
	else:
		result = commands.getoutput("smbclient -c ls //%s/%s -U %s" % (smb_host[0], smb_share[0], credentials))
	if "NT_STATUS_LOGON_FAILURE" in result:
		print colors.red + "\n Error: Invalid credentials. Please correct credentials and try again.\n" + colors.norm
		exit()
	elif "NT_STATUS_ACCESS_DENIED" in result:
		print colors.red + "\n Error: Valid credentials, but no access. Try another account.\n" + colors.norm
		exit()
	#start spidering
	print banner
	for host in smb_host:
		for share in smb_share:
			spider_host(credentials, host, share)

def parse_result(result, smb_host, smb_share):
	############################################################
	# this small section removes all of the unnecessary crap. yes, i know it's ugly.
	errors = ["STATUS_NO_SUCH_FILE","STATUS_ACCESS_DENIED",\
"STATUS_OBJECT_NAME_INVALID", "STATUS_INVALID_NETWORK_RESPONSE"] # these are "weird" error messages that appear with smbclient. Prior checks exist to ensure shares/files are accessible.
	result = result.split('\n')
	purge = []
	for num in range(0,len(result)):
		if "  .  " in result[num] or "  ..  " in result[num] or "Domain=" in result[num]\
 or "    D" in result[num] or len(result[num]) < 2 or "blocks of size" in result[num]:
			purge.append(num)
	purge = sorted(purge, reverse=True)
	for i in purge:
		del result[i]	
	############################################################
	directory = ""
	filename = ""
	for x in result:
		if x[0] == "\\":
			directory = x
		else:
			filename = x[2:]
			filename = filename[:filename.find("    ")]
		fail = 0
		for error in errors:
			if error in filename:
				fail = 1
		if "BAD_NETWORK" in filename:
			print colors.red + "Error: Invalid share -> smb://%s/%s" % (smb_host,smb_share) + colors.norm
			return
		if fail == 0 and len(filename) > 0:
			print "Spider\t \\\\%s\%s" % (smb_host,smb_share) + directory + "\\" + filename

def fingerprint_fs(smb_host, credentials):
	result = commands.getoutput("smbclient -c \"ls Users\\*\" //%s/C$ -U %s" % (smb_host, credentials)).split()
	if "NT_STATUS_OBJECT_NAME_NOT_FOUND" in result:
		return "old"
	else:
		return "new"

def find_users(result):
	result = result.split('\n')
	purge = []
	users = []
	for num in range(0,len(result)):
		if "  .  " in result[num] or "  ..  " in result[num] or "Domain=" in result[num]\
 or len(result[num]) < 2 or "blocks of size" in result[num]:
			purge.append(num)
	purge = sorted(purge, reverse=True)
	for i in purge:
		del result[i]

	#clean up users list a little bit
	for i in result:
		user = i[:i.find("   D")]
		user = user[2:user.rfind(re.sub(r'\W+', '', user)[-1])+1]
		users.append(user)
	return users

def spider_host(credentials, smb_host, smb_share):
	if smb_share.lower() == "profile":
		if fingerprint_fs(smb_host, credentials) == "old":
			folders = ['My Documents','Desktop']
			result = commands.getoutput("smbclient -c \"ls \\\"Documents and Settings\\*\" //%s/C$ -U %s" % (smb_host, credentials))
			if "UNREACHABLE" in result:
				print colors.red + "Error contacting system %s. Check to ensure that host is online." % smb_host + colors.norm
				return
			users = find_users(result)
			for user in users:
				for folder in folders:
					result = commands.getoutput("smbclient -c \"recurse;ls \\\"Documents and Settings\\%s\\%s\" //%s/C$ -U %s" % (user, folder, smb_host, credentials))
					parse_result(result, smb_host, "C$")
		else:
			folders = ['Documents','Desktop','Music','Videos','Downloads','Pictures']
			result = commands.getoutput("smbclient -c \"ls \\\"Users\\*\" //%s/C$ -U %s" % (smb_host, credentials))
			if "UNREACHABLE" in result:
				print colors.red + "Error contacting system %s. Check to ensure that host is online." % smb_host + colors.norm
				return
			users = find_users(result)
			for user in users:
				for folder in folders:
					result = commands.getoutput("smbclient -c \"recurse;ls \\\"Users\\%s\\%s\" //%s/C$ -U %s" % (user, folder, smb_host, credentials))
					parse_result(result, smb_host, "C$")
	else:
		result = commands.getoutput("smbclient -c \"recurse;ls\" //%s/%s -U %s" % (smb_host, smb_share, credentials))
		if "UNREACHABLE" in result:
			print colors.red + "Error contacting system %s. Check to ensure that host is online." % smb_host + colors.norm
			return
		parse_result(result, smb_host,smb_share)

if __name__ == "__main__":
	try:
		start(argv[1:])
	except KeyboardInterrupt:
		print "\n Exiting. Interrupted by user (ctrl-c)."
		exit()
	except Exception, err:
		print err
		exit()

print "\n-----"
print "Completed in: %.1fs" % (time.time() - start_time)
