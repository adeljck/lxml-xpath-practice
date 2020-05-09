import requests
from lxml import etree
import pandas as pd
from threading import Thread

def parser(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36 Edg/81.0.416.68",
    }
    res = requests.get(url, headers=headers)
    html = etree.HTML(res.text)
    contents = html.xpath('//div[@class="item"]')
    for content in contents:
        result = dict()
        result["img_link"] = content.xpath("div[1]/a/img/@src")[0].strip()
        result["title"] = content.xpath('div[2]/div[1]/a/span[@class="title"]')[0].text.strip()
        result["link"] = content.xpath('div[2]/div[1]/a/@href')[0].strip()
        result["info"] = content.xpath('div[2]/div[2]/p[@class=""]')[0].text.replace("...", "").strip()
        result["start"] = content.xpath('div[2]/div[2]/div/span[2]')[0].text.strip()
        result["quto"] = content.xpath('div[2]/div[2]/div/span[4]')[0].text.strip().replace("人评价", "")
        short_info = content.xpath('div[2]/div[2]/p[2]/span')
        if short_info:
            result["short_info"] = short_info[0].text.strip()
        else:
            result["short_info"] = "无"
        if content.xpath('div[2]/div[1]/span[@class="playable"]'):
            result["playable"] = "可播放"
        else:
            result["playable"] = "不可播放"
        results.append(result)


if __name__ == '__main__':
    results = list()
    threads = list()
    urls = ["https://movie.douban.com/top250?start={}&filter=".format(i * 25) for i in range(0, 20)]
    for url in urls:
        t = Thread(target=parser, args=(url,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    pd.DataFrame(results).to_excel("results.xlsx", index=False, encoding="utf-8")
