import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import platform

# ============================
# 0. 路径配置
# ============================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from utils import config

# ============================
# 1. 变量绑定
# ============================
# 输入文件
CLUSTERING_FILE = os.path.join(config.PROCESSED_DATA_DIR, 'clustering_result_for_plot.csv')
CLUSTER_REPORT = os.path.join(config.PROCESSED_DATA_DIR, 'cluster_keywords_report.csv')
SENTIMENT_FILE = os.path.join(config.PROCESSED_DATA_DIR, 'sentiment_analysis_result.csv')

# 输出图片路径
IMG_DIR = os.path.join(root_dir, '5_visualization', 'images')
if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)


# ============================
# 2. 全局绘图设置 (解决中文乱码)
# ============================
def set_chinese_font():
    """解决中文乱码的终极方案"""
    # 1. 【关键】先设置 Seaborn 样式！
    # 如果放在后面，它会覆盖掉我们设置的字体
    sns.set_style("whitegrid")

    system_name = platform.system()
    if system_name == "Darwin":  # Mac 系统
        # 优先使用 Mac 系统自带的“黑体-繁/简”，如果不适再尝试其他
        plt.rcParams['font.sans-serif'] = ['Heiti TC', 'PingFang HK', 'Hiragino Sans GB', 'Arial Unicode MS']
    elif system_name == "Windows":
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
    else:
        plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']

    # 解决负号显示为方块的问题
    plt.rcParams['axes.unicode_minus'] = False

    print(f"[INFO] 字体设置已更新，当前系统: {system_name}")


# ============================
# 3. 绘图函数
# ============================

def plot_clustering_scatter():
    """绘制 K-Means 聚类散点图"""
    print("[INFO] 正在绘制聚类散点图...")

    if not os.path.exists(CLUSTERING_FILE):
        print(f"[ERROR] 找不到聚类坐标文件: {CLUSTERING_FILE}")
        return

    # 1. 读取数据
    df = pd.read_csv(CLUSTERING_FILE)

    # 2. 准备图例标签 (如果有关键词报告，就用关键词做图例)
    legend_labels = {}
    if os.path.exists(CLUSTER_REPORT):
        df_keywords = pd.read_csv(CLUSTER_REPORT)
        for index, row in df_keywords.iterrows():
            # 取前3个关键词作为标签
            cid = row['Cluster_ID']
            # 兼容处理：防止关键词是数字或其他类型
            keywords = str(row['Top_Keywords']).split(',')[:3]
            short_kw = ",".join(keywords)
            legend_labels[cid] = f"C{cid}: {short_kw}"

    # 3. 绘图
    plt.figure(figsize=(12, 8))

    # 使用 Seaborn 绘制散点图
    scatter = sns.scatterplot(
        data=df,
        x='x',
        y='y',
        hue='label',  # 颜色根据类别区分
        palette='viridis',
        s=60,
        alpha=0.7
    )

    # 4. 替换图例文字
    if legend_labels:
        handles, _ = scatter.get_legend_handles_labels()
        # 确保标签顺序对应
        new_labels = []
        for l in _:
            try:
                # 尝试将标签转为整数以匹配 legend_labels 的 key
                key = int(float(l))
                new_labels.append(legend_labels.get(key, f"Cluster {l}"))
            except ValueError:
                new_labels.append(f"Cluster {l}")

        plt.legend(handles, new_labels, title="Topic Categories", bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.title('CS2 Comments Clustering Analysis (PCA)', fontsize=15)
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.tight_layout()

    save_path = os.path.join(IMG_DIR, 'clustering_scatter.png')
    plt.savefig(save_path, dpi=300)
    print(f"[SUCCESS] 散点图已保存: {save_path}")
    plt.close()


def plot_sentiment_pie():
    """绘制情感倾向饼图"""
    print("[INFO] 正在绘制情感饼图...")

    if not os.path.exists(SENTIMENT_FILE):
        print(f"[ERROR] 找不到情感分析结果: {SENTIMENT_FILE}")
        return

    df = pd.read_csv(SENTIMENT_FILE)

    # 统计数量
    counts = df['sentiment_label'].value_counts()
    # 假设 1=正面, 0=负面
    labels = ['Positive (1)', 'Negative (0)']
    sizes = [counts.get(1, 0), counts.get(0, 0)]
    colors = ['#66b3ff', '#ff9999']  # 蓝色和红色

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
            startangle=140, pctdistance=0.85, explode=(0.05, 0), shadow=True)

    # 绘制中心白圆（甜甜圈效果）
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.title('CS2 Sentiment Ratio', fontsize=16)
    plt.tight_layout()

    save_path = os.path.join(IMG_DIR, 'sentiment_pie.png')
    plt.savefig(save_path, dpi=300)
    print(f"[SUCCESS] 饼图已保存: {save_path}")
    plt.close()


def plot_sentiment_distribution():
    """绘制情感分数密度分布图 (直方图 + KDE)"""
    print("[INFO] 正在绘制情感分布直方图...")

    if not os.path.exists(SENTIMENT_FILE):
        print(f"[WARN] 文件不存在，跳过分布图绘制: {SENTIMENT_FILE}")
        return

    df = pd.read_csv(SENTIMENT_FILE)

    plt.figure(figsize=(10, 6))

    # 绘制直方图和密度曲线
    sns.histplot(df['sentiment_score'], bins=30, kde=True, color='purple', stat='density')

    # 添加辅助线
    plt.axvline(0.5, color='gray', linestyle='--', label='Neutral (0.5)')

    plt.title('Sentiment Score Distribution', fontsize=15)
    plt.xlabel('Score (0=Negative, 1=Positive)', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.legend()

    save_path = os.path.join(IMG_DIR, 'sentiment_distribution.png')
    plt.savefig(save_path, dpi=300)
    print(f"[SUCCESS] 分布图已保存: {save_path}")
    plt.close()


if __name__ == '__main__':
    # 1. 设置字体
    set_chinese_font()

    # 2. 依次绘图
    plot_clustering_scatter()
    plot_sentiment_pie()
    plot_sentiment_distribution()

    print("\n[DONE] 所有图表绘制完成，请检查 visualization/images 目录。")