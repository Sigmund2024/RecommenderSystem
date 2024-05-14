import random
import pandas as pd

def shuffle_and_save_data(input_file, output_file):
    # 读取数据
    with open(input_file, 'r') as file:
        data_lines = file.readlines()

    # 打乱数据
    random.shuffle(data_lines)

    # 保存数据
    with open(output_file, 'w') as file:
        file.writelines(data_lines)

# 打乱数据集user_data.dat,并保存到shuffle_user_data.dat
shuffle_and_save_data('Recommender_System/antidepressant-data_generation/data/user_rating.dat',
                      'Recommender_System/antidepressant-data_generation/data/shuffle_user_rating.dat')

# 打乱数据集pinsage_data.dat,并保存到shuffle_pinsage_data.dat
shuffle_and_save_data('Recommender_System/antidepressant-data_generation/data/pinsage_data.dat',
                      'Recommender_System/antidepressant-data_generation/data/shuffle_pinsage_data.dat')
