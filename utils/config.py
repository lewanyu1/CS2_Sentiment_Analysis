import os
import platform

# ============================
# 1. 根目录自动判定
# ============================
sys_name = platform.system()

if sys_name == 'Linux':
    BASE_DIR = r'/home/rulerwxe/Code/pycharm/CS2_Sentiment_Analysis'
elif sys_name == 'Darwin':
    BASE_DIR = r'/Users/rulerwxe/programming/temporory/NLP/CS2_Sentiment_Analysis'
else:
    BASE_DIR = r'D:\Code\CS2_Sentiment_Analysis'

# ============================
# 2. 文件夹路径定义
# ============================
DATA_WAREHOUSE_DIR = os.path.join(BASE_DIR, '2_data_warehouse')
RAW_DATA_DIR = os.path.join(DATA_WAREHOUSE_DIR, 'raw_data')
PROCESSED_DATA_DIR = os.path.join(DATA_WAREHOUSE_DIR, 'processed_data')

NLP_PROCESSOR_DIR = os.path.join(BASE_DIR, '3_nlp_processor')
DICT_DIR = os.path.join(NLP_PROCESSOR_DIR, 'dicts') # 你的字典都在这

MODEL_DIR = os.path.join(BASE_DIR, '4_analysis_service', 'models')
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# ============================
# 3. 具体数据文件 (完全还原你的文件名)
# ============================
# [Tokenizer] 输入：原始数据
FILE_RAW_COMMENT = os.path.join(RAW_DATA_DIR, 'tieba_raw.csv')

# [Tokenizer] 输出：分词结果 (截图里你有这个文件)
FILE_COMMENT_SEGMENTED = os.path.join(PROCESSED_DATA_DIR, 'comment_segmented.csv')

# [通用] 标准清洗后的数据 (很多脚本用的 comment.csv)
FILE_COMMENT = os.path.join(PROCESSED_DATA_DIR, 'comment.csv')

# [POS] 输出 & [Vectorizer] 输入：词性过滤后的数据
# 【重点】保留你的拼写习惯 'flittered'，不改动！
FILE_POS_FLITTERED = os.path.join(PROCESSED_DATA_DIR, 'comment_pos_flittered.csv')

# [NER] 输出：实体识别结果
FILE_NER_RESULT = os.path.join(PROCESSED_DATA_DIR, 'comment_ner_result.csv')

# [Vectorizer] 输出：TF-IDF 矩阵
FILE_TFIDF_MATRIX = os.path.join(PROCESSED_DATA_DIR, 'tfidf_matrix.pkl')

# ============================
# 4. 资源字典文件
# ============================
DICT_JIEBA = os.path.join(DICT_DIR, 'Cs2_dict.txt')
DICT_STOPWORDS = os.path.join(DICT_DIR, 'stopwords_hit.txt')
DICT_NER = os.path.join(DICT_DIR, 'Cs2_ner_dict_V1.json')

# ============================
# 5. 模型文件
# ============================
MODEL_TFIDF_VECTORIZER = os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl')