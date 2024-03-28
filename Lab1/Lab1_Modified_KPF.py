import datetime
import time
import tkinter as tk
import html_parsing
from tkinter import ttk
from selenium import webdriver
from pathlib import Path


# 浏览器driver默认存储位置，程序启动后自动更新
# "./"表示当前脚本所在目录
# chrome_driver_bin = './/WebDriver/ChromeDriver/chromedriver.exe'
# firefox_driver_bin = './//WebDriver/FirefoxDriver/geckodriver.exe'
# edge_driver_bin = './//WebDriver/Edgedriver/msedgedriver.exe'


def update_path():

    relative_chrome_path = Path('WebDriver/ChromeDriver') / 'chromedriver.exe'
    update_chrome_driver_bin = str(relative_chrome_path.resolve())

    relative_firefox_path = Path('WebDriver/EdgeDriver') / 'msedgedriver.exe'
    update_firefox_driver_bin = str(relative_firefox_path.resolve())

    relative_edge_path = Path('WebDriver/FirefoxDriver') / 'geckodriver.exe'
    update_edge_driver_bin = str(relative_edge_path.resolve())

    return update_chrome_driver_bin, update_firefox_driver_bin, update_edge_driver_bin


def simulate_browser(browser, url):

    # 浏览器默认安装路径
    chrome_bin = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
    firefox_bin = 'C:/Program Files/Mozilla Firefox/firefox.exe'
    edge_bin = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'

    # 自动更新浏览器内核路径
    chrome_driver_bin, firefox_driver_bin, edge_driver_bin = update_path()
    print(chrome_driver_bin)
    print(firefox_driver_bin)
    print(edge_driver_bin)

    # 根据选择的浏览器内核创建 WebDriver
    if browser == "Chrome":
        # 创建 ChromeOptions 实例
        options = webdriver.ChromeOptions()
        options.binary_location = chrome_bin

        # 创建 ChromeService 实例
        service = webdriver.ChromeService(executable_path=chrome_driver_bin)

        # 使用 ChromeService 和 ChromeOptions 创建 Chrome WebDriver
        driver = webdriver.Chrome(service=service, options=options)
    elif browser == "Firefox":
        # 创建 FirefoxOptions 实例
        options = webdriver.FirefoxOptions()
        options.binary_location = firefox_bin

        # 创建 FirefoxService 实例
        service = webdriver.FirefoxService(executable_path=firefox_driver_bin)

        # 使用 FirefoxService 创建 Firefox WebDriver
        driver = webdriver.Firefox(service=service, options=options)
    elif browser == "Edge":
        # 创建 EdgeOptions 实例
        options = webdriver.ChromeOptions()
        options.binary_location = edge_bin

        # 创建 EdgeService 实例
        service = webdriver.EdgeService(executable_path=edge_driver_bin)

        # 使用 EdgeService 创建 Edge WebDriver
        driver = webdriver.Edge(service=service, options=options)
    elif browser == "Safari":
        driver = webdriver.Safari()
    else:
        raise ValueError("Invalid browser specified")

    # 获取当前时间
    page_request_time = datetime.datetime.now()
    print("\nPage request time:", page_request_time)

    # 打开网页
    driver.get(url)

    # 获取当前页面的HTML源代码
    page = driver.page_source

    # 将页面内容保存到文件中
    with open("page.txt", "w", encoding="utf-8") as f:
        f.write(page)

    # 关闭浏览器
    driver.quit()

    return page


def set_window_position_and_size(window, width, height):
    # 获取屏幕的宽度和高度
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # 计算窗口位置
    x_position = (screen_width - width) // 2
    y_position = (screen_height - height) // 2

    # 设置窗口位置和大小
    window.geometry(f"{width}x{height}+{x_position}+{y_position}")


def spider_initialization(default_browser, default_url):
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口  # Hide the main window

    # 设置窗口标题  # Set window title
    input_window = tk.Toplevel(root)
    input_window.title("Spider Initialization")

    # 根据屏幕尺寸调整窗口大小和位置
    set_window_position_and_size(input_window, 400, 300)

    null_label = tk.Label(input_window)
    null_label.pack(side="top", ipady=6)
    # 创建浏览器内核输入框和标签  # Create browser kernel input boxes and labels
    browser_label_text = "Please Choose Browser Kernel (Default:" + default_browser + ")"
    browser_label = tk.Label(input_window, text=browser_label_text, bg='lightblue')
    browser_label.pack(pady=10)
    browsers = ["Chrome", "Firefox", "Edge", "Safari"]
    browser_entry = ttk.Combobox(input_window, values=browsers)
    browser_entry.pack(side="top", ipadx=90, pady=5)

    # 创建URL输入框和标签  # Create URL input box and label
    url_label_text = "Please Enter URL (Default:" + default_url + ")"
    url_label = tk.Label(input_window, text=url_label_text, bg='lightblue')
    url_label.pack(anchor="center", pady=10)
    url_entry = tk.Entry(input_window)
    url_entry.pack(ipadx=100, ipady=3, pady=5)

    # 保存输入的内容  # Save the entered content
    browser_value = tk.StringVar()
    url_value = tk.StringVar()
    browser_entry.config(textvariable=browser_value)
    url_entry.config(textvariable=url_value)

    # 创建确定按钮点击事件  # Create Confirm button click event
    def confirm():
        browser = browser_value.get()
        browser = browser.capitalize()
        url = url_value.get()
        return browser, url

    # 创建确定按钮  # Create Confirm button
    confirm_button = tk.Button(input_window, text="Confirm", command=input_window.destroy)
    confirm_button.pack(side="bottom", anchor="s", ipadx=50, ipady=10, pady=30)

    input_window.wait_window()
    return confirm()


def main():
    # 程序开始运行时间
    start_time = time.time()

    # time.sleep(1)

    # 设置默认浏览器内核
    default_browser = "Chrome"  # ["Chrome", "Firefox", "Edge", "Safari"]
    # 设置默认URL地址
    default_url = "https://www.bilibili.com/"
    # https://www.bilibili.com/
    # https://www.youtube.com/index

    print("\n*********Spider_Initialization*********\n")
    # 选择浏览器内核并输入网页URL地址
    browser, url = spider_initialization(default_browser, default_url)

    # 如果browser为空，则将其设为默认值"Chrome"
    if not browser:
        browser = default_browser
        print("Browser Kernel: {}(default)".format(default_browser))
    else:
        print("Browser Kernel:", browser)
    # 如果url为空，使用默认URL
    if not url:
        print("URL Input is empty.")
        url = default_url
        print("URL: {}(default)".format(url))
        # print("Program exited.")
        # exit()
    else:
        print("URL:", url)
    print("\n***END***")

    print("\n*********Spider_Initialized*********\n")

    # time.sleep(1)

    print("\n*********Request_Page*********\n")
    # 获取页面的HTML源代码
    page = simulate_browser(browser, url)
    # print("\n***Page***")
    # print(page)
    # print("***END***")
    print("\n*********Page_Requested*********\n")

    # time.sleep(1)

    print("\n*********Html_Parsing*********\n")

    # 解析页面的HTML源代码
    html_parsing.html_parsing(page)

    print("\n*********Html_parsed*********\n")

    # 计算程序运行时间
    end_time = time.time()
    execution_time = end_time - start_time
    print("Program Execution Time:", execution_time, "seconds")
    print("\n***END***")


if __name__ == "__main__":
    main()
