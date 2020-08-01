import os, time, csv
# import xml.dom.minidom as minidom

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from crawl.parser_cnvd.create_cnvd_table import db, add_cnvd

tree = ET.parse('/home/shijiuyi/Downloads/2020-07-20_2020-07-26.xml')
root = tree.getroot()


def paser_duo():
    item = {'source': 'cnvd'}
    for child in root:
        for node in child:
            # print(children.tag, children.attrib, children.text)
            if node.tag == 'number':
                item['cnvd_id'] = node.text
                # print(node.text)

            if node.tag == 'cves':
                if node.find('cve'):
                    cve_id = node.find('cve').find('cveNumber').text
                    item['cve_id'] = cve_id
                    item['cve_url'] = 'https://nvd.nist.gov/vuln/detail/' + cve_id

            if node.tag == 'title':
                item['title'] = node.text

            if node.tag == 'serverity':
                item['levle'] = f'{node.text}危' if node.text is not None else ''

            if node.tag == 'products':
                item['affect_product'] = ';'.join([p.text for p in node if node is not None])

            if node.tag == 'isEvent':
                item['vulnerability_type'] = node.text

            if node.tag == 'submitTime':
                item['posted_time'] = node.text

            if node.tag == 'openTime':
                item['update_time'] = node.text

            if node.tag == 'discovererName':
                item['company_name'] = node.text if node.text is not None else ''

            if node.tag == 'referenceLink':
                item['refer_link'] = node.text

            if node.tag == 'formalWay':
                item['solve_way'] = node.text

            if node.tag == 'description':
                item['describe'] = node.text

            if node.tag == 'patchName':
                item['patch'] = node.text if node.text is not None else ''

            if node.tag == 'patchDescription':
                item['patch_describe'] = node.text if node.text is not None else ''
        # print(item)
        # print(len(item))
        cnvd_id = item['cnvd_id']
        # print(cnvd_id)
        if item['cve_id']:
            cve_id = item['cve_id']
        else:
            cve_id = ''
        if item['cve_url']:
            cve_url = item['cve_url']
        else:
            cve_url = ''
        title = item['title']
        if item['levle']:
            levle = item['levle']
        else:
            levle = '未评级'
        if item['affect_product']:
            affect = item['affect_product']
        else:
            affect = ''
        vul_type = item['vulnerability_type']
        posted_time = item['posted_time']
        update_time = item['update_time']
        company_name = item.get('company_name', '')
        if item['refer_link']:
            refer_link = item['refer_link']
        else:
            refer_link = ''
        solve_way = item['solve_way']
        describe = item['describe']
        patch = item.get('patch', '')
        patch_describe = item.get('patch_describe', '')

        info = add_cnvd(
            cnvd_id=cnvd_id, cve_id=cve_id, cve_url=cve_url, title=title, levle=levle, affect_product=affect,
            vul_type=vul_type, posted_time=posted_time, openTime=update_time, company_name=company_name,
            refer_link=refer_link, solve_way=solve_way, describe=describe, patch=patch, patch_describe=patch_describe
        )
        db.session.add(info)
        db.session.commit()
        time.sleep(0.5)


if __name__ == '__main__':
    paser_duo()
    # pass
