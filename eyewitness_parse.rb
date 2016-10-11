#!/usr/bin/env ruby
#
# This tool simply parses the EyeWitness report in an HTML table for CLI tools
# Run the script in the same directory that contains the reports. 
#
require 'nokogiri'
require 'pry'
require 'terminal-table'

report_files = Dir.glob("./report*.html")

table = Terminal::Table.new do |t|
	t.headings = ['url','response code', 'title', 'powered by','server', 'report']
	report_files.each do |report_name|
		t.add_separator unless report_files.index(report_name) == 0
		report = Nokogiri::HTML(File.open(report_name))
		report.xpath('//td[contains(., "http://")] | //td[contains(., "https://")]').each do |data|
			data = data.to_s.split ("\n")
			url = title = response = powered_by = server = ""
			data.each do |d|
				d = d.gsub("</b>", "").gsub("<br><b> ", "")
				url = Nokogiri::HTML(d).xpath("//a").text if url.empty? and Nokogiri::HTML(d).xpath("//a").text.include? "http"
				title = d.gsub("Page Title: ", "") if title.empty? and d.include? "Page Title: "
				powered_by = d.gsub("x-powered-by: ", "") if powered_by.empty? and d.include? "x-powered-by: "
				server = d.gsub("server: ", "") if server.empty? and d.include? "server: "
				response = d.gsub("Response Code: ", "") if response.empty? and d.include? "Response Code: "
			end
			t.add_row [url, response, title[0..40], powered_by[0..20], server[0..20], report_name]
		end
	end
end

puts table
