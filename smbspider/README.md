Introduction
===
Smbspider is a pretty smart when it comes to spidering Windows systems on internal networks. Once you get your hands on some credentials, you can pass them around with smbspider to try spidering systems that the user account has access to. In many cases, you'll end up quickly finding all types of sensitive data hanging out on employees' workstations.

Instructions
===
Usage video: http://www.youtube.com/watch?v=skVZwynHECw
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