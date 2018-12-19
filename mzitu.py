# -*- coding:utf-8 -*-
import requests
import os
import re
import time
import threading
from lxml import etree
from bs4 import BeautifulSoup
from multiprocessing import Pool,cpu_count

HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': 'http://www.mzitu.com'
}

# page_urls = ['http://www.mzitu.com/page/{cnt}'.format(cnt=cnt) for cnt in range(1, int(bs) + 1)]

DIR_PATH = "D:/mzitu"


def get_url():
    index_url = "https://www.mzitu.com"
    bs = etree.HTML(requests.get(url=index_url, headers=HEADERS).text).xpath(
        '/html/body/div[2]/div[1]/div[2]/nav/div/a[4]/text()')[0]
    print(bs)
    page_urls = ['http://www.mzitu.com/page/{cnt}'.format(cnt=cnt) for cnt in range(1, int(bs) + 1)]
    img_urls = []
    for i in page_urls:
        print('正在获取' + i + '链接图片地址')
        try:
            bs = BeautifulSoup(requests.get(url=i, headers=HEADERS, timeout=10).text, 'lxml').find('ul', id='pins')
            res = re.findall(r'href="(.*?)" target="_blank"><img', str(bs))
            img_url = [url.replace('"', "") for url in res]
            img_urls.extend(img_url)
        except Exception as e:
            print(e)
    return set(img_urls)


lock = threading.Lock()


def urls_crawler(url):
    """
    爬虫主接口
    :param url:
    :return:
    """

    r = requests.get(url, headers=HEADERS, timeout=10).text

    img_name = etree.HTML(r).xpath('//div[@class="main-image"]/p/a/img/@alt')[0]
    print(img_name)
    # with lock:
    if mark_dir(img_name):
        max_count = etree.HTML(r).xpath('//div[@class="pagenavi"]/a[5]/span/text()')[0]
        page_url = [url + '/{cnt}'.format(cnt=cnt) for cnt in range(1, int(max_count) + 1)]
        img_urls = []
        for i, j in enumerate(page_url):
            time.sleep(0.3)
            r = requests.get(j, headers=HEADERS, timeout=10).text
            img_url = etree.HTML(r).xpath('//div[@class="main-image"]/p/a/img/@src')[0]
            img_urls.append(img_url)
        for cnt, url in enumerate(img_urls):
            save_pic(cnt, url)


def save_pic(cnt, url):
    """
    把图片保存到本地
    :param cnt:
    :param url:
    :return:
    """
    try:
        img = requests.get(url, headers=HEADERS, timeout=10).content
        img_name = '{}.jpg'.format(cnt)
        with open(img_name, 'ab') as f:
            f.write(img)
    except Exception as e:
        print(e)


def mark_dir(flot_name):
    """
    检测文件夹是否创建，没有创建则创建文件夹，创建了就跳过
    :param flot_name:
    :return:
    """
    PATH = os.path.join(DIR_PATH, flot_name)
    if not os.path.exists(PATH):                   # 检测是否有这个文件夹
        os.makedirs(PATH)
        os.chdir(PATH)
        return True
    print("Folder has existed! {}".format(flot_name))
    return False


def delete_empty_dir(save_dir):
    """
    如果程序半路中断的话，可能存在已经新建好文件夹但是仍没有下载的图片的
    情况但此时文件夹已经存在所以会忽略该套图的下载，此时要删除空文件夹
    :param save_dir:
    :return:
    """
    if os.path.exists(save_dir):                    # 检测是否有这个文件夹
        if os.path.isdir(save_dir):                 # 检测这个路径是否是一个文件夹
            for i in os.listdir(save_dir):          # 循环save_dir目录下的所有目录和文件的名字
                path = os.path.join(save_dir, i)    # 拼接出所有的目录或者文件路径
                if os.path.isdir(path):             # 判断这个路径是否是一个文件夹
                    delete_empty_dir(path)          # 是则递归上去继续
        if not os.listdir(save_dir):                # 如果save_dir没有文件和子目录则删除该文件夹
            os.rmdir(save_dir)

if __name__ == '__main__':
    stratTime = time.time()
    urls = get_url()
    pool=Pool(processes=cpu_count())
    try:
        delete_empty_dir(DIR_PATH)
        pool.map(urls_crawler,urls)
    except Exception:
        time.sleep(30)
        delete_empty_dir(DIR_PATH)
        pool.map(urls_crawler, urls)
    stopTime = time.time()
    print(int(stopTime) - int(stratTime))
