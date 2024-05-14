from typing import List, Callable, Dict
from Recommender_System.utility.evaluation import TopkData, topk_evaluate


def log(epoch, train_loss, train_auc, train_precision, train_recall, test_loss, test_auc, test_precision, test_recall):
    pr_train = train_precision + train_recall
    train_f1 = 2. * train_precision * train_recall / pr_train if pr_train else 0

    pr_test = test_precision + test_recall
    test_f1 = 2. * test_precision * test_recall / pr_test if pr_test else 0

    print('epoch=%d, train_loss=%.5f, train_auc=%.5f, train_f1=%.5f, test_loss=%.5f, test_auc=%.5f, test_f1=%.5f' %
          (epoch + 1, train_loss, train_auc, train_f1, test_loss, test_auc, test_f1))



def topk(topk_data: TopkData, score_fn: Callable[[Dict[str, List[int]]], List[float]], ks=[10, 15, 25]):
    # 使用 topk_evaluate 函数获取命中率、精确率、召回率和 F1 分数
    hrs, precisions, recalls, f1s = topk_evaluate(topk_data, score_fn, ks)

    # 遍历所有的 k 值和对应的性能指标
    for k, hr, precision, recall, f1 in zip(ks, hrs, precisions, recalls, f1s):
        # 打印每个 k 值的命中率、精确率、召回率和 F1 分数
        print('[k=%d, HR=%.3f%%, Precision=%.3f%%, Recall=%.3f%%, F1=%.3f%%]' %
              (k, 100. * hr, 100. * precision, 100. * recall, 100. * f1), end=' ')
    print()  # 在所有结果打印完后换行