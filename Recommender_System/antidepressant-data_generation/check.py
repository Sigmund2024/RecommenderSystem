from collections import defaultdict

def count_occurrences(input_file, col1_idx, col2_idx, sep):
    # 使用 defaultdict 初始化两个计数器
    col1_counts = defaultdict(int)
    col2_counts = defaultdict(int)

    # 读取数据并统计出现次数
    with open(input_file, 'r') as file:
        for line in file:
            cols = line.strip().split(sep)
            if len(cols) >= max(col1_idx, col2_idx) + 1:
                col1_counts[cols[col1_idx]] += 1
                col2_counts[cols[col2_idx]] += 1

    # 按照数据的升序输出
    sorted_col1_counts = dict(sorted(col1_counts.items(), key=lambda item: int(item[0])))
    sorted_col2_counts = dict(sorted(col2_counts.items(), key=lambda item: int(item[0])))

    return sorted_col1_counts, sorted_col2_counts

input_file = 'Recommender_System/antidepressant-data_generation/data/user_rating.dat'  # 输入文件路径
col1_idx = 0  # 第一列的索引（从0开始）
col2_idx = 1  # 第二列的索引（从0开始）
sep = '::'  # 分隔符

col1_counts, col2_counts = count_occurrences(input_file, col1_idx, col2_idx, sep)

# print("按照第一列的数据升序输出：")
# for key, value in col1_counts.items():
#     print(f"{key}: {value}")

print("\n按照第二列的数据升序输出：")
counter=0;
for key, value in col2_counts.items():
    print(f"{key}: {value}")
    counter=counter+1

print(counter)

# 读取数据并统计出现次数
data = []
with open(input_file, 'r') as file:
    for line in file:
        cols = line.strip().split(sep)
        data.append([int (cols[0]), int (cols[1]), int (cols[2]), int (cols[3])])
n_user, n_item = len(set(d[0] for d in data)), len(set(d[1] for d in data))
print(n_user, n_item)