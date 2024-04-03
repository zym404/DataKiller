from langchain.output_parsers import PydanticOutputParser
from core.output_parser import StructualInquiryLetter,TaggingInquiryLetter
from langchain.prompts import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


structual_prompt_template = """你是一个分析财务报表的专家,请用中文回答我以下问题:
 {question}
------
```{context}```
------
{format_instructions}
"""

# 用于对格式化prompt
# format_instructions_question = PydanticOutputParser(pydantic_object=StructualInquiryLetter)  
structual_parser = JsonOutputParser(pydantic_object=StructualInquiryLetter)  


STRUCTUAL_PROMPT = PromptTemplate(
    template=structual_prompt_template, 
    input_variables=["context", "question"],
    partial_variables={"format_instructions":structual_parser.get_format_instructions()}

)

examples = [
    {
        "监管问题类别": "关注公司经营持续性",
        "定义": "企业能够在长期内持续经营并取得稳定、可持续的盈利能力的能力",
        "例子": ["凯瑞德（002072.SZ）2022年煤炭贸易收入和销售毛利率分别为3.59亿元、3.11%，同比分别增加206.48%、下滑15.08%，其中煤炭业务自营模式下销售毛利率为3.06%，同比下滑6.73%。深交所要求公司结合在手订单情况，说明煤炭贸易业务的可持续性，公司持续经营能力是否存在重大不确定性"]
    },
    {
        "监管问题类别": "关注商誉减值、信用减值、资产减值",
        "定义": "指的是在企业财务报表中，对于资产价值的减少进行的调整。这些减值调整通常反映了企业资产的实际价值低于其账面价值，或者在特定时期内出现了减值迹象。",
        "例子": ["2022年公司计提各项减值准备7505.03万元，其中计提固定资产减值准备166.08万元，计提信用减值损失7338.95万元。深交所要求公司补充披露经营计划调整的具体流程，并结合三文鱼养殖行业生产、销售周期、公司近3年投苗计划及变动情况等，说明对Australis资产组组合计提商誉减值是否及时、充分，是否存在对2022年业绩进行“大洗澡”的情形。"]
    },
    {
        "监管问题类别": "关注年报中的异常信息",
        "定义": "企业在财务报表中披露的与往常不同或者引人关注的财务数据、业务情况或其他相关信息。",
        "例子": ["*ST海伦（300201.SZ）2022年度实现营业收入102241.76万元，同比下降38.52%，归属于上市公司股东的净利润（下称“净利润”）7273.01万元，同比下降44.34%。公司发生销售费用9901.74万元，同比增长9.15%。深交所要求公司补充说明收入、净利润同比大幅下降的原因，以及销售费用与收入变动趋势不一致的原因及其合理性。"]
    },
    {
        "监管问题类别": "定期报告披露问题",
        "定义": "存在较多未决事项，如对外投资、逾期债务、业绩对赌、重大诉讼和股东控制权变更等，表明公司可能在公司治理结构和风险管理方面存在重大缺陷。",
        "例子": ["某上市公司发布的季度财报中遗漏了重大财务义务的披露，监管机构随后要求该公司补充相关信息并对信息披露的完整性和准确性进行自查。"]
    },
    {
        "监管问题类别": "公司治理和内部控制问题",
        "定义": "存在较多未决事项，如对外投资、逾期债务、业绩对赌、重大诉讼和股东控制权变更等，表明公司可能在公司治理结构和风险管理方面存在重大缺陷。",
        "例子": ["某家上市公司劳务派遣用工比例存在超过规定上限的情况，反映了公司可能未能遵守相关劳动法规定，体现了内部控制的不足。"]
    },
    {
        "监管问题类别": "关联交易披露问题",
        "定义": "关联交易是指上市公司与其控股股东、实际控制人、董事、监事、高级管理人员以及其他关联方之间的交易，不具有交易的独立性。关联交易披露问题指的是上市公司在公告或报告中未能充分、准确、及时地披露与关联方之间进行的交易信息，或者披露的信息不符合监管要求的情形。",
        "例子": ["某家上市公司与其控股股东的交易价格明显低于市场价，未能充分披露交易背后的利益安排，引起监管机构的审查。"]
    },
    {
        "监管问题类别": "市场操纵和内幕交易问题",
        "定义": "指通过非法手段操纵市场价格或基于未公开信息进行交易，破坏市场公平性和透明度。",
        "例子": ["某上市公司重组提示性公告披露前，公司股价涨幅较大并达到异常波动标准，可能存在内幕信息提前泄露的情形，体现了市场操纵和内幕交易问题。"]

    },
    {
        "监管问题类别": "重大资产重组问题",
        "定义": "对公司涉及的重大资产重组、并购或资产出售等事项的合理性、交易对方选择、交易价格、影响等进行询问。",
        "例子": ["某上市公司宣布计划通过发行股份加现金的方式收购另一家在同行业内的公司B的100%股权，然而，交易对方B公司近年来业绩持续下滑，存在较大的财务风险，监管机构需要问询上市公司详细的业务整合计划和预期的协同效应，以证明此次重组能够为公司带来长期的利益。"]
    },
    {
        "监管问题类别": "业绩预报问题",
        "定义": "如果公司实际业绩与此前业绩预告差异较大，监管机构会要求公司对差异进行解释。",
        "例子": ["一家上市公司在年初发布的业绩预告中预计全年净利润同比增长20%-30%。然而，在年度快要结束时，该公司突然发布业绩修正公告，将净利润增长预期大幅下调至-10%-0%。监管机构需要问询导致业绩预告大幅下调的具体原因，包括是否存在突发的重大不利因素或之前业绩预测时未能合理考虑的因素。"]
    },
    {
        "监管问题类别": "会计师事务所更换问题",
        "定义": "指上市公司更换其审计事务所的行为及其相关的披露和程序问题，特别是在没有合理解释或在特定情况下更换会计师事务所。监管要求上市公司在更换会计师事务所时，必须充分披露更换的原因、过程和对公司财务报告可能产生的影响。",
        "例子": ["某上市公司在连续两个财年接受同一家会计师事务所的审计后，突然宣布更换为另一家事务所进行下一财年的审计工作。该公司在公告中仅简单说明更换的原因是“为了适应公司业务的发展需要”，而没有提供更详细的解释，如具体是哪些业务的发展需要导致了更换的决定，以及为什么现有的审计事务所无法满足这些需求。"]
    },
    {
        "监管问题类别": "非法担保和资金占用问题",
        "定义": "指的是上市公司未经适当授权或违反相关法律法规及公司章程，为控股股东、实际控制人或其他关联方提供担保，或者存在关联方非法占用上市公司资金的行为。",
        "例子": ["某上市公司未经董事会和股东大会批准，擅自为其控股股东的关联企业提供了大额贷款担保。该关联企业后来因经营不善无法偿还贷款，导致上市公司需要承担担保责任，造成巨大财务损失。此外，还被发现有数笔资金直接从上市公司转移到控股股东的账户，用于控股股东个人的其他商业活动，未在规定时间内归还。"]
    },

]


label_prompt_template = """你是一个分析财务报表的专家,请用中文回答我以下问题:
 {question}
------
```{context}```
------
监管问题类别如下json所示
{examples}
------
{format_instructions}
"""

label_paser = JsonOutputParser(pydantic_object=TaggingInquiryLetter) 
LABEL_PROMPT = PromptTemplate(
    template=label_prompt_template, 
    input_variables=["context", "question",],
    partial_variables={"format_instructions":label_paser.get_format_instructions(),
                       "examples": examples}
)


struc_prompt_template = """你是一个分析财务报表的专家,请用中文回答我以下问题:
 {question}
------
```{context}```
------
"""

QUESTION_PROMPT = PromptTemplate(
    template=struc_prompt_template, 
    input_variables=["context", "question"],
    
)

combine_prompt_template = """请以以下格式回答问题
Final Answer :

问题: {question}
```{summaries}```"""

COMBINE_PROMPT = PromptTemplate(
    template=combine_prompt_template, input_variables=["summaries", "question"]
)