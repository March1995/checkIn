# -*- coding: utf-8 -*-
# @Author    :yaoys
# @Desc      :
# @Author    ：https://github.com/yaoysyao
import re

import requests
import urllib3
from bs4 import BeautifulSoup
import checkin_util

__gufen_checkin_url = 'http://bbs.99lb.net/plugin.php?id=are_sign:getaward&typeid=1'


def __get_header(cookie_header):
    header = {
        'Host': 'bbs.99lb.net',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://bbs.99lb.net/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': cookie_header,
        'Connection': 'keep-alive',
    }
    return header


# 解决出现警告 Adding certificate verification is strongly advised.
urllib3.disable_warnings()


def __gufen_checkin(cookie=None):
    header = __get_header(cookie)
    resp = requests.get(url=__gufen_checkin_url, headers=header, verify=False)
    resp_code = resp.status_code
    checkin_message = ''
    if resp_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        result = soup.find_all('div', attrs={'id': 'messagetext'})
        for res in result:
            checkin_message = 'checkin success' + res.find_next(name='p').text
            break
    else:
        checkin_message = 'checkin error,the status code is ' + str(resp_code)
    resp.close()
    return checkin_message


def gufen_checkin_main(gufen_cookie=None, checkin_message=None):
    if gufen_cookie is not None and len(gufen_cookie) > 0:
        cookies = gufen_cookie.split(checkin_util.split_str)
        # 遍历cookie执行签到，并返回签到状态码和签到信息
        for idx, cookie in enumerate(cookies):
            account_checkin_message = __gufen_checkin(cookie=cookie)
            # 存在账户签到信息，说明成功执行了签到
            if account_checkin_message is not None and len(account_checkin_message) > 0:
                print(f"【gufen_Account_{idx + 1}】:", account_checkin_message)
                checkin_message.append(f"【gufen_Account_{idx + 1}】 checkin message:" + str(account_checkin_message) + "      \n")
    return checkin_message
