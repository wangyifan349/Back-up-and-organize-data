import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 确保脚本运行目录中有一个名为 'images' 的文件夹
if not os.path.exists('images'):
    os.makedirs('images')

# 目标网页的URL
url = 'https://telegra.ph/url'

# 自定义请求头，模仿浏览器的行为
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# 代理设置
proxies = {
    'http': 'http://127.0.0.1:1080',
    'https': 'https://127.0.0.1:1080'
}

# 发送HTTP请求获取网页内容
response = requests.get(url, headers=headers, proxies=proxies)
response.raise_for_status()  # 确保请求成功

# 解析网页内容
soup = BeautifulSoup(response.content, 'html.parser')

# 提取并保存文本内容
text_parts = soup.find_all('p')
with open('text_content.txt', 'w', encoding='utf-8') as file:
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
    with open(f'images/image_{i}.jpg', 'wb') as f:
        f.write(img_data)
    print(f'下载图片 {i} 从 {img_url}')

print('采集完成')
