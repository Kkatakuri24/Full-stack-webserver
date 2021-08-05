from http.cookiejar import Cookie, CookieJar
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import urllib
import os
from requests.models import Response
import xmltodict
import os.path
import random
import dict2xml
import collections
from http import cookies
import urllib.parse
import cgi, cgitb
import xmlDBr3 as xmldb
import requests
cgitb.enable()

hostName = "localhost"
serverPort = 8080
#please change the path for testing
root = "."
os.chdir(root)
#Class for server. Opening "http://localhost:8080" in browser will call the method 'do_Get'
class MyServer(BaseHTTPRequestHandler):
	os.environ['NO_PROXY'] = 'localhost'
	def do_GET(self):
		uri = self.path
		if uri == '/': uri = "/createUser.html"
		qmark = uri.rfind('?')	#position of '?' char
		p = uri.rfind('.')		#position of '.' char
		if qmark == -1:
			path = uri
			query = ""
			ext = uri [p:] 		#python slice
		else:
			path = uri[:qmark]
			query = uri[qmark+1:]
			ext = uri[p+1:qmark]
		db = xmldb.xmldb()
		#check if there is an existing cookie, if there is then we give the user's preferred page
		checkCookie = str(self.headers)
		themeString = checkCookie.find('theme')		#Find the theme string in the headers
		if themeString != -1:						#if there is a cookie in the headers, then find it's value
			themeValue = checkCookie[themeString:]
			x = themeValue.split(';')
			y = x[0]
			z = y.split('=')
			value = z[1]							#Extract the preference value
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			if value == 'white':
				self.send_response(200)
				self.send_header("Content-type", "text/html")
				if self.path == '/': 
					self.path = self.path + "page1_white.html"
				filename = root + self.path
				f = open(filename, "rb")
				data = f.read()
				self.end_headers()
				self.wfile.write(data)
			elif value == 'black':
				self.send_response(200)
				self.send_header("Content-type", "text/html")
				if self.path == '/': self.path = self.path + "page1_black.html"
				filename = root + self.path
				f = open(filename, "rb")
				data = f.read()
				self.end_headers()
				self.wfile.write(data)
		else:
			#If the browser didn't send any cookies, it must be a new user
			if path == "/": path = path + "createUser.html"
			filename = root + path
			input = dict(urllib.parse.parse_qsl(query[:]))
			print(self.headers)
		
			if(os.path.isfile(filename)):
				f = open(filename, "rb")
				data = f.read()
			
			#iterate the path returned by the browser input
			if 'fname' in input and 'theme' in input:
				print("User: %s's desired theme is %s" % (input['fname'], input['theme']))	#for error checking. This returns the Username value
				C = input
				C = cookies.SimpleCookie()
				C["fname"] = input['fname']
				C["theme"] = input['theme']
				key = random.randrange(1, 1000000)
				C["key"] = key
				self.send_response(301)
				for morsel in C.values():
					self.send_header("Set-Cookie", morsel.OutputString())
				#now we have cookie ID, username, theme preference
				db.add(input)
				#Check what the user wants i.e white background or black background
				if C["theme"].value == "white":
					print(C["theme"].value)
					new_path = 'http://localhost:8080/page1_white.html'
					self.send_header('Location', new_path)
					self.end_headers()
					db.save("database.xml")
				elif C["theme"].value == "black":
					new_path = 'http://localhost:8080/page1_black.html'
					self.send_header('Location', new_path)
					self.end_headers()
					db.save("database.xml")
				
			else:
				#browser didn't send any information or cookie
				self.send_response(200)
				self.send_header("Content-type", "text/html")
				self.end_headers()
				self.wfile.write(data)


	def do_POST(self):
		
		self.send_response(301)
		self.send_header("Content-type", 'text/html')
		self.send_header('Location', '/logon.html')
		print(self.headers)
		self.end_headers()
	


if __name__ == "__main__":        
	webServer = HTTPServer((hostName, serverPort), MyServer)
	print("Server started http://%s:%s" % (hostName, serverPort))
	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass

	webServer.server_close()
	
	print("Server stopped.")