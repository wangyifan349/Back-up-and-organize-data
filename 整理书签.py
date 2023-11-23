from bs4 import BeautifulSoup
import os,json

# 创建一个空列表来存储链接和对应的名字
link_list = []
root_folder = '/media/wangyifan/C2B0C479B0C47607/linux迁移/'

# 使用os.walk遍历文件夹中的所有HTML文件
for root, dirs, files in os.walk(root_folder):
    for filename in files:
        if filename.endswith('.html'):
            file_path = os.path.join(root, filename)
            
            # 打开HTML文件并解析为Beautiful Soup对象
            with open(file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
                
                # 提取<a>标签
                a_tags = soup.find_all('a')
                
                # 遍历<a>标签，提取链接和文本，并添加到列表中
                for a_tag in a_tags:
                    link = a_tag.get('href')
                    text = a_tag.get_text()
                    link_list.append((text, link))
# 根据文本去重链接，保留唯一的链接和文本组合
unique_link_list = []
seen_text = set()

for text, link in link_list:
    if text not in seen_text:
        unique_link_list.append((text, link))
        seen_text.add(text)

# 去重链接，保留唯一的链接和文本组合
link_list = unique_link_list

# 按链接降序排序
link_list.sort(key=lambda x: x[1], reverse=True)
print(link_list)
# 指定JSON文件路径
json_file_path = root_folder+'/link_list.json'

# 保存link_list为JSON文件
# 保存link_list为格式化的JSON文件
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(link_list, json_file, ensure_ascii=False, indent=4)  # 使用indent参数设置缩进为4个空格

# 创建一个HTML字符串
html_content = '<html>\n<body>\n'

# 将链接和文本组合转换为HTML格式
for text, link in link_list:
    html_content += f'  <a href="{link}">{text}</a><br>\n'

html_content += '</body>\n</html>'

# 将HTML字符串保存为HTML文件
output_html_file_path = root_folder+"/output.html"
with open(output_html_file_path, 'w', encoding='utf-8') as output_html_file:
    output_html_file.write(html_content)



