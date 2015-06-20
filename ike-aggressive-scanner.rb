#!/usr/bin/env ruby

#
# This script simply scans a list of systems to determine if IKE Aggressive Mode
# is supported. If so, it writes the hashed PSK value to a file.
#
# I simply stumbled upon like 20 systems with port 500/UDP opened, and didn't feel 
# like doing it manually, so that's where this came from.
#
# Author: Alton Johnson
# Contact: alton.jx@gmail.com
# Date: 06/29/2015
#

begin
  require 'terminal-table'
  require 'getopt/std'
rescue
  puts "It appears that you may be missing some prerequisites for this script."
  puts "Run the following commands:"
  puts "\t\t gem install terminal-table"
  puts "\t\t gem install getopt/std"
end

@banner = %Q{
  --------------------------------------------------------------------
    IKE Aggressive Mode Scanner - Alton Johnson (alton.jx@gmail.com)
  --------------------------------------------------------------------

}

def help
  puts @banner 

  puts "  Usage: #{$0} -f vpn_gateways.txt\n\n"
  puts "  -f <file> \t Specifies file containing IP addresses for scanning."
  puts
  exit
end

def start_scanning(filename)
  ips = File.open(filename).read.split

  results = []

  # Use ike-scan on all IP addresses in file.  
  ips.each do |ip|
    if `ike-scan #{ip} -A --id=test -Pike-aggressive-mode-#{ip}.txt`.include? "Aggressive Mode"
      results << [ip, "\e[34;1mAggressive Mode supported\e[00;0m", "ike-aggressive-mode-#{ip}.txt"]
    else
      results << [ip, 'Not supported', 'n/a'] 
    end
  end

  # Stdout.
  table = Terminal::Table.new :title => "IKE Aggressive Mode Scanner - Alton Johnson (alton.jx@gmail.com)",
    :headings => ['IP Address','Status', 'Saved file to'], :rows => results

  puts table
end

if $0 == __FILE__

  if ARGV.length == 0
    help
  end

  opt = Getopt::Std.getopts('f:')

  fail "You must specify a file with -f. If you only have one host, just use ike-scan :)" unless opt['f']

  start_scanning(opt['f'])

end
