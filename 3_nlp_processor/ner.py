'''
命名实体识别
修正版
'''
#导包
import jieba
import platform
import os
import json
import pandas as pd
from typing import Dict, List

# ============================
# 1. 路径配置
# ============================
if platform.system() == 'Linux':
    BASE_DIR = r'/home/rulerwxe/Code/pycharm/CS2_Sentiment_Analysis'
elif platform.system() == 'Darwin':
    BASE_DIR = r'/Users/rulerwxe/programming/temporory/NLP/CS2_Sentiment_Analysis'
else:
    # 建议加上 Windows 兜底，防止报错
    BASE_DIR = r'D:\Code\CS2_Sentiment_Analysis'

DATA_DIR = os.path.join(BASE_DIR, '2_data_warehouse/processed_data')
DICT_DIR = os.path.join(BASE_DIR, '3_nlp_processor')

# 建议：字典最好放在 dicts 子目录下
input_file = os.path.join(DATA_DIR, 'comment.csv')
output_file = os.path.join(DATA_DIR, 'comment_ner_result.csv')

# 注意检查您的文件名大小写，您写的是 Cs2...V1.json
CS2_NER_DICT_PATH = os.path.join(DICT_DIR, 'Cs2_ner_dict_V1.json')

# ============================
# 2. 功能函数
# ============================

# 加载资源
def load_resourse():
    print(f"正在加载字典: {CS2_NER_DICT_PATH}")
    if not os.path.exists(CS2_NER_DICT_PATH):
        print("❌ 找不到字典文件")
        return {}
    try:
        with open(CS2_NER_DICT_PATH, 'r', encoding='utf-8') as f:
            entity_dict = json.load(f)
            print(f"✅ 成功加载词典，共 {len(entity_dict)} 个词条")
            return entity_dict
    except json.JSONDecodeError as e:
        print(f"❌ JSON解码错误: {e}") # 修正：打印具体错误
    except Exception as e:
        print(f"❌ 未知错误: {e}")
    return {}

# 原子函数（只负责处理单条数据）
def extract_entities(text: str, entity_dict: dict):
    # 边界检查：防止非字符串输入报错
    if not isinstance(text, str) or not text.strip():
        return "{}" # 返回空JSON字符串，保持格式一致

    entities_dict = {}

    # 使用搜索引擎模式分词，召回率更高
    words = jieba.lcut_for_search(text)

    for word in words:
        # 归一化
        clean_word = word.strip().lower()

        # 核心逻辑：只有在字典里，才进行后续操作
        if clean_word in entity_dict:
            category = entity_dict[clean_word]

            # --- 修复 1：缩进修正 ---
            # 这些操作必须在 if 里面！
            if category not in entities_dict:
                entities_dict[category] = []

            # 去重添加
            if word not in entities_dict[category]:
                entities_dict[category].append(word)

    # 如果没找到，返回空JSON字符串
    if not entities_dict:
        return "{}"

    return json.dumps(entities_dict, ensure_ascii=False)

def save_ner_data(df, output_file):
    print(f"💾 正在保存结果至: {output_file}")
    # 容错：只保存存在的列
    cols = ["comment", "comment_ner"]
    valid_cols = [c for c in cols if c in df.columns]

    df[valid_cols].to_csv(output_file, index=False, encoding='utf-8-sig')

# 批处理
def process_ner(input_file: str, output_file: str, entity_dict: dict):
    if not os.path.exists(input_file):
        print("❌ 输入文件不存在")
        return

    try:
        print("🚀 开始 NER 匹配...")
        # 读csv文件
        df = pd.read_csv(input_file)

        # 容错：防止没有 'comment' 列
        target_col = 'comment' if 'comment' in df.columns else df.columns[0]

        # 应用函数
        df['comment_ner'] = df[target_col].astype(str).apply(
            lambda x: extract_entities(x, entity_dict)
        )
        df_clean=df[df['comment_ner']!="{}"]

        # --- 修复 2：比较逻辑修正 ---
        # 必须和字符串 "{}" 比较，不能和字典 {} 比较
        hit_count = len(df[df['comment_ner'] != "{}"])
        total = len(df)

        # --- 修复 3：打印变量修正 ---
        print(f"📊 处理完成：共 {total} 条数据，成功挖掘到实体 {hit_count} 条 ({(hit_count/total):.1%})")

        save_ner_data(df_clean, output_file)

    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    entity_dict = load_resourse()
    # 只有字典加载成功才运行
    if entity_dict:
        process_ner(input_file, output_file, entity_dict)
