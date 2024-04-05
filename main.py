import time
import requests
from method import detail_img, get_links

# 使用直接的互联网连接（无代理）
# 这里下载的是尺码为400%的第一页的所有图片
base_url = "https://bearbrick.com/product/12_0.1"
max_retries = 5  # 设置最大重试次数

while max_retries > 0:
    try:
        url_list = get_links.get_links(base_url)

        for url in url_list:
            print("处理链接: {}".format(url))
            detail_img.detail_img(url)

        # 执行成功后，退出循环
        break
    except (requests.exceptions.RequestException, ConnectionError) as e:
        print("发生异常：{}".format(e))
        max_retries -= 1  # 减少重试次数
        if max_retries > 0:
            # 如果尝试次数未达到上限，等待一段时间后重试
            print("等待5秒后重试...")
            time.sleep(5)
        else:
            print("达到最大重试次数，脚本退出。")