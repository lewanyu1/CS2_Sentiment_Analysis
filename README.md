这是一份经过深度优化的 **README.md** 源码。

我已经修复了您提供的文本中的格式问题（例如代码块没有正确闭合、列表排版混乱等），并美化了排版。您可以直接点击右上角的 **“复制”** 按钮，一键粘贴使用。


# 🔫 CS2 贴吧舆情分析系统 (CS2 Sentiment Analysis)

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg) ![Scrapy](https://img.shields.io/badge/Scrapy-2.11-green.svg) ![Sklearn](https://img.shields.io/badge/Sklearn-NLP-orange.svg) ![Jieba](https://img.shields.io/badge/Jieba-Chinese_Seg-red.svg)

> **项目简介**
> 本项目是一个基于 Python 的全流程舆情分析系统，针对百度贴吧《反恐精英 2 (CS2)》吧的评论数据进行深度挖掘。
> 系统实现了从**分布式爬虫数据采集**、**NLP 文本预处理**（分词、去停用词、NER）、**特征工程**（TF-IDF），到**无监督学习**（K-Means 聚类）及**情感倾向分析**的完整技术链路，并提供多维度的可视化展示。

---

## 📂 项目结构 (Project Structure)

本项目采用模块化设计，目录结构对应学术论文的章节逻辑：

```text
CS2_Sentiment_Analysis/
├── main.py                          # [总入口] 自动化全流程控制脚本 (Pipeline)
├── requirements.txt                 # [依赖] 项目所需第三方库列表
├── .gitignore                       # [配置] Git 忽略规则
│
├── 1_data_collection/               # [数据采集] 原 spider_service (对应论文第2章)
│   └── spiders/                     # Scrapy 爬虫核心
│       └── cs_spider/               # 百度贴吧解析规则与抓取逻辑
│
├── 2_data_warehouse/                # [数据仓库] (对应论文 2.1 & 2.2)
│   ├── raw_data/                    # 原始数据 (CSV格式)
│   └── processed_data/              # 中间数据 (清洗后/分词后/TF-IDF矩阵)
│
├── 3_nlp_processor/                 # [NLP 预处理] (对应论文第3章)
│   ├── dicts/                       # 词典资源
│   │   ├── Cs2_dict.txt             # 领域专用词典 (如: 磨损, 崭新出厂)
│   │   ├── stopwords_hit.txt        # 停用词表 (含单字与高频虚词过滤)
│   │   └── ner_dict.json            # 命名实体识别规则库
│   │
│   ├── cleaner.py                   # 1. 文本清洗 (正则去噪、HTML标签去除)
│   ├── tokenizer.py                 # 2. 中文分词 (Jieba精准模式 + 停用词过滤)
│   ├── pos_tagger.py                # 3. 词性标注 (POS Tagging)
│   ├── ner.py                       # 4. 命名实体识别 (NER)
│   └── vectorizer.py                # 5. 特征向量化 (TF-IDF 矩阵构建)
│
├── 4_analysis_service/              # [深度分析] (对应论文 4.1 - 4.4)
│   ├── models/                      # 模型持久化存储 (.pkl)
│   │
│   ├── keyword_extractor.py         # 6. 关键词提取 (基于 TF-IDF 权重)
│   ├── sentiment_classifier.py      # 7. 情感倾向分析 (SnowNLP + 自定义逻辑)
│   └── clustering.py                # 8. 文本聚类 (K-Means 算法)
│
└── 5_visualization/                 # [数据可视化] (对应论文 4.5)
    ├── images/                      # 结果图片输出目录
    ├── wordcloud_plot.py            # 特色词云绘制 (AK-47 蒙版)
    └── charts_plot.py               # 统计图表 (情感占比饼图、聚类散点图等)

```

---

## 🛠️ 核心功能与技术栈

### 1. 数据采集 (Data Collection)

* **核心技术**: `Scrapy` 框架
* **功能**: 异步并发爬取百度贴吧帖子及楼中楼回复，支持 IP 代理池与 User-Agent 轮询反爬策略。
* **产出**: 结构化 CSV 数据 (`user`, `content`, `time`, `platform`).

### 2. 自然语言处理 (NLP)

* **分词**: 使用 `Jieba` 进行中文分词，挂载 `Cs2_dict.txt` 保证游戏术语（如“大行动”、“印花”）切分准确。
* **清洗**: 实现了**动态停用词过滤**与**单字去除**逻辑，有效去除“兄弟”、“一下”、“都”等无意义高频词。
* **特征**: 使用 `Scikit-learn` 构建 **TF-IDF 向量空间模型** (Vector Space Model)，提取文本特征。

### 3. 挖掘与分析 (Mining)

* **聚类分析**: 使用 **K-Means** 算法将评论自动聚类为不同主题（如：饰品交易、游戏体验、外挂吐槽），并通过 **PCA** 降维进行二维可视化。
* **情感分析**: 基于 `SnowNLP` 计算每条评论的情感得分（0~1），量化社区舆论的正负面倾向。
* **关键词提取**: 提取各类别及全局的 Top 权重关键词。

### 4. 可视化 (Visualization)

* **词云图**: 结合 AK-47 剪影图片生成 CS2 特色词云。
* **统计图表**: 生成情感分布饼图、聚类散点图、Top 关键词条形图。

---

## 🚀 快速开始 (Quick Start)

### 环境要求

* Python 3.8+
* 操作系统: Windows / macOS / Linux

### 安装与运行

1. **克隆项目**
```bash
git clone [https://github.com/YourUsername/CS2-Sentiment-Analysis.git](https://github.com/YourUsername/CS2-Sentiment-Analysis.git)
cd CS2-Sentiment-Analysis

```


2. **安装依赖**
```bash
pip install -r requirements.txt

```


3. **运行全流程**
本项目内置了自动化流水线脚本 `main.py`，一键完成从预处理到可视化的所有工作：
```bash
python main.py

```


*(注：控制台将实时显示分词、向量化、聚类等各个阶段的执行进度与耗时)*
4. **查看结果**
程序运行结束后，请前往 `5_visualization/images/` 目录查看生成的分析图表。

