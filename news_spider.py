"""新闻文章库下载"""

import httpx
from lxml import etree
from fatgoose3 import FatGoose
from fatgoose3.text import StopWordsChinese
from retrying import retry


@retry(stop_max_attempt_number=3)
def spider(url, num,index):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    resp = httpx.get(url, headers=headers, timeout=30)

    print(f"[{index+1}] {url} 文章内容下载中...")

    tree = etree.HTML(resp.text)
    s = tree.xpath("//h4/a/@href")

    g = FatGoose()
    g.config.use_meta_language = False
    g.config.target_language = 'zh'
    g.config.stopwords_class = StopWordsChinese

    content = ""
    for i in s:
        print(i)
        resp = httpx.get(i, headers=headers, timeout=30)
        resp.encoding = 'utf8'
        news = g.extract(url=url, raw_html=resp.text)
        print(news.title)
        print(news.cleaned_text)
        content += news.title + "\n" + news.cleaned_text + "\n"
    with open(f'news/news{num}.txt', 'a', encoding="utf-8") as f:
        f.write(content)


for i in range(2765):
    if i > 80:
        url = f'http://sousuo.gov.cn/column/16705/{i}.htm'
        num = int(i/20)+1
        spider(url, num,i)
