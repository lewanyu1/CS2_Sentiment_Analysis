import pandas as pd
import joblib
import os
import sys
import numpy as np
#配置路径
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)
from utils import config
MODEL_PATH = config.MODEL_TFIDF_VECTORIZER
MATRIX_PATH = config.FILE_TFIDF_MATRIX
#存储路径
OUTPUT_CSV = os.path.join(config.PROCESSED_DATA_DIR, 'top_keywords_report.csv')

def extract_keywords(corpus):
    if not os.path.exists(MODEL_PATH) or not os.path.exists(MATRIX_PATH):
        print(f"错误：找不到模型文件！")
        print(f"请先运行 '3_nlp_processor/vectorizer.py' 生成 TF-IDF 矩阵。")
        return
    #加载模型
    vectorizer=joblib.load(MODEL_PATH)
    #加载矩阵
    tfidf_matrix=joblib.load(MATRIX_PATH)

    #计算
    feature_names=vectorizer.get_feature_names_out()
    mean_weights = np.array(tfidf_matrix.mean(axis=0)).flatten()
    df = pd.DataFrame({
        'keyword': feature_names,
        'weight': mean_weights
    })
    df_sorted = df.sort_values(by='weight', ascending=False)
    print("\n🏆 CS2 贴吧 Top 关键词预览:")
    print(df_sorted.head(10))  # 打印前10个看看

if __name__ == '__main__':
    extract_keywords(50)