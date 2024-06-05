import torch
import transformers
from transformers import LlamaForCausalLM, LlamaTokenizer

# 加载模型和分词器
model_dir = "./llama-2-7b-chat-hf"
model = LlamaForCausalLM.from_pretrained (model_dir)
tokenizer = LlamaTokenizer.from_pretrained (model_dir)

# 定义流水线任务
pipeline = transformers.pipeline (
"text-generation",
model=model,
tokenizer=tokenizer,
torch_dtype=torch.float16,
device_map="auto",
)

# 问题
question = 'I have tomatoes, basil and cheese at home. What can I cook for dinner?\n'
# 运行流水线任务
sequences = pipeline (
question,
do_sample=True,
top_k=10,
num_return_sequences=1,
eos_token_id=tokenizer.eos_token_id,
max_length=400,
)
answer = ""
for seq in sequences:
    answer += f"{seq ['generated_text']}"

print(answer.replace(question,''))

    