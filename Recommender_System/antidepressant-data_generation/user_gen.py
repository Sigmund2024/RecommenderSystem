import random
import pandas as pd
# 定义年龄范围和比例
age_ranges = [(10, 18, 0.10), (19, 39, 0.35), (40, 59, 0.35), (60, 80, 0.20)]

# 定义性别比例
gender_ratio = {0: 4, 1: 6}  # 0表示男性，1表示女性

# 定义MADRS-Score和HAM-A-Score比例
madr_ham_ratios = {(2, 1): 0.25, (3, 1): 0.20, (3, 2): 0.15,
                   (1, 1): 0.10, (2, 2): 0.10, (3, 3): 0.05,
                   (1, 2): 0.05, (1, 3): 0.05, (2, 3): 0.05}

# 生成用户数据
# 生成原则：
# 10-18岁：
# 主要选择青少年适用的抗抑郁药物，如某些SSRIs和Atypical Antidepressants类别的药物。
# 这个年龄段的用户通常需要较轻和适宜青少年使用的药物。
# 19-39岁：
# 可以选择更广泛的抗抑郁药物，包括SSRIs、SNRIs、Atypical Antidepressants等。
# 这个年龄段的用户对不同类别的药物可能有更好的耐受性和反应。
# 40-59岁：
# 除了SSRIs、SNRIs、Atypical Antidepressants外，也可以考虑Tricyclic and Tetracyclic Antidepressants和MAOIs这类药物。
# 因为这些药物可能更适合中年人的生理特征和病情。
# 60-80岁：
# SSRIs、Atypical Antidepressants等，同时避免选择对老年人不适宜的药物，如Tricyclic and Tetracyclic Antidepressants和MAOIs。
# 对于老年人群体，更需要考虑药物的安全性和耐受性。因此，主要选择安全性较高的抗抑郁药物。

# 药物选取原则：          1      2         3                           4                                         5      6                         7             
# 10-18岁使用的药物范围：SSRIs、SNRIs、   Atypical Antidepressants
# 19-39岁使用的药物范围：SSRIs、SNRIs、   Atypical Antidepressants、Tricyclic and Tetracyclic Antidepressants、MAOIs、NMDA Antagonist、GABA-A Receptor Positive Modulator
# 40-59岁使用的药物范围：SSRIs、SNRIs、   Atypical Antidepressants、Tricyclic and Tetracyclic Antidepressants、MAOIs、NMDA Antagonist、GABA-A Receptor Positive Modulator
# 60-80岁使用的药物范围：SSRIs、          Atypical Antidepressants

# 根据焦虑程度细化原则：
# 抑郁程度大于焦虑程度：              10-18               19-39           40-59                           60-80
#                     2 1 25%         1、3任选           七种选两种      七种选两种                      两种任选
#                     3 1 20%         1、2、3任选        七种选三种      七种选三种                      两种任选
#                     3 2 15%         1、2、3任选        七种选四种       七种选四种                     两种任选
# 抑郁程度等于焦虑程度：
#                     1 1 10%          1、2任选          SNRIs+任意一种   SNRIs+任意一种                  两种任选
#                     2 2 10%          1、2任选          SNRIs+任意两种   SNRIs+任意两种                  两种任选
#                     3 3 5%           1、2、3任选       SNRIs+任意三种   SNRIs+任意三种                  两种任选         
# 抑郁程度小于焦虑程度
#                     1 2 5%            1、2任选          SNRIs+任意一种    SNRIs+任意一种                两种任选
#                     1 3 5%            1、2任选          SNRIs+任意两种    SNRIs+任意两种                两种任选
#                     2 3 5%            1、2、3任选       SNRIs+任意三种    SNRIs+任意三种                两种任选
def generate_user_data(num_users):
    users = []
    for _ in range(num_users):
        # 随机选择年龄范围和性别
        age_range = random.choices(age_ranges, weights=[r[2] for r in age_ranges])[0]
        age = random.randint(age_range[0], age_range[1])
        gender = random.choices(list(gender_ratio.keys()), weights=gender_ratio.values())[0]
        
        # 随机选择MADRS-Score和HAM-A-Score
        madr_ham_score = random.choices(list(madr_ham_ratios.keys()), weights=madr_ham_ratios.values())[0]
        
        # 构建用户信息并添加到用户列表
        user = {'age': age, 'gender': gender, 'MADRS-Score': madr_ham_score[0], 'HAM-A-Score': madr_ham_score[1]}
        users.append(user)
    
    return users

# 生成用户数据
num_users = 10000
user_data = generate_user_data(num_users)

df = pd.DataFrame(user_data, index=range(1, num_users + 1))

# 保存DataFrame到dat文件，使用制表符作为分隔符
df.to_csv('user_data.dat', sep='\t')

# 打印生成的用户数据
for user in user_data:
    print(user)
