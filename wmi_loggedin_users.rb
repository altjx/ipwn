#!/usr/bin/ruby

begin
  require 'terminal-table'
  require 'getopt/std'
rescue Exception => e
  puts "\n Error loading required gems."
  puts " Install required gems using the following commands:\n
        gem install terminal-table\n\tgem install getopt\n\n"
  exit
end

def help_menu
 puts %Q{
 ---------------------------------------------------------------------------
  Logged In User Enumerator (via WMIC) - Alton Johnson (alton.jx@gmail.com)
 ---------------------------------------------------------------------------

 Usage: #{$0} -f <file> -d <domain> -u <username> -p <password>

 \t-f\tFile containing IP addresses to scan.
 \t-d\tDomain used for the valid account.
 \t-u\tAdministrator account that will be used for logging in.
 \t-p\tPassword for the administrator account.
 }
 exit 
end

def start(filename, domain, username, password)
  iplist = File.open(filename,'r').read.split

  # Extract logged in users via WMIC.
  table = Terminal::Table.new do |t|
    t << ["IP Address","Domain", "Username"]
    t.add_separator
    
    iplist.each do |ip|
      separate = 0
      users = []
      excluded_users = ["SYSTEM","IUSR"]

      # Prints status.
      puts " [*] Extracting users from #{ip}"

      data = `wmic -U #{domain}/#{username}%#{password} //#{ip} "select * from Win32_LoggedOnUser"`.split
      for row in data
        user_domain = row.scan(/Domain="(.*?)"/im)[0]
        user = row.scan(/Name="(.*?)"/im)[0]
        unless user_domain.nil? or user.nil?
          t << [ip, user_domain[0], user[0]] unless users.include? user or excluded_users.include? user[0]
          users << user
          separate = 1
        end
      end
      t.add_separator unless separate == 0 or ip == iplist[-1]
    end
  end
  puts
  puts table
end

if $0 == __FILE__
  if ARGV.length == 0
     help_menu
  end
  
  opt = Getopt::Std.getopts("f:u:p:d:")

  fail "One or more required options are missing." unless opt["f"] or opt["u"] or opt["d"] or opt["p"]
  begin
    start(opt["f"], opt["d"], opt["u"], opt["p"])
  rescue Exception => e
    puts e
  end

end
