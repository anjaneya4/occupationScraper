import pickle
import urllib2
import string
import StringIO
RESOURCE_BASE='http://www.occupationalinfo.org/'
IGNORE_BASIS=' cat_div_0.htmlOccupational Categories, Divisions, and Groups'
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
parentid=None
count=0
countmax=100
class MyHTMLParser(HTMLParser):
    def __init__(self,basis):
        global count
        print 'count: ',count
        # if count==countmax:
        #     quit()
        count+=1
        HTMLParser.__init__(self)
        self.decodebasis(basis)
        # print self.id,'||',self.parentid, '||',self.value
        if not self.url==None:
            global parentid
            parentid=self.parentid
            responsecache=urllib2.urlopen(self.url)
            self.httpresponse=responsecache.read()
            responsecache.close()
            self.rawscrp=''
            self.feed(self.httpresponse)
            if count==1:
                self.rawscrp=string.strip(self.rawscrp,IGNORE_BASIS)
            self.rawscrp=string.strip(self.rawscrp)
            self.kids=[]
            self.isleaf=False
            self.initnode()
    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            #print value
            if value is not None and (value.startswith('./') or value.startswith("cat") or value.startswith('defset')):
                self.rawscrp+=value.strip()
    def handle_data(self, data):
        if self.rawscrp[-5:] == '.html':
            clipindex=string.find(data,'(')
            data=data[:clipindex]
            data=string.strip(data)
            data+='\n'
            self.rawscrp+=data
            
    def initnode(self):
        if not self.rawscrp:
            self.isleaf=True
        # print 'isleaf: ',self.isleaf
        s = StringIO.StringIO(self.rawscrp) 
        for line in s:
            if not self.isleaf:
                kid= MyHTMLParser(line)
                kid.parentid=self.id
                self.kids.append(kid)
    
        
    def decodebasis(self,basis):
        #print '>>>InitNode: decoding basis: ',basis
        basis=string.strip(basis)
        #set id
        datastart=string.find(basis,'.html')+5
        #print 'datastart: ',datastart
        path=basis[:datastart]
        #print 'path: ',path
        self.url=RESOURCE_BASE+path
        if '/./' in self.url:
            self.url=None
        #print 'url: ',self.url
        data=basis[datastart:]
        data=string.strip(data)
        #print 'data: ',data
        delimpos=string.find(data,' ')
        #print 'delimpos: ',delimpos
        self.id=data[:delimpos]
        self.id=string.strip(self.id)
        #print 'id: ',self.id
        rawvalue=data[delimpos:]
        rawvalue=string.strip(rawvalue)
        rawvalue=string.strip(rawvalue,'-')
        self.value=string.strip(rawvalue)
        #print 'value: ',self.value
        global parentid
        self.parentid=parentid
        #print 'parentid: ',self.parentid
        parentid=self.id
    def traverse(self):
        print self.id,'||', self.parentid,'||',self.value
        if not self.url==None:
            for kid in self.kids:
                kid.traverse()
        # clearing dump overload since not required
        self.httpresponse=None
        self.rawscrp=None
parser = MyHTMLParser('contents.html0 - Occupational Categories, Divisions, and Groups')
parser.traverse()
filename='/home/anjaneya/software/utils/occupationScraper/scrapepickledump.pk1'
with open(filename, 'wb') as output:
        pickle.dump(parser, output, pickle.HIGHEST_PROTOCOL)
parser.close()
# filename='/home/anjaneya/software/utils/occupationScraper/scrapepickledump.pk1'
# with open(filename, 'rb') as input:
#     parser=pickle.load(input)
#     parser.traverse()