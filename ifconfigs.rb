#!/usr/bin/env ruby
require 'terminal-table'
require 'ipaddr'

ifconfig = `ifconfig`.split("\n\n")

oint = ''
int = ''
omac = ''

# Begin the table.
table = Terminal::Table.new do |t|
  # Define the table headers.
  t << ['Interface','IPv4 Address','Subnet Mask','Broadcast','MAC Address']
  t.add_separator

  ifconfig.each do |line|
  	int = ""
    # Regex used to grab for specific information.
    unless !int.empty?
    	int = line.split(" ")[0]
    end
    ipaddr = line.scan(/\b(?:\d{1,3}\.){3}\d{1,3}\b/)[0]
    netmask = line.scan(/\b(?:\d{1,3}\.){3}\d{1,3}\b/)[1]
    broadcast = line.scan(/\b(?:\d{1,3}\.){3}\d{1,3}\b/)[2]
    mac = line.scan(/(?:[A-Fa-f0-9]{2}[:-]){5}(?:[A-Fa-f0-9]{2})/)[0]

    # Clean up some stuff
    oint = int unless int.empty?
    ipaddr = '' if ipaddr.nil?
    broadcast = '' if broadcast.nil?
    omac = mac unless mac.nil?

    # Add the data to a table.
    unless oint.empty? and ipaddr.empty? and netmask.empty? and broadcast.empty? and omac.empty?
    	ipaddr = '' if ipaddr.nil?
    	netmask = '' if netmask.nil?
    	unless ipaddr.empty? or netmask.empty?
    		cidr = IPAddr.new(netmask).to_i.to_s(2).count("1")
    		t << [oint, ipaddr, "#{netmask} (/#{cidr})", broadcast, omac]
    		omac = ''
    	end
    end
end
end

table.title = "1337 H4x0Rz Linux Ifconfig Parser - Alton Johnson (alton.jx@gmail.com)"
puts table
