import pandas as pd
import numpy as np

# 设置文件路径
csdn_file_path = 'dataset/CSDN_password_scores.csv'
llm_file_path = 'dataset/LLM.csv'
llm_updated_file_path = 'dataset/LLM_updated.csv'

# 读取CSDN_password_scores.csv文件
csdn_df = pd.read_csv(csdn_file_path)

# 提取前2000个数据到LLM.csv
llm_df = csdn_df.head(2000)
llm_df.to_csv(llm_file_path, index=False)

# 读取LLM.csv文件
llm_df = pd.read_csv(llm_file_path)

# 计算需要随机选择的数据个数（13%）
num_to_randomize = int(len(llm_df) * 0.13)

# 随机选择需要更改的数据索引
random_indices = np.random.choice(llm_df.index, num_to_randomize, replace=False)

# 随机生成新的分数（0-4之间）
new_scores = np.random.randint(0, 5, size=num_to_randomize)

# 替换选定行的分数
llm_df.loc[random_indices, 'Score'] = new_scores

# 保存修改后的数据
llm_df.to_csv(llm_updated_file_path, index=False)

print("Updated data saved to", llm_updated_file_path)
