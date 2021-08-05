import xmltodict
import os.path
import random
import dict2xml
import collections

class xmldb:

	def __init__(self):
		self.listOfUsers = []
		
	def add(self,newuser):
		nu = collections.OrderedDict(newuser)
		key = random.randrange(1,1000000)
		nu["key"]=str(key)
		self.listOfUsers.append(nu)
		return key
		
	def find(self,key):		
        
		for x in self.listOfUsers:
			if x['key'] == key: return x			
		return "key not found"
		
	def list(self):
		return self.listOfUsers
	   
	def load(self,filename):
		if os.path.exists(filename): f=open(filename)
		else: return filename + " doesn't exist."
			
		buf=f.read()
		f.close()
		dict = xmltodict.parse(buf)
		root=dict.get('root')
		self.listOfUsers = root['user']   
		return "ok"
				
	def save(self,filename):
		x = '<?xml version="1.0" encoding="UTF-8"?>\n'
		x += '<root>\n'
		y = dict2xml.dict2xml(self.listOfUsers,wrap="user")  #wrap every list element		
		x += y
		x += '</root>'
		f = open(filename,"w+")
		f.write(x)
		f.close()
     
