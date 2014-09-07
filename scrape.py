import urllib2
import string
RESOURCE_BASE='http://www.occupationalinfo.org/'
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
parentid=None
level=0
class MyHTMLParser(HTMLParser):
    def __init__(self,basis):
        HTMLParser.__init__(self)
        self.decodebasis(basis)
        responsecache=urllib2.urlopen(self.url)
        self.httpresponse=responsecache.read()
        responsecache.close()
        self.rawscrp=''
        self.feed(self.httpresponse)
        self.kids=None
        self.level=level
        self.isleaf=True
#        self.initnode(self)
    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if value is not None and value.startswith("cat") or value is not None and value.startswith('defset'):
                self.rawscrp+=value.strip()
    def handle_data(self, data):
        self.rawscrp+=data
    def initnode(self):
        self.filtercontents(self)
        
    
        
    def decodebasis(self,basis):
        print 'decpoding basis: ',basis
        basis=string.strip(basis)
        #set id
        datastart=string.find(basis,'.html')+5
        #print 'datastart: ',datastart
        path=basis[:datastart]
        #print 'path: ',path
        self.url=RESOURCE_BASE+path
        print 'url: ',self.url
        data=basis[datastart:]
        data=string.strip(data)
        #print 'data: ',data
        delimpos=string.find(data,' ')
        #print 'delimpos: ',delimpos
        self.id=data[:delimpos]
        self.id=string.strip(self.id)
        print 'id: ',self.id
        rawvalue=data[delimpos:]
        rawvalue=string.strip(rawvalue)
        rawvalue=string.strip(rawvalue,'-')
        self.value=string.strip(rawvalue)
        print 'value: ',self.value
        global parentid
        self.parentid=parentid
        print 'parentid: ',self.parentid
        parentid=self.id
#    def handle_kids
parser = MyHTMLParser('contents.html0 - Occupational Categories, Divisions, and Groups')
print parser.rawscrp
print parser.id
print parser.value
parser.close()