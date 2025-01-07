import pandas as pd  
from bs4 import BeautifulSoup as bs
import requests
links = pd.read_csv('GetYourGuide.csv')['URL']
# print(links)
headers = {
    "authority": "www.getyourguide.com",
    "method": "GET",
    "path": "/destinations/argentina-l168992/",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "cookie": "visitor_id=CGI0XMIQUAOUQE21O7XALC8GMRB9CY3D; cur=INR; locale_code=en-US; __ssid=52465140d9f22182f0b6f066a53ac77; _gcl_au=1.1.2007466394.1735570093; _ga=GA1.1.1035470658.1735570093; FPID=FPID2.2.fgEGN8QiQ1q9AS%2BaYRF1dVLXJuk0ZBik0Q7AjGvxEeM%3D.1735570093; _fbp=fb.1.1735570093858.706268025917819690; FPAU=1.1.2007466394.1735570093; _gtmeec=eyJzdCI6IjU4Mjk2NzUzNGQwZjkwOWQxOTZiOTdmOWU2OTIxMzQyNzc3YWVhODdiNDZmYTUyZGYxNjUzODlkYjFmYjhjY2YiLCJjb3VudHJ5IjoiNTgyOTY3NTM0ZDBmOTA5ZDE5NmI5N2Y5ZTY5MjEzNDI3NzdhZWE4N2I0NmZhNTJkZjE2NTM4OWRiMWZiOGNjZiIsImV4dGVybmFsX2lkIjoiYzRhNDQyMDc3NTA2YWRjZGQyNzEyODlhODY4ODk4ZWI4ZTE3NTY3NGYxNjI2ODZjN2EyMjEyNGYxZWFiZGI3OCJ9; par_sess=h=CD951&c=brand&v=&t=0&s=; locale_autoredirect_origin=www.getyourguide.com; locale_autoredirect_deviceLocale=en-US; session_id=7c39dbf7-29a6-4449-b341-6dfe8272d2af; cf_enable_format_auto=true; _gcl_gs=2.1.k1$i1736134852$u81041921; FPLC=HbssiW%2Bg0X6sL%2FHX3DJs1FJpiB1MazcLczT8t6GrWBfp9MGwO5PLtmizjCZ0Z2vcq%2F%2FMh4CHyAabI7vl3Cy4SH1JYALRNfE2Ocbhnqcs%2Bx6Sp40WhrvYhFJ0fmRZmg%3D%3D; FPGCLAW=2.1.kCjwKCAiA-Oi7BhA1EiwA2rIu20ncBrDksolOu883wXJs3bSUoAMBfuBnXfgkM69K1W47KZa0dsL1sxoCgx8QAvD_BwE$i1736134862; FPGCLGS=2.1.k1$i1736134857; _hjSessionUser_318029=eyJpZCI6IjRkNzZkZDNhLTJlMmQtNWMyYy05OWY2LTI0ZGM2NDM5OTc0MCIsImNyZWF0ZWQiOjE3MzU1NzAxNTUyODAsImV4aXN0aW5nIjp0cnVlfQ==; _hjHasCachedUserAttributes=true; crto_is_user_optout=false; crto_mapped_user_id=Bw-Luf29_tamMv6PMbMHUi9zk1nqEplZ; _gcl_aw=GCL.1736134886.CjwKCAiA-Oi7BhA1EiwA2rIu20ncBrDksolOu883wXJs3bSUoAMBfuBnXfgkM69K1W47KZa0dsL1sxoCgx8QAvD_BwE; gtmDisplayInclusion=IN:2025-01-06; quoter=1; lastRskxRun=1736135054476; rskxRunCookie=0; rCookie=3y6gm0z4h6mtl5hfl8qrmbm5khzhjh; forterToken=218485444d874bfb938cc347549beed5_1736135053228__UDF43-m4_24ck_; tfeAppletName=shared; __cf_bm=iJVBrkZnBduOiUezLKJXZmHf51CC.aAt3AGjyPX93H4-1736165950-1.0.1.1-BWdkqWH3DUXJom9an7EnMuJezGeF5NNFnct2WnC7ZDc6APKPGzsESQ.aCcTjG67RZViTLs5RHs76sdGIyCGa9w; ab.storage.deviceId.32b57c7b-1181-4973-9f07-79cdd6d2c403=g%3Acdd60834-700c-72e4-3519-bd111e9254b7%7Ce%3Aundefined%7Cc%3A1735570093755%7Cl%3A1736166246529; csrfToken=1a8b22dd95ffe53f77ce25163b6819fdc18801ccea95131f05cc942e54d227b7; AP-VID=l342oybbuv5m98n35cuoks025fq9vkne; FPGSID=1.1736166249.1736166395.G-BJKL76S993.JepiFiGJzMNg53YRNWBMtA; _uetsid=0a987560cbe011ef8051dfe0a643f60e|1hozx93|2|fsc|0|1832; _uetvid=18e17020c6bd11ef85fcf30d584cbfda|10tdy82|1736166394401|2|1|bat.bing.com/p/insights/c/a; _ga_BJKL76S993=GS1.1.1736166246.3.1.1736166421.0.0.303763784; ab.storage.sessionId.32b57c7b-1181-4973-9f07-79cdd6d2c403=g%3A207dcd6f-76a2-e73c-9556-c387c52a5c4d%7Ce%3A1736168532209%7Cc%3A1736166246528%7Cl%3A1736166732209",
    "priority": "u=0, i",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
for link in links:
    print(link)
    page = requests.get(link,headers=headers)
    print(page.status_code)
    soup = bs(page.text, 'html.parser')
    # print(soup)
    city_list = soup.find('ul',class_="links-group-list")
    # print(city_list)
    break