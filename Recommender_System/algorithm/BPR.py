import time
import sys
import pandas as pd
import tensorflow as tf
import numpy as np

from libreco.algorithms import BPR
from libreco.data import DatasetPure, split_by_ratio_chrono,random_split
from sklearn.metrics import roc_auc_score

#指标计算函数
#HR
def hit_rate(test_data, recommend_data):
    hits = 0
    len_real_items=0
    for user in recommend_data:
        test_items = test_data[user]
        len_real_items+=len(test_items)
        recommender_items=recommend_data[user]
        #print("user:",user,"items:",recommender_items)
        for item in recommender_items:
            #print("item is :",item)
            if item in test_items:
                hits += 1
    return hits / len_real_items

#PPV
def precision(test_data, recommend_data):
    true_positives = 0
    false_positives = 0

    for user, items in recommend_data.items():
        test_items = test_data[user]
        for item in items:
            if item in test_items:
                true_positives += 1
            else:
                false_positives += 1

    if true_positives + false_positives == 0:
        return 0
    else:
        return true_positives / (true_positives + false_positives)

#recall
def recall(test_data,recommend_data):
    true_ps = 0  # 预测里为正例（预测正确）的数量
    positive_sample = 0  # 所有正例样本数量
    # 计算positive_sample
    for user_id, item_id_list in test_data.items():
        for item_id in item_id_list:
            positive_sample += 1
    # 计算true_ps
    for user_id, item_id_list in recommend_data.items():
        for item_id in item_id_list:
            if item_id in test_data[user_id]:
                true_ps += 1
    # 计算recall
    return true_ps / positive_sample

#F1
def F1(recall,precision):
    return (2*precision*recall)/(precision+recall) #f1计算公式，precision即ppv

#RCI
def recall_coverage_index(recommend_data, total_items):
    unique_items = set()
    for user,items in recommend_data.items():
        for item in items:
            unique_items.add(item)
            #print("user is :",user,", item is :",item)
    return len(unique_items) / total_items

#ROC-AUC
def roc_auc(predicted_scores,actual_behavior):
    total_auc = 0.0
    for i in range(predicted_scores.shape[0]):  # 遍历每个用户
        # 获取当前用户的预测评分和实际行为
        user_predicted_scores = predicted_scores[i]
        user_actual_behavior = actual_behavior[i]

        # 计算当前用户的 ROC-AUC
        #print(user_predicted_scores,user_actual_behavior)
        user_auc = roc_auc_score(user_actual_behavior, user_predicted_scores)
        #print(f"User {i+1} ROC-AUC:", user_auc)

        # 累加到总的 ROC-AUC
        total_auc += user_auc

    # 计算平均 ROC-AUC
    average_auc = total_auc / predicted_scores.shape[0]
    return average_auc

if __name__ == "__main__":
    start_time = time.perf_counter()
    data = pd.read_csv(
        "Recommender_System/sample_data/shuffle_user_rating.dat",
        sep="::",
        names=["user", "item", "label", "time"],
    )

    metrics = [
        "loss",
        "balanced_accuracy",
        "roc_auc",
        "pr_auc",
        "precision",
        "recall",
        "map",
        "ndcg",
    ]   

    train_data, eval_data, test_data = random_split(data, multi_ratios=[0.7, 0.15, 0.15])
    train_data, data_info = DatasetPure.build_trainset(train_data)
    eval_data = DatasetPure.build_evalset(eval_data)
    test_data = DatasetPure.build_testset(test_data)
    print("data_info:")
    print(data_info)

    bpr = BPR(
        "ranking",
        data_info,
        loss_type="bpr",
        embed_size=16,
        n_epochs=10,
        lr=3e-4,
        reg=None,
        batch_size=256,
        num_neg=1,
        use_tf=True,
        optimizer="adam",
        num_threads=4,
    )
    bpr.fit(
        train_data,
        neg_sampling=True,
        verbose=2,
        shuffle=True,
        eval_data=eval_data,
        metrics=metrics,
    )

    #测试预测结果
    print("prediction: ", bpr.predict(user=40, item=1))
    print("batch prediction",bpr.predict(user=[1,3,5,7,9,11],item=57))
    print("recommendation: ", bpr.recommend_user(user=44, n_rec=7))
    print("batch recommendation: ", bpr.recommend_user(user=[1, 2, 3], n_rec=7))

    # 测试集数据列表：用户-[多个项目]
    test_user_items = {}
    for user, item, label in test_data:
        if user not in test_user_items:
            test_user_items[user] = []
        if label >= 1:
            test_user_items[user].append(item)

    #测试集中的用户和项目列表
    user_column = list(set(test_data.user_indices))
    #print(user_column[:200])
    print("len of test_data_user_column is:",len(user_column))
    len_test_user=len(user_column)
    item_column = list(set(test_data.item_indices))
    print("len of test_data_item_column is:",len(item_column))
    len_test_item=len(item_column)

    # 创建用户ID和项目ID的映射字典
    user_id_map = {user_id: i for i, user_id in enumerate(user_column)}
    item_id_map = {item_id: i for i, item_id in enumerate(item_column)}
    # print(user_id_map)
    # print(item_id_map)
    user_id_map_reverse = {i:user_id for i, user_id in enumerate(user_column)}
    item_id_map_reverse = {i:item_id for i, item_id in enumerate(item_column)}

    
    #推荐的列表：用户-[指定k个项目]
    recommend_user_items = {}
    for user in user_column:
        #k=len(test_user_items[user])
        rec_items = bpr.recommend_user(user=user, n_rec=25)      
        recommend_user_items[user] = rec_items[user]
        
    # 计算ppv和recall
    p = precision(test_user_items, recommend_user_items)
    r = recall(test_user_items, recommend_user_items)

    print("Hit Rate:", hit_rate(test_user_items, recommend_user_items))
    print("Precision:", p)
    print("Recall:", r)
    print("F1:", F1(r, p))


