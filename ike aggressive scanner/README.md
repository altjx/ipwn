Introduction
===
Kali Linux comes with the tool <code>ike-scan</code> pre-installed already. However, what happens if you need to run this against 50 VPN gateways? Sure you can wrap it in a for loop, but this tool simplifies this process by outputting the PSK in a file (if found) for each respective device, and also provides a nice output table for you. The table looks great for reporting purposes. :)

Instructions
===
Create a file that contains a list of IP addresses (of VPN gateways) and then run the tool. Here's an example of the usage menu:
<pre><code>
[07.22.2017/21:34:09] root@box $ ./ike-aggressive-scanner.rb 

  --------------------------------------------------------------------
    IKE Aggressive Mode Scanner - Alton Johnson (alton.jx@gmail.com)
  --------------------------------------------------------------------

  Usage: ./ike-aggressive-scanner.rb -f vpn_gateways.txt

  -f <file>    Specifies file containing IP addresses for scanning.
</code></pre>
