import subprocess
import os
import sys
import time

# ============================
# 0. 环境配置
# ============================
PYTHON_EXEC = sys.executable
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_script(script_rel_path, step_name):
    """
    通用脚本执行器
    """
    script_path = os.path.join(BASE_DIR, script_rel_path)

    print(f"\n{'-' * 60}")
    print(f"[Step: {step_name}] 开始执行...")
    print(f"Script: {script_rel_path}")

    if not os.path.exists(script_path):
        print(f"[SKIP] 找不到脚本文件: {script_rel_path}")
        return False

    start_time = time.time()
    try:
        subprocess.run([PYTHON_EXEC, script_path], check=True)
        end_time = time.time()
        print(f"[SUCCESS] 阶段完成. 耗时: {end_time - start_time:.2f}s")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] 脚本执行出错 (Exit Code: {e.returncode})")
        return False


def main():
    print("=" * 60)
    print("CS2 舆情分析系统 - 自动化执行流水线")
    print("=" * 60)

    pipeline_start = time.time()

    # ========================================================
    # 流水线配置
    # ========================================================
    pipeline = [
        # --- 1. 数据采集 (默认跳过) ---
        # ("1_data_collection/run_spider.py", "Step 1: 贴吧数据爬取"),

        # --- 2. 自然语言处理 ---
        ("3_nlp_processor/tokenizer.py", "Step 2: 中文分词与清洗"),
        ("3_nlp_processor/vectorizer.py", "Step 3: 构建 TF-IDF 向量矩阵"),

        # --- 3. 分析服务 ---
        ("4_analysis_service/clustering.py", "Step 4: K-Means 聚类分析"),
        ("4_analysis_service/sentiment_classifier.py", "Step 5: 情感倾向分析"),
        ("4_analysis_service/keyword_extractor.py", "Step 6: 关键词提取"),

        # --- 4. 数据可视化 ---
        ("5_visualization/charts_plot.py", "Step 7: 生成统计图表"),
        ("5_visualization/wordcloud_plot.py", "Step 8: 生成词云图"),
    ]

    # ========================================================
    # 执行逻辑
    # ========================================================
    if not os.path.exists(os.path.join(BASE_DIR, '2_data_warehouse', 'raw_data', 'tieba_raw.csv')):
        print("[WARN] 未检测到原始数据 'tieba_raw.csv'，请确保数据已存在。")

    success_count = 0
    for script, desc in pipeline:
        if run_script(script, desc):
            success_count += 1
        else:
            print(f"\n[FATAL] 流水线因错误中断")
            sys.exit(1)

    # ========================================================
    # 结束
    # ========================================================
    pipeline_end = time.time()
    total_time = pipeline_end - pipeline_start

    print(f"\n{'=' * 60}")
    print(f"[DONE] 所有任务执行完毕")
    print(f"进度: {success_count}/{len(pipeline)}")
    print(f"总耗时: {total_time:.2f}s")
    print(f"结果输出: 5_visualization/images/")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    main()