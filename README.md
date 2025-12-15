# CS2_Sentiment_Analysis
基于 Scrapy 的百度贴吧（CS2）评论爬取与情感分析\

## 📂 项目结构图

```text
CS2_Sentiment_Analysis/  (项目总目录)
│
├── 1_spider_service/        <-- 【收菜部】Scrapy爬虫模块
│   └── cs_spider/           (标准的Scrapy项目结构)
│       ├── spiders/
│       │   └── tieba.py     (具体的爬虫逻辑)
│       ├── items.py         (定义数据模型)
│       ├── pipelines.py     (存数据：存入数据库/Raw Data)
│       ├── middlewares.py   (反爬中间件：加代理、换User-Agent)
│       └── settings.py      (配置文件)
│
├── 2_data_warehouse/        <-- 【仓库部】数据存储
│   ├── raw_data/            (存放爬下来的原始 dirty data，如 json/csv)
│   └── processed_data/      (存放清洗后的干净数据)
│
├── 3_nlp_processor/         <-- 【洗菜切菜部】数据清洗与预处理 (Pandas/Jieba)
│   ├── cleaner.py           (去广告、去重、去表情)
│   └── tokenizer.py         (分词、去停用词)
│
├── 4_analysis_service/      <-- 【大厨部】模型分析与可视化
│   ├── emotion_model.py     (情感分析模型)
│   ├── wordcloud_gen.py     (生成词云)
│   └── charts.py            (画matplotlib/echarts图)
│
├── requirements.txt         (依赖包列表)
└── README.md                (说明书)
```

