Introduction
===
These Nmap scripts were created to make parsing Nmap files much more convenient. For example, with <code>nmap_parser.py</code>, it simply creates a text file, named whatever port that was found to be opened, and it contains a list of IP addresses that has that port open. It's much easier to feed other tools a list of IP addresses that have a port opened this way.

With the <code>nmapscrape.rb</code> script, this allows for you to parse a greppable Nmap output into a nicely formatted table.

Instructions
===
With regards to the Nmap parser script, here's an example of the usage menu:

<pre><code>
 ------------------------------------------------------------------------
  nmapparse 1.0 - Nmap Output Parser, Alton Johnson (alton.jx@gmail.com)
 ------------------------------------------------------------------------
 
 Usage: ./nmapparse.py results.gnmap

 Note: This script must point to a grepable output file from nmap to work properly.
</code></pre>

With regards to the Nmap scrape script, here's an example of the usage menu:

<pre><code>
 ----------------------------------------------------
 Nmap Parser v1.0, Alton Johnson (alton.jx@gmail.com) 
 ----------------------------------------------------

 Usage: nmapscrape.py &lt;gnmap file&gt;
</code></pre>