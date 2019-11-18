import pickle
import pandas as pd

def to_df(file_path):
  with open(file_path, 'r') as fin:
    df = {}
    i = 0
    for line in fin:
      df[i] = eval(line)#数值化
      i += 1
    df = pd.DataFrame.from_dict(df, orient='index')#方向为行
    return df

reviews_df = to_df('../raw_data/reviews_Electronics_5.json')
with open('../raw_data/reviews.pkl', 'wb') as f:
  pickle.dump(reviews_df, f, pickle.HIGHEST_PROTOCOL)#将对象reviews_df保存到文件f中，HIGHEST_PROTOCOL意为最高配置

meta_df = to_df('../raw_data/meta_Electronics.json')
meta_df = meta_df[meta_df['asin'].isin(reviews_df['asin'].unique())]  #判断数列筛选，#asin为商品ID
meta_df = meta_df.reset_index(drop=True)   #重置索引，多次写入会导致索引混乱
with open('../raw_data/meta.pkl', 'wb') as f:
  pickle.dump(meta_df, f, pickle.HIGHEST_PROTOCOL)
