# db-ancient-code-translation

### TLDR; this repo demonstrates code translation capabilities using LLMs on Databricks

## Getting Started

* Clone this repo into your Databricks Workspace
* Configure a Databricks single node cluster with [Databricks Runtime 13.2 for Machine Learning](https://docs.databricks.com/release-notes/runtime/13.2ml.html) and an A100 GPU
    * On Azure: `Standard_NC24ads_A100_v4` [instances](https://learn.microsoft.com/en-us/azure/virtual-machines/nc-a100-v4-series)
    * On AWS: `EC2 P4d` [instances](https://aws.amazon.com/ec2/instance-types/p4/#:~:text=P4d%20instances%20are%20powered%20by,support%20400%20Gbps%20instance%20networking.)
* Install the following libraries into the cluster:

<img src="https://github.com/rafaelvp-db/db-ancient-code-translation/blob/main/img/libraries.png?raw=true" style="width: 600px" />

* Run the notebooks from the `notebooks` folder

## Authors

* [Rafael V. Pierre](https://github.com/rafaelvp-db/)
* [Andreas Jack](https://github.com/AndreasJaeck)

## Reference

@article{Tunstall2023starchat-alpha,
  author = {Tunstall, Lewis and Lambert, Nathan and Rajani, Nazneen and Beeching, Edward and Le Scao, Teven and von Werra, Leandro and Han, Sheon and Schmid, Philipp and Rush, Alexander},
  title = {Creating a Coding Assistant with StarCoder},
  journal = {Hugging Face Blog},
  year = {2023},
  note = {https://huggingface.co/blog/starchat},
}
