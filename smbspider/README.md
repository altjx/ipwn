Introduction
===
Smbspider is a pretty smart when it comes to spidering Windows systems on internal networks. Once you get your hands on some credentials, you can pass them around with smbspider to try spidering systems that the user account has access to. In many cases, you'll end up quickly finding all types of sensitive data hanging out on employees' workstations.

Instructions
===
Usage menu:

  - Menu: https://dl.dropboxusercontent.com/u/2526790/smbspider/smbspiderpy.png
  - Script usage screenshot #1: https://dl.dropboxusercontent.com/u/2526790/smbspider/whole_output.png
  - Usage video: http://www.youtube.com/watch?v=skVZwynHECw

<pre><code>
 ************************************************************
 *                  _                                         *
 *                 | |       //  \\                           *
 *    ___ _ __ ___ | |__    _\\()//_                        *
 *   / __| '_ ` _ \| '_ \  / //  \\ \                       *
 *   \__ \ | | | | | |_) |   |\__/|                         *
 *   |___/_| |_| |_|_.__/                                   *
 *                                                          *
 * SMB Spider v2.4, Alton Johnson (alton.jx@gmail.com)      *
 ************************************************************

 Usage: /root/scripts/ipwn/smbspider.py <OPTIONS>

 Target(s) (required): 

   -h <host>   Provide IP address or a text file containing IPs.
       Supported formats: IP, smb://ip/share, \\ip\share\

 Credentials (required): 

   -u <user>   Specify a valid username to authenticate to the system(s).
   -p <pass>   Specify the password which goes with the username.
   -P <hash>   Use -P to provide password hash if cleartext password isn't known.
   -d <domain>   If using a domain account, provide domain name.

 Shares (optional):

   -s <share>  Specify shares (separate by comma) or specify "profile" to spider user profiles.
   -f <file>   Specify a list of shares from a file.

 Other (optional):

   -w      Avoid verbose output. Output successful spider results to smbspider_host_share_user.txt.
       This option is HIGHLY recommended if numerous systems are being scanned.
   -n      ** Ignore authentication check prior to spidering.
   -g <file>   Grab (download) files that match strings provided in text file. (Case sensitive.)
       ** Examples: *assword.doc, *assw*.doc, pass*.xls, etc.

</code></pre>
<br />
<b><a name="smsspam">SMSpam</a></b><br />
This was my first python script. I created this simple script when someone pissed me off by continuously playing on my phone. They quickly revealed their identity after approximately 50 text messages in about 10 seconds :).<br />
Usage menu:
<pre><code>
===================================================
 SMSpam v1.0 created by Alton (alton.jx@gmail.com)
===================================================

		-r: Recipient to send an email to.
		-u: Gmail username (include @gmail.com).
		-p: Password to login to gmail with.
		-m: Message to send to user.
		-s: Subject for the email.
		-n: How many times you want to send this email.
</code></pre>
<b><a name="nmapparser">Nmap Parser</a></b><br />
If you have tons of nmap results and want to look at them in a pretty table, check out this nmap result parser. <br />
	- Usage screenshot #2: https://dl.dropboxusercontent.com/u/2526790/nmap_parser1.png <br />
Usage menu:
<pre><code>
 ------------------------------------------------------------------------
  nmapparse 1.0 - Nmap Output Parser, Alton Johnson (alton.jx@gmail.com)
 ------------------------------------------------------------------------
 
 Usage: ./nmapparse.py results.gnmap

 Note: This script must point to a grepable output file from nmap to work properly.
</code></pre>
<br />
<b><a name="nmapscrape">Nmap Scrape</a></b><br />
This script will take the nmap grepable output format and create text files (filename = port number) with a list of IP addresses in these text files. For example, it'll create an 80.txt file with all IPs with port 80 open. See screenshots for a better understanding. <br />
	- Usage screenshot #2: https://dl.dropboxusercontent.com/u/2526790/nmapscrape1.png <br />
Usage menu:
<pre><code>
 ----------------------------------------------------
 Nmap Parser v1.0, Alton Johnson (alton.jx@gmail.com) 
 ----------------------------------------------------

 Usage: nmapscrape.py &lt;gnmap file&gt;
</code></pre>
Nmap Parser
=======
 Nmap Parser v2.0, Alton Johnson (alton.jx@gmail.com) 
<pre><code>
 Usage: nmapscrape.rb &lt;gnmap file&gt;
</code></pre>