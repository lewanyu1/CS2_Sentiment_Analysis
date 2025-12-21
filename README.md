# CS2_Sentiment_Analysis
基于 Scrapy 的百度贴吧（CS2）评论爬取与情感分析\

## 📂 项目结构图


```text
CS2_Sentiment_Analysis/
├── main.py                          # [入口] 主程序
├── requirements.txt                 # [依赖]
│
├── 1_data_collection/               # [改名] 原 spider_service，对应论文第2章
│   └── spiders/                     # Scrapy 爬虫
│       └── cs_spider/               # 具体爬虫代码
│
├── 2_data_warehouse/                # [数据] 对应论文 2.1 & 2.2
│   ├── raw_data/                    # 原始数据
│   └── processed_data/              # 中间数据(清洗后/向量化后)
│
├── 3_nlp_processor/                 # [预处理] 对应论文第3章
│   ├── dicts/                       # 字典文件夹
│   │   ├── Cs2_dict.txt             # 分词词典
│   │   ├── stopwords_hit.txt        # 停用词表
│   │   └── ner_dict.json            # 实体识别字典
│   │
│   ├── cleaner.py                   # 1. 文本预处理 (对应要求: 文本预处理)
│   ├── tokenizer.py                 # 2. 分词 (对应要求: 分词)
│   ├── pos_tagger.py                # 3. 词性标注 (对应要求: 词性标注)
│   ├── ner.py                       # 4. 命名实体识别 (对应要求: NER)
│   └── vectorizer.py                # 5. 文本向量化 (对应要求: 文本向量化)
│
├── 4_analysis_service/              # [分析] 对应论文 4.1 - 4.4
│   ├── models/                      # 存放训练好的 pkl 模型
│   │
│   ├── keyword_extractor.py         # 6. 关键词提取 (对应要求: 关键词提取)
│   ├── sentiment_classifier.py      # 7. 文本分类 (原emotion_model，对应要求: 文本分类)
│   └── clustering.py                # 8. 文本聚类 (对应要求: 文本聚类)
│
├── 5_visualization/                 # [展示]  对应论文 4.5
│   ├── wordcloud_plot.py            # 词云图绘制
│   └── charts_plot.py               # 原 charts.py，绘制柱状图/饼图/折线图
│
└── utils/                           # [工具]
    └── config.py                    # 全局配置

```

