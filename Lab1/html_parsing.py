from bs4 import BeautifulSoup


def add_https_prefix(url):
    if not url.startswith("https://"):
        url = "https:" + url
    return url


def bilibili_index_video_details(soup, log):
    index_body = soup.find('div', class_='container is-version8')
    video_cards = index_body.find_all('div', class_='feed-card')

    # 创建一个空的结构体数组
    index_video_info_list = []

    for card in video_cards:

        # 提取视频播放量、评论数、时长
        stats_tag = card.find('div', class_='bili-video-card__stats')
        # 提取播放量
        view_count_tag = stats_tag.find("span", class_="bili-video-card__stats--item")
        view_count = view_count_tag.find("span", class_="bili-video-card__stats--text").text

        # 提取评论数
        comment_count_tag = view_count_tag.find_next_sibling("span", class_="bili-video-card__stats--item")
        comment_count = comment_count_tag.find("span", class_="bili-video-card__stats--text").text.strip()
        # 提取视频时长
        duration = stats_tag.find("span", class_="bili-video-card__stats__duration").text
        # 提取视频标题
        video_title_tag = card.find("h3", class_="bili-video-card__info--tit")
        video_title = video_title_tag["title"]
        video_link = video_title_tag.a["href"]

        # 提取UP主名称和链接
        up_info_tag = card.find("a", class_="bili-video-card__info--owner")
        up_name = up_info_tag.find("span", class_="bili-video-card__info--author").text
        up_link = "https:" + up_info_tag["href"]
        # 提取上传时间
        upload_date = up_info_tag.find("span", class_="bili-video-card__info--date").text.strip()
        upload_date = upload_date.replace('· ', '')

        video_info = {
            'Video Title': video_title,
            'Video Link': video_link,
            'Views': view_count,
            'Comments': comment_count,
            'Duration': duration,
            'Author': up_name,
            'Author Link': up_link,
            'Upload Date': upload_date
        }

        # 将视频信息字典添加到结构体数组中
        index_video_info_list.append(video_info)

    if log == 1:

        print("\n******Home Video Info******\n")

        # 打印结构体数组
        for idx, video_info in enumerate(index_video_info_list, start=1):
            print('Video Number:', idx)
            print('Video Title:', video_info['Video Title'])
            print('Video Link: ', video_info['Video Link'])
            print('Views:      ', video_info['Views'])
            print('Comments:   ', video_info['Comments'])
            print('Duration:   ', video_info['Duration'])
            print('Author:     ', video_info['Author'])
            print('Author Link:', video_info['Author Link'])
            print('Upload Date:', video_info['Upload Date'])

        print("\n******Home Video Info Printed******\n")

    return index_video_info_list


def bilibili_channels(soup, log):

    # 提取频道名称和链接
    channels = []

    channel_sections = soup.find_all('div', class_='header-channel-fixed-right-item')
    for section in channel_sections:
        channel_name = section.text
        channel_link = section.parent['href']  # 使用父级对象获取链接
        channel_link = add_https_prefix(channel_link)

        channel_info = {
            'channel_name': channel_name,
            'channel_link': channel_link
        }

        # 将视频信息字典添加到结构体数组中
        channels.append(channel_info)

    if log == 1:
        print("\n******Channels******\n")

        # 打印结构体数组
        for idx, channel_info in enumerate(channels, start=1):
            # print('Video Number a:', idx)
            print('Channel Name:', channel_info['channel_name'])
            print('Channel Link:', channel_info['channel_link'])

        print("\n******Channels Printed******\n")

    return channels


def bilibili_index_parsing(soup):

    bili_channels_log = 1  # 是否频道信息
    bilibili_channels(soup, bili_channels_log)

    bili_index_video_log = 1  # 是否打印首页视频详细信息
    bilibili_index_video_details(soup, bili_index_video_log)


def wiki_parsing(soup):
    # 找到页面标题并打印
    title = soup.find("h1", id="firstHeading")
    print("Page Title:", title.text.strip())

    # 找到页面主要内容部分并打印
    content = soup.find("div", class_="mw-parser-output")
    paragraphs = content.find_all("p")
    print("\nPage Content:")
    for paragraph in paragraphs:
        print(paragraph.text.strip())


def html_parsing(html_content, url):

    # 使用 BeautifulSoup 解析 HTML 内容
    soup = BeautifulSoup(html_content, "html.parser")
    # print("\n***Soup***")
    # print(soup)
    # print("***END***")

    if "www.bilibili.com" in url:
        if url == "https://www.bilibili.com/":
            bilibili_index_parsing(soup)
    elif "wikipedia.org/" in url:
        wiki_parsing(soup)
    else:
        print("Unsupported Website")
        print("Program exited.")
        exit()
