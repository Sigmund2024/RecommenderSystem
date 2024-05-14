import json

# 读取user_data.dat文件
user_data = {}
with open('Recommender_System/antidepressant-data_generation/data/user_data.dat', 'r') as file:
    for line in file:
        user, age, sex, MADRS_Score, HAM_A_Score = line.strip().split('\t')
        user_data[user] = {'sex': sex, 'age': age, 'MADRS-Score': MADRS_Score, 'HAM-A-Score': HAM_A_Score}

#print(user_data)
# 读取user_rating.dat文件
user_rating = []
with open('Recommender_System/antidepressant-data_generation/data/user_rating.dat', 'r') as file:
    for line in file:
        user, item, label, time = line.strip().split('::')
        user_rating.append({'user': user, 'item': item, 'label': label, 'time': time})
#print(user_rating)
# 读取drugs.json文件
with open('Recommender_System/antidepressant-data_generation/data/drugs.json', 'r') as file:
    drugs_data = json.load(file)

# 读取drug2id.txt文件
id2drug = {}
with open('Recommender_System/antidepressant-data_generation/data/drug2id.txt', 'r') as file:
    for line in file:
        drug, drug_id = line.strip().split('\t')
        id2drug[drug_id] = drug

# 生成pinsage_data.dat文件
with open('Recommender_System/antidepressant-data_generation/data/pinsage_data.dat', 'w') as file:
    for record in user_rating:
        user_info = user_data.get(record['user'])
        if user_info:
            user_id = record['user']
            item_id = record['item']
            label=record['label']
            time=record['time']
            sex = user_info['sex']
            age = user_info['age']
            MADRS_Score = user_info['MADRS-Score']
            HAM_A_Score = user_info['HAM-A-Score']
            item_name=id2drug[item_id]
            if item_id:
                item_type = None
                for drug_type, drugs_list in drugs_data.items():
                    if item_name in drugs_list:
                        item_type = drug_type
                        break
                file.write(f"{user_id},{item_id},{label},{time},{sex},{age},{MADRS_Score},{HAM_A_Score},{item_type}\n")
                #输出用户-药物-评分-时间戳-性别-年龄-MADRS评分-HAM-A评分-药物类型
                print({user_id},{item_id},{label},{time},{sex},{age},{MADRS_Score},{HAM_A_Score},{item_type})
