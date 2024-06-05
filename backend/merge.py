from peft import AutoPeftModelForCausalLM
from transformers import AutoTokenizer
import torch

base_model_dir ='./Llama-2-7b-chat-hf'
lora_model_dir =base_model_dir + "-finetuned"
tokenizer = AutoTokenizer.from_pretrained(base_model_dir, trust_remote_code=False)
model = AutoPeftModelForCausalLM.from_pretrained(lora_model_dir, device_map='auto', torch_dtype=torch.bfloat16)
model = model.merge_and_unload()
output_dir =base_model_dir + "-merged"
model.save_pretrained(output_dir)