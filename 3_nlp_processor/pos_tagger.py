#导包
import jieba
import pandas as pd
import jieba.posseg as pseg
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from utils import config
input_file = config.FILE_COMMENT
output_file = config.FILE_POS_FLITTERED  # 注意：这里用 filtered 这个变量

user_dict_path = config.DICT_JIEBA
stopwords_path = config.DICT_STOPWORDS

# #路径配置
# if platform.system() == 'Linux':
#     BASE_DIR = r'/home/rulerwxe/Code/pycharm/CS2_Sentiment_Analysis' #wsl
# elif platform.system() == 'Darwin':
#     BASE_DIR = r'/Users/rulerwxe/programming/temporory/NLP/CS2_Sentiment_Analysis'#mac
#
# DATA_DIR = os.path.join(BASE_DIR, '2_data_warehouse/processed_data')
# DICT_DIR = os.path.join(BASE_DIR, '3_nlp_processor')
#
# # 输入输出文件
# input_file = os.path.join(DATA_DIR, 'comment.csv')
# output_file = os.path.join(DATA_DIR, 'comment_pos_flittered.csv')
#
# # 词典文件路径
# user_dict_path = os.path.join(DICT_DIR, 'Cs2_dict.txt')
# stopwords_path = os.path.join(DICT_DIR, 'stopwords_hit.txt')

#通过标签
ALLOWED_POS_TAGS={'n','v','a','d','eng','i'}
#加载资源
def load_resources():
    #加载特定的用户词典
    if os.path.exists(user_dict_path):
        jieba.load_userdict(user_dict_path)
        print(f"已挂载用户词典", user_dict_path)
    else:
        print("未找到用户词典")

    #加载停用词
    stop_word = set()
    if os.path.exists(stopwords_path):
        with open(stopwords_path, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if word:
                    stop_word.add(word)
        print(f"已加载停用词表，共 {len(stop_word)} 个词")
    else:
        print("未找到停用词表，不过滤停用词")
    return stop_word

#原子函数（只负责处理单条数据）
def fliter_sentence_by_pos(text:str,stop_word:set):
    #边界检查
    if not isinstance(text, str) or not text.strip():
        return ""
    flitered_words = []

    #词性标注
    words_flags=pseg.lcut(text)
    for w in words_flags:
        word = w.word.strip()
        flag=w.flag.lower()
        if len(word)<2:
            continue
        if word in stop_word:
            continue

        if flag and (flag[0] in ALLOWED_POS_TAGS or flag in ALLOWED_POS_TAGS):
            flitered_words.append(word)
    return " ".join(flitered_words)

'''
jieba.enable_parallel只对jieba.cut有效
'''
#并行加速
# def raise_speed(num):
#     sys_name=platform.system()
#     num_core=num
#     if sys_name != 'Windows':
#         try:
#             jieba.enable_parallel(num_core)
#             print(f" 检测到 {sys_name} 系统，已开启{num_core}核并行加速！")
#         except Exception as e:
#             print(e)
#     else:
#         print("检测到 Windows 系统，Jieba 并行加速不可用，将使用单线程模式.")
def save_tag_data(comment_tag):
    comment_tag['comment_tag'].to_csv(output_file, index=False, encoding='utf-8-sig')
#批量处理csv文件
def process_dataset(input_file, output_file, stop_word):
    #读取数据
    data=pd.read_csv(input_file)
    # #并行加速
    # raise_speed(10)
    #批量处理
    data['comment_tag']=data['comment'].astype(str).apply(lambda x: fliter_sentence_by_pos(x,stop_word))
    #去除空行
    initial_len = len(data)
    data = data[data['comment_tag'] != ""]
    print(f"清洗完成删除了 {initial_len - len(data)} 条无效数据")
    '''
    另一种方法：
    import numpy as np
    data['comment_tag'].repace("",np.nan,inplace=true)
    data.dropna(subset=['comment_tag'], inplace=True)
    
    '''
    #保存
    save_tag_data(data)

if __name__ == '__main__':
    try:
        stop_word=load_resources()
        process_dataset(input_file, output_file,stop_word)
        print("成功运行")
    except Exception as e:
        print(e)











