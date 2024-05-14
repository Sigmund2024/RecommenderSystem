def count_value_in_second_column(file_path, value):
    # 打开dat文件
    with open(file_path, 'r') as file:
        # 初始化计数器
        count = 0
        # 逐行读取文件内容
        for line in file:
            # 分割每行数据，以双冒号(::)作为分隔符
            data = line.strip().split('::')
            # 检查第n列是否为指定的值，并增加计数器
            if data[0] == value:
                count += 1
    return count

def main():
    # 文件路径
    file_path = 'sample_data/sample_movielens_rating.dat'
    # 要计数的值
    value = '12'
    # 调用函数计算第n列中值为value的数量
    count = count_value_in_second_column(file_path, value)
    # 输出结果
    print("第1列中值为", value, "的数量：", count)

if __name__ == "__main__":
    main()
