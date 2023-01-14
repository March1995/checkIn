# -*- coding: utf-8 -*-
# @Author    :yaoys
# @Desc      :
# @Author    ：https://github.com/yaoysyao

import requests
import urllib3

import checkin_util

bilbi_checkin_url = 'https://www.bilibili.com/'
bilibili_coin_count_url = 'https://account.bilibili.com/site/getCoin?csrf=66d56f905a20735f69bf816d2d867e83'
bilibili_coin_log_url = 'https://api.bilibili.com/x/member/web/coin/log?csrf=66d56f905a20735f69bf816d2d867e83&jsonp=jsonp'


def __get_header(cookie_header):
    header = {
        'Connection': 'Keep-Alive',
        'Accept': '*/*',
        'Accept-Language': 'zh-cn',
        'Cookie': cookie_header,
        'Content-Type': 'application/json;charset=UTF-8',
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-G930K Build/NRD90M; wv)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74"
                      ".0.3729.136 Mobile Safari/537.36 Ecloud/8.6.3 Android/22 clie"
                      "ntId/355325117317828 clientModel/SM-G930K imsi/46007111431782"
                      "4 clientChannelId/qq proVersion/1.0.6",
        "Accept-Encoding": "gzip, deflate",
    }
    return header


def __get_coin_count_header(cookie_header):
    header = {
        'Connection': 'Keep-Alive',
        'Accept': '*/*',
        'Accept-Language': 'zh-cn',
        'Cookie': cookie_header,
        'referer': 'https://account.bilibili.com/account/coin',
        'Content-Type': 'application/json;charset=UTF-8',
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-G930K Build/NRD90M; wv)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74"
                      ".0.3729.136 Mobile Safari/537.36 Ecloud/8.6.3 Android/22 clie"
                      "ntId/355325117317828 clientModel/SM-G930K imsi/46007111431782"
                      "4 clientChannelId/qq proVersion/1.0.6",
        "Accept-Encoding": "gzip, deflate",
    }
    return header


def __get_coin_log_header(cookie_header):
    header = {
        'Connection': 'Keep-Alive',
        'Accept': '*/*',
        'Accept-Language': 'zh-cn',
        'Cookie': cookie_header,
        'referer': 'https://account.bilibili.com/',
        'Content-Type': 'application/json;charset=UTF-8',
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-G930K Build/NRD90M; wv)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74"
                      ".0.3729.136 Mobile Safari/537.36 Ecloud/8.6.3 Android/22 clie"
                      "ntId/355325117317828 clientModel/SM-G930K imsi/46007111431782"
                      "4 clientChannelId/qq proVersion/1.0.6",
        "Accept-Encoding": "gzip, deflate",
    }
    return header


# 解决出现警告 Adding certificate verification is strongly advised.
urllib3.disable_warnings()


def bilibili_checkin(cookie):
    header = __get_header(cookie)
    resp = requests.get(url=bilbi_checkin_url, headers=header, verify=False)
    resp_code = resp.status_code
    resp.close()

    if resp_code == 200:
        # get coin count
        header = __get_coin_count_header(cookie)
        resp = requests.get(url=bilibili_coin_count_url, headers=header, verify=False)
        # print(resp.json()['code'], resp.json()['status'], resp.json()['data']['money'])
        if resp.json()['code'] == 0:
            check_message = 'get bilibili count success,the code is {},the status is {},the coin count is {},' \
                .format(resp.json()['code'], resp.json()['status'], resp.json()['data']['money'])
        else:
            check_message = ''
        resp.close()

        # get coin log and latest log
        header = __get_coin_log_header(cookie)
        resp = requests.get(url=bilibili_coin_log_url, headers=header, verify=False)
        # print(resp.json()['code'], resp.json()['status'], resp.json()['data']['money'])
        if resp.json()['code'] == 0 and resp.json()['message'] == '0':
            check_message += ' get bilibili log success,the code is {},the message is {},the latest log is {}' \
                .format(resp.json()['code'], resp.json()['message'], resp.json()['data']['list'][0])
        resp.close()

    else:
        check_message = 'get bilibili coin  error,the code is ' + str(resp_code)

    check_message = 'The bilibili get coin checkin message: ' + check_message
    print(check_message)
    return check_message


def bilibili_checkin_main(bilibili_cookie=None, checkin_message=None):
    if bilibili_cookie is not None and len(bilibili_cookie) > 0:
        bilibili_cookie = bilibili_cookie.split(checkin_util.split_str)
        # 遍历cookie执行签到，并返回签到状态码和签到信息
        for idx, cookie in enumerate(bilibili_cookie):
            print(f"【Bilibili_Account_{idx + 1}】:")
            account_checkin_message = bilibili_checkin(cookie)

            # 存在账户签到信息，说明成功执行了签到
            if account_checkin_message is not None and len(account_checkin_message) > 0:
                checkin_message.append(f"【Bilibili_Account_{idx + 1}】 checkin message:" + str(account_checkin_message) + "      \n")
    return checkin_message
