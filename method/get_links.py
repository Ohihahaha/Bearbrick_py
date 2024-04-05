import requests
from bs4 import BeautifulSoup

def get_links(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # 获取所有class为"new"的<li>元素
        li_elements = soup.find_all("li", class_="new")

        url_list = []
        for li in li_elements:
            a_tag = li.find("a")
            if a_tag:
                link = a_tag.get("href")
                if link:
                    # 链接可能是相对链接，需要拼接成完整链接
                    if not link.startswith("http"):
                        link = "https://bearbrick.com" + link
                    url_list.append(link)

        return url_list

    else:
        print("请求失败，状态码: {}".format(response.status_code))
        return []

# 使用方法
# base_url = "https://bearbrick.com"
# url_list = get_links(base_url)
# print(url_list)
