import random
#随机生成15-25个药物记录，并将数量随机分配到drug_category的每个大类中
num_records = random.randint(15, 25)
print(num_records)
#把num_records分成三个不小于5的正整数，分别对应drug_category的三个大类
num1 = random.randint(5, num_records-10)
num2 = random.randint(5, num_records-num1-5)
num3 = num_records-num1-num2
print(num1, num2, num3)

#将以上的程序循环5000次，统计每个大类的药物记录数量。