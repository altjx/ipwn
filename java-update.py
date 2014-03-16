#!/usr/bin/python
#
# This script is simply a Java updater for Kali Linux. In my past experiences doing 
# internal penetration tests, I've ran into issues sometimes to where I can't get an application
# to work because it depends on Java. In some cases I couldn't even ignore the outdated warnings.
# So considering I update my Kali Linux installation before every engagement, I decided to find a
# way to automate this process. Obviously, this wasn't hard, but it's very useful.
#
# Author: Alton Johnson (alton.jx@gmail.com)
# Updated: 01/23/2014
#
# Credit: https://forums.kali.org/showthread.php?41-Installing-Java-on-Kali-Linux
#

import commands, urllib2, re, urllib

jdkfolder = "/opt" #change this if necessary, but this is the default folder in Kali
mainurl = "http://www.oracle.com/technetwork/java/javase/downloads/index.html"

class colors:
	blue = "\033[1;34m"
	red = "\033[1;31m"
	normal = "\033[0;00m"

class update:
	def __init__(self):
		self.arch = self.check_arch()
		self.dl_link = ""
		self.link = ""
		self.update_fn = ""
		self.file_size = ""

	def parse_ver(self, version):
		if "http://" in version:
			version = re.findall(r"(?<=jdk-)(.*?)(?=-)", version)
			return str(version[0]).replace("u",".")
		else:
			version = str(version.split()[2]).replace("\"","").replace("0_","").replace("1.","")
			if version[version.find("."):] == ".0":
				version = version[:version.find(".")]
			return version

	def check_arch(self):
		arch = commands.getoutput("uname -a")
		if "amd64" in arch:
			return "64"
		else:
			return "32"

	def check_web(self):
		request = urllib2.Request(mainurl) #connect to java site in mainurl
		
		try:
			response = urllib2.urlopen(request).read()
			secondurl = re.findall(r"/technetwork/java/javase/downloads/jdk(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", response)[0] #grab link for second URL
			
			self.link = urllib.quote_plus("http://www.oracle.com" + secondurl) #encode secondurl for cookie in next request
			
			request2 = urllib2.Request("http://www.oracle.com" + secondurl) #connect to second URL containing packages to download
			response2 = urllib2.urlopen(request2).read()
			x86,x64 = re.findall(r"http://(?:[a-zA-Z]|[0-9]|[$-_@.&+])+(?:linux-x64.tar.gz|linux-i586.tar.gz)", response2) #grab download links for x64 and x86 versions of java
			x86ver = self.parse_ver(x86)
			x64ver = self.parse_ver(x64)

			if self.arch == "32":
				self.dl_link = x86
				self.file_size = re.findall(r"(?<=size\":\")(.*?)(?=\",\"filepath\":\"%s)+" % self.dl_link, response2)[0]
				return x86ver
			else:
				self.dl_link = x64
				self.file_size = re.findall(r"(?<=size\":\")(.*?)(?=\",\"filepath\":\"%s)+" % self.dl_link, response2)[0]
				return x64ver	
		except Exception, err:
			print err
	
	def check_chrome(self):
		print "[*] Checking if Google Chrome exists."
		result = commands.getoutput("ls /opt/google/chrome") #default folder for Google Chrome installations
		if "no such file" in result.lower():
			print "[*] Skipping Java for Google Chrome fix."
		else:
			if "/opt/google/chrome/plugins/libjavaplugin.so" not in commands.getoutput("ls /opt/google/chrome/plugins/libjavaplugin.so"):
				print "[*] Fixing Java work with Google Chrome."
				commands.getoutput("mkdir /opt/google/chrome/plugins")
				commands.getoutput("cd /opt/google/chrome/plugings && ln -s /usr/lib/mozilla/plugins/libjavaplugin.so")
				print "[*] Updated Google Chrome to work with Java."
			else:
				print "[*] Java already configured to work with Google Chrome."
	
	def run_update(self):
		self.update_fn = self.dl_link[self.dl_link.rfind("/")+1:]
		
		if self.arch == "32":
			arch = "i586"
		else:
			arch = "amd64"
		
		print "[*] Old version detected. Performing Java update."
		print "[*] Downloading Java update: %s [size: %s]" %  (self.update_fn, self.file_size)
		
		url = 'https://edelivery.oracle.com' + self.dl_link[self.dl_link.find("otn")-1:]
	
		request = urllib2.Request(url)
		request.add_header("Cookie","s_cc=true; gpw_e24=%s; oraclelicense=accept-securebackup-cookie; " % self.link)
		response = urllib2.urlopen(request)
	
		f = open("%s" % self.update_fn,"w")
		f.write(response.read())
		f.close()
			
		print "[*] Download complete."
		print "[*] Extracting archive."
		commands.getoutput("tar -xzvf %s" % self.update_fn)
		commands.getoutput("rm %s" % self.update_fn)
		print "[*] Extraction complete."
		foldername = commands.getoutput("ls | grep jdk | grep -vi tar")
		commands.getoutput("mv %s /opt/" % foldername)
		print "[*] Updating alternatives."
		commands.getoutput("update-alternatives --install /usr/bin/java java /opt/%s/bin/java 1" % foldername)
		commands.getoutput("update-alternatives --install /usr/bin/javac javac /opt/%s/bin/javac 1" % foldername)
		commands.getoutput("update-alternatives --install /usr/lib/mozilla/plugins/libjavaplugin.so mozilla-javaplugin.so /opt/%s/jre/lib/%s/libnpjp2.so 1" % (arch,foldername))
		commands.getoutput("update-alternatives --set java /opt/%s/bin/java" % foldername)
		commands.getoutput("update-alternatives --set javac /opt/%s/bin/javac" % foldername)
		commands.getoutput("update-alternatives --set mozilla-javaplugin.so /opt/%s/jre/lib/%s/libnpjp2.so" % (foldername, arch))
		print "[*] Alternatives updated."
		self.check_chrome()
		print "[*] Java update complete. Verify with java -version."
	
	def checkupdate(self):
		print colors.blue + "Updating Java." + colors.normal
		current = self.parse_ver(commands.getoutput("java -version")) #check jdk version
		latest = str(self.check_web())
		print "[*] Installed version: " + current
		print "[*] Latest version: " + latest

		if current == latest:
			self.run_update()
#			print "[*] Already up-to-date."
#			self.check_chrome()
#			print
#			exit()
		else:
			self.run_update()
		print

if __name__ == "__main__":
	try:
		start = update()
		start.checkupdate()
	except Exception, err:
		print err; exit()
