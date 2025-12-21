#导包
import pandas as pd
import joblib
import os
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from utils import config
input_file = config.FILE_COMMENT_SEGMENTED      # 输入：词性清洗后的 CSV
matrix_output = config.FILE_TFIDF_MATRIX    # 输出：矩阵文件 (.pkl)
model_output = config.MODEL_TFIDF_VECTORIZER # 输出：模型文件 (.pkl)

def run_vectorizer():
    #读取数据
    if not os.path.exists(input_file):
        print(f"❌ 找不到输入文件: {input_file}")
        print("💡 请先运行 pos_tagger.py 生成清洗后的数据。")
        return

    df = pd.read_csv(input_file)
    target_col ='tokenized_comment'

    #处理空值
    corpus=df[target_col].fillna("").astype(str).tolist()

    #配置 TF-IDF
    vectorizer = TfidfVectorizer(
        max_features=5000,  # 只保留最重要的 5000 个词 (防止矩阵过大内存爆炸)
        ngram_range=(1, 2),  # 同时提取 "服务器" 和 "服务器 炸了" (1-2元组)
        min_df=3,  # 忽略出现少于 3 次的生僻词/错别字
        token_pattern=r"(?u)\b\w+\b"
    )
    tfidf_matrix = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names_out()
    print(f" - 词表大小: {len(feature_names)}")
    print(f" - 矩阵形状: {tfidf_matrix.shape}")
    print(f" - 示例特征: {feature_names[:10]}")

    #保存矩阵
    joblib.dump(tfidf_matrix, matrix_output)
    print(f"💾 矩阵已保存至: {matrix_output}")
    # 保存模型 (给未来预测用)
    joblib.dump(vectorizer, model_output)
    print(f"💾 模型已保存至: {model_output}")
if __name__ == '__main__':
    run_vectorizer()