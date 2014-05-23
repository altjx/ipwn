#!/usr/bin/ruby

msf_rc = File.open('http_title.rc','w')
msf_rc.write("use auxiliary/scanner/http/http_title\n")
if ARGV[-1] == "ssl"
  msf_rc.write("set SSL true\n")
else

ARGV.each do |file|
  unless ARGV[-1] == "ssl" and file == ARGV[-1]
    port = file[0..file.index(".")-1]
    msf_rc.write("set RHOSTS file:#{file}\n")
    msf_rc.write("set RPORT #{port}\n")
    msf_rc.write("spool http_title_#{port}.txt\n")
    msf_rc.write("run\n")
    msf_rc.write("spool off\n")
  end
end

msf_rc.write("exit\n")
msf_rc.close
puts " [*] Launching: msfconsole -r http_title.rc"
exec "msfconsole -r http_title.rc"
