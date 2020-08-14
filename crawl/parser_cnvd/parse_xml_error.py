import os, time, csv
# import xml.dom.minidom as minidom

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from crawl.parser_cnvd.create_table import db, add_cnvd
data_list = []


def paser_duo():
    item = {'source': 'cnvd'}
    for child in root:
        # print('---------------'+child.tag, child.attrib)
        for node in child:
            # print(node.tag, node.text)
            # print(type(node.tag))
            data_list.append(node.text)
            if node.tag == 'number':
                item['cnvd_id'] = node.text
                print(item['cnvd_id'])

            if node.tag == 'cves':
                if node.find('cve'):
                    cve_id = node.find('cve').find('cveNumber')  # xiugai
                    item['cve_id'] = cve_id.text if cve_id is not None else 'null'
                    print(item['cve_id'])
                    url = node.find('cve').find('cveUrl')
                    item['cve_url'] = url.text if url is not None else 'null'
                    print(item['cve_url'])

            if node.tag == 'title':  # node.tag是str类型
                item['title'] = node.text

            if 'serverity' not in node.tag:
                item['levle'] = '未评级'
            if 'serverity' in node.tag:
                item['levle'] = f'{node.text}危'
                print(item['levle'])

            # if node.get('serverity', default=None):
            #     serverity = node.get('serverity', default=None)
            #     item['levle'] = serverity if serverity else 'wei'
            # if node.findtext('.//serverity'):
            #     print(node.text)
            #     item['levle'] = node.text
            # if node.find('serverity'):
            #     if node.find('serverity') is not None:
            #         item['levle'] = node.find('serverity').text
            #     else:
            #         item['levle'] = 'wei'

            if node.tag == 'products':
                item['affect_product'] = ';'.join([p.text for p in node if node is not None])

            if node.tag == 'isEvent':
                item['vulnerability_type'] = node.text

            if node.tag == 'submitTime':
                item['posted_time'] = node.text

            if node.tag == 'openTime':
                item['update_time'] = node.text

            if node.tag == 'discovererName':  # xiugai
                item['company_name'] = node.text if node.text is not None else ''
                print(item['company_name'])

            if node.tag == 'referenceLink':  # xiugai
                item['refer_link'] = node.text if node.text is not None else ''

            if node.tag == 'formalWay':
                item['solve_way'] = node.text

            if node.tag == 'description':
                item['describe'] = node.text

            if node.tag == 'patchName':  # xiugai
                item['patch'] = node.text if node.text is not None else ''
                print(item['patch'])

            if node.tag == 'patchDescription':  # xiugai
                item['patch_describe'] = node.text if node.text is not None else ''
        # print(item)
        # print(len(item))

        cnvd_id = item.get('cnvd_id', '')
        cve_id = item.get('cve_id', '')
        cve_url = item.get('cve_url', '')
        title = item.get('title', '')
        levle = item.get('levle', 'null')
        affect = item.get('affect_product', '')
        vul_type = item.get('vulnerability_type', '')
        posted_time = item.get('posted_time', '')
        update_time = item.get('update_time', '')
        company_name = item.get('company_name', '')
        refer_link = item.get('refer_link', '')
        solve_way = item.get('solve_way', '')
        describe = item.get('describe', '')
        patch = item.get('patch', '')
        patch_describe = item.get('patch_describe', '')
        print(cnvd_id, levle, cve_id, cve_url, patch)
        print()

        # info = add_cnvd(
        #     cnvd_id=cnvd_id, cve_id=cve_id, cve_url=cve_url, title=title, levle=levle, affect_product=affect,
        #     vul_type=vul_type, posted_time=posted_time, openTime=update_time, company_name=company_name,
        #     refer_link=refer_link, solve_way=solve_way, describe=describe, patch=patch, patch_describe=patch_describe
        # )
        # db.session.add(info)
        # db.session.commit()
        # time.sleep(0.5)


if __name__ == '__main__':
    # file = open('xml_test.txt', 'r')
    # number = 0
    # for i in file:
    #     path = i.strip()
    #     tree = ET.parse(path)
    #     root = tree.getroot()
    #     paser_duo()
    #     number += 1
    #     # print("解析第{}个xml文件".format(number))
    #     time.sleep(0.5)

    file = '/home/shijiuyi/Desktop/other_crawl/crawl_cnvd_list/xml_test/2020-07-20_2020-07-26.xml'
    tree = ET.parse(file)
    root = tree.getroot()
    paser_duo()
    time.sleep(0.5)
    # print(data_list)
