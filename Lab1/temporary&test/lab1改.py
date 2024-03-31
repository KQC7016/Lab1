import requests
from bs4 import BeautifulSoup

# 定义要抓取的页面 URL
url = "https://en.wikipedia.org/wiki/Python_(programming_language)"

# 发送 HTTP 请求获取页面内容
response = requests.get(url)

# 检查响应状态码是否为 200 (成功)
if response.status_code == 200:
    # 使用 BeautifulSoup 解析 HTML 内容
    soup = BeautifulSoup(response.content, "html.parser")

    # 找到页面标题并打印
    title = soup.find("h1", id="firstHeading")
    print("Page Title:", title.text.strip())

    # 找到页面主要内容部分并打印
    content = soup.find("div", class_="mw-parser-output")
    paragraphs = content.find_all("p")
    print("\nPage Content:")
    for paragraph in paragraphs:
        print(paragraph.text.strip())
else:
    print("Failed to retrieve page. Status code:", response.status_code)
