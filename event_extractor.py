import csv
import json
import pandas as pd
import jpype
from pyhanlp import *
import re
pattern = r',|\.|;|<|>|\?|:|!|，|。|；|·|！| |…'
HanLP.newSegment().enableOrganizationRecognize(True)
HanLP.newSegment().enableNameRecognize(True)
HanLP.newSegment().enablePlaceRecognize(True)


def day_analysis(string):
    act = []
    del_nature = {'d', 'rz', 'rzv', 'm', 'mq', 'q', 'qt', 'c', 'nx', 'f', 't', 'b', 'tg', 'ad', 'qv'}
    place = {'ns', 'nis', 'nsf', 'nth', 'ntcb'}
    ext_term = {'起', '（', '）', '许', '时许', '时乘', '时坐', '、', '医', '从', '至', '到', '市', '-'}
    in_term = {'未', '郑', '家', '集', '场', '共', '餐', '无'}
    HanLPseg = HanLP.segment(string)
    # print('@', HanLPseg)
    seg_len = len(HanLPseg)
    result = ''
    for i, term in zip(range(seg_len), HanLPseg):
        if str(term.nature) not in del_nature or term.word in in_term:
            if term.word not in ext_term and str(term.nature) not in place:
                result += term.word
    # print('$', HanLP.extractKeyword(result, 2))
    # print('#', result)
    return result


def json_analysis(info):
    outcome = '{'
    string = ''
    for key, value in info.items():
        string += '"' + key + '": "'
        string += day_analysis(HanLP.extractSummary(value, 3)[0]) + '", '
    string = string.strip(", ")
    return outcome + string + '}'


def adjust_raw_json(string):
    return json.loads(dict(string)['行为轨迹'].replace('\'', '"'))


with open('raw_traces_0220.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    traces = [row for row in reader]


write_list = []
for item in traces:
    print('---------------------------')
    try:
        # print(adjust_raw_json(item))
        data = json_analysis(adjust_raw_json(item))
        write_list.append(data)
        print(data)
    except json.decoder.JSONDecodeError:
        write_list.append('"traces": {}')
        print('error')


data = pd.read_csv(r'raw_traces_0220.csv')
data['action'] = write_list
data.to_csv(r"action_data_0220x.csv", mode='a', index=False, quoting=2)


'''
testCases = [document]
for sentence in testCases: print(HanLP.segment(sentence))
# 关键词提取

print(HanLP.extractSummary(document, 3))
print((HanLP.parseDependency(document)))
'''
