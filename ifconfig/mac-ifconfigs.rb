#!/usr/bin/env ruby
require 'terminal-table'
require 'ipaddr'

ifconfig = `ifconfig`.split("\n")

oint = ''
int = ''
omac = ''

# Convert hexadecimal netmask to decimal.
def convert_netmask(mask)
  first_octet = mask[0..1].to_i(16)
  second_octet = mask[2..3].to_i(16)
  third_octet = mask[4..5].to_i(16)
  fourth_octet = mask[6..7].to_i(16)
  mask = "#{first_octet}.#{second_octet}.#{third_octet}.#{fourth_octet}"
  return mask
end

data = []

# Begin the table.
table = Terminal::Table.new do |t|
  # Define the table headers.
  t << ['Interface','IPv4 Address','Subnet Mask','Broadcast','MAC Address']
  t.add_separator

  ifconfig.each do |line|
    # Regex used to grab for specific information.
    int = line.scan(/(.*?): flags=/)
    ipaddr = line.scan(/inet \b(?:\d{1,3}\.){3}\d{1,3}\b/)
    netmask = line.scan(/0x\h\h\h\h\h\h\h\h/)
    broadcast = line.scan(/broadcast \b(?:\d{1,3}\.){3}\d{1,3}\b/)
    mac = line.scan(/(?:[A-Fa-f0-9]{2}[:-]){5}(?:[A-Fa-f0-9]{2})/)

    # Fix the variables if the regex matches aren't empty.
    int = int unless int.nil?
    ipaddr = ipaddr[0][5..-1] unless ipaddr.empty?
    netmask = convert_netmask(netmask[0][2..-1]) unless netmask.empty?
    broadcast = broadcast[0][10..-1] unless broadcast.empty?
    omac = mac[0] unless mac.empty?

    # Clean up some stuff.
    int = int[0][0] unless int.empty?
    oint = int unless int.empty?
    broadcast = '' if broadcast.empty?
    ipaddr = '' if ipaddr.empty?
    netmask = '' if netmask.empty?
    
    # Add the data to a table.
    unless oint.empty? and ipaddr.empty? and netmask.empty? and broadcast.empty? and omac.empty?
      unless ipaddr.empty? and omac.empty?
        cidr = "(/" +IPAddr.new(netmask).to_i.to_s(2).count("1").to_s + ")"  unless ipaddr.empty?
        data << [oint, ipaddr, "#{netmask} #{cidr}", broadcast, omac]
        omac = ''
      end
    end
  end
  
  # Remove weird entries and then add them to our terminal table.
  data.each do |d|
    lastline = data[data.index(d)-1]
    if lastline[0] == d[0] and d[-1].empty?
      d[-1] = lastline[-1]
      data.delete_at(data.index(lastline))
    end
  end
  
  # Add data array to the terminal table.
  data.each do |entry|
    t << entry
  end

  # Grab public IP address
  public_ip = `curl "https://api.ipify.org" -s`
  t.add_separator
  t.add_row ["Public IP Address", public_ip, "", "", ""]
  
end
table.title = "1337 H4x0Rz Mac OS Ifconfig Parser - Alton Johnson (alton.jx@gmail.com)"
puts table
