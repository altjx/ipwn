Introduction
===
Sometimes when you run ifconfig on both Mac OS and also UNIX/Linux, you like to just get straight to the point. Sometimes it takes you a few seconds to look for the MAC address and/or IP address for a specific interface. These tools basically simplify that process for you.

Instructions
===
Usage menu (from Linux CLI):
<pre><code>
[07.22.2017/21:34:09] root@box $ ./ifconfigs.rb 
+-----------+--------------+---------------------+---------------+-------------------+
|       1337 H4x0Rz Linux Ifconfig Parser - Alton Johnson (alton.jx@gmail.com)       |
+-----------+--------------+---------------------+---------------+-------------------+
| Interface | IPv4 Address | Subnet Mask         | Broadcast     | MAC Address       |
+-----------+--------------+---------------------+---------------+-------------------+
| ens33:    | 192.168.1.10 | 255.255.255.0 (/24) | 192.168.1.255 | 00:0c:29:56:d8:ea |
| lo:       | 127.0.0.1    | 255.0.0.0 (/8)      |               |                   |
+-----------+--------------+---------------------+---------------+-------------------+

</code></pre>
