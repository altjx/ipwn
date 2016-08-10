#!/usr/bin/env python
#
# This program automates the process of auditing web servers on internal
# penetration tests. As opposed to opening numerous sites manually to view what they're
# hosting, you can use this script to grab the HTTP titles from every page.
# After you're done, you can easily prioritize what you want to start looking 
# at first starting from a nice, formatted list of IPs and page titles
#
# Author: Alton Johnson (alton.jx@gmail.com)
# Updated: 01/23/2014
#
# Note: Many thanks to Victor M. and Mark T. for assistance
#
# Future consideration: HTTP Put Method Detection [completed]; auto-update attempt via wiki
#

from sys import argv
import urllib2
import getopt
import time
import httplib
import socket

container = list()
spaces = [0,0,0]

# Defines the colors which can be called later. Can identify colors using echo -e "\033[x;nnm"
# from terminal. x = 1 (bold) or 0 (non-bold). n = numbers from 01 = 99 (must be two digits). 
class colors:
	lightblue = '\033[1;36m'
	blue = '\033[1;34m'
	normal = '\033[0;00m'
	red = '\033[1;31m'
	white = '\033[1;37m'

# Prints out the help function, which guides users how to use the script.
def help():
	print "\n", "-" * 78
	print colors.white, "iWebAudit v1.5 - Web Page Title Analyzer, Alton Johnson (alton.jx@gmail.com) ", colors.normal
	print "-" * 78, "\n"
	print " Usage: iWebAudit -f <file> -o <output_file> -v -h -t 5\n"
	print "\t-f <file>\tSupports list of IPs and/or http[s]:// formatted IPs."
	print "\t-o <file>\tOutputs the results to a file of your choice."
	print "\t-h \t\tEnables HTTP PUT Method Discovery. (optional)"
	print "\t-t <secs>\tSets default timeout. Default is 5. (optional)"
	print "\t-v \t\tDisplays details as script runs. (optional)\n"

# Takes the response (html source) from http_request and parses it for title
def FindTitle(source):
	source = source.replace("\n", "").replace("\r", "").replace("\t", "").split("<")
	for i in range(0,len(source)):
		if 'title>' in source[i].lower(): 
			if not (source[i][source[i].lower().find("title>")+6:]):
				return "-"
			else:
				return source[i][source[i].lower().find('title>')+6:]
			break
		elif 'title ' in source[i].lower(): # alt for code such as <title ID="test>".
			for n in range(0,30):
				parsed_title = source[i][source[i].lower().find('title')+n:]
				if not ">" in parsed_title:
					return parsed_title
					break
	return "-"

def http_method(url):
	if 'http://' in url:
		url = url[url.find("http://")+7:]
	elif 'https://' in url:
		url = url[url.find("https://")+8:] 
	connection = httplib.HTTPConnection(url)
	connection.request('OPTIONS','/')
	response = connection.getresponse()
	http_parse = response.getheader('allow')
	if http_parse:
		if "PUT" in http_parse:
			return "PUT"
		else:
			return "-"
	else:
		return "-"

# Checks to see what format the current line is in and connects accordingly
def http_request(request):
	if 'http://' in request:
		request = urllib2.Request(request) # construct rqst
	elif 'https://' in request:
		request = urllib2.Request(request) # construct rqst
	else:
		request = urllib2.Request('http://%s' %request) # construct rqst
	
	request.add_header('User-Agent','Lewlsauce, Inc.')
	try:
		response = urllib2.urlopen(request)
		return response.read()
	except urllib2.URLError, err:
		return "-"	
	except urllib2.HTTPError, err:
		return "-"
	except Exception, err:
		return "-"

# Takes argv (everything provided after the program name) and passes it to this function.
def start(argv):
	if len(argv) < 2:
		help()
		exit()
	try:
		opts, args = getopt.getopt(argv, 'vhf:o:t:') #colons are needed if option is req'd.
	except getopt.GetoptError:
		help()
		exit()
	# Define default variables so script doesn't fail if "if" statements aren't true.
	use_https = False
	output_file = ""
	verbose = False
	length = 0
	httpmethod = False
	cur_time = time.time()
	timeout = 5
	socket.setdefaulttimeout(timeout)
	# Check which options and agruments have been provided to CLI.
	for opt, arg in opts:
		if opt == '-f':
			http_file = open(arg)
		elif opt == '-o':
			output_file = open(arg, 'w')
		elif opt == '-v':
			verbose = True
		elif opt == '-h':
			httpmethod = True
		elif opt == '-t':
			socket.setdefaulttimeout(float(arg))
	file_contents = http_file.read().split() # Converted to list; assigned to variable.

	# setting the space for the first column; used for verbose mode
	for line in file_contents:
		if len(line) > spaces[0]:
			spaces[0] = len(line)
	spaces[0] += 3

	# grabbing titles, adding to container, and outputting (if verbose is enabled)
	for site in file_contents:
		try:
			title = FindTitle(http_request(site)) # pass http_request data to FindTitle function
			if httpmethod:
				method = http_method(site)
			else:
				method = False
			container.append([site,method,title])
			if output_file != "":
				if method:
					output_file.write("%s%s%s%s\n" % (site," " * (spaces[0]-len(site)),method + " " * (6 - len(method)),title))
				else:
					output_file.write("%s%s%s\n" % (site, " " * (spaces[0]-len(site)),title))
			if verbose:
				output(verbose,site,method,title)
		except Exception, err:
			print err

	#adds the necessary space lengths for each field
	if method:
		for i in container:
			i[1] = i[1] + "  "
			for num in range(0,len(spaces)):
				if len(i[num]) > spaces[num]:
					spaces[num] = len(i[num])
	else:
		for i in container:
			i[1] = ''
			for num in range(0,len(spaces)):
				if len(i[num]) > spaces[num]:
					spaces[num] = len(i[num])
	if not verbose:
		output(verbose)
	print "-" * 5
	print "Completed in: %.1fs" % (time.time() - cur_time)

# this determines whether to print status line after line (verbose), or wait until file is finished
def output(verbose,site='',httpmethod='',title=''):
	if not verbose:
		if not httpmethod:
			httpmethod = '  '
		for i in container:
			for num in range(0,len(i)):
					print i[num] + " " * (spaces[num]-len(i[num])),
			print 
	else:
		site = site + " " * (spaces[0]-len(site))
		title = " " + title
		if httpmethod:
			httpmethod =  httpmethod + " " * (5 - len(httpmethod))
			print site + httpmethod + title
		else:
			print site + title
	
if __name__ == "__main__":
	try:
		start(argv[1:])
	except KeyboardInterrupt:
		print "\nClosed by user. Now exiting... (ctrl+c)"
		exit()
