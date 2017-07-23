#!/usr/bin/env ruby
#
# This script simply parses a greppable nmap file for opened TCP
# and UDP ports. Run the file and target the nmap file for results.
#
# Author: Alton Johnson
# Contact: alton.jx@gmail.com
# Updated: 08/10/2016
#
$banner = "\n " + "-" * 54 + "\n Nmap Parser v2.0,  Alton Johnson (alton.jx@gmail.com)\n " + "-" * 54
$banner += "\n\n Usage: #{$0} /path/to/results.gnmap\n\n"

(puts $banner; exit(0)) if ARGV.first.nil?
port_files = {}

Dir.mkdir 'open-ports' unless File.exists? "open-ports"
File.open(ARGV.first) { |f|
	f.read.split("\n").each do |l|
		ipaddr = l.split(" ")[1]
		l.scan(/(\d+)\/open/).flatten.each do |p|
			port_files[p] = File.open("open-ports/#{p}.txt", 'a') unless port_files.key? p
			port_files[p].write("#{ipaddr}\n")
		end
	end
	port_files.values.each {|pf| pf.close}
	puts "\n [Nmap Port Parser] Completed. Check the 'open-ports' folder.\n\n"
}
