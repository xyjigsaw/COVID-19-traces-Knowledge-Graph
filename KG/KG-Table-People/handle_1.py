'''
那边好了之后构建一个患者表，用于存放基于患者id的患者基本信息，性别、年龄、姓名
之后构建一个<患者,地点>表
<患者id, 地点id>
'''
import pandas as pd
import csv
data=pd.read_csv('raw_traces_0222.csv',header=None)
 #必须添加header=None，否则默认把第一行数据处理成列名导致缺失
list_csv=data.values.tolist()
flag=1

fileHeader = ["id","name","age","gender","position"]
csvFile = open("huanzhe.csv", "w",encoding='utf-8-sig')
writer = csv.writer(csvFile)
writer.writerow(fileHeader)

for single_row in list_csv:
    if flag:
        flag=0
        continue
    
    mixed=single_row[3]
    if '男' in mixed:
        gender='男'
    elif '女' in mixed:
        gender='女'
    else:
        gender=''
    
    if '岁' in mixed:
        n_pos=mixed.find('岁')
        age=mixed[(n_pos-2)]+mixed[(n_pos-1)]+'岁'
    elif "年" in mixed:
        n_pos=mixed.find('年')
        age=str(2020-int('19'+mixed[(n_pos-2)]+mixed[(n_pos-1)]))+'岁'
    else:
        age=''

    name_count=mixed.count('某')
    if name_count>0:
        n_pos=mixed.find('某')
        if name_count==1:
            name=mixed[(n_pos-1)]+'某'
        elif name_count==2:
            name=mixed[(n_pos-1)]+'某某'
        elif name_count==3:
            name=mixed[(n_pos-1)]+'某某某'
    else:
            name=''      

    if '例' in mixed:
        if '确'in mixed:
            if '号':
                if '，'in mixed:
                    name=mixed.split('，')[0]


    position=single_row[1]
    id_1=str(int(single_row[0]))

    writer.writerow([id_1,name,age,gender,position])
    

csvFile.close()