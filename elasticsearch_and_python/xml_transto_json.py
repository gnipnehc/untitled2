from xml.etree import ElementTree as et
import json


def readxml_et():
    tree = et.ElementTree(file="/home/shijiuyi/下载/2020-05-25_2020-05-31.xml")
    root = tree.getroot()
    dic = dict()
    listbigoption = []
    for child_root in root:
        if child_root.tag == 'filename':
            imagePath = child_root.text
        if child_root.tag == "object":
            listobject = dict()
            for xylabel in child_root:
                if xylabel.tag == "name":
                    label = xylabel.text
                if xylabel.tag == 'polygon':
                    listoption = []
                    for pt in xylabel:
                        if pt.tag == 'pt':
                            listxy = []
                            for i in pt:
                                if i.tag == 'x':
                                    listxy.append(int(i.text))
                                if i.tag == 'y':
                                    listxy.append(int(i.text))
                                listoption.append(listxy)
                    listobject['option'] = listoption
                    listobject['line_color'] = 'null'
                    listobject['label'] = label
                    listobject['file_color'] = 'null'
                    listbigoption.append(listobject)
                # print(listbigoption)
    dic['lineColor'] = [0, 255, 0, 128]
    dic['imageData'] = 'imageData'
    dic['imagePath'] = 'imagePath'
    dic['fillColor'] = [255, 0, 0, 128]
    dic['shapes'] = listbigoption
    dic['flags'] = {}
    with open('2020-05-25_2020-05-31.json', 'w') as f:
        json.dump(dic, f)

readxml_et()
