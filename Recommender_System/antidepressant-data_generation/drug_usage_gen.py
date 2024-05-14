import random
import json
import os
import sys

# 从JSON文件中读取药物数据
def read_drugs_data(filename):
    with open(filename, 'r') as file:
        drugs_data = json.load(file)
    for category, drugs_list in drugs_data.items():
        print(category,':',drugs_list,len(drugs_list))
    return drugs_data

# 从文件中读取用户信息
def read_user_data(filename):
    users_data = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            user_id = int(parts[0])
            age = int(parts[1])
            gender = int(parts[2])
            madrs_score = int(parts[3])
            hama_score = int(parts[4])
            users_data.append({'id': user_id, 'age': age, 'gender': gender, 'MADRS-Score': madrs_score, 'HAM-A-Score': hama_score})
    return users_data

def generate_medication_records(users_data, drugs_data):
    for user in users_data:
        #一行输出用户信息
        print(user['id'],',',user['age'],',',user['MADRS-Score'],',',user['HAM-A-Score'])
        #根据用户的年龄和抑郁/焦虑程度为每个用户选择药物的大类，总共有7种大类,
        drug_category = []
        #10-18岁
        if user['age'] >= 10 and user['age'] <= 18:
            #(3,1)(3,2)(3,3)(2,3)的情况下，从SSRIs、SNRIs、Atypical Antidepressants中选择
            if user['MADRS-Score']==3 and user['HAM-A-Score']==1 or user['MADRS-Score']==3 and user['HAM-A-Score']==2 or user['MADRS-Score']==3 and user['HAM-A-Score']==3 or user['MADRS-Score']==2 and user['HAM-A-Score']==3:
                drug_category = ['SSRIs', 'SNRIs', 'Atypical_Antidepressants']
            #(2,1)的情况下，从SSRIs、Atypical Antidepressants中选择
            elif user['MADRS-Score']==2 and user['HAM-A-Score']==1:
                drug_category = ['SSRIs', 'Atypical_Antidepressants']
            #其他情况下，从SSRIs、SNRIs中选择
            else:
                drug_category = ['SSRIs', 'SNRIs']
        #19-39岁 40-59岁
        elif (user['age'] >= 19 and user['age'] <= 39) or (user['age'] >= 40 and user['age'] <= 59):
            #(2,1)的情况下，七类药物中选择两类
            if user['MADRS-Score']==2 and user['HAM-A-Score']==1:
                drug_category = random.sample(['SSRIs', 'SNRIs', 'Atypical_Antidepressants', 'Tricyclic_and_Tetracyclic_Antidepressants', 'MAOIs', 'NMDA_Antagonist', 'GABA-A_Receptor_Positive_Modulator'], 2)
            #(3,1)的情况下，七类药物中选择三类
            elif user['MADRS-Score']==3 and user['HAM-A-Score']==1:
                drug_category = random.sample(['SSRIs', 'SNRIs', 'Atypical_Antidepressants', 'Tricyclic_and_Tetracyclic_Antidepressants', 'MAOIs', 'NMDA_Antagonist', 'GABA-A_Receptor_Positive_Modulator'], 3)
            #(3,2)的情况下，七类药物中选择四类
            elif user['MADRS-Score']==3 and user['HAM-A-Score']==2:
                drug_category = random.sample(['SSRIs', 'SNRIs', 'Atypical_Antidepressants', 'Tricyclic_and_Tetracyclic_Antidepressants', 'MAOIs', 'NMDA_Antagonist', 'GABA-A_Receptor_Positive_Modulator'], 4)
            #(1,1)(1,2)的情况下，必须包含SNRIs，额外的类药物中选择一类
            elif user['MADRS-Score']==1 and user['HAM-A-Score']==1 or user['MADRS-Score']==1 and user['HAM-A-Score']==2:
                drug_category = ['SNRIs'] + random.sample(['SSRIs', 'Atypical_Antidepressants', 'Tricyclic_and_Tetracyclic_Antidepressants', 'MAOIs', 'NMDA_Antagonist', 'GABA-A_Receptor_Positive_Modulator'], 1)
            #(2,2)(1,3)的情况下，必须包含SNRIs，额外的类药物中选择两类
            elif user['MADRS-Score']==2 and user['HAM-A-Score']==2 or user['MADRS-Score']==1 and user['HAM-A-Score']==3:
                drug_category = ['SNRIs'] + random.sample(['SSRIs', 'Atypical_Antidepressants', 'Tricyclic_and_Tetracyclic_Antidepressants', 'MAOIs', 'NMDA_Antagonist', 'GABA-A_Receptor_Positive_Modulator'], 2)
            #(3,3)(2,3)的情况下，必须包含SNRIs，额外的类药物中选择三类
            else:
                drug_category = ['SNRIs'] + random.sample(['SSRIs', 'Atypical_Antidepressants', 'Tricyclic_and_Tetracyclic_Antidepressants', 'MAOIs', 'NMDA_Antagonist', 'GABA-A_Receptor_Positive_Modulator'], 3)   
        #60-80岁
        else:
            #必须在SSRIs和Atypical Antidepressants中选择
            drug_category = ['SSRIs', 'Atypical_Antidepressants']

        #选择了药物大类后，为每个用户生成药物记录，并确保其选择的每个大类的药物都被覆盖
        #'SSRIs', 'SNRIs', 'Atypical_Antidepressants', 'Tricyclic_and_Tetracyclic_Antidepressants', 'MAOIs', 'NMDA_Antagonist', 'GABA-A_Receptor_Positive_Modulator'七类药物对应的选取数量为
        #8-15, 5-7, 10-15, 2-4, 2-4, 1-3, 4-7
        #创建一个字典，记录每个大类药物的选取的最大数量和最小数量
        drug_category_num = {'SSRIs': [8,15], 'SNRIs': [5,7], 'Atypical_Antidepressants': [10, 15], 'Tricyclic_and_Tetracyclic_Antidepressants': [2, 4], 'MAOIs': [2, 4], 'NMDA_Antagonist': [1, 3], 'GABA-A_Receptor_Positive_Modulator': [4, 7]}
        #根据选取的数量，生成该用户的药物记录
        user['medication'] = []
        for category in drug_category:
            random.seed()
            num = random.randint(drug_category_num[category][0], drug_category_num[category][1])
            random.seed()
            drug=random.sample(drugs_data[category], num)
            user['medication'] += drug
            #一行输出用户选择的药物大类和药物
            print(category,':',drug)
        #打乱药物记录的顺序
        random.shuffle(user['medication'])

#生成用户-药物-评分-时间戳格式的数据集
def generate_data(users_data):
    data = []
    for user in users_data:
        user_id = user['id']
        for drug in user['medication']:
            # if drug in ["Asendin", "Asendis", "Defanyl", "Demolox", "Duxil", "Esmolax", "Moxadil", "Viibryd"]:
            #     print(drug)
            data.append({'user_id': user_id, 'drug': drug, 'rating': random.randint(1, 5), 'timestamp': random.randint(1, 1000000000)})
    return data
#main函数
if __name__ == '__main__':
    print(os.getcwd())
    #读取用户信息
    users_data = read_user_data('Recommender_System/antidepressant-data_generation/data/user_data.dat')
    #读取药物信息
    drugs_data = read_drugs_data('Recommender_System/antidepressant-data_generation/data/drugs.json')
    #生成用户的药物记录
    generate_medication_records(users_data, drugs_data)
    #生成数据集
    data = generate_data(users_data)
    #通过drug2id.txt文件将药物名转换为id
    drug2id={}
    with open('Recommender_System/antidepressant-data_generation/data/drug2id.txt', 'r') as file:
        for line in file:
            cols = line.strip().split('\t')
            drug2id[cols[0]]=cols[1]
    print(drug2id)
    #将生成的数据集写入文件,形式为1425::1354::5::1024172237
    with open('Recommender_System/antidepressant-data_generation/data/user_rating.dat', 'w') as file:
        for record in data:
            file.write(f"{record['user_id']}::{drug2id[record['drug']]}::{record['rating']}::{record['timestamp']}\n")
