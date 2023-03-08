"""新闻文章库下载"""

import threading
import httpx
from lxml import etree
from fatgoose3 import FatGoose
from fatgoose3.text import StopWordsChinese
from retrying import retry


class NewsSpider():
    """新闻文章库下载"""

    def __init__(self):
        self.links = []
        self.title = ''
        self.content = ''
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        self.goose = FatGoose()
        self.goose.config.use_meta_language = False
        self.goose.config.target_language = 'zh'
        self.goose.config.stopwords_class = StopWordsChinese
        self.lock = threading.Lock()

    @retry(stop_max_attempt_number=3)
    def thread_go(self,tname):
        """多线程下载内页"""
        while len(self.links) > 0:
            with self.lock:
                link = self.links.pop(0)
            if not link.startswith('http://www.gov.cn'):
                continue
            resp = httpx.get(link, headers=self.headers, timeout=30)
            resp.encoding = 'utf8'
            news = self.goose.extract(url=link, raw_html=resp.text)
            print(f"[{tname}]标题：{news.title}")
            print(f"[{tname}]文章：{news.cleaned_text[:20]}......")
            self.title += news.title + "\n"
            self.content += news.title + "\n" + news.cleaned_text + "\n"

    def spider(self, url, num, index):
        """蜘蛛"""

        resp = httpx.get(url, headers=self.headers, timeout=30)
        print(f"[{index+1}] {url} 文章内容下载中...")
        tree = etree.HTML(resp.text)
        self.links = tree.xpath("//h4/a/@href")
        threads = [threading.Thread(
            target=self.thread_go, args=(f't{i}',)) for i in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        with open(f'news/news{num}.txt', 'a', encoding="utf-8") as txt_f:
            txt_f.write(self.content)
        with open('news/title.txt', 'a', encoding="utf-8") as txt_f:
            txt_f.write(self.title)


def main():
    """主程"""
    for i in range(2765):
        if i > 620:
            url = f'http://sousuo.gov.cn/column/16705/{i}.htm'
            num = int(i/20)+1
            try:
                news = NewsSpider()
                news.spider(url, num, i)
            except Exception as err:
                print(err)


if __name__ == "__main__":
    main()
