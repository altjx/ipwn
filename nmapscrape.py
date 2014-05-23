#!/usr/bin/env python         
#
#  This script simply parses the scans/sS.gnmap and scans/sU.gnmap files    
#  and places any open ports into a text file with the respective IP address  
#  in it. So for example, you should end up with a scans directory    
#  containing files such as 80.txt, 443.txt, 53.tct, etc.       
#  These files will contain the IP addresses that have that port open.    
#                     
#  Author: Alton Johnson                
#  Contact: alton.jx@gmail.com              
#  Updated: 04-06-2013
#

import re,os
from sys import argv

def help():
  print "\n " + "-" * 52
  print " Nmap Parser v1.5, Alton Johnson (alton.jx@gmail.com) "
  print " " + "-" * 52
  print "\n Usage: %s <gnmap file>" % argv[0]
  print
  exit()

def start(argv):
  if len(argv) < 1:
    help()
  if not os.path.exists('open-ports'):
    os.makedirs('open-ports')

  target_file = open(argv[-1])
  targett_file = target_file.read().split('\n')

  for line in targett_file:
    ip_address = line[line.find(":")+2:line.find("(")-1]
    pattern = '([0-9]+)/open/(tcp|udp)/'
    find_pattern = re.findall(pattern, line)

    tcpwrapped_pattern = '([0-9]+)/open/tcp//tcpwrapped'
    find_tcpwrapped = re.findall(tcpwrapped_pattern, line)

    if find_pattern:
      for i in find_pattern:
        if i in find_tcpwrapped:
          continue
        tcp_file = open('open-ports/%s-%s.txt' % (i[0], i[1]),'a')
        tcp_file.write("%s\n" % ip_address)
        tcp_file.close()
  target_file.close()
  print "Done. Check the \"open-ports\" folder for results."

if __name__ == "__main__":
  try:
    start(argv[1:])
  except KeyboardInterrupt:
    print "\nExiting. Closed by user (ctrl-c)."
  except Exception, err:
    print err
