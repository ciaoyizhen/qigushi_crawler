import os
import re
import requests
from tqdm import tqdm
from lxml import etree
from urllib.parse import urljoin

base_url = "https://www.qigushi.com/"

headers = {
    "User-Agent": "你自己的浏览按F12找到下面的User-Agent，copy进来"
}
response = requests.get(base_url, headers=headers)
print(response)
response.encoding = "utf-8"
html = etree.HTML(response.text)
urls_1 = html.xpath("//*[@class='story_list']//li/a/@href")
urls_2 = html.xpath("//*[@class='story_list ']//li/a/@href")
urls_1.extend(urls_2)
urls = list(set(urls_1))

save_dir = "stories"
if not os.path.exists(save_dir):
    os.mkdir(save_dir)

for url in tqdm(urls):
    if not url.startswith("http"):
        url = urljoin(base_url, url)
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    html = etree.HTML(response.text)
    title = html.xpath("//div[@class='title']/h1/text()")
    content = html.xpath("//div[@class='article_content']//text()")
    if len(title) != 1:
        print(url)
        print(title)
        continue
    title = title[0]
    with open(os.path.join(save_dir, f"{title}.txt"), "w", encoding="utf-8") as f:
        for line in content:
            line = re.sub("\s+", "", line).strip()
            if line:
                f.write(line + "\n")
                
                
                