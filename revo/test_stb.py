import socket
import os
import csv
import io
import re
import sys
import urllib2
from xml.etree import ElementTree as ET
from xml.dom.minidom import parse


def discover_devices_list_on_slave():
    '''
    function to dynamically discover the Manageable Devices available under each slave host.
    :return: file with list of STB devices available under each slave host.
    '''
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
    count = 0
    i = 0
    slave_devices = []
    try:
        while True:
            count += 1
            data, addr = s.recvfrom(65507)
            print "========================="
            print "data: " + data
            print "addr: " + str(addr)
            print "========================="
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
                        slave_devices.append(str(r))
                        i += 1
                        print i

        slave_devices = ["M11543TH4292", "M11543TH4258", "M11509TD9937"]                
        log_to_file(slave_devices)

    except socket.timeout:
        print 'I Was in the except block'
        pass


def log_to_file(log_txt):
    '''
    funtion to create serialnumber.txt
    :param log_txt:
    :return: write the discovered data to serialnumber.txt
    '''
    logFile = open("serialnumber.txt", "w")
    logFile.write(log_txt)
    logFile.close()


discover_devices_list_on_slave()

