import os, time, csv
import xml.dom.minidom as minidom

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

file = '/home/shijiuyi/Desktop/other_crawl/crawl_cnvd_list/xml_test/2020-07-20_2020-07-26.xml'
doc = minidom.parse(file)

root = doc.documentElement
# print(root.nodeName)
# print(root.nodeValue)
# child = root.childNodes
# # print(child)
# print(len(child))

nodes = root.getElementsByTagName('vulnerability')

for i in nodes:
    title = i.getElementsByTagName('title')[0]
    print('title: %s' %title.childNodes[0].data)
    cnvd_id = i.getElementsByTagName('number')[0]
    print('cnvd_id: %s' %cnvd_id.childNodes[0].data)

    levle = i.getElementsByTagName("servertiy")
    if len(levle) > 0:
        print('levle: %s' %levle[0].firstChild.data)
    else:
        print('level: %s' %'null')
        pass
    # if i.getElementsByTagName('cveNumber')[0]:
    #     cve_id = i.getElementsByTagName('cveNumber')[0]
    #     if cve_id.childNodes[0]:
    #         id = cve_id.childNodes[0].data
    #     else:
    #         id = 'null'
    # else:
    #     id = 'null'
    # print('cve_id: %s' %id)


