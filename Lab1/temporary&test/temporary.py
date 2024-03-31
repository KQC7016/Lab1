# import datetime
# import time
# import tkinter as tk
# import html_parsing
# import platform
import os
import re
import subprocess
# from tkinter import ttk
# from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pathlib import Path



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

# def add_https_prefix(url):
#     if "://" not in url:
#         url = "//" + url
#     if not url.startswith("https:"):
#         url = "https:" + url
#     return url
#
# # 使用示例
# urls = ["www.example.com", "//www.example.com", "://www.example.com", "s://www.example.com", "http://www.example.com"]
# for url in urls:
#     url_with_https = add_https_prefix(url)
#     print(url_with_https)

def get_chrome_version():
    try:
        # Windows下Chrome浏览器版本信息保存在注册表中
        output = subprocess.check_output(['reg', 'query', 'HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon',
                                          '/v', 'version'], stderr=subprocess.DEVNULL)
        version_info = output.decode('utf-8').strip().split()[-1]
        return version_info
    except subprocess.CalledProcessError:
        return None


def get_firefox_version():
    try:
        # 获取 Firefox 安装路径
        output = subprocess.check_output(['reg', 'query', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows'
                                                          '\CurrentVersion\App Paths\firefox.exe', '/ve'],
                                         stderr=subprocess.DEVNULL)
        path_info = output.decode('utf-8').strip().split('\n')[-1].split()
        firefox_exe_path = ' '.join(path_info[1:])
        firefox_install_dir = os.path.dirname(firefox_exe_path)

        # 在 Firefox 安装目录中查找 application.ini 文件
        application_ini_path = os.path.join(firefox_install_dir, 'application.ini')
        if os.path.isfile(application_ini_path):
            with open(application_ini_path, 'r') as file:
                content = file.read()
                version_match = re.search(r'^Version=(\d+\.\d+\.\d+)', content, re.MULTILINE)
                if version_match:
                    return version_match.group(1)
        return None
    except (FileNotFoundError, subprocess.CalledProcessError, IndexError):
        return None


def get_edge_version():
    try:
        # 获取 Edge 浏览器安装路径
        output = subprocess.check_output(['reg', 'query', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows'
                                                          '\CurrentVersion\App Paths\msedge.exe', '/ve'],
                                         stderr=subprocess.DEVNULL)

        # print('output:', output)

        # 将字节字符串解码为字符串
        output_str = output.decode('gbk')

        # print('output_str:', output_str)

        # 使用正则表达式来匹配路径
        match = re.search(r'REG_SZ\s+(.*)', output_str)
        if match:
            path_info = match.group(1)
        else:
            print("Path not found")
            path_info = None

        # print('path_info:', path_info)

        # 从安装路径中获取 Edge 浏览器的安装目录
        edge_install_dir = os.path.dirname(path_info)
        # 列出 Edge 安装目录中的所有文件夹
        folder_list = os.listdir(edge_install_dir)

        # 遍历文件夹列表，提取版本号
        for folder_name in folder_list:
            # 使用正则表达式匹配版本号
            version_match = re.match(r'(\d+\.\d+\.\d+\.\d+)', folder_name)
            if version_match:
                return version_match.group(1)

        # 如果未找到匹配的版本号，则返回 None
        return None

    except (FileNotFoundError, subprocess.CalledProcessError, IndexError):
        return None


def update_path():

    print("\n\n***chrome***")
    chrome_version = get_chrome_version()
    print("chrome_version:", chrome_version)
    relative_chrome_path = Path('WebDriver') / 'ChromeDriver' / f'{chrome_version}' / 'chromedriver.exe'
    print("relative_chrome_path:", relative_chrome_path)
    update_chrome_driver_bin = str(relative_chrome_path.absolute())

    print("\n\n***firefox***")
    firefox_version = get_firefox_version()
    print("firefox_version:", firefox_version)
    relative_firefox_path = Path('WebDriver') / 'FirefoxDriver' / f'{firefox_version}' / 'geckodriver.exe'
    print("relative_firefox_path:", relative_firefox_path)
    update_firefox_driver_bin = str(relative_firefox_path.absolute())

    print("\n\n***edge***")
    edge_version = get_edge_version()
    print("edge_version:", edge_version)
    relative_edge_path = Path('WebDriver') / 'EdgeDriver' / f'{edge_version}' / 'msedgedriver.exe'
    print("relative_edge_path:", relative_edge_path)
    # update_edge_driver_bin_str = relative_edge_path.absolute()
    # print("update_edge_driver_bin_str:", update_edge_driver_bin_str)
    # update_edge_driver_bin = str(update_edge_driver_bin_str)
    update_edge_driver_bin = str(relative_edge_path.absolute())
    print("update_edge_driver_bin:", update_edge_driver_bin)

    return update_chrome_driver_bin, update_firefox_driver_bin, update_edge_driver_bin


chrome_driver_bin, firefox_driver_bin, edge_driver_bin = update_path()
print(chrome_driver_bin)
print(firefox_driver_bin)
print(edge_driver_bin)
