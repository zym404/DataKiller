from langchain.output_parsers import PydanticOutputParser
from core.output_parser import StructualInquiryLetter,TaggingInquiryLetter
from langchain.prompts import PromptTemplate



question_prompt_template = """你是一个分析财务报表的专家,请用中文回答我以下问题:
 {question}
------
```{context}```
------
{format_instructions}
"""

# 用于对格式化prompt
format_instructions_question = PydanticOutputParser(pydantic_object=StructualInquiryLetter)  

QUESTION_PROMPT = PromptTemplate(
    template=question_prompt_template, 
    input_variables=["context", "question"],
    partial_variables={"format_instructions":format_instructions_question.get_format_instructions()}

)

label_prompt_template = """你是一个分析财务报表的专家,请用中文回答我以下问题:
 {question}
------
```{context}```
------
这是一些例子：
1. 关注公司经营持续性：企业能够在长期内持续经营并取得稳定、可持续的盈利能力的能力


凯瑞德（002072.SZ）2022年煤炭贸易收入和销售毛利率分别为3.59亿元、3.11%，同比分别增加206.48%、下滑15.08%，其中煤炭业务自营模式下销售毛利率为3.06%，同比下滑6.73%。

深交所要求公司结合在手订单情况，说明煤炭贸易业务的可持续性，公司持续经营能力是否存在重大不确定性


2. 关注商誉减值、信用减值、资产减值：指的是在企业财务报表中，对于资产价值的减少进行的调整。这些减值调整通常反映了企业资产的实际价值低于其账面价值，或者在特定时期内出现了减值迹象。

2022年公司计提各项减值准备7505.03万元，其中计提固定资产减值准备166.08万元，计提信用减值损失7338.95万元。

深交所要求公司补充披露经营计划调整的具体流程，并结合三文鱼养殖行业生产、销售周期、公司近3年投苗计划及变动情况等，说明对Australis资产组组合计提商誉减值是否及时、充分，是否存在对2022年业绩进行“大洗澡”的情形。

3. 关注年报中的异常信息：企业在财务报表中披露的与往常不同或者引人关注的财务数据、业务情况或其他相关信息。

*ST海伦（300201.SZ）2022年度实现营业收入102241.76万元，同比下降38.52%，归属于上市公司股东的净利润（下称“净利润”）7273.01万元，同比下降44.34%。公司发生销售费用9901.74万元，同比增长9.15%。深交所要求公司补充说明收入、净利润同比大幅下降的原因，以及销售费用与收入变动趋势不一致的原因及其合理性。
------
{format_instructions}
"""
format_instructions_label = PydanticOutputParser(pydantic_object=TaggingInquiryLetter) 

LABEL_PROMPT = PromptTemplate(
    template=question_prompt_template, 
    input_variables=["context", "question"],
    partial_variables={"format_instructions":format_instructions_label.get_format_instructions()}

)
# 用于对格式化prompt



combine_prompt_template = """请以以下格式回答问题
Final Answer :

问题: {question}
```{summaries}```"""

COMBINE_PROMPT = PromptTemplate(
    template=combine_prompt_template, input_variables=["summaries", "question"]
)