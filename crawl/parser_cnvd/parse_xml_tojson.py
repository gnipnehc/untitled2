
import os, time, json
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

data_list = []


def paser_duo():
    item = {'source': 'cnvd'}
    count = 0
    for child in root:
        # print('---------------'+child.tag, child.attrib)
        info_list = []
        vul = {}
        for node in child:
            vul[node.tag] = node.text
            if node.tag == 'cves':
                for cves in node:
                    if cves.tag == 'cve':
                        for cve in cves:
                            vul[cve.tag] = cve.text
            if node.tag == 'products':
                vul['product'] = '; '.join([p.text for p in node if node is not None])
        info_list.append(vul)
        # print(info_list[0])
        count += 1
        for info in info_list:
            name = info.get('number')
            info.pop('cves', ['null'])
            info.pop('products', ['null'])
            file = '/home/shijiuyi/Desktop/other_crawl/crawl_cnvd_list/cnvd_json_one/{}.json'.format(name)
            with open(file, 'w') as fw:
                info_json = json.dumps(info, indent=4, ensure_ascii=False)
                fw.write(info_json)
                print('success write: {}  {}.josn'.format(count, name))


if __name__ == '__main__':
    file = '/home/shijiuyi/Desktop/other_crawl/crawl_cnvd_list/xml_test/2020-07-20_2020-07-26.xml'
    tree = ET.parse(file)
    root = tree.getroot()
    paser_duo()
    time.sleep(0.5)

