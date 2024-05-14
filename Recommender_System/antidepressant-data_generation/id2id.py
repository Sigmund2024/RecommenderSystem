def generate_file(n, output_file):
    with open(output_file, 'w') as file:
        for k in range(1, n + 1):
            file.write(f"{k}\t{k}\n")

# 输入数字n和输出文件路径
n = 155  # 你可以根据需要修改n的值
output_file = 'Recommender_System/antidepressant-data_generation/data/item_id2entity_id.txt'  # 输出文件路径

generate_file(n, output_file)
print(f"已生成文件：{output_file}")
