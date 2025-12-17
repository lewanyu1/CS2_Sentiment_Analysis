# Scrapy settings for cs_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "cs_spider"

SPIDER_MODULES = ["cs_spider.spiders"]
NEWSPIDER_MODULE = "cs_spider.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "cs_spider (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Concurrency and throttling settings
#CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 5

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "cs_spider.middlewares.CsSpiderSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   "cs_spider.middlewares.CsSpiderDownloaderMiddleware": 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "cs_spider.pipelines.CsSpiderPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
# 1. 确保这一行是 False

## 3. 设置 User-Agent (使用你提供的 Mac 版本)
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'

DEFAULT_REQUEST_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'connection': 'keep-alive',
    # 粘贴最新 Cookie（包含 BA_HECTOR 和最新的校验位）
    'cookie': 'BAIDUID_BFESS=F3B87751835B41E3E7A843F158C032F7:FG=1; BDUSS=X41LTN1ckhTYkd5cTV3U1JORDhxY1poaGppNjF4WGVRMjlCY05MTXRPYmdLVmxvSVFBQUFBJCQAAAAAAAAAAAEAAACa1qiwwNbA8cC0wPHN-QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOCcMWjgnDFoR; BDUSS_BFESS=X41LTN1ckhTYkd5cTV3U1JORDhxY1poaGppNjF4WGVRMjlCY05MTXRPYmdLVmxvSVFBQUFBJCQAAAAAAAAAAAEAAACa1qiwwNbA8cC0wPHN-QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOCcMWjgnDFoR; BAIDU_WISE_UID=wapp_1748098094696_836; Hm_lvt_292b2e1608b0823c1cb6beef7243ef34=1753194049; BIDUPSID=F3B87751835B41E3E7A843F158C032F7; PSTM=1754492969; H_WISE_SIDS=60279_62327_63143_63325_63881_63947_64009_64128_64142_64165_64173_64183_64215_64245_64247_64254_64258_64261_64306_64271_64317_64358_64365_64362_64364; STOKEN=0b6ccd8816a9962410f794139996da9fb5532563fd273293344201d2541081b2; wise_device=0; USER_JUMP=-1; 2963855002_FRSVideoUploadTip=1; video_bubble2963855002=1; BDRCVFR[abe9uUBlp-C]=mbxnW11j9Dfmh7GuZR8mvqV; H_PS_PSSID=60279_63143_66220_66242_66381_66291_66393_66529_66588_66580_66594_66604_66654_66678_66669_66718_66745_66616_66771_66787_66801_66803_66827_66850_66599_66841_66605; ZFY=Mjk1NN:BsIQBtyK3M5jPZJzAmg1v58NktHQ96IHJzjPs:C; arialoadData=false; TIEBA_SID=H4sIAAAAAAAAAzO0tDQwNo83BAATZ608CAAAAA; __ymg_scsc=1_8b0fc33b0ed8c9d299d085288c668b473cbf7373_06942c8ba; XFI=715d1d40-db5b-11f0-b7ea-3704d834255b; BA_HECTOR=8h24010l81842g21a5810k0h2h81001kk5ibg25; ariaappid=c890648bf4dd00d05eb9751dd0548c30; ariauseGraymode=false; XFCS=FB189D361E5017E616149CC74989B8EE7551D7C687908180C9F1AEB382FD1993; XFT=vmf5P5PZdcfOFZr6lablzNaIti31WduqK3Lh18sPpRc=',
    'host': 'tieba.baidu.com',
    'referer': 'https://tieba.baidu.com/f?kw=csgo&ie=utf-8&pn=350',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
}
COOKIES_ENABLED = False


# --- 8. 编码 ---
FEED_EXPORT_ENCODING = 'utf-8'
FEEDS = {
    # 键(Key)：填您指定的完整路径（必须带文件名，比如 .csv）
    '/home/rulerwxe/Code/pycharm/CS2_Sentiment_Analysis/2_data_warehouse/raw_data/tieba_result.csv': {

        # 格式：存成 CSV 表格
        'format': 'csv',

        # 编码：必须是 utf-8，不然中文会变乱码
        'encoding': 'utf-8',

        # 覆盖模式：True = 每次运行把旧的删了存新的 (相当于 -O)
        #           False = 每次运行接着往后写 (相当于 -o)
        # 太奶您测试的时候，建议用 True，看着清爽
        'overwrite': False,
    }
}

# 4. 自动限速与反爬保护
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2.0      # 初始延迟
AUTOTHROTTLE_MAX_DELAY = 10.0       # 最大延迟
RANDOMIZE_DOWNLOAD_DELAY = True     # 随机抖动延迟
CONCURRENT_REQUESTS = 2             # 降低并发，稳定压倒一切



# --- 4. 也是限制并发 (双重保险) ---
CONCURRENT_REQUESTS_PER_IP = 1







# 4. 最快也不能快过多少 (比如最快1秒，防止太快被封)
# 如果您觉得太慢，可以改成 3.0，但建议稳一点
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# 5. 开启调试模式 (方便您在日志里看到现在的真实速度)
AUTOTHROTTLE_DEBUG = True

HTTPERROR_ALLOWED_CODES = [403]
RETRY_HTTP_CODES = [403, 429, 500, 503]
RETRY_TIMES = 5 # 遇到403重试5次
# --- 其他配置保持不变 ---

CLOSESPIDER_ITEMCOUNT = 5100

