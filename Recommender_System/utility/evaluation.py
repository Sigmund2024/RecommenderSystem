from dataclasses import dataclass
from typing import Tuple, List, Callable, Dict


@dataclass
class TopkData:
    test_user_item_set: dict  # 在测试集上每个用户可以参与推荐的物品集合
    test_user_positive_item_set: dict  # 在测试集上每个用户有行为的物品集合


@dataclass
class TopkStatistic:
    hit: int = 0  # 命中数
    ru: int = 0  # 推荐数
    tu: int = 0  # 行为数
    h_user: int = 0  # 命中用户数

# 定义函数topk_evaluate，用于进行TopK评估
def topk_evaluate(epoch,topk_data: TopkData, score_fn: Callable[[Dict[str, List[int]]], List[float]],
                  ks=[1, 2, 5, 10, 15, 20, 30]) -> Tuple[List[float], List[float],List[float],List[float]]:
    #print("epoch==================================",epoch)
    # 初始化保存TopK指标的字典，键为k值，值为TopkStatistic对象
    kv = {k: TopkStatistic() for k in ks}
    #用户命中率
    h=0
    # 遍历测试集中每个用户的可推荐物品集合
    for user_id, item_set in topk_data.test_user_item_set.items():
        # 构建字典ui，包含用户id和其可推荐物品集合
        ui = {'user_id': [user_id] * len(item_set), 'item_id': list(item_set)}
        # 计算每个物品的得分并排序，得到排序后的物品列表
        item_score_list = list(zip(item_set, score_fn(ui)))
        sorted_item_list = [x[0] for x in sorted(item_score_list, key=lambda x: x[1], reverse=True)]
        #如果epoch=10,那么存储每个用户的排序后的物品列表
        if epoch==9:
            print('user_id:',user_id)
            with open('Recommender_System/sorted_rec_result.txt','a') as f:
                f.write(str(user_id)+'::'+str(sorted_item_list)+'\n')
        # 获取用户在测试集中的正样本集合
        positive_set = topk_data.test_user_positive_item_set[user_id]
        # 遍历每个k值
        for k in ks:
            # 取前k个物品作为推荐结果，并计算命中数、推荐数和正样本数
            topk_set = set(sorted_item_list[:k])
            kv[k].hit += len(topk_set & positive_set)
            if len(topk_set & positive_set) !=0:
                kv[k].h_user += 1
            kv[k].ru += len(topk_set)
            kv[k].tu += len(positive_set)
            # 计算ppv,recall,f1,hit
    p=[kv[k].hit / kv[k].ru for k in ks]
    r=[kv[k].hit / kv[k].tu for k in ks]
    f1=[(2 * p[i] * r[i]) / (p[i] + r[i]) if (p[i] + r[i]) != 0 else 0 for i in range(len(p))]
    h=[kv[k].h_user/len(topk_data.test_user_item_set) for k in ks]

    return h,p, r, f1 # hit,precision, recall,f1，
