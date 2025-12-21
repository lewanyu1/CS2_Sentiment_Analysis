import pandas as pd
import joblib
import os
import sys
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

#配置路径
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)
from utils import config
MATRIX_PATH = config.FILE_TFIDF_MATRIX       # 输入：TF-IDF 矩阵
MODEL_PATH = config.MODEL_TFIDF_VECTORIZER   # 输入：词典模型
OUTPUT_CLUSTERING_CSV = os.path.join(config.PROCESSED_DATA_DIR, 'clustering_result_for_plot.csv')
OUTPUT_CENTER_REPORT = os.path.join(config.PROCESSED_DATA_DIR, 'cluster_keywords_report.csv')

def run_clustering(n_clusters=5):
    if os.path.exists(OUTPUT_CLUSTERING_CSV):
        print(" 找不到矩阵文件，请先运行 vectorizer.py")
        return
    #加载矩阵和模型
    tfidf_matrix = joblib.load(MATRIX_PATH)
    vectorizer=joblib.load(MODEL_PATH)
    feature_names = vectorizer.get_feature_names_out()
    #训练K-means模型
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(tfidf_matrix)

    #获取标签
    ordered_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]#是把权重从大到小排序，取前 10 个词的索引
    labels = kmeans.labels_
    # cluster_centers_ 是一个 (n_clusters, n_features) 的矩阵
    cluster_keywords = []
    for i in range(n_clusters):
        top_words = [feature_names[ind] for ind in ordered_centroids[i, :10]]
        keywords_str = ", ".join(top_words)
        print(f"🏷️  类别 {i}: {keywords_str}")
        cluster_keywords.append({
            "Cluster_ID": i,
            "Top_Keywords": keywords_str
        })

    pd.DataFrame(cluster_keywords).to_csv(OUTPUT_CENTER_REPORT, index=False, encoding='utf-8-sig')



    print("正在进行 PCA 降维 (为了可视化)...")
    dense_matrix = tfidf_matrix.toarray()
    pca = PCA(n_components=2)
    coords = pca.fit_transform(dense_matrix)
    df_plot = pd.DataFrame({
        'x': coords[:, 0],
        'y': coords[:, 1],
        'label': labels
    })
    df_plot.to_csv(OUTPUT_CLUSTERING_CSV, index=False)
    print(f"✅ 聚类坐标已保存至: {OUTPUT_CLUSTERING_CSV}")
    print(f"✅ 聚类关键词报告已保存至: {OUTPUT_CENTER_REPORT}")


if __name__ == '__main__':
    run_clustering()

