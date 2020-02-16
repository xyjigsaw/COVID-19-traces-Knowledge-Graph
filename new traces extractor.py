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
# PerceptronLexicalAnalyzer = JClass('com.hankcs.hanlp.model.perceptron.PerceptronLexicalAnalyzer')
# analyzer = PerceptronLexicalAnalyzer()


def exist_ns(string):
    cnt = 0
    for term in HanLP.segment(string):
        if str(term.nature) in {'ns'}:
            cnt += 1
    if cnt <= 1:
        return True
    return False


def day_analysis(day, string):
    loc = []
    act = ''
    place = {'ns'}
    sub_place = {'nis', 'nsf', 'nth'}
    movement = {'v', 'vi', 'vn', 'd', 'f', 'nhd', 'cc', 'nr', 'n', 'pbei', 'rz', 'ng'}
    p_cat = {'p'}
    HanLPseg = HanLP.segment(string)
    seg_len = len(HanLPseg)
    loc_str = ''
    for i, term in zip(range(seg_len), HanLPseg):
        if str(term.nature) in place:
            if str(HanLPseg[i - 1].nature) in place:
                loc_str += term.word
            else:
                loc.append(loc_str)
                loc_str = term.word
        elif str(term.nature) in sub_place:
            loc_str += term.word
        elif str(term.nature) not in sub_place and str(term.nature) not in place:
            act += term.word
    if loc_str == '':
        loc.append('确诊地')
    day_outcome = ''
    if act == '':
        act = '行为未知'
    act = HanLP.extractSummary(act.strip(), 3)[0]
    for i in loc:
        if i != '':
            day_outcome += '' + (day + ': {loc:' + i + ', act: ' + act) + '}, '
    return day_outcome


def json_analysis(info, addr):
    outcome = 'traces: {'
    for key, value in info.items():
        day_outcome = day_analysis(key, value)
        if day_outcome != '':
            outcome += day_outcome.replace('确诊地', addr)
            # print(day_outcome.replace('确诊地', addr))
    outcome = outcome[:-2]
    outcome += '}'
    return outcome


def adjust_raw_json(string):
    return json.loads(dict(string)['行为轨迹'].replace('\'', '"'))


with open('raw_traces_0214.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    traces = [row for row in reader]


write_list = []
for item in traces:
    print('---------------------------')
    try:
        # print(adjust_raw_json(item))
        data = json_analysis(adjust_raw_json(item), item['位置'].replace(' ', ''))
        write_list.append(data)
        print(data)
    except json.decoder.JSONDecodeError:
        write_list.append('"traces": {}')
        print('error')


data = pd.read_csv(r'raw_traces_0214.csv')
data['structured_traces'] = write_list
data.to_csv(r"structured_traces_data_0214x.csv", mode='a', index=False, quoting=2)


'''
testCases = [document]
for sentence in testCases: print(HanLP.segment(sentence))
# 关键词提取

print(HanLP.extractSummary(document, 3))
print((HanLP.parseDependency(document)))
'''
