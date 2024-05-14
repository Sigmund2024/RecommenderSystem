#读取下面几个文件：drugs.json，记录了药物所属的类别；drug2id.txt，记录了药物的字符串名称对应id；
#生成kg.txt，知识图谱，记录药物之间的关系，这里的关系指的是：两个药物同属于一个类别。
#kg.txt的格式是：药物id1\t关系\t药物id2
import json

# 读取 drugs.json 文件，记录药物所属的类别
def read_drugs_json(file_path):
    with open(file_path, 'r') as file:
        drugs_data = json.load(file)
    return drugs_data

# 读取 drug2id.txt 文件，记录药物的字符串名称对应id
def read_drug2id(file_path):
    drug2id = {}
    with open(file_path, 'r') as file:
        for line in file:
            drug, drug_id = line.strip().split('\t')
            drug2id[drug] = drug_id
    return drug2id

# 生成 kg.txt 文件，记录药物之间的关系（同属于一个类别）
def generate_kg(drugs_data, drug2id, output_file):
    with open(output_file, 'w') as file:
        for category, drugs_list in drugs_data.items():
            for i in range(len(drugs_list)):
                for j in range(i + 1, len(drugs_list)):
                    drug1_id = drug2id.get(drugs_list[i])
                    drug2_id = drug2id.get(drugs_list[j])
                    if drug1_id and drug2_id:
                        file.write(f"{drug1_id}\t{category}\t{drug2_id}\n")

# 输入文件路径和输出文件路径
drugs_json_file = 'Recommender_System/antidepressant-data_generation/data/drugs.json'
drug2id_file = 'Recommender_System/antidepressant-data_generation/data/drug2id.txt'
output_kg_file = 'Recommender_System/antidepressant-data_generation/data/kg.txt'

# 读取数据并生成知识图谱文件
drugs_data = read_drugs_json(drugs_json_file)
drug2id = read_drug2id(drug2id_file)
generate_kg(drugs_data, drug2id, output_kg_file)

print(f"已生成知识图谱文件：{output_kg_file}")


