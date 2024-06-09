import pandas as pd
from sklearn.metrics import cohen_kappa_score, f1_score, precision_score, recall_score


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


def main():
    # 读取LLM.csv和LLM_updated.csv文件
    llm_file_path = 'dataset/LLM.csv'
    llm_updated_file_path = 'dataset/LLM_updated.csv'

    llm_df = pd.read_csv(llm_file_path)
    llm_updated_df = pd.read_csv(llm_updated_file_path)

    # 提取分数列
    true_labels = llm_df['Score']
    model_predictions = llm_updated_df['Score']

    # 调用evaluate_password_strength函数
    kappa, f1, precision, recall = evaluate_password_strength(model_predictions, true_labels)

    # 打印评估结果
    print(f"Kappa coefficient: {kappa:.2f}")
    print(f"F1-score: {f1:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")


if __name__ == "__main__":
    main()
