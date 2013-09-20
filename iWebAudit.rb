#!/usr/bin/ruby
['thread','open-uri','hpricot',
'timeout','time'].each(&method(:require))
begin
	require 'getopt/std'
rescue Exception => e
	puts "Looks like the getopt ruby gem isn't installed."
	puts "Install it by typing \"gem install getopt\""
	exit()
end

def help_menu
	puts """Usage: %s -h <host or file> -t <thread>
""" % $0
	exit()
end

def get_title(url,offset)
	if url.include? "http"
		doc = Hpricot(open(url))
	else
		doc = Hpricot(open("http://" + url))
	end
	title = (doc/"title").inner_text #this grabs text in between <title> and </title> tags.
title = title.delete("\n").delete("\r")
	if title.length >= 50
		title = title[0..50] + " [stripped]"
	end
	title = title.lstrip
	puts url + " " * (offset - url.length+4) + title + "\n"
end

def handle_error(url, error, offset)
	if error.include? "redirection" and error.include? "https" #if error is a redirect to https, then
		url = error[error.index(">")+2..-1] # replace url with whatever the suggested https redirect url is
		get_title(url, offset)
	else
#	elsif error.include? "500 Internal Server Error" #ignore errors that are just 500 status codes
	end
end

def start(host_list, threads)
	titles = []
	mutex = Mutex.new
	file_open = 0

	#check if either a file or host is provided. proceed accordingly.
	if File.exists?(host_list)
		file = File.open(host_list)
		urls = file.read().split("\n")
		file_open = 1
	else
		urls = host_list.split()
	end

	#fix the offset array to ensure that output looks pretty enough.
	offset = [0] #define offset so we know how to organize our output later
	urls.each do |item|
		if item.length > offset[0]
			offset[0] = item.length
		end
	end

	#start the multi-threading process.
	threads.times.map {
		Thread.new(urls, titles) do |urls, titles|
			while url = mutex.synchronize { urls.pop }
				begin
					title = get_title(url,offset[0])
				rescue Exception => err
					handle_error(url, err.to_s, offset[0])
				end
				mutex.synchronize { titles << title }
			end
		end
	}.each(&:join)
	puts
	if file == 1
		puts "test"
		file_open.close()
	end
end

if $0 == __FILE__
	if ARGV.length == 0
		help_menu
	end
	
	#define parameters used within script. colon means argument is required if option is provided.
	opt = Getopt::Std.getopts("h:t:")
	
	#specify default threads value if none is provided.
	unless opt["t"]
		opt["t"] = 5
	end

	#spit out error if these options aren't provided with the script.
	fail "No host or filename was provided with -h." unless opt["h"]
	start_time = Time.now
	#begin the script while passing arguments
	begin
		start(opt["h"], opt["t"].to_i)
	rescue Exception => err
#		puts err
	end
end
puts "-" * 5
puts "Completed in: %.1fs" % [Time.now - start_time]
