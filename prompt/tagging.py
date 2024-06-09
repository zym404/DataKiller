from output_parser.tagging_inquiry_letter import TaggingInquiryLetter
from langchain.prompts import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from core.model_config import EMB
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from vector_store.Milvus import get_vector_store




# tagging_prompt_template = """

# 你是一个分析财务报表的专家,请用中文回答我以下问题:
# 以下是证券交易所年报问询函的一条问询问题json格式记录，
# 请根据"问询问题内容"、"问询问题概括"和"监管要求"三个字段，结合"{tag}"业务标签的规则，为这条记录打标签
# 业务标签分为两种，一种是枚举类标签，如关键字，需要你枚举出它的类别；一种是阈值类标签，如严重性、复杂性、重要性，这种标签只有程度高低的等级。
# 输出模板如下所示
# ```json
# {{
#     "标签结果": "业务标签的判断结果",
#     "判断依据": "业务标签的判断依据",
#     "原文引用": "业务标签判断依据的引用原文",
# }}
# ```
# **请不要输出与输出模板无关的东西,不要输出全角引号！json中的引号为半角引号！**
# ------
#  问题：
#  {question}
# ------
# 规则定义:
# {rules}
# ------
# 例子:
# {examples}
# ------
# {format_instructions}
# """

tagging_prompt_template = """

{{
  "Role": "财务报表分析专家",
  "Background": "用户需要对证券交易所年报问询函的问询记录进行标签化处理，并且需要根据特定的字段和业务标签规则进行操作。",
  "Profile": "你是一位经验丰富的财务分析师，擅长从复杂的财务文档中提取关键信息，并根据既定规则进行分类和标记。",
  "Skills": "财务分析，数据标签化，JSON格式处理，关键字识别，规则应用。",
  "Goals": "根据提供的问询问题背景、问询问题和监管要求，结合业务标签规则，为记录打上合适的标签，并提供判断依据和引用原文。",
  "Constrains": "输出必须遵循给定的JSON模板，**对键值对使用半角引号（英文引号）！对键值对使用半角引号（英文引号）！对键值对使用半角引号（英文引号）！不要输出与Json文本无关的任何文字**",
  "OutputFormat": "JSON格式的字符串，包含标签结果、判断依据和原文引用。",
  "Workflow": [
    "分析问询记录中包含的问询问题背景、问询问题和监管要求以及关键字（如果有）。",
    "根据业务标签规则、问询问题背景、问询问题、监管要求以及关键字（如果有）判断标签结果",
    "按照输出Json模板格式化标签结果、判断依据和原文引用。",
    "确保使用半角引号，**不要输出与Json文本无关的任何文字**"
  ],
  "Examples": {{
    "question": "一条问询记录",
    "rules": "规则定义",
    "examples": "提供的标签化示例",
    "format_instructions": "格式化指令说明"
  }},
  "Initialization": "请提供问询问题背景、问询问题、和监管要求、关键字（如果有）以及规则定义和格式化指令，我将根据这些信息为问询函记录打上相应的业务标签。"
}}
------
问题：
{question}
------
规则定义:
{rules}
------
例子:
{examples}
------
{format_instructions}

"""



# 用于对格式化prompt

behavior_risk_points_parser = JsonOutputParser(pydantic_object=TaggingInquiryLetter)  


TAGGING_PROMPT = PromptTemplate(
    template=tagging_prompt_template, 
    input_variables=["tag", "question", "rules","examples"],
    partial_variables={"format_instructions":behavior_risk_points_parser.get_format_instructions()}

)