import json
import requests
import csv
from datetime import datetime
import os

with open(r"station-min-yb2.json", "r", encoding="utf-8") as f:
    info = json.load(f)
info_dict = {s["station_no"]: s for s in info}

session = requests.Session()
session.get("https://www.youbike.com.tw/")

url_status = "https://apis.youbike.com.tw/tw2/parkingInfo"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.youbike.com.tw/",
    "Content-Type": "application/json"
}

station_list = [
    # 第一頁
    "500304001","500304002","500304003","500304004","500304005",
    "500304006","500304007","500304008","500304009","500304010",
    "500304011","500304012","500304013","500304014","500304015",
    "500304016","500304017","500304018","500304019","500304020",

    # 第二頁
    "500304021","500304022","500304023","500304024","500304025",
    "500304026","500304027","500304028","500304029","500304030",
    "500304031","500304032","500304033","500304034","500304035",
    "500304036","500304037","500304038","500304039","500304040",

    # 第三頁
    "500304041","500304042","500304043","500304044","500304045",
    "500304046","500304047","500304048","500304049","500304050",
    "500304051","500304052","500304053","500304054","500304055",
    "500304056","500304057","500304058","500304059","500304060",

    # 第四頁
    "500304061","500304062","500304063","500304064","500304065",
    "500304066","500304067","500304068","500304069","500304070",
    "500304071","500304072","500304073","500304074","500304075",
    "500304076","500304077","500304078","500304079","500304080",

    # 第五頁
    "500304081","500304082","500304083","500304084","500304085",
    "500304086","500304087","500304088","500304089","500304090",
    "500304091","500304092","500304093","500304094","500304095",
    "500304096","500304097","500304098","500304099","500304100",

    # 第六頁
    "500304101","500304102","500304103","500304104","500304105",
    "500304106","500304107","500304108","500304109","500304110",
    "500304111","500304112","500304113","500304114","500304115",
    "500304116","500304117","500304118","500304119","500304120",

    # 第七頁
    "500304121","500304122","500304123","500304125","500304126",
    "500304127","500304128","500304129","500304130","500304131",
    "500304132","500304133","500304134","500304135","500304136",
    "500304137","500304138","500304139"
]

batch_size = 20
all_status = []

for i in range(0, len(station_list), batch_size):
    batch = station_list[i:i+batch_size]
    payload = {"station_no": batch}
    resp = session.post(url_status, json=payload, headers=headers)
    data = resp.json()["retVal"]["data"]
    all_status.extend(data)

current_time = datetime.now().strftime("%Y/%m/%d_%H:%M:%S")
print(f"\n=== 抓取時間：{current_time} ===")
print("總共抓到筆數:", len(all_status))

rows = []
for s in all_status:
    no = s["station_no"]
    total = s["parking_spaces"]
    available = s["available_spaces"]
    empty = s["empty_spaces"]

    if no in info_dict:
        station = info_dict[no]
        name = station["name_tw"]
        district = station["district_tw"]
        address = station["address_tw"]
    else:
        name = "未知"
        district = "未知"
        address = "未知"

    row = [current_time, no, district, name, address, total, available, empty]
    rows.append(row)
    print(f"{current_time} | {no} | {district} - {name} | 地址:{address} | 總車位:{total}, 可借:{available}, 可還:{empty}")

filename = "data/youbike_zhongli.csv"
file_exists = os.path.isfile(filename)
with open(filename, "a", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["抓取時間", "站號", "行政區", "站名", "地址", "總車位", "可借車數", "可還車位"])
    writer.writerows(rows)

print(f"\n已存成 {filename}")