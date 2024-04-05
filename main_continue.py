import time
import requests
from method import detail_img, get_links

# 使用直接的互联网连接（无代理）
base_url = "https://bearbrick.com/product/12_0.1"
max_retries = 5  # 设置最大重试次数

# 获取所有链接
url_list = get_links.get_links(base_url)

# 指定要从哪个链接开始运行
start_url = "https://bearbrick.com/5375.html"
start_index = url_list.index(start_url) if start_url in url_list else 0

for url in url_list[start_index:]:
    retries = max_retries
    while retries > 0:
        try:
            print("处理链接: {}".format(url))
            detail_img.detail_img(url)

            # 执行成功后，退出循环
            break
        except (requests.exceptions.RequestException, ConnectionError) as e:
            print("发生异常：{}".format(e))
            retries -= 1  # 减少重试次数
            if retries > 0:
                # 如果尝试次数未达到上限，等待一段时间后重试
                print("等待5秒后重试...")
                time.sleep(5)
            else:
                print("达到最大重试次数，脚本退出。")