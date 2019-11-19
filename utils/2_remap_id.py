import random
import pickle
import numpy as np

random.seed(1234)

with open('../raw_data/reviews.pkl', 'rb') as f:
  reviews_df = pickle.load(f)         #dump将对象保存到文件中去，file有write（）接口，load将文件解析成对象，文件有read（）、readline（）接口
  reviews_df = reviews_df[['reviewerID', 'asin', 'unixReviewTime']]       #reviews_df有评论者ID，商品ID，评论时间
with open('../raw_data/meta.pkl', 'rb') as f:
  meta_df = pickle.load(f)
  meta_df = meta_df[['asin', 'categories']]  #商品ID，商品类别
  meta_df['categories'] = meta_df['categories'].map(lambda x: x[-1][-1])#此时lambda函数用于指定对列表中每一个元素的共同操作。例如map(lambda x: x+1, [1, 2,3])将列表[1, 2, 3]中的元素分别加1，其结果[2, 3, 4]。


def build_map(df, col_name):
  key = sorted(df[col_name].unique().tolist())  #sort()排序，tolist()将数组转化成列表
  m = dict(zip(key, range(len(key)))) #dict(zip(keys,values))将两个列表转化成一个字典d={k1:v1,k2:v2...}
  df[col_name] = df[col_name].map(lambda x: m[x])
  return m, key

asin_map, asin_key = build_map(meta_df, 'asin')
cate_map, cate_key = build_map(meta_df, 'categories')
revi_map, revi_key = build_map(reviews_df, 'reviewerID')

user_count, item_count, cate_count, example_count =\
    len(revi_map), len(asin_map), len(cate_map), reviews_df.shape[0]
print('user_count: %d\titem_count: %d\tcate_count: %d\texample_count: %d' %
      (user_count, item_count, cate_count, example_count))

meta_df = meta_df.sort_values('asin')
meta_df = meta_df.reset_index(drop=True)
reviews_df['asin'] = reviews_df['asin'].map(lambda x: asin_map[x])
reviews_df = reviews_df.sort_values(['reviewerID', 'unixReviewTime'])
reviews_df = reviews_df.reset_index(drop=True)
reviews_df = reviews_df[['reviewerID', 'asin', 'unixReviewTime']]

cate_list = [meta_df['categories'][i] for i in range(len(asin_map))]
cate_list = np.array(cate_list, dtype=np.int32)


with open('../raw_data/remap.pkl', 'wb') as f:
  pickle.dump(reviews_df, f, pickle.HIGHEST_PROTOCOL) # uid, iid
  pickle.dump(cate_list, f, pickle.HIGHEST_PROTOCOL) # cid of iid line
  pickle.dump((user_count, item_count, cate_count, example_count),
              f, pickle.HIGHEST_PROTOCOL)
  pickle.dump((asin_key, cate_key, revi_key), f, pickle.HIGHEST_PROTOCOL)
