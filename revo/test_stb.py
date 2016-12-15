import json
import socket
import os
import csv
import io
import re
import urllib2
from xml.etree import ElementTree as ET
from xml.dom.minidom import parse

i = 0

msg = \
    'M-SEARCH * HTTP/1.1\r\n' \
    'HOST:239.255.255.250:1900\r\n' \
    'MX:2\r\n' \
    'MAN:ssdp:discover\r\n' \
    'ST:urn:schemas-upnp-org:device:ManageableDevice:2\r\n'

# Set up UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.settimeout(5)
s.sendto(msg, ('239.255.255.250', 1900))

try:
    os.remove('serialnumbers.txt')
except OSError:
    pass

def logToFile(logTxt):
    logFile = open("serialnumbers.txt", "a+")
    logFile.write(logTxt + "\n")

count = 0
try:
    while True:
        count = count + 1
        data, addr = s.recvfrom(65507)

        print "========================="
        print "data: " + data
        print "addr: " + str(addr)
        print "========================="

        mylist = data.split('\r')
        url = re.findall('http?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)
        print url[0]
        response = urllib2.urlopen(url[0])
        the_page = response.read()

        tree = ET.XML(the_page)
        with open("temp.xml", "w") as f:
            f.write(ET.tostring(tree))

        document = parse('temp.xml')
        actors = document.getElementsByTagName("ns0:serialNumber")
        for act in actors:
            for node in act.childNodes:
                if node.nodeType == node.TEXT_NODE:
                    r = "{}".format(node.data)
                    print r
                    logToFile(str(r))
                    i += 1
                    print i

except socket.timeout:
    print "ERROR: I WAs in the except block"
    pass


from ftplib import FTP
import socket
    
ftp = FTP('ftp.cwi.nl') 
ftp.login(user='username', passwd = 'password')
ftp.cwd("PATH ON FTP SERVER")
placeFile("serialnumbers.txt")
ftp.storbinary("STOR "+ filename + "_" + socket.gethostname(), open(filename, 'rb'))
ftp.quit()