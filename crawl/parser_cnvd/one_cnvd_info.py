import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


# data = open('/home/shijiuyi/Downloads/2020-07-20_2020-07-26.xml').read()

tree = ET.parse('/home/shijiuyi/Downloads/2020-07-20_2020-07-26.xml')
root = tree.getroot()
# print(root.tag, ":", root.attrib)  # 打印根元素的tag和属性

for child in root:
    # print(child.tag, ":", child.attrib)  # 第二层节点的标签名称和属性
    for children in child:
        # print(children.tag, ":", children.attrib)  # 遍历xml文档的第三层
        pass

number = root[0][0].text
cvenumber = root[0][1][0][0].text
cveUrl = root[0][1][0][1].text
title = root[0][2].text
serverity = root[0][3].text
products = root[0][4][0].text
isEvent = root[0][5].text
submitTime = root[0][6].text
openTime = root[0][7].text
referenceLink = root[0][8].text
formalWay = root[0][9].text.strip('\n')
description = root[0][10].text

print("number: "+number)
print("cvenumber: "+cvenumber)
print("cveUrl: "+cveUrl)
print("title: "+title)
print("serverity: "+serverity)
print("products: "+products)
print("isEvent: "+isEvent)
print("submitTime: "+submitTime)
print("openTime: "+openTime)
print("referenceLink: "+referenceLink)
print("formalWay: "+formalWay)
print("description: "+description)

