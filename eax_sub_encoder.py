#!/usr/bin/python
import struct, getopt
from sys import argv

# provide the characters that are allowed within the exploit
good_chars = [ 
"02","03","04","05","06","07","08","09","31","32","33","34","35","36",
"37","38","39","3b","3c","3d","3e","41","42","43","44","45","46","47","48","49","4a",
"4b","4c","4d","4e","4f","50","51","52","53","54","55","56","57","58","59","5a","5b",
"5c","5d","5e","5f","60","61","62","63","64","65","66","67","68","69","6a","6b","6c",
"6d","6e","6f","70","71","72","73","74","75","76","77","78","79","7a","7b","7c","7d",
"7e","7f"
]

frow = [0,0,0,0]
srow = [0,0,0,0]
trow = [0,0,0,0]
forow = [0,0,0,0]

def begin(input_row):
	clean_rows()
	code = input_row.replace("\\x","").lower()
	code = "0x" + code[-2:] + code[-4:-2] + code[-6:-4] + code[-8:-6]
	end_sum = hex(int("0xFFFFFFFF", 16) - int(code, 16) + 1)[2:-1]
	print "Searching for a match for: " + code #+ " (0xFFFFFFFF - %s + 1 = %s)" % (code, end_sum)
	while len(end_sum) < 8:
		end_sum = "0" + end_sum
	end_sum = "0x" + end_sum
	step2(end_sum)

def clean_rows():
	global frow, srow, trow, forow
	frow = [0,0,0,0]
	srow = [0,0,0,0]
	trow = [0,0,0,0]
	forow = [0,0,0,0]

def step2(end_sum):
	complete = [0,0,0,0]
	first = "0x" + end_sum[-2:].replace("00","ff")
	second = "0x" + end_sum[-4:-2].replace("00","ff")
	third = "0x" + end_sum[-6:-4].replace("00","ff")
	fourth = "0x" + end_sum[-8:-6].replace("00","ff")
	depth = 2
	for a in good_chars:
		for b in good_chars:
			pwnsauce = hex(int(a, 16) + int(b, 16))[2:]
			if len(pwnsauce) == 1:
				pwnsauce = "0" + pwnsauce
			pwnsauce = "0x" + pwnsauce
			if pwnsauce == first and complete[0] == 0:
#				print "Found first"
#				print "%s + %s = %s" % (hex(int(a, 16)),hex(int(b, 16)),first)
				complete[0] = 1
				frow[3] = a
				srow[3] = b
				
			if pwnsauce == second and complete[1] == 0:
#				print "Found second"
#				print "%s + %s = %s" % (hex(int(a, 16)),hex(int(b, 16)),second)
				complete[1] = 1
				frow[2] = a
				srow[2] = b
		
			if pwnsauce == third and complete[2] == 0:
#				print "Found third"
#				print "%s + %s = %s" % (hex(int(a, 16)),hex(int(b, 16)),third)
				complete[2] = 1
				frow[1] = a
				srow[1] = b

			if pwnsauce == fourth and complete[3] == 0:
#				print "Found fourth"
#				print "%s + %s = %s" % (hex(int(a, 16)),hex(int(b, 16)),fourth)
				complete[3] = 1
				frow[0] = a
				srow[0] = b

	if sum(complete) != 4:
		complete = [0,0,0,0]
		depth = 3
		for x in good_chars:
			for y in good_chars:
				for z in good_chars:
					pwnsauce1 = hex(int(x, 16) + int(y, 16) + int(z, 16))[2:]
					if len(pwnsauce1) == 1:
						pwnsauce1 = "0" + pwnsauce1
					pwnsauce1 = "0x" + pwnsauce1
					if pwnsauce1 == first and complete[0] == 0:
#						print "Found first"
#						print "%s + %s + %s = %s" % (hex(int(x, 16)),hex(int(y, 16)),hex(int(z, 16)), first)
						complete[0] = 1
						frow[3] = x
						srow[3] = y
						trow[3] = z
						
					if pwnsauce1 == second and complete[1] == 0:
#						print "Found second"
#						print "%s + %s + %s = %s" % (hex(int(x, 16)),hex(int(y, 16)),hex(int(z, 16)), second)
						complete[1] = 1
						frow[2] = x
						srow[2] = y
						trow[2] = z
				
					if pwnsauce1 == third and complete[2] == 0:
#						print "Found third"
#						print "%s + %s + %s = %s" % (hex(int(x, 16)),hex(int(y, 16)),hex(int(z, 16)), third)
						complete[2] = 1
						frow[1] = x
						srow[1] = y
						trow[1] = z

					if pwnsauce1 == fourth and complete[3] == 0:
#						print "Found fourth"
#						print "%s + %s + %s = %s" % (hex(int(x, 16)),hex(int(y, 16)),hex(int(z, 16)), fourth)
						complete[3] = 1
						frow[0] = x
						srow[0] = y
						trow[0] = z
	
	if sum(complete) != 4:
		complete = [0,0,0,0]
		depth = 4
		for q in good_chars:
			for w in good_chars:
				for e in good_chars:
					for r in good_chars:
						pwnsauce2 = hex(int(q, 16) + int(w, 16) + int(e, 16) + int(r, 16))[2:]
						if len(pwnsauce2) == 1:
							pwnsauce2 = "0" + pwnsauce2
						pwnsauce2 = "0x" + pwnsauce2
						if pwnsauce2 == first and complete[0] == 0:
#						print "Found first"
#						print "%s + %s + %s = %s" % (hex(int(x, 16)),hex(int(y, 16)),hex(int(z, 16)), first)
							complete[0] = 1
							frow[3] = q
							srow[3] = w
							trow[3] = e
							forow[3] = r
							
						if pwnsauce2 == second and complete[1] == 0:
#						print "Found second"
#						print "%s + %s + %s = %s" % (hex(int(x, 16)),hex(int(y, 16)),hex(int(z, 16)), second)
							complete[1] = 1
							frow[2] = q
							srow[2] = w
							trow[2] = e
							forow[2] = r
					
						if pwnsauce2 == third and complete[2] == 0:
#						print "Found third"
#						print "%s + %s + %s = %s" % (hex(int(x, 16)),hex(int(y, 16)),hex(int(z, 16)), third)
							complete[2] = 1
							frow[1] = q
							srow[1] = w
							trow[1] = e
							forow[1] = r

						if pwnsauce2 == fourth and complete[3] == 0:
#						print "Found fourth"
#						print "%s + %s + %s = %s" % (hex(int(x, 16)),hex(int(y, 16)),hex(int(z, 16)), fourth)
							complete[3] = 1
							frow[0] = q
							srow[0] = w
							trow[0] = e
							forow[0] = r

	if sum(complete) != 4:
		print "Using the allowable characters, no four combinations can be added to get the provided mem address."
		print "Sorry! Perhaps five or more combinations can be added, but the script doesn't go that far.\n"
	else:
		completed_math(depth)

def completed_math(depth):
	print
	print "\\x25\\x4a\\x4d\\x4e\\x55\tand eax,554e4D4a"
	print "\\x25\\x35\\x32\\x31\\x2a\tand eax,2a313235"
	row1 = frow[0] + frow[1] + frow[2] + frow[3]
	row2 = srow[0] + srow[1] + srow[2] + srow[3]
	row3 = trow[0] + trow[1] + trow[2] + trow[3]
	row4 = forow[0] + forow[1] + forow[2] + forow[3]
	if depth >= 2:
		print "\\x2d\\x%s\\x%s\\x%s\\x%s\tsub eax,%s" % (frow[3], frow[2], frow[1], frow[0], row1)
		print "\\x2d\\x%s\\x%s\\x%s\\x%s\tsub eax,%s" % (srow[3], srow[2], srow[1], srow[0], row2)
	if depth >= 3:
		print "\\x2d\\x%s\\x%s\\x%s\\x%s\tsub eax,%s" % (trow[3], trow[2], trow[1], trow[0], row3)
	if depth >= 4:
		print "\\x2d\\x%s\\x%s\\x%s\\x%s\tsub eax,%s" % (forow[3], forow[2], forow[1], forow[0], row4)
	print "\\x50\t\t\tpush eax" 
	print

class colors:
	red = "\033[1;31m"
	normal = "\033[0;00m"
	blue = "\033[1;34m"

banner = "\n " + "-" * 58 + "\n " + " EAX SUB Encoder v1.0, Alton Johnson (alton.jx@gmail.com)\n " + "-" * 58 + "\n "

def help():
	print banner
	print " Usage: %s <OPTIONS>" % argv[0]
	print "\n -s <4-byte memory address>\tCalculate EAX for only four bytes."
	print " -f <file>\t\t\tYou can import a file, containing four bytes on each line."
	print "\n Usage example: %s -s \"\\xdd\\xcc\\xbb\\xaa\"" % argv[0]
	print " Usage example: %s -f test.txt" % argv[0]
	print

def main(argv):
	if len(argv) < 1:
		help()
		exit()
	try:
		opts, args = getopt.getopt(argv, "h:f:s:")
	except getopt.GetoptError, err:
		print colors.red + "\n Error: %s" % err + colors.normal
		help()

	for opt, arg in opts:
		if opt == "-s":
			begin(arg)
		elif opt == "-f":
			try:
				row = open(arg).read().split()[::-1]
				for i in row:
					begin(i)
			except Exception, err:
				print colors.red + "\n Error: %s\n" % err + colors.normal
				exit()
	
if __name__ == "__main__":
	try:
		main(argv[1:])
	except KeyboardInterrupt:
		print "\nExiting. Closed by user (ctrl-c)."
		exit()
