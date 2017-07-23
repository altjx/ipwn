#!/usr/bin/python
import re
from sys import argv

class colors:
  lightblue = "\033[1;36m"
  blue = "\033[1;34m"
  normal = "\033[0;00m"
  red = "\033[1;31m"
  white = "\033[1;37m"
  green = "\033[1;32m"

try:
  from prettytable import *
except Exception:
  print colors.red + " Error: The 'prettytables' python module isn't installed."
  print " Download prettytables and then run the script again. Link: https://code.google.com/p/prettytable/"
  exit()

banner = "\n " + "-" * 72 + "\n " + colors.white + " nmapparse 1.0 - Nmap Output Parser, Alton Johnson (alton.jx@gmail.com)\n " + colors.normal + "-" * 72 + "\n "

def help():
  print banner
  print " Usage: %s results.gnmap" % argv[0]
  print "\n Note: This script must point to a grepable output file from nmap to work properly.\n"
  exit()


def start(argv):
  table = PrettyTable(["IP Address","Port","Service","Version"])
  if len(argv) == 0:
    help()
  contents = sorted(open(argv[0]).read().split('\n'))
  data = []

  class colors:
    blue = "\033[1;34m"
    normal = "\033[0;00m"

  for item in contents:
    ip_addr = item[item.find(":")+2:item.find("(")-1]
    info = re.findall("(?<=Ports: )(.*?)(?=Ignored)", item)
    if len(info) == 0:
      info = re.findall("(?<=Ports: )(.*?)(?=Seq Index)", item)
    if len(info) == 0:
      info = re.findall("(?<=Ports: )(.*?)(?=$)", item)
    if len(info) != 0:
      for i in info:
        result = i.split(',')
        for x in result:
          port = re.findall("([0-9]+/open/.*?)/", x)
          if "[]" in str(port):
            continue
          port = port[0].replace("/open", "")
          service = re.findall("(?<=//)(.*?)(?=/)", x)[0]
          version = x.split("/")[-2]
          if len(version) > 40:
            version = version[:40]
          if len(version) == 0:
            version = "-"
          table.add_row([ip_addr, port, service, version])
  print table


try:
  start(argv[1:])
except Exception, err:
  print err
