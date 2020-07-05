import time
import requests
from fake_useragent import UserAgent


ua = UserAgent(verify_ssl=False)
headers = {
    'User-Agent': ua.random,
    'Referer': 'https://shimo.im/login?from=home',
    # ':authority': 'shimo.im',
    # ':method': 'POST',
    # ':path': '/lizard-api/auth/password/login',
    # ':scheme': 'https',
    'accept': '*/*',
    'x-requested-with': 'XmlHttpRequest',
    'x-source':	'lizard-desktop',
    'content-type':	'application/x-www-form-urlencoded; charset=utf-8',
    'accept': '*/*',
    'origin': 'https://shimo.im',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://shimo.im/login?from=home',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
}

s = requests.Session()

login_url = 'https://shimo.im/lizard-api/auth/password/login'
form_data = {
    'email': 'zrmpop@qq.com',
    'password': '123456',
    'mobile': '+86undefined'
}

pre_login = 'https://shimo.im/login?from=home'
pre_resp = s.get(pre_login, headers=headers)
print(pre_resp)


response = s.post(login_url, data=form_data,
                  headers=headers, cookies=s.cookies)
print(response.json)
print(s.cookies)
