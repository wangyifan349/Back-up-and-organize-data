import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
# 创建目录的函数
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
# 下载并保存页面内容的函数
def download_page_content(base_url, page_path, headers, proxies):
    # 构造完整的URL
    url = urljoin(base_url, page_path)

    # 发送HTTP请求获取网页内容
    response = requests.get(url, headers=headers, proxies=proxies)
    response.raise_for_status()  # 确保请求成功
    # 解析网页内容
    soup = BeautifulSoup(response.content, 'html.parser')
    # 为每个页面创建一个单独的文件夹
    page_dir = os.path.join('images', page_path)
    ensure_dir(page_dir)
    # 提取并保存文本内容
    text_parts = soup.find_all('p')
    with open(os.path.join(page_dir, 'text_content.txt'), 'w', encoding='utf-8') as file:
        for part in text_parts:
            file.write(part.get_text() + '\n')
    # 提取并保存图片
    image_tags = soup.find_all('img')
    for i, img in enumerate(image_tags):
        # 构建完整的图片URL
        img_url = urljoin(url, img['src'])
        # 获取图片内容
        img_data = requests.get(img_url, headers=headers, proxies=proxies).content
        # 写入图片文件
        with open(os.path.join(page_dir, f'image_{i}.jpg'), 'wb') as f:
            f.write(img_data)
        print(f'Downloaded image {i} from {img_url}')

    print(f'Text and images for {page_path} have been saved.')

# 主程序
if __name__ == '__main__':
    # 确保脚本运行目录中有一个名为 'images' 的文件夹
    ensure_dir('images')
    # 基础URL
    base_url = 'https://telegra.ph/'
    # 页面路径列表
    page_paths = ['aaaa', 'bbbb', 'cccc']
    # 自定义请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    # 代理设置
    proxies = {
        'http': 'http://127.0.0.1:1080',
        'https': 'https://127.0.0.1:1080'
    }
    # 遍历列表，下载每个页面的内容
    for page_path in page_paths:
        download_page_content(base_url, page_path, headers, proxies)
#
