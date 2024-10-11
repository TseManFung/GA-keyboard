import requests
from bs4 import BeautifulSoup
import re
import time

s = requests.Session()

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'cache-control': 'max-age=0',
    'cookie': '_ga=GA1.1.2101828073.1728635690; night=0; Hm_lvt_1251eb70bc6856bd02196c68e198ee56=1728635708; HMACCOUNT=448964DE3B8E19C9; jieqiRecentRead=2139.76674.0.1.1728636778.0; _ga_NG72YQN6TX=GS1.1.1728635690.1.1.1728636778.0.0.0; cf_clearance=PJKhcIrIIkQ_HaoAtWV6rVM2zIXPv66TMviE.oGc1KM-1728636779-1.2.1.1-9cWaRJWwykDWbd9DDm_GKSv2yYCqMsCU2nUe.eZebzgVZqbo.Iu8qNnjXFgKvhk2SEAVHoW8QVIet4xuZmeUuxq3DC3By.xclYqZBbPXqnC_Mpa8QcZUZ24gPhPOIG1_k.5AyRDd5jx6jdzgmMJRiw_MZyMCK0Lh5zz_QhCV8Q7TE8HLOIZvJB.AaHngujAC6y_uxKbuOedxU7ZwbIpNqsPNeTm6v9tiN3KMXYBUE.uoC1AvZ02XhOoNidMSIzpZ_MCdktNdFVDPC9mKjtnhrPUao5fsRRGG4q025pGjDc07.uDGVY8buVscGQz3valYUvFNNRdt.qs.2YTmte_h8ezLRd0to83zYiro_MJenA1gWH0slzy3h0OjKRBX1AqNQDOkL_VOlrk.sdwW1BxDtQ; FCNEC=%5B%5B%22AKsRol_5ejaY8oAdRJIR2c3K5t_Pr7WjXR_qXLtRBg8DXfDf4PL4LRZQUcyaQV85KjrWuNvq68TKzZg2WFGmkn1qXqWczR6wuXFNNaKXn0N3hlPsIPYuUvi68D9WyDMJhN8NSjlq6t0JiqOLHPIVKOSEq0CKe0lYKA%3D%3D%22%5D%5D; Hm_lpvt_1251eb70bc6856bd02196c68e198ee56=1728636780',
    'if-modified-since': 'Thu, 10 Oct 2024 03:29:26 GMT',
    'priority': 'u=0, i',
    'referer': 'https://tw.linovelib.com/novel/2139/76673.html',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

s.headers.update(headers)


# URL of the catalog page
catalog_url = input(
    r"Enter the URL of the catalog page (exp: 'https://tw.linovelib.com/novel/2139/catalog'): ")

pattern = r'[\t ，。,.:：;；!！?？—\-「」『』【】《》〈〉〔〕〖〗〘〙〚〛〝〞〟〰‥…‧﹏﹑﹔﹖﹪﹫？｡。\\/:*?"<>|\(\)─]'

# Send a GET request to the catalog page
response = s.get(catalog_url)
soup = BeautifulSoup(response.content, 'html.parser')
title = soup.title.string.split('線上看')[0]
title = re.sub(pattern, '', title)

chapter_links = soup.find_all('a', class_='chapter-li-a')

# Iterate through each chapter link
for link in chapter_links:
    href = link.get('href')
    href = 'https://tw.linovelib.com' + href
    if href:
        # Send a GET request to the chapter page
        try:
            chapter_response = s.get(href)
            chapter_soup = BeautifulSoup(chapter_response.content, 'html.parser')
        except:
            pass
        # Find the element with id 'apage' and get its text
        apage_element = chapter_soup.find(id='apage')
        if apage_element:
            # save to file dataset\text\
            with open(f'dataset\\text\\{title}.txt', 'a',
                      encoding='utf-8') as file:
                file.write(re.sub(pattern, '', apage_element.text))
