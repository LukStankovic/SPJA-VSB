# 
#  RSS Tester for SPJA
#  Stanislav Bohm
#

from http.server  import HTTPServer, BaseHTTPRequestHandler
from http.server import SimpleHTTPRequestHandler
from datetime import datetime

def write_element(wfile, tagname, content):
    wfile.write("         <{}>{}</{}>\n".format(tagname, content, tagname).encode())

class RssItem(object):
    
    def __init__(self, title, link, description, counter):
        self.title = title
        self.link = link
        self.description = description
        self.pubdate = datetime.now()
        self.guid = "cs.vsb.cz:%s:%s" % (self.pubdate.isoformat(), counter) 


    def write(self, wfile):
        wfile.write("      <item>\n".encode())
        write_element(wfile, "title", self.title)
        write_element(wfile, "link", self.link)
        write_element(wfile, "description", self.description)
        write_element(wfile, "pubDate", self.pubdate.isoformat())
        write_element(wfile, "guid", self.guid)
        wfile.write("      </item>\n".encode())

class RssServer(HTTPServer):

    def __init__(self, *args):
        HTTPServer.__init__(self, *args)
        self.counter = 0
        self.items = [ self.new_item() for x in range(5) ]

    def get_items(self):
        return self.items

    def new_item(self):
        self.counter += 1
        return RssItem("Article %s" % self.counter, "http://link", "Description of item %s" % self.counter, self.counter)

    def add_item(self):
        del self.items[0]
        self.items.append(self.new_item())

class RssRequest(SimpleHTTPRequestHandler):

    def send_rss_head(self):
        s = """<?xml version="1.0"?>
            <rss version="2.0">
            <channel>
            <title>SPJA News</title>
            <description>SPJA Test RSS Server</description>
            <language>en-us</language>
            <generator>SPJA RSS TESTER</generator>\n"""

        self.wfile.write(s.encode())

    def send_rss_tail(self):
        self.wfile.write("</channel>\n</rss>\n".encode())

    def send_items(self):
        for item in self.server.get_items():
            item.write(self.wfile)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/rss+xml')
        self.end_headers()
        self.send_rss_head()
        self.send_items()
        self.send_rss_tail()
        self.server.add_item()

server_address = ('', 9000)
server = RssServer(server_address, RssRequest)
server.serve_forever()
