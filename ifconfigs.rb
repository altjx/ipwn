#!/usr/bin/env ruby
require 'terminal-table'
require 'ipaddr'
require 'pry'

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
    ipaddr = line.scan(/addr:\b(?:\d{1,3}\.){3}\d{1,3}\b/)
    netmask = line.scan(/Mask:\b(?:\d{1,3}\.){3}\d{1,3}\b/)
    broadcast = line.scan(/Bcast:\b(?:\d{1,3}\.){3}\d{1,3}\b/)
    mac = line.scan(/(?:[A-Fa-f0-9]{2}[:-]){5}(?:[A-Fa-f0-9]{2})/)

    # Fix the variables if the regex matches aren't empty.
    int = int unless int.nil?
    ipaddr = ipaddr[0][5..-1] unless ipaddr.empty?
    netmask = netmask[0][5..-1] unless netmask.empty?
    broadcast = broadcast[0][6..-1] unless broadcast.empty?
    omac = mac[0] unless mac.empty?

    # Clean up some stuff
    oint = int unless int.empty?
    broadcast = '' if broadcast.empty?
    
    # Add the data to a table.
    unless oint.empty? and ipaddr.empty? and netmask.empty? and broadcast.empty? and omac.empty?
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
