import requests
import json
from datetime import datetime
import os

# 获取当前日期
today = datetime.now().strftime("%Y-%m-%d")

# 知乎热榜 API（非官方，可能需要调整）
url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50"

# 设置请求头，模拟浏览器访问
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def fetch_zhihu_hot():
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["data"]
    except Exception as e:
        print(f"Error fetching Zhihu hot list: {e}")
        return []


def generate_markdown(hot_list, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# 知乎热榜 - {today}\n\n")
        for i, item in enumerate(hot_list, 1):
            title = item["target"]["title"]
            link = f"https://www.zhihu.com/question/{item['target']['id']}"
            f.write(f"{i}. [{title}]({link})\n")
    print(f"Generated {filename}")


def update_readme(hot_list):
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# 知乎每日热榜 - {today}\n\n")
        f.write("以下是知乎当日的热榜内容，自动更新于北京时间每天上午 8:00 。\n\n")
        for i, item in enumerate(hot_list, 1):
            title = item["target"]["title"]
            link = f"https://www.zhihu.com/question/{item['target']['id']}"
            f.write(f"{i}. [{title}]({link})\n")
    print("Updated README.md")


def main():
    # 创建 hot 文件夹（如果不存在）
    os.makedirs("hot", exist_ok=True)

    # 获取热榜数据
    hot_list = fetch_zhihu_hot()

    if hot_list:
        # 生成当日的热榜文件
        filename = f"hot/{today}.md"
        generate_markdown(hot_list, filename)

        # 更新 README.md
        update_readme(hot_list)


if __name__ == "__main__":
    main()
