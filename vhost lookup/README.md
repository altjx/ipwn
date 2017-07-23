Introduction
===
VHostLookup is a script designed to assist with identifying virtual hosts. For example, if you have an IP address of a domain and want to see what other domains are hosted on that same exact server, you can use this tool to get that information.

Instructions
===
Simply provide the script an IP address of a potential virtual host.
Usage example:
<pre><code>
[07.22.2017/21:49:31] root@box $ host altonj.com
altonj.com has address 68.65.120.201
altonj.com mail is handled by 10 mx2.privateemail.com.
altonj.com mail is handled by 10 mx1.privateemail.com.
[07.22.2017/21:49:42] root@box $ ./vhost_lookup.rb -i 68.65.120.201

 ---------------------------------------------------
  VHost Lookup - Alton Johnson (alton.jx@gmail.com)
 ---------------------------------------------------
 
 [*] Finding virtualhosts for: 68.65.120.201
 [*] 10 potential domain(s) identified to match IP. Parsing results.
 [*] Results parsed. Performing additional IP lookups on each domain.
 [*] Complete! Printing table.

+-------------------------+-------------------------+-----------------+----------------------+
| Query                   | Additional DNS Name     | DNS Record Type | DNS Entry            |
+-------------------------+-------------------------+-----------------+----------------------+
| www.eddiescalzones.com  | www.eddiescalzones.com  | CNAME           | eddiescalzones.com.  |
| www.eddiescalzones.com  | eddiescalzones.com      | A               | 68.65.120.201        |
| beachlineraceway.com    | beachlineraceway.com    | A               | 68.65.120.201        |
| zebiak.website          | zebiak.website          | A               | 68.65.120.201        |
| tableandchairdirect.com | tableandchairdirect.com | A               | 68.65.120.201        |
| gisesb.com              | gisesb.com              | A               | 68.65.120.201        |
| wazivision.com          | wazivision.com          | A               | 68.65.120.201        |
| hellscanyoninn.com      | hellscanyoninn.com      | A               | 68.65.120.201        |
| www.inglenookhearth.com | www.inglenookhearth.com | CNAME           | inglenookhearth.com. |
| www.inglenookhearth.com | inglenookhearth.com     | A               | 68.65.120.201        |
| zeroplaneualberta.com   | zeroplaneualberta.com   | A               | 68.65.120.201        |
| fatfreezing.club        | fatfreezing.club        | A               | 68.65.120.201        |
+-------------------------+-------------------------+-----------------+----------------------+
</code></pre>