import torch
from transformers import LlamaTokenizer, LlamaForCausalLM
from peft import PeftModel

base_model_path = './Llama-2-7b-chat-hf'
finetune_model_path = base_model_path + "-finetuned"
nerged_model_path = base_model_path + "-merged"
tokenizer = LlamaTokenizer.from_pretrained(base_model_path, trust_remote_code=True)
#先加载基座模型，再加入finetune后的参数
model = LlamaForCausalLM.from_pretrained(base_model_path, load_in_8bit=False, device_map = 'auto', torch_dtype = torch.float16)
model = PeftModel.from_pretrained(model, finetune_model_path)
#或者直接加载 合并基座模型和finetune参数后的模型
#model =LlamaforcausallM,from pretrained(merged_model_path, load_in_8bit=False, device_map='auto', torch_dtype = torch.float16)

test_prompt ="""
Below is a password for a certain user. Please explain the reasons why the password is strong, medium, or weak from the perspectives of mixed characters, character jumping, password length, character repetition, specific patterns: keyboard, common words, and specific number patterns.

Input:
password: aaawz001
The password strength is weak

Output:
"""
model_input = tokenizer(test_prompt, return_tensors='pt').to('cuda')
model.eval()
with torch.no_grad():
    res = model.generate(**model_input, max_new_tokens=200)[0]
    print(tokenizer.decode(res,skip_special_tokens=True))