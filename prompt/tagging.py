from output_parser.tagging_inquiry_letter import TaggingInquiryLetter
from langchain.prompts import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from core.model_config import EMB
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from vector_store.Milvus import get_vector_store




tagging_prompt_template = """
你是一个分析财务报表的专家,请用中文回答我以下问题:
以下是证券交易所年报问询函的一条问询问题json格式记录，
请根据"问询问题内容"、"问询问题概括"和"补充说明"三个字段，结合"{tag}"业务标签的规则，为这条记录打标签
业务标签分为两种，一种是枚举类标签，如关键字，需要你枚举出它的类别；一种是阈值类标签，如严重性、复杂性、重要性，这种标签只有程度高低的等级。
输出模板如下所示
```json
{{
    "标签": "业务标签名称",
    "标签结果": "业务标签的判断结果",
    "判断依据": "业务标签的判断依据",
    "原文引用": "业务标签判断依据的引用原文",
}}
```
**请不要输出与输出模板无关的东西,json中的引号为半角引号！**
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