import pandas as pd
import joblib
import os
import sys
from snownlp import SnowNLP
from tqdm import tqdm  # 进度条库
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

#配置路径
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from utils import config
INPUT_TEXT_FILE = config.FILE_COMMENT_SEGMENTED
INPUT_MATRIX_FILE = config.FILE_TFIDF_MATRIX

OUTPUT_SENTIMENT_CSV = os.path.join(config.PROCESSED_DATA_DIR, 'sentiment_analysis_result.csv')
MODEL_OUTPUT = os.path.join(config.MODEL_DIR, 'sentiment_logistic_model.pkl')
def get_sentiment_score(text):
    if not isinstance(text, str) or len(text.strip()) == 0:
        return 0.5  # 空内容给中性分
    try:
        s = SnowNLP(text)
        return s.sentiments
    except:
        return 0.5
def run_sentiment_analysis():


    if not(os.path.exists(INPUT_TEXT_FILE)):
        print(f"找不到文本文件: {INPUT_TEXT_FILE}")
        return
    #读取文本
    df=pd.read_csv(INPUT_TEXT_FILE)
    text_col='tokenized_comment'
    print("正在使用 SnowNLP 进行情感打分 (这可能有点慢，请耐心等待)...")
    tqdm.pandas(desc="Processing Sentiment")  # 开启 pandas 进度条
    df['sentiment_score']=df[text_col].progress_apply(get_sentiment_score)
    df['sentiment_label'] = df['sentiment_score'].apply(lambda x: 1 if x >= 0.5 else 0)

    print(df['sentiment_label'].value_counts())
    if os.path.exists(INPUT_MATRIX_FILE):
        print("\n🎓 开始训练逻辑回归分类模型...")
        tfidf_matrix = joblib.load(INPUT_MATRIX_FILE)
        # 确保矩阵行数和文本行数一致 (防止之前 dropna 导致对不齐)
        # 这是一个简单的对齐检查，实际工程中需要更严谨的 Index 对齐
        if tfidf_matrix.shape[0] == len(df):
            X = tfidf_matrix
            y = df['sentiment_label']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = LogisticRegression(max_iter=1000)
            model.fit(X_train, y_train)
            #评估
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            print(f"模型训练完成！测试集准确率: {acc:.4f}")
            print("分类报告:")
            print(classification_report(y_test, y_pred))
            # 保存模型
            joblib.dump(model, MODEL_OUTPUT)
            print(f"模型已保存至: {MODEL_OUTPUT}")
        else:
            print(f"警告: 矩阵行数 ({tfidf_matrix.shape[0]}) 与 文本行数 ({len(df)}) 不一致，跳过模型训练。")
            print("提示: 仅保存情感打分结果，不影响后续可视化。")
    columns_to_save = [text_col, 'sentiment_score', 'sentiment_label']
    df.to_csv(OUTPUT_SENTIMENT_CSV, index=False, encoding='utf-8-sig')
    print(f"\n最终结果表已保存至: {OUTPUT_SENTIMENT_CSV}")

if __name__ == '__main__':
    run_sentiment_analysis()
