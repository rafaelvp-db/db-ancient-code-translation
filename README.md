# Databricks Ancient Code Translation

![huggingface](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-StarChat-brightgreen?style=for-the-badge)  ![pytorch](https://img.shields.io/badge/pytorch-EE4C2C?logo=pytorch&logoColor=white&style=for-the-badge) ![pyspark](https://img.shields.io/badge/PySpark-E25A1C?logo=apachespark&style=for-the-badge&logo=Databricks&logoColor=white) ![databricks](https://img.shields.io/badge/Databricks-FF3621.svg?style=for-the-badge&logo=Databricks&logoColor=white)

<p align="center">
<img src="https://github.com/rafaelvp-db/db-ancient-code-translation/blob/main/img/ancient_code.jpeg?raw=true" style="width: 50%"/>
</p>

<hr/>

## TLDR;

This repo demonstrates code translation (Code to Text, Code to Code) capabilities using Large Language Models (LLMs) on Databricks

## Getting Started

* Clone this repo into your Databricks Workspace
* Configure a Databricks single node cluster with [Databricks Runtime 13.2 for Machine Learning](https://docs.databricks.com/release-notes/runtime/13.2ml.html) and an [NVIDIA A100](https://www.nvidia.com/en-us/data-center/a100/) GPU ([A10](https://www.nvidia.com/en-us/data-center/products/a10-gpu/) might also work, though with lower floating point precision)
    * A100 Instances On Azure: `Standard_NC24ads_A100_v4` [instances](https://learn.microsoft.com/en-us/azure/virtual-machines/nc-a100-v4-series)
    * A100 Instances On AWS: `EC2 P4d` [instances](https://aws.amazon.com/ec2/instance-types/p4/#:~:text=P4d%20instances%20are%20powered%20by,support%20400%20Gbps%20instance%20networking.)
* Install the following libraries into the cluster (you can also do it directly in the notebooks and leverage `requirements.txt` for that):

```
accelerate==0.21.0
ninja
alibi
einops
transformers
triton
xformers
```

* Run the notebooks from the `notebooks` folder

## Authors

* [Rafael V. Pierre](https://github.com/rafaelvp-db/)
* [Andreas Jack](https://github.com/AndreasJaeck)

## Reference

* 💫 [StarCoder Github Project](https://github.com/bigcode-project/starcoder)
* Tunstall, Lewis and Lambert, Nathan and Rajani, Nazneen and Beeching, Edward and Le Scao, Teven and von Werra, Leandro and Han, Sheon and Schmid, Philipp and Rush, Alexander. [Creating a Coding Assistant with StarCoder](https://huggingface.co/blog/starchat). Hugging Face Blog, 2023.
* [Big Science Open RAIL-M License](https://www.licenses.ai/blog/2022/8/26/bigscience-open-rail-m-license)

## Appendix

### Evaluation
To evaluate StarCoder and its derivatives, you can use the [BigCode-Evaluation-Harness](https://github.com/bigcode-project/bigcode-evaluation-harness) for evaluating Code LLMs.
### Inference hardware requirements

In FP32 the model requires more than 60GB of RAM, you can load it in FP16 or BF16 in ~30GB, or in 8bit under 20GB of RAM with

```python
# make sure you have accelerate and bitsandbytes installed
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bigcode/starcoder")
# for fp16 replace with  `load_in_8bit=True` with   `torch_dtype=torch.float16`
model = AutoModelForCausalLM.from_pretrained("bigcode/starcoder", device_map="auto", load_in_8bit=True)
print(f"Memory footprint: {model.get_memory_footprint() / 1e6:.2f} MB")
```

```
Memory footprint: 15939.61 MB
```
