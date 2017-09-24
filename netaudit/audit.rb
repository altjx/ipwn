#!/usr/bin/env ruby
#
# This script was developed to allow network adminstrators to periodically
# run port scans on their external environment to check for unnecessarily 
# opened ports. If an unusual port is identified, a network administrator
# will be notified.
#
# Authors:
# 	Alton Johnson (ajohnson@directdefense.com)
# 	Jonathan Broche (jbroche@directdefense.com)
#
# Created: 09/01/2017
# Updated: N/A
# Version: 1.0
#

require 'yaml'
require 'nokogiri'
require 'pry'
require 'getopt/std'
require 'terminal-table'

def help
  puts
  puts  "-" * 24
  puts " NetAudit, version 1.0"
  puts "-" * 24  + "\n\n"
  puts " -c\tSpecify YML configuration file included with script."
  puts " -b\tIf this is a baseline scan, specify this option."
  puts "\nExample: #{$0} -c configuration.yml -b"
  puts
  exit
end

class Audit
  def initialize(configuration_file, baseline)
    # Parse configuration file.
    data = YAML.load_file(configuration_file)
    @date = Time.now.strftime("%m%d%Y")

    @baseline = baseline
    @new_ip_port_map = []
    @first_report = 0
    log_file = ""

    # Create logs folder if it doesn't exist.
  	existing_files = Dir.glob("logs/{*port_scan_results*,base*}")
  	if existing_files.empty?
  		FileUtils.mkdir_p "logs"
  		@first_report = 1
  	end

    # If baseline and files exist, wipe and reload.
    if baseline and !existing_files.empty?
      FileUtils.rm_f "logs"
      FileUtils.mkdir_p "logs"
      @first_report = 1
    end

    count = existing_files.length
    if @baseline
      log_file = "logs/base.xml"
    else
      log_file = "logs/#{count}_port_scan_results.xml"
    end

    # Nmap information.
    @nmap_discovery = data["discovery"] + " -oG logs/discovered_assets_#{@date}.gnmap"
    @nmap_port_scan = data["port_scan"] + " -iL logs/alive.txt -oX #{log_file}"

    # Notification details.
    @notification_email = data["notification_email"]
    @attach_output = data["attach_output_to_email"]

    # SMTP Information.
    @smtp_server = data["smtp_server"]
    @smtp_username = data["smtp_username"]
    @smtp_password = data["smtp_password"]
    @smtp_port = data["smtp_port"]

    # IP exclusion information.
    @ip_exclusions = data["ip_exclusions"]
  end

  def run_nmap
    # Perform discovery scan.
    stdout("good", "Starting Nmap discovery scans.")
    nmap_discovery_command = "sudo #{@nmap_discovery} > /dev/null"
    system(nmap_discovery_command)
    stdout("good", "Completed Nmap discovery scans.")

    # Parse discovered systems.
    command = "cat logs/discovered_assets_#{@date}.gnmap | awk '/Up/{print $2}' >> logs/alive.txt"
    system(command)

    # Perform port scans.
    stdout("good", "Starting Nmap port scans.")
    nmap_port_scan_command = "sudo #{@nmap_port_scan} > /dev/null"
    system(nmap_port_scan_command)
    stdout("good", "Completed Nmap port scans.")
  end

  def compare_results
  	if @first_report == 0 # Previous reports exists, do comparisons. 
  		@mappings = {"new_info" => [], "changes" => []}
  		tmp_mappings = []

  		base_report = Dir.glob("logs/base*")[0]
  		latest_report = Dir.glob("logs/*port_scan_results*")[-1]

  		# Produce differences with Nmap's Ndiff tool.
  		command = "ndiff --xml #{base_report} #{latest_report} | tee differences.xml > /dev/null"
  		system(command)

  		data = Nokogiri::XML(File.open("differences.xml"))
  		data.xpath("//address").each do |host|
  			ipaddr = host.attr("addr")

  			host.xpath("//port").each do |portf|
  				port = portf.attr("portid")
  				protocol = portf.attr("protocol")
          begin
  				  status = portf.xpath(".//state").attr("state").value
          rescue
            next
          end

  				tmp_mappings << [ipaddr, port, protocol, status]
  			end
  		end

  		# Go through tmp_mappings and add to final list of mappings, cleaning up tmp_mappings.
  		while tmp_mappings.length > 0 do
  			current_mapping = tmp_mappings[0] # Start with the first element in array.
  			if current_mapping[-1] == "open"
  				opposite = "closed"
  			else
  				opposite = "open"
  			end
  			opposite_mapping = [current_mapping[0..2], opposite].flatten

  			if tmp_mappings.include? opposite_mapping
  				@mappings["changes"] << [{"old_state" => current_mapping, "new_state" => opposite_mapping}]

  				tmp_mappings.delete(opposite_mapping) # Delete opposite mapping from array.
  			else
  				@mappings["new_info"] << current_mapping
  			end
  			tmp_mappings.delete(current_mapping) # Delete current mapping from array.
  		end
  	end
  end

  def create_report
    return if @mappings.nil?
    return if @mappings.empty? and (@mappings["new_info"].empty? and mappings["changes"].empty?)

    # Create report based on new data.
    if !@mappings["new_info"].empty?
      rows = @mappings["new_info"]
      new_table = Terminal::Table.new :headings => ["IP Address","Port","Protocol","Status"], :rows => rows
      File.open("data_new.txt","w") {|f| f.write("#{new_table}\n")}
    end

    # Create report based on changes.
    if !@mappings["changes"].empty?
      rows = []
      @mappings["changes"].each do |change|
        old_state = change[0]["old_state"]
        new_state = change[0]["new_state"]

        changes = old_state + [new_state[-1]]

        rows << changes
      end
      change_table = Terminal::Table.new :headings => ["IP Address", "Port","Protocol", "Old State","New State"], :rows => rows
      File.open("data_changes.txt","w") {|f| f.write("#{change_table}\n")}
    end
  end

  def send_notification
    return if (@smtp_username.empty? and @smtp_server.empty?) or @mappings.nil?

    # Configure notification email
    password = ""
    username = ""
    attachments = ""
    credentials = ""

    if !Dir.glob("data_changes.txt").empty?
      attachments += "-a data_changes.txt "
    end
    if !Dir.glob("data_new.txt").empty?
      attachments += "-a data_new.txt"
    end

    return unless !attachments.empty?

    if !@smtp_username.empty?
      credentials += "-xu #{@smtp_username} "
    end
    if !@smtp_password.empty?
      credentials += "-xp \"#{@smtp_password}\""
    end

    command = "sendemail -f #{@smtp_username} -t #{@notification_email} -m \"See attachment.\" -u \"NetAudit Report\" -s #{@smtp_server}:#{@smtp_port} #{credentials} #{attachments}"
    system(command)
  end

  def clean_up
    FileUtils.rm_f "differences.xml"
    #FileUtils.rm_f Dir.glob("data_*")
    FileUtils.rm_f Dir.glob("logs/{alive*,*port*,discovered*}")
  end

  def stdout(status, message)
    good = "\e[1;34m [*] "
    bad = "\e[1;31m [*] "
    status = (status == "good" ? good : bad)

    puts "#{status} #{message}\e[0;00m"
  end
end

if $0 == __FILE__
  if ARGV.length == 0
    help
  end

  opt = Getopt::Std.getopts("c:b")

  fail "Must have a configuration file specified with -c." unless opt['c']

  baseline = opt['b'] ? true : false

  a = Audit.new(opt['c'], baseline)

  # Perform host discovery / port scans.
  a.run_nmap

  # Compare new results with old results.
  a.compare_results

  # Create report, if necessary.
  a.create_report

  # Send notification email.
  a.send_notification

  # Clean up.
  a.clean_up
end