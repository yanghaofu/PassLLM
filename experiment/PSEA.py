from sklearn.metrics import cohen_kappa_score, f1_score, precision_score, recall_score
import numpy as np


def evaluate_password_strength(model_predictions, true_labels):
    """
    评估大模型的口令强度评估准确性和一致性。

    :param model_predictions: 大模型对口令强度的评估结果
    :param true_labels: 口令模型的真实强度标签
    :return: kappa系数和F1-score
    """
    # 计算Kappa系数
    kappa = cohen_kappa_score(true_labels, model_predictions)

    # 计算F1-score
    f1 = f1_score(true_labels, model_predictions, average='weighted')

    # 计算精确率和召回率
    precision = precision_score(true_labels, model_predictions, average='weighted')
    recall = recall_score(true_labels, model_predictions, average='weighted')

    return kappa, f1, precision, recall