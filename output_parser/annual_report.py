from langchain_core.pydantic_v1 import BaseModel, Field

class _AnnualReportLetter(BaseModel):
    问询问题内容: str = Field(description='问询问题的具体内容，说明了监管问询的原因')
    问询问题概括: str = Field(description='概括一下问询问题的内容')
    补充说明: str = Field(description='需要公司补充、披露、说明的事项，是一个list')
    # 问询科目: str = Field(description='问询函的涉及的会计科目')
    
class AnnualReportLetter(BaseModel):
    列表: list[_AnnualReportLetter] = Field(description='所有问询问题的列表')
    问询机构: str = Field(description='证券交易所名称')
    函件标题: str = Field(description='函件的标题')
    公司名称: str = Field(description='公司的名称，为工商信息登记的全称,请注意全称的格式为“XXX股份有限公司”')
    公告日期: str = Field(description='证券交易所发布函件的日期，格式为“YYYY年MM月DD日”')
    # 几日内回复: str = Field(description='证券交易所要求几日内进行回复，上海证券交易所特有')
    回复截止日期: str = Field(description='公司做出回复的截止日期，格式为“YYYY年MM月DD日”')
