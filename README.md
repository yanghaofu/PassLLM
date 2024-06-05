# 代码说明

## 一、实验代码
实验部分的代码存放在experiment文件夹，运行main.py即可进行结果评估。

## 二、插件代码
前端和后端代码都在web文件夹中，启用LLM.py可在本地运行插件。

## 三、模型部署

### （1）申请权限

- 在[Meta Llama](https://llama.meta.com/)网站，点击`Download the Model`按钮。然后在申请表格上填写申请信息，填完滑到最下面勾选同意协议，点击提交按钮就可以了，之后静等权限通过。
- 进到 HuggingFace 的[Meta Llama 网站](https://huggingface.co/meta-llama)，可以看到有很多个 Llama2 的仓库，我们选择`meta-llama/Llama-2-7b-chat-hf`，进入后，点击`Submit`按钮进行申请，若申请成功，则会获得模型的tokens。

### （2）下载模型

使用下面的代码（token换成自己的）

```
import huggingface_hub

huggingface_hub.snapshot_download(
        "meta-llama/Llama-2-7b-chat-hf",
        local_dir="./Llama-2-7b-chat-hf",
        token=""
)
```

### （3）配置环境

- CUDA版本： 11.8
- 系统版本： Ubuntu 22.04.4 LTS
- GRID驱动版本：NVIDIA-SMI 384.37
- GPU配置：两个NVIDIA GeForce RTX 4090
- 由于 NVIDIA RTX 4000 系列 GPU 的特性，需要设置特定的 NCCL 环境变量以禁用 P2P 和 IB。

我们使用anaconda来配置虚拟环境，相关库和语言如下：

- 语言：Python 3.10.14
- peft：0.6.0
- huggingface_hub
- transformers
- torch（GPU版本，若cuda、GRID驱动和系统版本一致，可使用`pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`进行安装）
- trl
- datasets

相关库可详见requirements.txt文件

### （4）web/backend中的代码文件说明

- chat.py：运行基础模型

- formal-chat：运行微调后的模型，来进行推理。
- formal-finetuning.py：微调代码
- merge：合并基础模型和微调后的权重



### 
