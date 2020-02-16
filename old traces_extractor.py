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


def element_analysis(string):
    cau = ''
    loc = ''
    act = ''
    place = {'ns', 'nis', 'nsf', 'nth'}
    movement = {'v', 'vi', 'vn', 'd', 'f', 'nhd', 'cc', 'nr', 'n', 'pbei', 'rz', 'ng'}
    p_cat = {'p'}
    for term in HanLP.segment(string):
        if str(term.nature) in place:
            # print('#{}\t{}'.format(term.word, term.nature))  # 获取单词与词性
            if str(term.nature) == 'ns' and exist_ns(loc):
                loc += ' ' + term.word
            else:
                loc += term.word
        if str(term.nature) in movement:
            # print('@{}\t{}'.format(term.word, term.nature))  # 获取单词与词性
            act += term.word
        if str(term.nature) in {'p'}:
            cau += term.word
    if cau == '':
        cau = '未知'
    if act == '':
        act = ''
    return cau.strip(), loc.strip('-'), str(HanLP.extractSummary(act.strip(), 3)[0])


def sentence_analysis(sentence):
    sub_value_list = re.split(pattern, sentence)
    # print(sub_value_list)
    merge_loc = ''
    merge_act = ''
    outcome_list = []
    for sub_value in sub_value_list:
        if sub_value != '':
            outcome = element_analysis(sub_value)
            outcome_list.append(outcome)
            merge_loc += ' ' + outcome[1]
            if outcome[2] == '':
                merge_act += outcome[2]
            else:
                merge_act += ', ' + outcome[2]
    return merge_loc.strip(), merge_act.strip(',').strip()


def item_analysis(jsonx):
    out_str_list = ''
    for key, value in jsonx.items():
        # print(value)
        # print(HanLP.segment(value))
        try:
            outcome = sentence_analysis(value)
        # print(outcome)
            out_str = '"' + key + '": {' + '"location": "{}", "action": "{}"'.format(outcome[0], outcome[1]) + '}, '
        except:
            out_str = '"' + key + '": {}, '
        out_str_list += out_str
    return '"traces": {' + out_str_list.strip(', ') + '}'


def adjust_raw_json(string):
    return json.loads(dict(string)['行为轨迹'].replace('\'', '"'))


with open('raw_track0213.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    traces = [row for row in reader]

write_list = []
for item in traces:
    print('---------------------------')
    try:
        data = item_analysis(adjust_raw_json(item))
        write_list.append(data)
        print(data)
    except json.decoder.JSONDecodeError:
        write_list.append('"traces": {}')
        print('error')


data = pd.read_csv(r'raw_track0213.csv')

data['structure_traces'] = write_list
data.to_csv(r"structure_traces_data_0213.csv", mode='a', index=False, quoting=2)


'''
testCases = [document]
for sentence in testCases: print(HanLP.segment(sentence))
# 关键词提取

print(HanLP.extractSummary(document, 3))
print((HanLP.parseDependency(document)))
'''
