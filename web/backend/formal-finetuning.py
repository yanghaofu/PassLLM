import torch
from peft import LoraConfig, get_peft_model
from transformers import TrainingArguments, AutoModelForCausalLM, AutoTokenizer
from trl import SFTTrainer
from datasets import Dataset
import random

# 生成propmt函数
def general_prompt():
    data = []
    # 读取数据文件并处理每一部分数据
    with open('漫步数据.txt', 'r', encoding='UTF-8') as file:
        kind = 0
        instructions = ""
        Input_text = ""
        Output_text = ""
        for line in file:
            line = line.strip()
            if not line:
                continue
            if "Below is a password for a certain user. " in line:
                if instructions != "":
                    data_part = f"{instructions}\n\n{Input_text}{Output_text}"
                    # 将字符串写入文件
                    data_part += '\n'
                    data.append({'text': data_part})
                    instructions = ""
                    Input_text = ""
                    Output_text = ""
                kind = 1
            if line == "Input:":
                kind = 2
            if line == "Output:":
                kind = 3
            if kind == 1:
                instructions = instructions + line + ' '
            if kind == 2:
                Input_text = Input_text + line + '\n'
            if kind == 3:
                Output_text = Output_text + '\n' + line
    return data


prompt = general_prompt()

# 设置随机种子以确保结果可重复
random.seed(42)

# 打乱数据集顺序
random.shuffle(prompt)

# 计算分割点，3:7 比例
split_index = int(len(prompt) * 0.3)

# 分割数据集
train_dataset = prompt[split_index:]
val_dataset = prompt[:split_index]


# 训练集和验证集
train_dataset = Dataset.from_dict({key: [dic[key] for dic in train_dataset] for key in train_dataset[0]})
val_dataset = Dataset.from_dict({key: [dic[key] for dic in val_dataset] for key in val_dataset[0]})

model_dir = "./Llama-2-7b-chat-hf"
# 输出模型路径
output_dir = model_dir + '-finetuned'

# 配置lora参数
peft_config = LoraConfig(
    r=8,
    lora_alpha=8,
    target_modules=['q_proj', 'v_proj'],
    lora_dropout=0.05,
    bias='none',
    task_type='CAUSAL_LM'
)

#配置训练参数
training_aruments = TrainingArguments(
    output_dir=output_dir, # 模型输出的目录
    per_device_train_batch_size=64,
    optim='adamw_torch',
    learning_rate=10e-4,
    eval_steps=50,
    save_steps=100,
    logging_steps=20,
    evaluation_strategy='steps',
    group_by_length=False,
    max_steps=200,
    gradient_accumulation_steps=1,
    gradient_checkpointing=True,
    gradient_checkpointing_kwargs={'use_reentrant':False},
    max_grad_norm=0.3,
    bf16=True,
    lr_scheduler_type='cosine',
    warmup_steps=100
)


model = AutoModelForCausalLM.from_pretrained(model_dir, torch_dtype=torch.float16, device_map='auto', trust_remote_code=False)


model.enable_input_require_grads()
model = get_peft_model(model, peft_config)
model.print_trainable_parameters()
model.config.use_cache = False


tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=False)
tokenizer.pad_token_id = 0
tokenizer.padding_side = 'right'

trainer = SFTTrainer(
    model=model,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    dataset_text_field='text',
    peft_config=peft_config,
    max_seq_length=1800,
    tokenizer=tokenizer,
    args=training_aruments
)
trainer.train()
trainer.model.save_pretrained(output_dir)