from selenium import webdriver
import bs4
import pandas as pd
from selenium.webdriver.chrome.options import Options


def getRank2Excle(url):
    # 配置浏览器驱动路径，这里以Chrome浏览器为例
    # chromedriver路径
    driver_path = r'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    # 创建Chrome浏览器实例
    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

    # 设置浏览器窗口大小（可选）
    driver.set_window_size(1366, 768)

    # 设置浏览器隐式等待时间（可选）
    driver.implicitly_wait(10)
    split = url.split('/')[-1]
    driver.get(url)

    # 获取网页HTML内容
    html_content = driver.page_source
    soap = bs4.BeautifulSoup(html_content, 'lxml')
    list = soap.find(class_='rank-list pgc-list')
    if list is None:
        list = soap.find(class_='rank-list')
    list = list.find_all('li')
    data = []
    rank = 1
    for i in list:
        title_element = i.find_all(class_='title')
        href = title_element[0]['href'].split('//')[1]
        value = title_element[0].contents[0]
        data.append({'rank': rank, 'href': href, 'value': value})
        rank = rank + 1

    df = pd.DataFrame(data)
    driver.quit()
    # 写入Excel文件---设置保存路径,如果文件已存在则会覆盖
    df.to_excel(r'D:\Desktop\%s.xlsx' % split, index=False)
if __name__ == '__main__':
    # 打开网页
    # 设置爬虫网址--以bilibili音乐排行榜为例，爬取blibli其他排行榜只需修改url即可
    url = 'https://www.bilibili.com/v/popular/rank/music'
    getRank2Excle(url)