import json

def read_drugs_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        drugs_data = json.load(file)
    return drugs_data

def map_drugs_to_indices(drugs_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        index = 1
        for category, drugs in drugs_data.items():
            for drug in drugs:
                file.write(f"{drug}\t{index}\n")
                index += 1

# 从JSON文件中读取药物数据
drugs_data = read_drugs_data('Recommender_System/antidepressant-data_generation/data/drugs.json')

# 生成索引文件
output_file = 'Recommender_System/antidepressant-data_generation/data/help_info/drugs_list.txt'
map_drugs_to_indices(drugs_data, output_file)
print(f"药物名词和索引已写入文件：{output_file}")
