Introduction
===
There's been countless times when I've needed to test for SMTP user enumeration (RCPT TO and VRFY), internal spoofing, and open relay. I've never found a tool that tested for all three and with great flexibility. iSMTP does just that, making it much easier to knock that process out of the way.

Instructions
===
Usage menu:
<pre><code>
[07.22.2017/21:34:09] root@box $ ./iSMTP.py

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