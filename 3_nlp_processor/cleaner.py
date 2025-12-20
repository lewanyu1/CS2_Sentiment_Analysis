#导包
import pandas as pd
import csv
#读取数据
# tieba_comment_path=r"/home/rulerwxe/Code/pycharm/CS2_Sentiment_Analysis/2_data_warehouse/raw_data/tieba_result.csv" #wsl
tieba_comment_path=r"/Users/rulerwxe/programming/temporory/NLP/CS2_Sentiment_Analysis/2_data_warehouse/raw_data/tieba_result.csv" #mac
comment=pd.read_csv(tieba_comment_path)
# print(comment.head(5))#看一下数据
#清洗数据
print(f"去重前，去空前：",comment.shape)
clean_comment=comment.drop_duplicates(subset=['link','title'])
clean_comment=clean_comment.dropna()
print(f"去重后，去空后：",clean_comment.shape)

#提取评论
clean_comment['temp']=clean_comment['content'].astype(str).str.split(r'\\n|\n')
clean_comment=clean_comment.explode('temp').rename(columns={'temp':'comment'}).reset_index(drop=True)

#用正则去掉无用信息
clean_comment['comment']=clean_comment['comment'].astype(str).str.replace(r'来自.*?客户端', '', regex=True)
clean_comment['comment']=clean_comment['comment'].astype(str).str.replace(r'\d+楼', '', regex=True)
clean_comment['comment']=clean_comment['comment'].astype(str).str.replace(r'\d{4}-\d{2}-\d{2}.*', '', regex=True)
clean_comment['comment']=clean_comment['comment'].astype(str).str.replace(r'回复$|收起$', '', regex=True)
clean_comment['comment']=clean_comment['comment'].astype(str).str.replace(r'\[.*?\]', '', regex=True)
clean_comment['comment']=clean_comment['comment'].astype(str).str.strip()

#去除评论小于2评论
print(f"清洗前！剩余数据量：",clean_comment.shape)
clean_comment=clean_comment[clean_comment['comment'].str.len()>2].reset_index(drop=True)
print(f"清洗完毕！剩余数据量：",clean_comment.shape)

#分别保存title和comment

#wsl
# clean_comment['title'].drop_duplicates().to_csv("/home/rulerwxe/Code/pycharm/CS2_Sentiment_Analysis/2_data_warehouse/processed_data/title.csv",index=False,encoding='utf-8')
# clean_comment['comment'].to_csv("/home/rulerwxe/Code/pycharm/CS2_Sentiment_Analysis/2_data_warehouse/processed_data/comment.csv",index=False,encoding='utf-8')
#mac
clean_comment['title'].drop_duplicates().to_csv("/Users/rulerwxe/programming/temporory/NLP/CS2_Sentiment_Analysis/2_data_warehouse/processed_data/title.csv",index=False,encoding='utf-8')
clean_comment['comment'].to_csv("/Users/rulerwxe/programming/temporory/NLP/CS2_Sentiment_Analysis/2_data_warehouse/processed_data/comment.csv",index=False,encoding='utf-8')


# print(content.head(5))#看一下数据
# for content in contents:
#     list_com=content.split('\n')
#     if len(list_com):
#         for i in range(len(list_com)):
#             for j in range(len(list_com)):
#                 if i==j:
#                     comment['review'][i]=list_com[j]
#                 else:
#                     continue



# title=comment['title']
