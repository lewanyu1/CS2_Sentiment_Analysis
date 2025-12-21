import os
import platform

# ============================
# 1. 根目录自动判定 (核心修改：动态获取)
# ============================
# 逻辑：config.py 位于 utils 文件夹内
# 1. 获取当前脚本的绝对路径
current_path = os.path.abspath(__file__)
# 2. 获取父目录 (即 utils 文件夹路径)
utils_dir = os.path.dirname(current_path)
# 3. 再向上一级，就是项目根目录 (CS2_Sentiment_Analysis)
BASE_DIR = os.path.dirname(utils_dir)

# ============================
# 2. 文件夹路径定义
# ============================
DATA_WAREHOUSE_DIR = os.path.join(BASE_DIR, '2_data_warehouse')
RAW_DATA_DIR = os.path.join(DATA_WAREHOUSE_DIR, 'raw_data')
PROCESSED_DATA_DIR = os.path.join(DATA_WAREHOUSE_DIR, 'processed_data')

NLP_PROCESSOR_DIR = os.path.join(BASE_DIR, '3_nlp_processor')
DICT_DIR = os.path.join(NLP_PROCESSOR_DIR, 'dicts')

MODEL_DIR = os.path.join(BASE_DIR, '4_analysis_service', 'models')
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# ============================
# 3. 具体数据文件 (保留您的变量名和习惯)
# ============================
# [Tokenizer] 输入：原始数据
FILE_RAW_COMMENT = os.path.join(PROCESSED_DATA_DIR, 'comment.csv')

# [Tokenizer] 输出：分词结果
FILE_COMMENT_SEGMENTED = os.path.join(PROCESSED_DATA_DIR, 'comment_segmented.csv')

# [通用] 标准清洗后的数据
FILE_COMMENT = os.path.join(PROCESSED_DATA_DIR, 'comment.csv')

# [POS] 输出 & [Vectorizer] 输入：词性过滤后的数据
# 【重点】保留 'flittered' 拼写
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
# 顺便帮您加上情感模型路径，防止后面报错
MODEL_SENTIMENT = os.path.join(MODEL_DIR, 'sentiment_logistic_model.pkl')

# ============================
# 6. 调试打印 (运行此文件可检查路径是否正确)
# ============================
if __name__ == '__main__':
    print(f"✅ 自动定位项目根目录: {BASE_DIR}")
    print(f"📂 检查分词文件路径: {FILE_COMMENT_SEGMENTED}")
    print(f"🤔 文件是否存在? {os.path.exists(FILE_COMMENT_SEGMENTED)}")