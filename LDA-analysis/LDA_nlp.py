import csv
import json
from pyhanlp import *
from gensim import corpora, models
import pandas as pd
HanLP.newSegment().enableOrganizationRecognize(True)
HanLP.newSegment().enableNameRecognize(True)
HanLP.newSegment().enablePlaceRecognize(True)

# archive
string_words_ls = []
texts = []
topic_ls = []
score_ls = []
write_list = []  # Last Step


# read data
def adjust_raw_json(string):
    return json.loads(dict(string)['行为轨迹'].replace('\'', '"'))


# read csv column
with open('raw_traces_0220.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    traces = [row for row in reader]


# filter
del_nature = {'d', 'rz', 'rzv', 'm', 'mq', 'q', 'qt', 'c', 'f', 't', 'b', 'tg', 'ad', 'qv', 'w'}
stop_words = {'经', '到', 'D', 'G', '在', '与', '的', '从', '为', '回', '回到', '自', '站', '村', '出租车', '至', '无', '武汉',
              '五院', '冠状病毒', '人', '有', '返', '超市', '医疗机构', '医院', '返回', '人民医院', '由', '于', '市', '过', '去',
              '定点', '小区', '珠海', '病情', '患者', '私家车', '治疗', '前往', '卫生院', '肺炎', '车', '下车', '等', '父母',
              '阜阳市第二人民医院', '稳定', '开车', '一家', '检测', '区', '病', '大', '中大', '救护车', '并', '妻子', '口罩', '-',
              '平稳', '和县'}
# place = {'ns', 'nis', 'nsf', 'nth', 'ntcb'}
white_words = {'发热', '症状', '出现', '就诊', '门诊', '家中', '外出', '隔离', '在家', '感染', '入院', '就诊', '确诊', '逗留',
               '发病', '抵达', '乘坐', '乘', '自驾', '高铁', '回家', '到达', '乘坐', '输液', '咳嗽', '聚集', '聚餐', '聚', '吃饭',
               '一起', '餐馆', '治疗'}


# tokenize
def token_analysis(string):
    word_ls = []
    seg = HanLP.segment(string)
    # print('@', seg)
    seg_len = len(seg)
    flag = 0
    for i, term in zip(range(seg_len), seg):
        # if str(term.nature) not in del_nature and term.word not in stop_words:
        if term.word in white_words:
            word_ls.append(term.word)
            flag = 1
    if not flag:
        for i, term in zip(range(seg_len), seg):
            if str(term.nature) not in del_nature and term.word not in stop_words:
                word_ls.append(term.word)
    return word_ls


def json_analysis(info):
    for key, _val in info.items():
        string_words_ls.append(token_analysis(HanLP.extractSummary(_val, 3)[0]))
        texts.append(_val)
    return ''


print('Analyzing', len(traces), 'items.')
for item in traces:
    try:
        data = json_analysis(adjust_raw_json(item))
    except json.decoder.JSONDecodeError:
        print('error')

dictionary = corpora.Dictionary(string_words_ls)
# 基于词典，使【词】→【稀疏向量】，并将向量放入列表，形成【稀疏向量集】
corpus = [dictionary.doc2bow(words) for words in string_words_ls]
# lda模型，num_topics设置主题的个数
lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=5)
# 展示所有主题，每个主题显示5个词
for topic in lda.print_topics(num_words=5):
    print(topic)

for e, values in enumerate(lda.inference(corpus)[0]):

    topic_val = 0
    topic_id = 0
    for tid, val in enumerate(values):
        if val > topic_val:
            topic_val = val
            topic_id = tid
    # print(e, ': Topic: %d, score=%.2f ' % (topic_id, topic_val), texts[e])
    topic_ls.append(str(topic_id))
    score_ls.append(str(topic_val))


def merge_info(info, _id):
    outcome = '{'
    string = ''
    for key, _val in info.items():
        string += '"' + key + '": "'
        string += topic_ls[_id] + '", '
        _id += 1
    string = string.strip(", ")
    return outcome + string + '}', _id


_id = 0
for item in traces:
    print('---------------------------')
    try:
        data, _id = merge_info(adjust_raw_json(item), _id)
        write_list.append(data)
        print(data)
    except json.decoder.JSONDecodeError:
        write_list.append('"traces": {}')
        print('Error')
        break


data = pd.read_csv(r'raw_traces_0220.csv')
data['topic'] = write_list
data.to_csv(r"topic_data_0220x.csv", mode='a', index=False, quoting=2)


'''
testCases = [document]
for sentence in testCases: print(HanLP.segment(sentence))
# 关键词提取

print(HanLP.extractSummary(document, 3))
print((HanLP.parseDependency(document)))
'''
