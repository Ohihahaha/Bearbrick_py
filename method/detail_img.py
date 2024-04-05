import requests
from bs4 import BeautifulSoup
import os
import re
from datetime import datetime

def clean_filename(filename):
    # 移除无效字符
    cleaned_filename = re.sub(r'[\/:*?"<>|]', '_', filename)
    return cleaned_filename

def create_html_with_link(url, folder_name, file_name):
    # 构建HTML内容
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>Link Page</title>
    </head>
    <body>
    <h1>Click the link below to visit the website:</h1>
    <a href="{}" target="_blank">{}</a>
    </body>
    </html>
    """.format(url, url)

    # 保存HTML文件
    html_file_name = "{}.html".format(file_name)
    html_file_path = os.path.join(folder_name, html_file_name)

    with open(html_file_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    print("HTML文件保存成功: {}".format(html_file_name))

def detail_img(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # 获取id为slideWrapper的所有图片
        slide_wrapper = soup.find("div", id="slideWrapper")
        if slide_wrapper:
            images = slide_wrapper.find_all("img")

            # 获取<h3>标签的文本内容
            item_name_h3 = soup.find("h3", class_="itemName")
            item_name = item_name_h3.text.strip() if item_name_h3 else "default_name"

            # 获取<dd>标签的文本内容
            price_dd = soup.find("dd")
            price_content = price_dd.text.strip() if price_dd else "default_price"

            # 创建文件夹Bearbrick_News，添加时间戳
            timestamp = datetime.now().strftime("%y%m%d")
            folder_name = "Bearbrick_News_Imgs_{}".format(timestamp)
            os.makedirs(folder_name, exist_ok=True)

            for index, image in enumerate(images):
                src = image.get("src")

                # 链接可能是相对链接，需要拼接成完整链接
                if src and not src.startswith("http"):
                    src = "http://www.bearbrick.com" + src

                # 按数字顺序命名图片，数字序号放在文件末尾
                file_name = "{}_{}_{}.jpg".format(clean_filename(item_name.replace("/", "_")), clean_filename(price_content.replace("￥", "").replace("（税込）", "")), index + 1)
                file_path = os.path.join(folder_name, file_name)

                # 下载图片
                image_response = requests.get(src, stream=True)
                if image_response.status_code == 200:
                    with open(file_path, "wb") as img_file:
                        for chunk in image_response.iter_content(chunk_size=128):
                            img_file.write(chunk)
                    print("图片 {} 下载成功".format(file_name))
                else:
                    print("图片 {} 下载失败，状态码: {}".format(file_name, image_response.status_code))

            # 创建包含链接的 HTML 文件
            create_html_with_link(url, folder_name, file_name)

    else:
        print("请求失败，状态码: {}".format(response.status_code))


