import requests

# 该算法效果不好，目前没有用
def save_html(url, output_file="output.html"):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功

        with open(output_file, "w", encoding="utf-8") as html_file:
            html_file.write(response.text)
        print("网页已保存到 {}".format(output_file))

    except requests.RequestException as e:
        print("保存网页失败：{}".format(e))

# 使用方法
save_html("https://bearbrick.com/5375.html", "5375.html")
