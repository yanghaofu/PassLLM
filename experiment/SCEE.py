from sklearn.feature_extraction.text import TfidfVectorizer
from torch import cosine_similarity


def calculate_scee_accuracy(expert_explanations, model_explanations, threshold=0.80):
    """
    计算大模型生成的解释与专家解释之间的语义契合度准确率。

    :param expert_explanations: List of lists containing expert explanations for each password.
                                每个子列表包含3个专家解释。
    :param model_explanations: List of model explanations corresponding to each password.
    :param threshold: The threshold for considering an explanation accurate (default is 0.80 for 80%).
    :return: The overall accuracy of the model explanations.
    """
    # 展平专家解释列表，并为每个口令生成一个相应的标签
    flattened_expert_explanations = [exp for sublist in expert_explanations for exp in sublist]

    # 将所有解释合并到一个列表中
    all_explanations = flattened_expert_explanations + model_explanations

    # 计算TF-IDF向量
    vectorizer = TfidfVectorizer().fit_transform(all_explanations)
    vectors = vectorizer.toarray()

    # 获取专家和模型解释的向量
    expert_vectors = vectors[:len(flattened_expert_explanations)]
    model_vectors = vectors[len(flattened_expert_explanations):]

    accurate_count = 0

    for i in range(len(model_explanations)):
        expert_sublist = expert_vectors[i * 3:(i + 1) * 3]
        model_vector = model_vectors[i].reshape(1, -1)
        similarities = cosine_similarity(expert_sublist, model_vector)
        average_similarity = similarities.mean()

        # 判断是否大于阈值
        if average_similarity >= threshold:
            accurate_count += 1

    # 计算整体准确率
    accuracy = accurate_count / len(model_explanations)
    return accuracy
