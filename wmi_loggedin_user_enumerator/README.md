Introduction
===
This tool was designed to assist with enumerating a list of domain-attached computers to identify what users are logged on to them. A penetration tester may want to do this for a variety of reasons, including looking for domain administrator accounts, accounts that may have access to data of interest, etc.

Instructions
===
Usage menu:
<pre><code>
[07.22.2017/21:50:56] root@box $ ./wmi_loggedin_users.rb 

 ---------------------------------------------------------------------------
  Logged In User Enumerator (via WMIC) - Alton Johnson (alton.jx@gmail.com)
 ---------------------------------------------------------------------------

 Usage: ./wmi_loggedin_users.rb -f <file> -d <domain> -u <username> -p <password>

  -f  File containing IP addresses to scan.
  -d  Domain used for the valid account.
  -u  Administrator account that will be used for logging in.
  -p  Password for the administrator account.
</code></pre>