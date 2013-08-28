Here you will find some tools that I've created which may help you out on your next pentest. Nothing exciting as of yet, but useful. :)
Unfortunately, I was too lazy to capture screenshots while using these tools, so I've just uploaded the help menu for the ones I don't have live examples for.

iSMTP - This is a script that I've made while pentesting at a previous company I worked for. Many tools will simply either do SMTP user enumeration, relay testing, or internal spoofing. I've never found any tool that did all three with flexible options. A former coworker of mine (Josh Stone) initially wrote a Ruby SMTP tester that initially made me jump on this.
	- Help menu: https://dl.dropboxusercontent.com/u/2526790/iSMTP/iSMTP.png
	- Usage screenshot #1 (user enumeration): https://dl.dropboxusercontent.com/u/2526790/iSMTP/SMTP%20User%20Enumeration.png

iWebAudit - When you're on an internal pentest, many times you run across numerous printers and other useless web-based applications. Inspired by a former coworker of mine (Victor Mata), I've decided to write my own tool to simply pull back the titles from these pages. I found it to be significantly helpful with helping me more easily prioritize the web applications I wanted to target. Check out the help menu here: https://dl.dropboxusercontent.com/u/2526790/iWebAudit.png

pyFoca - Inspired by the Windows FOCA application, I've decided to recreate this into a python version. One minor issue I've found while using the FOCA application for Information Gathering is that I've have to take multiple screenshots to represent the Users, Folders, etc. that I've identified with the tool. Therefore, I've written a python version which displays all of its findings into a nice table. Check out the help menu here: https://dl.dropboxusercontent.com/u/2526790/pyfoca.png

smbspider - Inspired by a similar tool written by Josh Stone, I wanted to basically rewrite my own version of his tool so that I could add/remove features according to my preference. This is a script that you can use during post-exploitation to identify sensitive/confidential data laying around on users' workstations. You've probably already won in the pentest by the time you consider using this tool, but identifying more passwords, SSNs, salary info, etc. makes the pentest a bit more fun :).
	- Help menu: https://dl.dropboxusercontent.com/u/2526790/smbspider/smbspider.png
	- Usage screenshot #1: https://dl.dropboxusercontent.com/u/2526790/smbspider/smbspider%201.png
	- Usage screenshot #2: https://dl.dropboxusercontent.com/u/2526790/smbspider/smbspider%202.png

smsspam - This was my first python script. I created this simple script when someone pissed me off by continuously playing on my phone. They quickly revealed their identity after approximately 50 text messages in about 10 seconds :).
	- Help menu: https://dl.dropboxusercontent.com/u/2526790/smsspam.png

pymsf - My FUD meterpreter payload creator. You can't have it, but you can see it.
	- Usage screenshot #1: https://dl.dropboxusercontent.com/u/2526790/pymsf.png
