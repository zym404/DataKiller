from langchain.schema.language_model import BaseLanguageModel
from langchain.callbacks.base import BaseCallbackManager
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from typing import Any, Optional
from langchain.chains.question_answering import _load_map_reduce_chain
from langchain.prompts import PromptTemplate

question_prompt_template = """你是一个分析财务报表的专家: {question}
```{context}```
"""
QUESTION_PROMPT = PromptTemplate(
    template=question_prompt_template, input_variables=["context", "question"]
)

combine_prompt_template = """请以以下格式回答问题
Final Answer :

问题: {question}
```{summaries}```"""

COMBINE_PROMPT = PromptTemplate(
    template=combine_prompt_template, input_variables=["summaries", "question"]
)


"""
定义了两种类型的提示模板，分别命名为 QUESTION_PROMPT 和 COMBINE_PROMPT。这些模板将在问答过程中使用，以引导语言模型生成合适的回答。

首先，我们来看看 PromptTemplate 是什么：PromptTemplate 是 LangChain 库中的一个核心概念，它描述了如何格式化输入数据以供语言模型使用。
你可以想象它就像一个填充好某些槽位的句子，只有插入正确的数据才能形成有效的句子。
"""

"""
_load_map_reduce_chain 函数，该函数专门设计用于构建基于映射/归约策略的问答链。

load_qa_chain 的函数，它负责加载一个基于映射/归约策略的问答链。这种策略涉及到将大型问题分解为较小的子问题，
解决每一个子问题，然后合并所有子问题的答案以获得整体答案。
"""
def load_qa_chain(
        llm: BaseLanguageModel,
        verbose: Optional[bool] = None,
        callback_manager: Optional[BaseCallbackManager] = None,
        **kwargs: Any,
) -> BaseCombineDocumentsChain:
    return _load_map_reduce_chain(
        llm,
        verbose=verbose,
        question_prompt=QUESTION_PROMPT,
        combine_prompt=COMBINE_PROMPT,
        callback_manager=callback_manager, **kwargs
    )






