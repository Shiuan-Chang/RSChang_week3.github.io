import bs4
import urllib.request as req

url = "https://www.ptt.cc/bbs/movie/index.html"
request = req.Request(url, headers={
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
})

with req.urlopen(request) as response:
    data = response.read().decode("utf-8")

root = bs4.BeautifulSoup(data, "html.parser")


def movie():
    global root
    result = ""
    page_count = 0

    while page_count < 3:
        titles = root.find_all("div", class_="title")
        tweets = root.find_all("div", class_="nrec")
        for title, tweet in zip(titles, tweets):

            if title.a is not None:
                title_text = title.a.string
                title_link = title.a["href"]
                title_url = "https://www.ptt.cc" + title_link
                title_request = req.Request(title_url, headers={
                    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
                })

                with req.urlopen(title_request) as title_response:
                    title_data = title_response.read().decode("utf-8")

                title_root = bs4.BeautifulSoup(title_data, "html.parser")
                date_element = title_root.find(
                    "span", class_="article-meta-tag", string="時間")

                if date_element is not None:
                    date = date_element.find_next_sibling("span").string
                else:
                    date = "Not found"

                tweet_num = tweet.string

                if tweet_num is not None:
                    tweet_num = tweet.string
                else:
                    tweet_num = "0"

                result += f"{title_text},{tweet_num},{date}\n"
                print(result)

        pre_link_element = root.find("a", class_="btn wide", string="‹ 上頁")

        if pre_link_element is not None:
            pre_link = pre_link_element["href"]
            pre_url = "https://www.ptt.cc" + pre_link
            pre_request = req.Request(pre_url, headers={
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
            })

            with req.urlopen(pre_request) as pre_response:
                pre_data = pre_response.read().decode("utf-8")
                root = bs4.BeautifulSoup(pre_data, "html.parser")
                page_count += 1
        else:
            print("Can't find the link to the previous page")
            break

    with open("movie.txt", "w", encoding="utf-8") as file:
        file.write(result)


movie()
