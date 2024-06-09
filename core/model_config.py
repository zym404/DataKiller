import os
from langchain_community.embeddings import QianfanEmbeddingsEndpoint
from langchain_community.llms.baidu_qianfan_endpoint import QianfanLLMEndpoint
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# 设置 API 密钥

os.environ["QIANFAN_AK"] = "gKMOfVu47gp3BMMUJb8EPpfG"
os.environ["QIANFAN_SK"] = "1G5RdeXf9RdIjj6bzeF4A1udqT8jTEPl"



# LLM = ChatOpenAI(model='gpt-4-turbo',temperature=0.0)

# LLM = QianfanLLMEndpoint(
#     model="ERNIE-Speed-128k",
#     temperature=0.01,
#     )

LLM = ChatOpenAI(
    openai_api_base="https://api.moonshot.cn/v1/", 
    openai_api_key="sk-F2JsFeY0wKLRIDtnlL9JABWGYa9wvtqh1kIppvhO4PFMxsk9",
    model_name="moonshot-v1-8k",
    temperature=0.4,
    # max_tokens=5060,
    timeout=301.0
)

LLM_STRUC = ChatOpenAI(
    openai_api_base="https://api.moonshot.cn/v1/", 
    openai_api_key="sk-F2JsFeY0wKLRIDtnlL9JABWGYa9wvtqh1kIppvhO4PFMxsk9",
    model_name="moonshot-v1-32k",
    temperature=0.1,
    max_tokens=5120,
    
)

EMB = QianfanEmbeddingsEndpoint(model="bge-large-zh")
# EMB = OpenAIEmbeddings(model="text-embedding-3-large")

# LLM = ChatOpenAI(
#     openai_api_base="https://api.moonshot.cn/v1/", 
#     openai_api_key="sk-F2JsFeY0wKLRIDtnlL9JABWGYa9wvtqh1kIppvhO4PFMxsk9",
#     model_name="moonshot-v1-32k",
#     temperature=0.1,
#     max_tokens = 4048,
#     timeout=301.0
# )
# LLM.invoke('hello')
# def load_llm():


# 效果比ERNIE-Speed-128k好，但很容易出现超token的情况
# LLM = QianfanLLMEndpoint(
#     model="ERNIE-4.0-8K",
#     temperature=0.3,
#     request_timeout=116.0
#     )

# 一下代码可查看千帆支持的所有模型
# import qianfan
# qianfan.ChatCompletion().models()
