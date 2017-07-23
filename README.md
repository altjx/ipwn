Introduction
===
Just a random list of tools that you may or may not find helpful during penetration test engagements and just during normal CLI usage.

Tools
===
* [iSMTP](#user-content-ismtp)
* [iWebAudit](#user-content-iwebaudit)
* [pyFoca](#user-content-pyfoca)
* [smbspider](#user-content-smbspider)
* [SMSpam](#user-content-smsspam)
* [Nmap Parser](#user-content-nmapparser)
* [Nmap Scrape](#user-content-nmapscrape)

<br />
<b><a name="ismtp">iSMTP</a></b><br />
There's been countless times when I've needed to test for SMTP user enumeration (RCPT TO and VRFY), internal spoofing, and open relay. I've never found a tool that tested for all three and with great flexibility. iSMTP does just that, making it much easier to knock that process out of the way. <br />
	- Usage screenshot #1 (user enumeration): https://dl.dropboxusercontent.com/u/2526790/iSMTP/SMTP%20User%20Enumeration.png <br />
Usage menu:
<pre><code>
 ---------------------------------------------------------------------
  SMTP v1.6 - SMTP Server Tester, Alton Johnson (alton.jx@gmail.com)
 ---------------------------------------------------------------------
 
 Usage: ./iSMTP.py &lt;OPTIONS&gt;

 Required:

   -f &lt;import file&gt;  Imports a list of SMTP servers for testing.
                     (Cannot use with '-h'.)
   -h &lt;host&gt;         The target IP and port (IP:port).
                     (Cannot use with '-f'.)

 Spoofing:

   -i &lt;consultant email&gt;   The consultant's email address.
   -s &lt;sndr email&gt;         The sender's email address.
   -r &lt;rcpt email&gt;         The recipient's email address.
      --sr &lt;email&gt;         Specifies both the sender's and recipient's email address.
   -S &lt;sndr name&gt;          The sender's first and last name.
   -R &lt;rcpt name&gt;          The recipient's first and last name.
      --SR &lt;name&gt;          Specifies both the sender's and recipient's first and last name.
   -m                      Enables SMTP spoof testing.
   -a                      Includes .txt attachment with spoofed email.

 SMTP enumeration:

   -e &lt;file&gt;   Enable SMTP user enumeration testing and imports email list.
   -l &lt;1|2|3&gt;  Specifies enumeration type (1 = VRFY, 2 = RCPT TO, 3 = all).
               (Default is 3.) 

 SMTP relay:

   -i &lt;consultant email&gt;   The consultant's email address.
   -x                      Enables SMTP external relay testing.

 Misc:

   -t &lt;secs&gt;   The timeout value. (Default is 10.)
   -o          Creates "ismtp-results" directory and writes output to
               ismtp-results/smtp_&lt;service&gt;_&lt;ip&gt;(port).txt

 Note: Any combination of options is supported (e.g., enumeration, relay, both, all, etc.).
</code></pre>
<br />
<b><a name="iwebaudit">iWebAudit</a></b><br />
Many times, on an internal penetration test, you run across numerous web servers that you don't care about. As opposed to opening up every web server to see what they are, iWebAudit will scan a list of web servers and grab all their titles. By only reading a little bit from each server's response, this makes reporting only the titles much faster. <br />Usage menu:
<pre><code>
------------------------------------------------------------------------------
 iWebAudit v1.5 - Web Page Title Analyzer, Alton Johnson (alton.jx@gmail.com)  
------------------------------------------------------------------------------ 

 Usage: iWebAudit -f &lt;file&gt; -o &lt;output file&gt; -v -h -t 5

   -f &lt;file&gt;   Supports list of IPs and/or http[s]:// formatted IPs.
   -o &lt;file&gt;   Outputs the results to a file of your choice.
   -h          Enables HTTP PUT Method Discovery. (optional)
   -t &lt;secs&gt;   Sets default timeout. Default is 5. (optional)
   -v 	       Displays details as script runs. (optional)
</code></pre>
<br />
<b><a name="pyfoca">pyFoca</a></b><br />
If you're familiar with the Windows FOCA application, this is basically a python version of it. Pyfoca will use Google to discover files with extensions such as .pdf, .xls, .doc, etc. and download them. Once downloaded, it will extract all metadata which, in many cases, include usernames you can use for password attacks. <br />
Usage menu:
<pre><code>
 -------------------------------------------------------------------------------
  pyfoca v1.6 - Document Metadata Extractor, Alton Johnson (alton.jx@gmail.com)
 -------------------------------------------------------------------------------

 Usage: ./pyfoca.py &lt;OPTIONS&gt;

 Domain options:

    -d &lt;domain&gt;      Harvests all documents from a domain (saves to pyfoca-downloads/).
				     Afterwards, extract metadata.

 Parse file/dir:

    -f &lt;file&gt;     Extracts metadata specifically from one file. (Cannot use with '-d')
    -w &lt;dir&gt;      Extracts metadata from files within specified directory. (Cannot use with '-d')

 Foca Export Parsing:

    -r &lt;directory&gt;      Parses data exported from FOCA. Provide directory containing exported files.

 Misc:

    -x                     After parsing metadata, delete files downloaded from the domain.
    -e &lt;pdf|doc|xls|all&gt;   Search based on provided extension(s). Separate with comma. (Default is all.)
    -p &lt;number&gt;            Searches x amount of google pages (per extension). (Default is 2.)
    -t &lt;secs&gt;              Sets timeout value. (Default is 5.)
    -v                     Prints status messages for files that are downloaded.

 Supported extensions are: .pdf, .doc, .docx, .xls, .xlsx, and .ppt
 Example: ./pyfoca.py -d www.domain.com -e pdf,doc -p 3
</code></pre>
<br />
<b><a name="smbspider">smbspider</a></b><br />
Smbspider is a pretty smart when it comes to spidering Windows systems on internal networks. Once you get your hands on some credentials, you can pass them around with smbspider to try spidering systems that the user account has access to. In many cases, you'll end up quickly finding all types of sensitive data hanging out on employees' workstations. <br />
	- Menu: https://dl.dropboxusercontent.com/u/2526790/smbspider/smbspiderpy.png <br />
	- Script usage screenshot #1: https://dl.dropboxusercontent.com/u/2526790/smbspider/whole_output.png <br />
	- Usage video: http://www.youtube.com/watch?v=skVZwynHECw <br />
Usage menu:
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