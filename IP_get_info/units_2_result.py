import numpy as np
import pandas as pd

from config import file, es

result = {}


def callback(unit_name):
    response = es.search(index='units', body={
        "query": {
            "term": {
                "unit_name.keyword": unit_name
            }
        }
    })
    if response['hits']['total']['value'] == 0:
        return
    data = response['hits']['hits'][0]['_source']
    area = f"{data['province']}/{data['city']}/{data['district']}"
    result[unit_name] = [area, data['unit_type'], data['industry']]


def main():
    df = pd.read_excel(file)
    df = df.replace(np.NaN, '')

    df['责任单位'].map(callback)

    for unit_name, (area, unit_type, industry) in result.items():
        df.loc[df['责任单位'] == unit_name, '单位归属地'] = area
        df.loc[df['责任单位'] == unit_name, '行政区划'] = area
        df.loc[df['责任单位'] == unit_name, '机构类型'] = unit_type
        # 只有一个行业相关的，与行业相关的都属于行业类型/行业分类
        df.loc[df['责任单位'] == unit_name, '行业分类'] = industry

    new_filename = '.'.join(file.split('.')[:-1]) + '-new2.xlsx'
    df.to_excel(new_filename)


if __name__ == '__main__':
    main()
