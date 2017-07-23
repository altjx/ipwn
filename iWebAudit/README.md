Introduction
===
Many times, on an internal penetration test, you run across numerous web servers that you don't care about. As opposed to opening up every web server to see what they are, iWebAudit will scan a list of web servers and grab all their titles. By only reading a little bit from each server's response, this makes reporting only the titles much faster. 

Instructions
===
Usage menu:
<pre><code>
[07.22.2017/21:34:09] root@box $ ./iWebAudit.py

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
