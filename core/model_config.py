import os
from langchain_community.embeddings import QianfanEmbeddingsEndpoint
from langchain_community.llms.baidu_qianfan_endpoint import QianfanLLMEndpoint

# 设置 API 密钥

os.environ["QIANFAN_AK"] = "gKMOfVu47gp3BMMUJb8EPpfG"
os.environ["QIANFAN_SK"] = "1G5RdeXf9RdIjj6bzeF4A1udqT8jTEPl"


LLM = QianfanLLMEndpoint(
    model="ERNIE-Speed-128k",
    temperature=0.1,
    )

EMB = QianfanEmbeddingsEndpoint(model="bge-large-zh")


# # 效果比ERNIE-Speed-128k好，但很容易出现超token的情况
# LLM = QianfanLLMEndpoint(
#     model="ERNIE-3.5-8K",
#     temperature=0.1,
#     )

# 一下代码可查看千帆支持的所有模型
# import qianfan
# qianfan.ChatCompletion().models()