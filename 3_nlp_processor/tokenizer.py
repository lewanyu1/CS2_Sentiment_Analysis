import jieba
import pandas as pd
import os
import platform
import sys
#路径配置
# BASE_DIR = r'/home/rulerwxe/Code/pycharm/CS2_Sentiment_Analysis' #wsl
# BASE_DIR = r'/Users/rulerwxe/programming/temporory/NLP/CS2_Sentiment_Analysis'#mac
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
# output_file = os.path.join(DATA_DIR, 'comment_segmented.csv')
#
# # 词典文件路径
# user_dict_path = os.path.join(DICT_DIR, 'Cs2_dict.txt')
# stopwords_path = os.path.join(DICT_DIR, 'stopwords_hit.txt')
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from utils import config
input_file = config.FILE_RAW_COMMENT     # 输入：原始爬虫数据
output_file = config.FILE_COMMENT_SEGMENTED       # 输出：分词后的标准数据
user_dict_path = config.DICT_JIEBA       # 字典路径
stopwords_path = config.DICT_STOPWORDS   # 停用词路径

def load_resources():
    #判断用户词典是否存在，并挂载
    if os.path.exists(user_dict_path):
        jieba.load_userdict(user_dict_path)
        print(f"已挂载用户词典", user_dict_path)
    else:
        print("未找到用户词典")

    #加载停用词（用set加速）
    stop_word=set()
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

def raise_speed():
    sys_name=platform.system()
    num_core=8
    if sys_name != 'Windows':
        try:
            jieba.enable_parallel(num_core)
            print(f" 检测到 {sys_name} 系统，已开启{num_core}核并行加速！")
        except Exception as e:
            print(e)
    else:
        print("检测到 Windows 系统，Jieba 并行加速不可用，将使用单线程模式.")
#定义单行处理逻辑
def process_single_text(text, stop_word):
    result_list = []
    if not isinstance(text, str):
        return ""
    words = jieba.lcut(text,cut_all=False)
    for word in words:
        word = word.strip()#去除两边空白
        if word in stop_word:
            continue
        else:
            if word.isnumeric():
                continue
            else:
                result_list.append(word)
    return " ".join(result_list)



def tokenize(input_file,stop_word):
    #读取csv文件
    data=pd.read_csv(input_file)
    data['tokenized_comment']=data['comment'].astype(str).apply(lambda x: process_single_text(x, stop_word))
    tokenized_comment=data[data['tokenized_comment']!=""]
    return tokenized_comment

def save_tokenized_data(tokenized_comment):
    tokenized_comment['tokenized_comment'].to_csv(output_file, index=False, encoding='utf-8-sig')
def close_para():
    if platform.system() != 'Windows':
        jieba.disable_parallel()

if __name__ == '__main__':
    stop_word=load_resources()
    raise_speed()
    tokenized_comment=tokenize(input_file, stop_word)
    save_tokenized_data(tokenized_comment)
    close_para()














