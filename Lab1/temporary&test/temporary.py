# import tkinter as tk
#
# root = tk.Tk()
# root.title("Pack Example")
#
# # 创建标签部件并放置在顶部
# label1 = tk.Label(root, text="Label 1", bg="red")
# label1.pack(side="top", fill="x")
#
# # 创建按钮部件并放置在底部
# button1 = tk.Button(root, text="Button 1", bg="green")
# button1.pack(side="bottom", fill="x")
#
# # 创建另一个标签部件并放置在左侧
# label2 = tk.Label(root, text="Label 2", bg="blue")
# label2.pack(side="left", fill="y")
#
# root.mainloop()

def add_https_prefix(url):
    if "://" not in url:
        url = "//" + url
    if not url.startswith("https:"):
        url = "https:" + url
    return url

# 使用示例
urls = ["www.example.com", "//www.example.com", "://www.example.com", "s://www.example.com", "http://www.example.com"]
for url in urls:
    url_with_https = add_https_prefix(url)
    print(url_with_https)