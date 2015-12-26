# coding=UTF-8
"""
    use for sentence segmentation and pos tagging via Sinica
    http://ckipsvr.iis.sinica.edu.tw/
"""
import xml.etree.ElementTree as ET
import cgi
import socket
import re

def parse (get):
    root = ET.fromstring(get)
    assert root[0].items() == [('code', '0')]

    result = root[1]
    
    res = []
    for sen in result:
        ary = sen.text.split()
        for ss in ary:
            t = re.findall(r'^(.*)\((.*)\)$', ss)
            res.append(t[0])
    return res

def segment(text):
    sock = socket.socket()
    sock.connect(('140.109.19.104', 1501))

    text = cgi.escape(text)

    data = """
    <?xml version="1.0" ?>
    <wordsegmentation version="0.1" charsetcode="utf8">
    <option showcategory="1" />
    <authentication username="%s" password="%s" />
    <text>%s</text>
    </wordsegmentation>
    """ % ("quizpop", "aiproject", text)
    
    sock.send(data)
    get_from_sock = sock.recv(1024)
    arr = parse(get_from_sock)

    return arr

