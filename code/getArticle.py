import requests
from bs4 import BeautifulSoup
import re
import time
import random
from tqdm import tqdm

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}
s = requests.Session()
s.headers.update(headers)

#catalog_url = input(r"Enter the URL of the catalog page (exp: 'https://tw.linovelib.com/novel/2139/catalog'): ")
pattern = r'[\t ，。,，.:：;；!！?？—\-「」『』【】《》〈〉〔〕〖〗〘〙〚〛〝〞〟〰‥…‧﹏﹑﹔﹖﹪﹫？｡。\\/:*?"<>|\(\)─（）／＊、]'

def read_urls():
    with open(r"research\urls.txt", 'r', encoding='utf-8') as file:
        return file.readlines()

def main():
    urls = read_urls()
    for catalog_url in tqdm(urls,desc='All novels'):
        if catalog_url.startswith('#'):
            continue
        response = s.get(catalog_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string.split('小說線上看')[0]
        title = re.sub(pattern, '', title)
        chapter_links = soup.find_all('a', class_='chapter-li-a')

        for link in tqdm(chapter_links,desc=title):
            href = link.get('href')
            href = 'https://tw.linovelib.com' + href
            if href:
                try:
                    chapter_response = s.get(href)
                    chapter_soup = BeautifulSoup(
                        chapter_response.content, 'html.parser')
                except:
                    pass
                apage_element = chapter_soup.find(id='apage')
                if apage_element:
                    # save to file dataset\text\
                    with open(f'dataset\\text\\{title}.txt', 'a',
                            encoding='utf-8') as file:
                        file.write(re.sub(pattern, '', apage_element.text))
                time.sleep(random.random()+1 * 4)

if __name__ == "__main__":
    main()