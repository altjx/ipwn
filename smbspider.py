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

banner = "\n " + "*" * 56
banner += "\n *     		        _     				*"
banner += "\n *    		       | |       //  \\\\			* "
banner += "\n *	  ___ _ __ ___ | |__    _\\\\()//_		*"
banner += "\n *	 / __| '_ ` _ \| '_ \  / //  \\\\ \ 		*"
banner += "\n *	 \__ \ | | | | | |_) |   |\__/|			*"
banner += "\n *	 |___/_| |_| |_|_.__/				*"
banner += "\n *							*"
banner += "\n * SMB Spider v1.0, Alton Johnson (alton.jx@gmail.com) 	*"
banner += "\n " + "*" * 56 + "\n"

def help():
	print banner
	print " Usage: %s <OPTIONS>" % argv[0]
	print colors.red + "\n Credentials (required): \n" + colors.norm
	print "\t -u <user>\t Specify a valid username to authenticate to the system(s)."
	print "\t -p <pass>\t Specify the password which goes with the username."
	print "\t -P <hash>\t Use -P to provide password hashes if cleartext pw isn't known."
	print "\t -d <domain>\t If using a domain account, provide domain name."
	print colors.red + "\n Target(s) (required): \n" + colors.norm
	print "\t -h <host>\t Provide IP address or a text file containing IPs."
	print colors.green + "\n Shares (optional):\n" + colors.norm
	print "\t -s <share>\t Specify shares (separate by comma) or specify \"profile\" to spider profiles."
	print "\t -f <file>\t Specify a list of shares from a file."
	print
	exit()

def start(argv):
	if len(argv) < 1:
		help()
	try:
		opts, args = getopt.getopt(argv, "u:p:d:h:s:f:P:")
	except getopt.GetoptError, err:
		print colors.red + "\n Error: " + err + colors.normal
	
	# set default variables to prevent errors later in script
	smb_user = ""
	smb_pass = ""
	smb_domain = ""
	smb_host = []
	smb_share = ["profile"]
	pth = False

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
		elif opt == "-P":
			if arg[-3:] == ":::":
				arg = arg[:-3]
			smb_pass = arg
			pth = True

	#check options before proceeding
	if (not smb_user or not smb_pass or not smb_host):
		print colors.red + "\nError: Please check to ensure that all required options are provided." + colors.norm
		help()
	if pth:
		result = commands.getoutput("pth-smbclient")
		if "not found" in result.lower():
			print colors.red + "\nError: The passing-the-hash package was not found. Therefore, you cannot pass hashes."
			print "Please run \"apt-get install passing-the-hash\" to fix this error and try running the script again.\n" + colors.norm
			exit()

	#make smb_domain, smb_user, and smb_pass one variable
	if smb_domain:
		credentials = smb_domain + "\\\\" + smb_user + " " + smb_pass
	else:
		credentials = smb_user + " " + smb_pass
	
	#start spidering
	print banner
	print "Spidering %s system(s)...\n" % len(smb_host)
	begin = spider(credentials, smb_host, smb_share, pth)
	begin.start_spidering()

class spider:
	def __init__(self, credentials, hosts, shares,pth):
		self.list_of_hosts = hosts
		self.list_of_shares = shares
		self.credentials = credentials
		self.smb_host = ""
		self.smb_share = ""
		self.skip_host = ""
		self.pth = pth
	
	def start_spidering(self):
		for host in self.list_of_hosts:
			print "Attempting to spider %s. Please wait..." % host
			for share in self.list_of_shares:
				if self.skip_host == host:
					break
				self.smb_host = host
				self.smb_share = share
				self.spider_host()

	def parse_result(self, result):
		############################################################
		# this small section removes all of the unnecessary crap. a bit ugly, i know! :x
		errors = ["STATUS_NO_SUCH_FILE","STATUS_ACCESS_DENIED",
"STATUS_OBJECT_NAME_INVALID", "STATUS_INVALID_NETWORK_RESPONSE"
	]
		result = result.split('\n')
		purge = []
		trash = ["  .  ", "  ..  ", "Domain=", "    D", "blocks of size",
"wrapper called", "Substituting user supplied"]
		for num in range(0,len(result)):
			for d in trash:
				if d in result[num] or len(result[num]) < 2:
					purge.append(num)
		purge = list(set(purge))
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
				print colors.red + "Error: Invalid share -> smb://%s/%s" % (self.smb_host,self.smb_share) + colors.norm
				return
			if fail == 0 and len(filename) > 0:
				print "Spider\t \\\\%s\%s" % (self.smb_host,self.smb_share) + directory + "\\" + filename

	def fingerprint_fs(self):
		result = commands.getoutput("%s -c \"ls Users\\*\" //%s/C$ -U %s" % (self.smbclient(), self.smb_host, self.credentials)).split()
		if self.check_errors(result[-1]):
			return "error"
		if "NT_STATUS_OBJECT_NAME_NOT_FOUND" in result:
			return "old"
		else:
			return "new"

	def find_users(self, result):
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
	
	def check_errors(self, result):
		access_error = {
"UNREACHABLE":"Error [%s]: Check to ensure that host is online." % self.smb_host,
"UNSUCCESSFUL":"Error [%s]: Check to ensure that host is online." % self.smb_host,
"TIMEOUT":"Error [%s]: Check to ensure that host is online." % self.smb_host,
}
		for err in access_error:
			if err in result:
				print colors.red + access_error[err] + colors.norm
				self.skip_host = self.smb_host
				return True
		
		if "LOGON_FAIL" in result.split()[-1]:
			print colors.red + "Error [%s]: Invalid credentials. Please correct credentials and try again." % self.smb_host + colors.norm
			exit()
		elif "ACCESS_DENIED" in result.split()[-1]:
			print colors.red + "Error [%s]: Valid credentials, but no access. Try another account." % self.smb_host + colors.norm
		
	def smbclient(self):
		if self.pth:
			return "pth-smbclient"
		else:
			return "smbclient"
	
	def spider_host(self):
		if self.smb_share.lower() == "profile":
			self.smb_share = "C$"
			if self.fingerprint_fs() == "error":
				return
			elif self.fingerprint_fs() == "old":
				folders = ['My Documents','Desktop']
				result = commands.getoutput("%s -c \"ls \\\"Documents and Settings\\*\" //%s/C$ -U %s" % (self.smbclient(), self.smb_host, self.credentials))
				if self.check_errors(result):
					return
				users = self.find_users(result)
				for user in users:
					for folder in folders:
						result = commands.getoutput("%s -c \"recurse;ls \\\"Documents and Settings\\%s\\%s\" //%s/C$ -U %s"\
	 % (self.smbclient(), user, folder, self.smb_host, self.credentials))
						self.parse_result(result)
			else:
				folders = ['Documents','Desktop','Music','Videos','Downloads','Pictures']
				result = commands.getoutput("%s -c \"ls \\\"Users\\*\" //%s/C$ -U %s" % (self.smbclient(), self.smb_host, self.credentials))
				if self.check_errors(result):
					return
				users = self.find_users(result)
				for user in users:
					for folder in folders:
						result = commands.getoutput("%s -c \"recurse;ls \\\"Users\\%s\\%s\" //%s/C$ -U %s" % (self.smbclient(), user, folder, self.smb_host, self.credentials))
						self.parse_result(result)
		else:
			result = commands.getoutput("%s -c \"recurse;ls\" //%s/%s -U %s" % (self.smbclient(), self.smb_host, self.smb_share, self.credentials))
			if self.check_errors(result):
				return
			self.parse_result(result)

if __name__ == "__main__":
	try:
		start(argv[1:])
	except KeyboardInterrupt:
		print "\nExiting. Interrupted by user (ctrl-c)."
		exit()
	except Exception, err:
		print err
		exit()

print "\n-----"
print "Completed in: %.1fs" % (time.time() - start_time)
