import urllib.request
import json
import csv
url = 'https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json'
output = "data.json"
with urllib.request.urlopen(url) as response:
    data = json.load(response)
# with可以自動關閉文件，不需要使用到file.close/UTF-8是一种通用的字符编码标准，可以用于表示几乎所有的字符，包括ASCII字符和非ASCII字符(如中文)
with open(output, "w", encoding='utf-8') as file:
    # JSON轉譯時會將非ascii字符轉譯為Unicode轉譯序列，為了要將非ascii字符轉譯成非Unicode，要在這邊設定ensre_ascii=false，這樣系統不會轉譯Unicode序列，並成功顯示中文
    json.dump(data, file, ensure_ascii=False)


def attraction():
    results = data["result"]["results"]
    rows = []
    for result in results:
        stitle = result["stitle"]
        address = result["address"]
        # 把地址按空白建分割後，會有三組資料，取得第三組資料(即區域+地址)，取前面三個字(即地區)
        district = address.split(" ")[2][:3]
        longitude = result["longitude"]
        latitude = result["latitude"]
        file_urls = result["file"].split("https://")  # 用http:// 作為切分的依據
        first_url = "https://" + file_urls[1]
        final_result = [stitle, district, str(
            longitude), str(latitude), first_url]
        rows.append(final_result)
    with open("attraction.csv", "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ["stitle", "district", "longitude", "latitude", "first_url"])
        writer.writerows(rows)


attraction()


def mrt():
    results = data["result"]["results"]
    mrt_set = set()
    rows = []
    for result in results:
        mrt = result["MRT"]
        if mrt is None:
            mrt = "None"  # None的資料還是要抓，捷運站就顯示none
        mrt_set.add(mrt)
    for mrt in mrt_set:
        stitle_result = []
        for result in results:
            result_mrt = result["MRT"]
            if result_mrt is None:  # 就算沒有捷運站，也要顯示景點
                result_mrt = 'None'
            if mrt == result_mrt:
                stitle_result.append(result["stitle"])
        stitle_result = [title for title in stitle_result if title.strip()]
        stitle_str = ", ".join(stitle_result)
        final_result = [mrt, stitle_str]
        rows.append(final_result)

    with open("mrt.csv", "w", newline='', encoding='utf-8') as csvfile:
        # 寫入標題行，這邊不用上述attraction的語法，主要是因為沿用上述語法，景點多於一個時，會有""出現
        csvfile.write("MRT,stitle\n")
        for row in rows:
            line = ",".join(row)  # 將行中的欄位用逗號連接成一個字串
            csvfile.write(line + "\n")  # 寫入這一行並添加換行符號


mrt()
