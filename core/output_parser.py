from langchain_core.pydantic_v1 import BaseModel, Field

class _StructualInquiryLetter(BaseModel):
    监管问题: str = Field(description='证券交易所问询函中披露的上市公司存在的关注事项和监管问题，需要上市公司做出回复说明')
    公司答复: str = Field(description='上市公司就监管问题做出的回复，简明扼要')
    涉及财报科目: str = Field(description='监管问题涉及的财报科目，该科目为上市公司会计准则中规定的会计科目')
    涉及金额: str = Field(description='监管问题中涉及的金额')
    公司名称: str = Field(description='公司的名称，为工商信息登记的全称')
    证券代码: str = Field(description='上市公司的证券代码')
    公告日期: str = Field(description='问询函的发布日期')
    

class StructualInquiryLetter(BaseModel):
    列表: list[_StructualInquiryLetter] = Field(description='所有监管问题的列表')
