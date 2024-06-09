import pandas as pd
import os
import matplotlib.pyplot as plt
from core.model_config import LLM
from langchain.prompts import PromptTemplate
from vector_store.Milvus import get_all_file_name, get_all_sub_path



def checking(df,save_file=False) -> pd.DataFrame:
    # 筛选条件1：在问询问题内容中出现“请”字样
    cond_1 = df['问询问题内容'].apply(lambda x: "请" in x)

    # 筛选条件2：补充说明的字数少于一定的长度
    length = df['补充说明'].apply(lambda x: len(x))

    # length.hist(bins=200)
    # plt.show() # 阈值定位10%的分位数，即41
    # length.quantile(0.1)

    cond_2 = length.apply(lambda x: x < length.quantile(0.1))
    cond_2 = length.apply(lambda x: x < 41)

    df_with_problem = df[cond_1 | cond_2]
    if save_file:
        df_with_problem.to_excel(r'./docs/存在问题的问询函.xlsx')
    return df_with_problem



