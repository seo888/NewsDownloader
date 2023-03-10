"""过滤new目录所有文章"""

import re
import os


def filter_news(file_name):
    """过滤new目录所有文章"""
    with open(f"news/{file_name}", 'r', encoding='utf-8')as txt_f:
        text = txt_f.read().strip()
    text = text.replace("习近平", "席大大").replace("李克强", "李大大")
    lines = text.split("\n")
    words = set()
    for line in lines:
        re_find = re.findall(" _.*", line)
        if len(re_find) > 0:
            for i in re_find:
                words.add(i)
    print(words)
    for i in words:
        text = text.replace(i, "")

    words = set()
    for line in lines:
        re_find = re.findall("_.*", line)
        if len(re_find) > 0:
            for i in re_find:
                words.add(i)
    print(words)
    for i in words:
        text = text.replace(i, "")

    text_list = []
    for line in text.split("\n"):
        new_line = line.strip()
        if len(new_line) > 5:
            # print(new_line)
            text_list.append(new_line)
    with open(f'news_ok/{file_name}', 'w', encoding='utf-8')as txt_f:
        txt_f.write("\n".join(text_list))


def main():
    """主程"""
    if not os.path.exists('news_ok'):
        os.mkdir('news_ok')
    for i in os.listdir("news"):
        print(i)
        filter_news(i)


if __name__ == "__main__":
    main()
