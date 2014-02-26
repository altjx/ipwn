#!/usr/bin/python

import httplib, urllib, urllib2
import requests

host = 'connect.data.com'
url = '/loginProcess'

post_data = {
	'j_username' : 'alton.jx@gmail.com',
	'j_password' : 'P@xxw0rd1!'
}

headers = {
	'User-Agent' : 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36',
	'Content-Type' : 'aopplication/x-www-form-urlencoded',
	'Content-Length': 27,
	'Connection' : 'keep-alive'
}

encoded_data = urllib.urlencode(post_data)

session = requests.session()
r = requests.post("https://" + host + url, encoded_data)
http_cookie = str(r.cookies)
http_cookie = http_cookie[http_cookie.find("JSESSIONID"):http_cookie.find(" for")]

request = urllib2.Request('https://connect.data.com/home')
request.add_header('User-Agent','Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36')
request.add_header('Cookie', http_cookie)
response = urllib2.urlopen(request)
print response.read()
