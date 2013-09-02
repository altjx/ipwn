Introduction
===
Here you will find some tools that I've created which may help you out on your next pentest. Nothing exciting as of yet, but useful. :)<br /><br>
Unfortunately, I wasn't able to capture screenshots of me using some of these tools in networks other than my home. However, I've tried to demonstrate how they're used via screenshots and videos as much as I can.

Tools
===
<br />
<b>iSMTP</b> - This is a script that I've made while pentesting at a company I worked for. Many tools will simply either do SMTP user enumeration, relay testing, or internal spoofing. I've never found any tool that did all three with flexible options. A former coworker of mine (Josh Stone) initially wrote a Ruby SMTP tester that initially made me jump on this. <br />
	- Help menu: https://dl.dropboxusercontent.com/u/2526790/iSMTP/iSMTP.png <br />
	- Usage screenshot #1 (user enumeration): https://dl.dropboxusercontent.com/u/2526790/iSMTP/SMTP%20User%20Enumeration.png <br />
<br />
<b>iWebAudit</b> - When you're on an internal pentest, many times you run across numerous printers and other useless web-based applications. Inspired by a former coworker of mine (Victor Mata), I've decided to write my own tool to simply pull back the titles from these pages. I found it to be significantly helpful with helping me more easily prioritize the web applications I wanted to target. <br />
	- Help menu: https://dl.dropboxusercontent.com/u/2526790/iWebAudit.png <br />
<br />
<b>pyFoca</b> - Inspired by the Windows FOCA application, I've decided to recreate this into a python version. One minor issue I've found while using the FOCA application for Information Gathering is that I've had to take multiple screenshots to represent the Users, Folders, etc. that I've identified with the tool. Therefore, I've written a python version which displays all of its findings into a nice table.<br />
	- Help menu: https://dl.dropboxusercontent.com/u/2526790/pyfoca.png <br />
<br />
<b>smbspider</b> - Inspired by a similar tool written by Josh Stone, I wanted to basically rewrite my own version of his tool so that I could add/remove features according to my preference. This is a script that you can use during post-exploitation to identify sensitive/confidential data laying around on users' workstations. You've probably already won on the pentest by the time you consider using this tool, but identifying more passwords, SSNs, salary info, etc. makes the pentest a bit more fun :).<br />
	- Help menu: https://dl.dropboxusercontent.com/u/2526790/smbspider/smbspider.png <br />
	- Usage screenshot #1: https://dl.dropboxusercontent.com/u/2526790/smbspider/smbspider%201.png <br />
	- Usage screenshot #2: https://dl.dropboxusercontent.com/u/2526790/smbspider/smbspider%202.png <br />
	- Usage video: http://www.youtube.com/watch?v=skVZwynHECw <br />
<br />
<b>smsspam</b> - This was my first python script. I created this simple script when someone pissed me off by continuously playing on my phone. They quickly revealed their identity after approximately 50 text messages in about 10 seconds :).<br />
	- Help menu: https://dl.dropboxusercontent.com/u/2526790/smsspam.png <br />
<br />
<b>pymsf</b> - My FUD meterpreter payload creator. You can't have it, but you can see it.<br />
	- Usage screenshot #1: https://dl.dropboxusercontent.com/u/2526790/pymsf.png
