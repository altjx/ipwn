##
# This module requires Metasploit: http//metasploit.com/download
# Current source: https://github.com/rapid7/metasploit-framework
##

require 'rex/proto/http'
require 'msf/core'


class Metasploit3 < Msf::Auxiliary

  # Exploit mixins should be called first
  include Msf::Exploit::Remote::HttpClient
  include Msf::Auxiliary::WmapScanServer
  # Scanner mixin should be near last
  include Msf::Auxiliary::Scanner

  def initialize
    super(
      'Name'        => 'HTTP Title Parser',
      'Description' => %q{Reports back web page titles. Very useful for when
      you have numerous web servers to inspect and need to figure out what's
      running on them. Other methods exist, such as taking screenshots, but
      they may potentially be a slower process.},
      'Author'      => 'Alton Johnson alton.jx[at]gmail.com',
      'License'     => MSF_LICENSE
    )

      register_options([
            OptInt.new('ReadBytes', [false, "Specify # of bytes to parse. 0 to parse entire pages.", 0]),
            OptString.new('URI_Path', [true, "Specify the URI path that should be followed on targets.", "/"]),
            OptBool.new('Follow_Redirects', [false, "Attempts to follow redirects.", true]),
            OptBool.new('SSL', [false, "Negotiate SSL connection", false])
         ], self.class)

    register_wmap_options({
        'OrderID' => 0,
        'Require' => {},
      })
  end

  def run_host(ip, uri=datastore['URI_Path'], attempt=0)
    begin
      connect

         opts = {'uri' => uri,
         'method' => 'GET',
         'SSL' => datastore['SSL']
         }
      res = send_request_cgi(opts)
      return if not res

         if datastore['ReadBytes'] == 0
            body = res.body.to_s
         else
            body = res.body.to_s[0..datastore['ReadBytes']]
         end

         return if res.body.length == 0
         # Parse web page response.
         if (res.code >= 300 and res.code < 400)
           print_title(ip, rport, body, res.code, 0, res.headers['Location'], attempt)
           # print_error("#{ip}:#{rport} - #{res.code} - <Redirect>")
         elsif res.code >= 200 and res.code < 300
            print_title(ip, rport, body, res.code, 0, res.headers['Location'], attempt)
         elsif res.code >= 300 and res.code < 400
            print_title(ip, rport, body, res.code)
         elsif res.code >= 400 and res.code < 500
            print_title(ip, rport, body, res.code)
         elsif res.code >= 500 and res.code < 600
            print_title(ip, rport, body, res.code)
         end

         disconnect
    rescue ::Timeout::Error, ::Errno::EPIPE
    end
  end

   def print_title(ip, rport, response, code, status=0, header="", attempt=0)
    # A little redirect handling.
    if datastore['Follow_Redirects']
      if header.to_s.include? "(http://|https://)"
        print_error("#{ip}:#{rport} - #{code} - <Unhandled 302 HTTPS/HTTP redirect>")
        return
      else
        if code == 302 and attempt != 3
          new_uri = header
          run_host(ip, new_uri, attempt+=1)
          return
        end
      end
      unless response.downcase.include? "<title>" and response.downcase.include? "</title>"
        if response.include? "location.replace(\"" 
          if response.include? "https:"
            print_error("#{ip}:#{rport} - #{code} - <Javascript redirect>")
            return
          end
          new_uri = response.to_s.scan(/replace\(\"(.*?)\"/im)[0][0].to_s
          run_host(ip, new_uri)
          return
        end
      end
    end

    # Stripping title from response body.
    title = response.to_s.scan(/<title[^>]*>(.*?)<\/title>/im)
    if title.kind_of?(Array)
      title = title[0][0] if title.length > 0
    else
      title = title[-1].to_s[2..-3]
    end
    begin
      title = title.strip
    rescue
    end
    title = title.inspect.to_s.gsub(/(\\x)+(..)/, "")[1..-2]

    if code == 302
      status = 1
      title = "<302 HTTPS/HTTP Redirect>"
    end

    # Printing out the title.
    if title.to_s.length == 0
        print_error("#{ip}:#{rport} - #{code} - <No title found>")
    else
      if status == 0
        print_good("#{ip}:#{rport} - #{code} - #{title}")
      else
        title = title.gsub("#{code} - ", "")
        print_error("#{ip}:#{rport} - #{code} - #{title}")
      end
    end
   end
  end
