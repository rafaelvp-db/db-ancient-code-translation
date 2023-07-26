# db-ancient-code-translation

### TLDR; this repo demonstrates code translation capabilities using LLMs on Databricks

## Getting Started

* Clone this repo into your Databricks Workspace
* Configure a Databricks single node cluster with MLR 13.2 and an A100 GPU
    * On Azure: `Standard_NC24ads_A100_v4` [instances](https://learn.microsoft.com/en-us/azure/virtual-machines/nc-a100-v4-series)
    * On AWS: `EC2 P4d` [instances](https://aws.amazon.com/ec2/instance-types/p4/#:~:text=P4d%20instances%20are%20powered%20by,support%20400%20Gbps%20instance%20networking.)
* Install the following libraries into the cluster:

<img src="https://github.com/rafaelvp-db/db-ancient-code-translation/blob/main/img/libraries.png?raw=true" style="width: 600px" />

* Run the notebooks from the `notebooks` folder

## Authors

* [Rafael V. Pierre](https://github.com/rafaelvp-db/)
* [Andreas Jack](https://github.com/AndreasJaeck)
