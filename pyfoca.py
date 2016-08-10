#!/usr/bin/python
#
#############################################################################################################
#                                                                                                            #
#    This reason behind creating this script is due to the issues                                             #
#  I've experienced in the FOCA application such as with downloading files.                                 # 
#  Additionally, taking screen captures for reports can turn into three and                                 #
#    four captures depending on what metadata was gathered. Therefore, this script                              #
#  can perform some of the same functions as FOCA, and outputs the data into a nicely                        #
#  formatted table.                                                                                          #
#                                                                                                            #
#    For those of you who have already used FOCA in the past to perform metadata                              #
#  extraction, you can export the data you've received (e.g., user, software, printers, folders, etc.)      #
#  into a directory, and have this script                                                                     #
#   to parse those files and print it to a table. This will make the screenshot look much better.            #
#                                                                                                            #
#   Author: Alton Johnson                                                                                     #
#   Contact: alton.jx@gmail.com                                                                              #
#   Updated: 06/06/2013                                                                                       #
#    Version: 1.6                                                                                             #
#                                                                                                            #
#############################################################################################################

import getopt, os, httplib, socket, urllib2, re, time, commands,sys
from sys import argv

curr_time = time.time()
totalFiles = 0
extractedFrom = 0

class colors:
   white = "\033[1;37m"
   normal = "\033[0;00m"
   red = "\033[1;31m"
   blue = "\033[1;34m"
   green = "\033[1;32m"

try:
   import pyPdf
   from pyPdf import PdfFileReader
except Exception, err:
   print colors.red + " Warning: To obtain maximum data from PDF documents, it's highly recommended that you install the pyPDF python module."
   print " pyPDF can be downloaded from http://pybrary.net/pyPdf/" + colors.normal

banner = '\n ' + "-" * 79 + colors.white + '\n  pyfoca v1.6 - Document Metadata Extractor, Alton Johnson (alton.jx@gmail.com)\n ' + colors.normal + "-" * 79 + "\n"
class metaparser:
   def __init__(self, fileName, workingDir, domainName, pageResults,exts,report_dir,del_files,verbose):
      self.fileName = fileName
      self.container = list()
      self.offset = [0]
      self.data_exists = [0]
      self.top_row = [' | File Name','Creation Date','Author','Produced By','Modification Date','Last Saved By']
      self.top_rowf = ['Folders','Operating System(s)','Printers','Software','Users','Emails']
      self.domainName = domainName
      self.workingDir = workingDir
      self.pageResults = pageResults
      self.totalSuccess = 0
      self.exts = exts
      self.report_dir = report_dir
      self.del_files = del_files
      self.verbose = verbose

      if self.report_dir == "":
         while len(self.offset) < len(self.top_row):
            self.offset.append(0)
            self.data_exists.append(0)
      else:
         while len(self.offset) < len(self.top_rowf):
            self.offset.append(0)
            self.data_exists.append(0)
   def processFile(self, curr_file):
      global extractedFrom
      author = '-'
      date = '-'
      generator = '-'
      created = '-'
      producer = '-'
      modded = '-'
      last_saved = '-'
      if ".pdf" in curr_file:
         try:
            pdfFile = PdfFileReader(file(curr_file, 'rb'))
            if pdfFile.getIsEncrypted():
               pdfFile.decrypt('')
            docInfo = pdfFile.getDocumentInfo()
            if not docInfo:
               return
            last_saved = '-'
            #looks at the entire dictionary to parse for information   
            if "/CreationDate" in docInfo:
               data = docInfo["/CreationDate"].strip("D:|'")
               year = data[0:4]
               date = data[4:6] + "/" + data[6:8]
               created_time = data[8:10] + ":" + data[10:12]
               created_time = time.strftime("%I:%M %p", time.strptime(created_time, "%H:%M"))
               created = date + "/" + year + " " + created_time
            if "/Author" in docInfo:
               author = docInfo["/Author"] + " "
               if len(author) <=1:
                  author = "-"
            if "/Producer" in docInfo:
               producer = docInfo["/Producer"].strip("(Windows)")
               producer = re.sub(r'[^\w]', ' ', producer)
               if len(producer) == 0:
                  producer = "-"
               while True:
                  if "  " in producer:
                     producer = producer.replace("  ", " ")
                  else:
                     break
            if "/ModDate" in docInfo:
               data = docInfo["/ModDate"].strip("D:|'")
               year = data[0:4]
               date = data[4:6] + "/" + data[6:8]
               modded_time = data[8:10] + ":" + data[10:12]
               modded_time = time.strftime("%I:%M %p", time.strptime(modded_time, "%H:%M"))
               modded = date + "/" + year + " "  + modded_time

            #strips '/' off file name (if it includes directory name)
            if "/" in curr_file:
               curr_file = curr_file[curr_file.rfind("/")+1:]
            if "\\" in curr_file:
               curr_file = curr_file.replace("\\","")

            #trim information if it's too long
            if len(curr_file) > 15: # trims file name
               curr_file = curr_file[:15] + "..." + curr_file[-13:]
            if len(producer) > 30:
               producer = producer[:20] + " [snipped] "
            if len(author) > 20:
               author = author[:20] + " [snipped] "

            #appends each piece of information. output will show ONLY if at least ONE file has data in a column
            self.container.append([" | " + curr_file,created,author,producer,modded,last_saved])
         except Exception, err:
            return
      else:
         try:
            curr_file = curr_file.replace(" ","\ ").replace("(", "\(").replace(")", "\)")
            output = commands.getoutput('extract -V ' + curr_file).split('\n')
            if "extract: not found" in output[0]:
               print colors.red + " Error: This script requires the extract command."
               print " Please install extract by typing \'apt-get install extract\' in terminal.\n" + colors.normal
               exit()
            for i in output:
               if "creator" in i:
                  author = i[i.find("-")+2:]
                  rem_alphanumeric = re.compile('\W')
                  author = re.sub(rem_alphanumeric, ' ', author)
                  while True:
                     if "  " in author:
                        author = author.replace("  ", " ")
                     elif author[0] == " ":
                        author = author[1:]
                     else:
                        break
               elif "date" in i and "creation" not in i:
                  year = i[i.find('-')+2:(i.find('-')+2)+4]
                  date = i[i.find(year)+5:(i.find(year)+5)+5].replace("-","/")
                  modded_time = i[i.find(":")-2:i.rfind(":")-1]
                  modded_time = time.strftime("%I:%M %p", time.strptime(modded_time, "%H:%M"))
                  modded = date + "/" + year + " " + modded_time
               elif 'generator' in i:
                  producer = i[i.find('-')+2:]
               elif 'creation' in i:
                  year = i[i.find('-')+2:(i.find('-')+2)+4]
                  date = i[i.find(year)+5:(i.find(year)+5)+5].replace("-","/")
                  created_time = i[i.find(":")-2:i.rfind(":")-1]
                  created_time = time.strftime("%I:%M %p", time.strptime(created_time, "%H:%M"))
                  created = date + "/" + year + " " + created_time
               elif 'last saved' in i:
                  last_saved = i[i.find('-')+2:]
            if "/" in curr_file:
               curr_file = curr_file[curr_file.rfind("/")+1:]
            if "\\" in curr_file:
               curr_file = curr_file.replace("\\","")
            #trim the file name if it's longer than 15 characters
            if len(curr_file) > 15:
               curr_file = curr_file[:9] + "..." + curr_file[-13:]
            if author != "-" or date != "-" or generator != "-" or created != "-" or producer != "-" or modded != "-" or last_saved != "-":   
               self.container.append([" | " + curr_file,created,author,producer,modded,last_saved])
         except Exception, err:
            if "command not found" in str(err):
               print colors.red + "\n Error: This program requires the \"extract\" command, and it cannot be found."
               print " Please install extract by using 'apt-get install extract' from terminal." + colors.normal
               exit()
#            print colors.red + curr_file + " --------------- " + str(err) + colors.normal
            return
      extractedFrom = len(self.container)
   
   def parseReport(self, folders_file, OS_file, printers_file, software_file, users_file, emails_file):
      supported_options = [folders_file, OS_file, printers_file, software_file, users_file, emails_file]
      #grab variable with most lines -- this determines how many times we append to container
      max_lines = 0
      for i in supported_options:
         if len(i) > max_lines:
            max_lines = len(i)
      for ln in range(0,max_lines):
         if ln < len(folders_file):
            add_folder = folders_file[ln].replace("%20", " ")
         else:
            add_folder = "-"
         if ln < len(OS_file):
            add_os = OS_file[ln]
         else:
            add_os = "-"
         if ln < len(printers_file):
            add_printer = printers_file[ln]
         else:
            add_printer = "-"
         if ln < len(software_file):
            add_software = software_file[ln]
         else:
            add_software = "-"
         if ln < len(users_file):
            add_user = users_file[ln]
         else:
            add_user = "-"
         if ln < len(emails_file):
            add_email = emails_file[ln]
         else:
            add_email = "-"
         self.container.append([add_folder, add_os, add_printer, add_software, add_user, add_email])
            
   def grabMeta(self):
      print banner
      global totalFiles
      foundFile = False
      files = []
      # FOCA file types
      folders_file = []
      OS_file = []
      printers_file = []
      software_file = []
      users_file = []
      emails_file = []
      self.foca_filetypes = []
      if self.report_dir:
         if self.report_dir == ".":
            self.report_dir = "./"
         self.report_dir = self.report_dir.replace(" ", "\ ")
         print " Reading files..."
         for dirname, dirnames, filenames in os.walk(self.report_dir):
            for z in filenames:
               try:
                  new_open = open(dirname + z)
                  file_contents = new_open.read().replace("\r", "").replace("\t","").split('\n')
                  while '' in file_contents:
                     file_contents.remove('')
                  if "Metadata" in file_contents[0]:
                     self.foca_files = file_contents[1][file_contents[1].find("(")+1:file_contents[1].find("/")]
                     for ext in file_contents:
                        if ext != "":
                           if "." == file_contents[file_contents.index(ext)][0]:
                              self.foca_filetypes.append(file_contents[file_contents.index(ext)])
                  elif "folders" in file_contents[0]:
                     for i in file_contents[1:]:
                        if i not in folders_file:
                           folders_file.append(i)
                           folders_file.sort()
                  elif "operating systems" in file_contents[0]:
                     for a in file_contents[1:]:
                        if a not in OS_file:
                           OS_file.append(a)
                           OS_file.sort()
                  elif "printers" in file_contents[0]:
                     for b in file_contents[1:]:
                        if b not in printers_file:
                           printers_file.append(b)
                           printers_file.sort()
                  elif "software" in file_contents[0]:
                     for c in file_contents[1:]:
                        if c not in software_file:
                           software_file.append(c)
                           software_file.sort()
                  elif "users" in file_contents[0]:
                     for d in file_contents[1:]:
                        if d not in users_file:
                           users_file.append(d)
                           users_file.sort()
                  elif "emails" in file_contents[0]:
                     for e in file_contents[1:]:
                        if e not in emails_file:
                           emails_file.append(e)
                           emails_file.sort()
                  new_open.close()
               except Exception, err:
#                  print err
                  pass
         if len(emails_file) == 0 and len(users_file) == 0 and len(software_file) == 0 and len(printers_file) == 0 and len(OS_file) == 0 and len(folders_file) == 0:
            print colors.red + " Error: There are no supported files within the specified directory.\n" + colors.normal
            exit()
         self.parseReport(folders_file, OS_file, printers_file, software_file, users_file, emails_file)
      elif self.workingDir != "":
         if self.workingDir == ".":
            self.workingDir = "./"
         for dirname, dirnames, filenames in os.walk(self.workingDir):
            if len(filenames) == 0:
               print colors.red + " Error: There are no files within the specified directory.\n" + colors.normal
               exit()
            for i in filenames:
               for ext in self.exts:
                  if ext in i:
                     foundFile = True
                     curr_file = dirname + i
                     curr_file = curr_file.replace(" ","\ ").replace("(", "\(").replace(")", "\)")
                     self.processFile(curr_file)
                     totalFiles += 1
         if foundFile == False:
            print colors.red + "\n Error: Sorry, no supported files were located within the specified directory. Please try another file or directory.\n" + colors.normal
            exit()
      elif self.fileName != "":
         self.fileName = self.fileName.replace(" ", "\ ").replace("(", "\(").replace(")", "\)")
         self.processFile(self.fileName)
         totalFiles += 1
      elif self.domainName != "":
         print " Domain: %s" % self.domainName
         print " Attempting to gather links from google searches..."
         conn = httplib.HTTPConnection('www.google.com')
         total_count = 0
         for e in self.exts:
            count = 0
            while count < self.pageResults:
               conn.request("GET","/search?q=site:" + self.domainName + "+ext:" + e + "&start=%s0" % str(count))
               r1 = conn.getresponse()
               contents = r1.read()
               new_pattern = "(?P<url>https?://[^:]+\.%s)" % e
               new_pattern = re.findall(new_pattern,contents)
               for n in new_pattern:
                  if n not in files:
                     files.append(n)
               count += 1
               total_count += 1
               totalFiles = len(files)
         if len(files) == 0:
            print " No files were located within Google based on the extension(s) and domain you provided.\n"
            exit()
         print " Discovered " + str(len(files)) + " files from " + str(total_count) + " total google searches..."
         #create pyfoca-downloads directory if it doesn't exist
         if not os.path.exists('pyfoca-downloads'):
            print " Creating pyfoca-downloads folder..."
            os.makedirs('pyfoca-downloads')
         
         #set max amount of spaces for pdf file names
         spaces = 0
         for item in files:
            item = item[item.rfind("/")+1:]
            if len(item) > 10:
               short_file = item[:10] + "..." + item[-10:]
            else:
               short_file = item
            if len(short_file) > spaces:
               spaces = len(short_file) + 3
         
         print " Attempting to download files..."
         if self.verbose == False:
            print " Please wait..."
         #download each file that we added to the 'files' variable
         print " -------------------------------"
         for f in files:
            if "..." in f:
               del files[files.index(f)]
               continue
            pdf_name = f[f.rfind("/")+1:]
            print f
            try:
               response = urllib2.urlopen(f)
               source = response.read()
               write_file = open('pyfoca-downloads/%s' % pdf_name, 'w')
               write_file.write(source)
               write_file.close()
               name = pdf_name.replace("(", "\(").replace(")", "\)")
               filesize = commands.getoutput('ls -lh pyfoca-downloads/%s | awk \'{print $5}\'' % name) 
               if len(pdf_name) > 10:
                  short_file = pdf_name[:10] + "..." + pdf_name[-10:]
               else:
                  short_file = pdf_name
               if self.verbose == True:
                       print; print colors.blue + " [+] " + short_file, "-" * (spaces-len(short_file)), "success", "[%s of %s] [size: %s]" % (str(files.index(f)+1),str(len(files)), filesize) + colors.normal
            except Exception, err:
               if self.verbose == True:
                       print colors.red + " [-] " + short_file, "-" * (spaces-len(short_file)), "fail", "[%s of %s]" % (str(files.index(f)+1),str(len(files))) + colors.normal
               totalFiles -= 1
               continue
         print
         for e in files:
            pdf_name = e[e.rfind("/")+1:]
            self.processFile('pyfoca-downloads/%s' % pdf_name)
   
   def printMeta(self):
      #check to see if user requested FOCA file parsing; if so, print statistics first
      if self.report_dir != "":
         print " User specified option for \"FOCA\" text file parsing. Printing details..."
         print " ----------------------------------------------------------------------"
         for i in self.foca_filetypes:
            print " Total " + i[:i.find("(")-1] + " files: " + i[i.find("(")+1:i.find(")")]
         print
      #for self.data_exists, add 1 to any column with data, and 0 to column without data
      for i in self.container:
         for num in range(0,len(self.top_row)):
            if i[num] != "-":
               self.data_exists[num] = 1
      #check self.data_exists for empty columns, and remove them.
      restart_check = 1
      while restart_check == 1:
         restart_check = 0
         for data in self.data_exists:
            if data == 0:
               if self.report_dir == "":
                  del self.top_row[self.data_exists.index(data)]
               else:
                  del self.top_rowf[self.data_exists.index(data)]
               del self.offset[self.data_exists.index(data)]
               for citem in self.container:
                  del citem[self.data_exists.index(data)]
               del self.data_exists[self.data_exists.index(0)]
               restart_check = 1

      totalFiles = len(self.container)
            
      #states that no data exists if nothing really does. this prevents the output of self.top_row from showing with nothing in the table.
      if len(self.container) == 0:
         print colors.red + " Either no data was found on Google, or there were issues opening the documents." 
         print colors.red + " Ensure that the 'extract' tool is installed by running 'sudo apt-get install extract'\n" + colors.normal 
         exit()

      #goes through each item in container and make sure max spaces are correct
      for item in self.container:
         for num in range(0,len(item)):
            if "|" not in item[0]:
               item[0] = " | " + item[0]
            if len(item[num]) > self.offset[num]:
               self.offset[num] = len(item[num]) + 1
      if self.report_dir == "":
         for x in range(0,len(self.offset)):
            if len(self.top_row[x]) > self.offset[x]:
               self.offset[x] = len(self.top_row[x]) + 1
      else:
         for x in range(0,len(self.offset)):
            if "|" not in self.top_rowf[0]:
               self.top_rowf[0] = " | " + self.top_rowf[0]
            if len(self.top_rowf[x]) > self.offset[x]:
               self.offset[x] = len(self.top_rowf[x]) + 1
         
      #prints the top row (formatted according to the # of spaces set from above code)
      if self.report_dir == "":
         top_bottom_lines = " " + "-" * (sum(self.offset) + len(self.top_row) + len(self.top_row)-2)
         print top_bottom_lines
         for top in self.top_row:
            print top + " " * (self.offset[self.top_row.index(top)] - len(top)) + "|",
         print "\n" + top_bottom_lines
      else:
         top_bottom_lines = " " + "-" * (sum(self.offset) + len(self.top_rowf) + len(self.top_rowf)-2)
         print top_bottom_lines
         for top in self.top_rowf:
            print top + " " * (self.offset[self.top_rowf.index(top)] - len(top)) + "|",
         print "\n" + top_bottom_lines

      #prints the metadata details for each file
      for item in self.container:
         for num in range(0,len(item)):
            print item[num] + " " * (self.offset[num] - len(item[num])) + "|",
         if item == self.container[-1]:
            print "\n" + top_bottom_lines + "\n"
         else:
            print

      print " " + "--" * 5
      if self.report_dir == "":
         if self.del_files:
            print " Deleting pyfoca-downloads folder..."
            commands.getoutput('rm pyfoca-downloads/ -rf')
         print " Extracted data from %s file(s)." % str(totalFiles)
      else:
         print " Extracted data from %s file(s)." % self.foca_files
      
def help():
   print banner
   print " Usage: ./pyfoca.py <OPTIONS> \n"
   print colors.green + " Domain options:\n" + colors.normal
   print "\t -d <domain>\t\tHarvests all documents from a domain (saves to pyfoca-downloads/). \n\t\t\t\tAfterwards, extract metadata."
   print colors.green + "\n Parse file/dir:\n" + colors.normal
   print "\t -f <file>\t\tExtracts metadata specifically from one file. (Cannot use with '-d')"
   print "\t -w <dir>\t\tExtracts metadata from files within specified directory. (Cannot use with '-d')"
   print colors.green + "\n Foca Export Parsing:\n" + colors.normal
   print "\t -r <directory>\t\tParses data exported from FOCA. Provide directory containing exported files."
   print colors.green + "\n Misc:\n" + colors.normal   
   print "\t -x\t\t\tAfter parsing metadata, delete files downloaded from the domain."
   print "\t -e <pdf|doc|xls|all>\tSearch based on provided extension(s). Separate with comma. (Default is all.) "
   print "\t -p <number>\t\tSearches x amount of google pages (per extension). (Default is 2.)"
   print "\t -t <secs>\t\tSets timeout value. (Default is 5.)"
   print "\t -v\t\t\tPrints status messages for files that are downloaded."
   print "\n Supported extensions are: .pdf, .doc, .docx, .xls, .xlsx, and .ppt"
   print " Example: ./pyfoca.py -d www.domain.com -e pdf,doc -p 3\n"
   exit()
      
def main(argv):
   if len(argv) < 2:
      help()
   try:
      opts, args = getopt.getopt(argv, 'vxf:d:r:w:p:t:e:')
   except getopt.GetoptError:
      help()

   fileName = ''
   workingDir = ''
   domainName = ''
   pageResults = 2
   verbose = False
   socket.setdefaulttimeout(5)
   exts = ['all']
   supported_exts = ['all','pdf','doc','docx','xls','xlsx','ppt']
   report_dir = ''
   del_files = False
   for opt, arg in opts:
      if opt == "-f":
         fileName = arg
      elif opt == "-w":
         workingDir = arg
      elif opt == "-d":
         domainName = arg
      elif opt == "-p":
         pageResults = int(arg)   
      elif opt == "-t":
         socket.setdefaulttimeout(float(arg))
      elif opt == "-e":
         exts = arg.split(',')
      elif opt == "-r":
         report_dir = arg
      elif opt == "-x":
         del_files = True
      elif opt == "-v":
         verbose = True

   #checks for errors before submitting for processing
   if domainName != "" and (fileName != "" or workingDir != ""):
      print colors.red + "\n Error: You have provided a domain name, yet you also have provided a file and/or working directory."
      print " You can only use the domain name option by itself." + colors.normal
      help()
   if fileName != "" and (workingDir != "" or domainName != ""):
      print colors.red + "\n Error: You have provided a file name, yet you also have provided a working directory and/or domain name."
      print " You can only use the file name option by itself." + colors.normal
      help()
   if workingDir != "" and (fileName != "" or domainName != ""):
      print colors.red + "\n Error: You have provided a working directory, yet you have also provided a file name and/or domain name."
      print " You can only use the working directory option by itself." + colors.normal
      help()
   if report_dir and (workingDir != "" or fileName != "" or domainName != ""):
      print colors.red + "\n Error: You've enabled report mode. Therefore, you can only provide a directory with files exported from FOCA."
      print " It appears that you've enabled report mode, along with some other options (e.g., directory, file name, domain name, etc.)."
      print " Please check your options and try again." + colors.normal
      help()
   if del_files == True and domainName == "":
      print colors.red + "\n Error: You've provided the '-x' option when you have no domain name specified. Please check your options." + colors.normal
      help()
   for i in exts:
      if i.lower() not in supported_exts:
         print colors.red + "\n Error: You've provided an unsupported extension. Please try again." + colors.normal
         help()
   if fileName != "":
      try:
         with open(fileName) as f: pass
      except IOError, err:
         print colors.red + "\n Error: " + str(err) + "\n"
         exit()
      if " " in fileName:
         fileName = fileName.replace(" ","\ ")
   if "all" in exts:
      exts = supported_exts[1:]
   startparse = metaparser(fileName, workingDir, domainName, pageResults,exts,report_dir,del_files,verbose)
   startparse.grabMeta()
   startparse.printMeta()

if __name__ == "__main__":
   try:
      main(argv[1:])
   except KeyboardInterrupt:
      print "\n Exiting. Interrupted by user (ctrl-c)."
      if os.path.exists('pyfoca-downloads'):
         del_folder = raw_input(" Remove pyfoca-downloads folder? [Y/n] ")
         if "n" not in del_folder:
            commands.getoutput('rm pyfoca-downloads/ -r')
      print 
      exit()

print " Completed in: %.1fs\n" % (time.time() - curr_time)
