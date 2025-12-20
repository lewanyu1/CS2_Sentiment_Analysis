import scrapy
from cs_spider.items import CsSpiderItem
from scrapy.exceptions import CloseSpider
import re


class TiebaSpider(scrapy.Spider):
    name = "tieba"
    allowed_domains = ["baidu.com"]
    # 1. 设置起始页为 pn=200（第 5 页）
    start_urls = ["https://tieba.baidu.com/f?ie=utf-8&kw=csgo&pn=200"]

    # 2. 如果您希望日志显示的进度包含之前的 2149 条，可以将初始值设为 2149
    # 如果设为 0，则只计算本次运行抓到的数量
    scraped_comment_count = 0
    TARGET_TOTAL = 5000  # 目标总数

    def parse(self, response):
        """解析列表页并处理翻页"""
        html_content = response.text

        # 提取当前页帖子链接和标题
        pattern = r'<a\s+[^>]*?href="/p/(\d+)"[^>]*?title="([^"]+)"[^>]*?class="j_th_tit\s*"'
        results = re.findall(pattern, html_content)

        for tid, title in results:
            if tid in ['10206118138', '10303647508', '9040890016']:
                continue

            full_link = f"https://tieba.baidu.com/p/{tid}"
            yield scrapy.Request(
                url=full_link + "?pn=1",
                callback=self.parse_detail,
                meta={
                    'title': title,
                    'link': full_link,
                    'page': 1,
                    'all_comments': []
                }
            )

        # 列表页翻页逻辑
        current_pn_match = re.search(r'pn=(\d+)', response.url)
        current_pn = int(current_pn_match.group(1)) if current_pn_match else 0

        if self.scraped_comment_count < self.TARGET_TOTAL and current_pn < 3000:
            next_pn = current_pn + 50
            next_list_url = f"https://tieba.baidu.com/f?kw=csgo&ie=utf-8&pn={next_pn}"
            self.logger.info(f"--- 正在跳转至列表页下一页: pn={next_pn} ---")
            yield scrapy.Request(url=next_list_url, callback=self.parse, priority=-10)

    def parse_detail(self, response):
        """解析帖子详情页：聚合评论并实施计数停止"""
        title = response.meta.get('title')
        link = response.meta.get('link')
        current_page = response.meta.get('page', 1)
        all_comments = response.meta.get('all_comments', [])

        blacklist = ["该楼层疑似违规已被系统折叠", "隐藏此楼", "查看此楼", "来自客户端"]

        # 抓取评论内容
        post_nodes = response.xpath(
            "//div[contains(@class, 'd_post_content')] | //span[contains(@class, 'lzl_content_main')]")

        for node in post_nodes:
            text_segments = node.xpath(".//text()").getall()
            content = "".join([t.strip() for t in text_segments if t.strip()])

            if any(word in content for word in blacklist):
                continue
            content = re.sub(r'IP属地:[^ ]+', '', content)
            content = re.sub(r'\d+楼\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}', '', content)
            content = content.replace("回复", "").strip()

            if len(content) > 2:
                all_comments.append(content)

        # 获取网页上的总页数信息（用于翻页判断）
        page_info = response.xpath("//li[@class='l_reply_num']//span[@class='red']/text()").getall()
        total_page = 1
        if len(page_info) >= 2:
            try:
                total_page = int(page_info[1])
            except ValueError:
                total_page = 1

        # 判定是否翻页
        if current_page < total_page:
            yield scrapy.Request(
                url=f"{link}?pn={current_page + 1}",
                callback=self.parse_detail,
                meta={
                    'title': title,
                    'link': link,
                    'page': current_page + 1,
                    'all_comments': all_comments
                }
            )
        else:
            # --- 核心改动：计算本帖实际抓取的评论数 ---
            actual_this_thread_count = len(all_comments)
            self.scraped_comment_count += actual_this_thread_count

            item = CsSpiderItem()
            item['title'] = title
            item['link'] = link

            # 这里存入的是本次【真实抓取】的数量，而不是网页显示的数字
            item['reply_num'] = str(actual_this_thread_count)

            item['content'] = "\n".join(all_comments)
            yield item

            self.logger.info(
                f"--- 帖子抓取完毕：{title} | 实际提取: {actual_this_thread_count} 条 | 总进度: {self.scraped_comment_count} 条 ---")

            if self.scraped_comment_count >= self.TARGET_TOTAL:
                raise CloseSpider(f'已完成本次采集目标：{self.scraped_comment_count}')