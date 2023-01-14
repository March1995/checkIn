# -*- coding: utf-8 -*-
# @Author    :yaoys
# @Desc      :
# @Author    ：https://github.com/yaoysyao

import requests
import urllib3

import checkin_util

bilbi_checkin_url = 'https://api.live.bilibili.com/xlive/web-ucenter/v1/sign/DoSign'


def __get_header(cookie_header):
    header = {
        'Connection': 'Keep-Alive',
        'Accept': '*/*',
        'Accept-Language': 'zh-cn',
        'Cookie': cookie_header,
        'Host': 'api.live.bilibili.com',
        'Content-Type': 'application/json;charset=UTF-8',
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-G930K Build/NRD90M; wv)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74"
                      ".0.3729.136 Mobile Safari/537.36 Ecloud/8.6.3 Android/22 clie"
                      "ntId/355325117317828 clientModel/SM-G930K imsi/46007111431782"
                      "4 clientChannelId/qq proVersion/1.0.6",
        "Referer": "https://api.live.bilibili.com/xlive/web-ucenter/v1/sign/DoSign",
        "Accept-Encoding": "gzip, deflate",
    }
    return header


# 解决出现警告 Adding certificate verification is strongly advised.
urllib3.disable_warnings()


def bilibili_checkin(cookie):
    header = __get_header(cookie)
    resp = requests.get(url=bilbi_checkin_url, headers=header, verify=False)
    result = resp.text
    result_json = resp.json()
    resp.close()
    # 签到成功
    if 'code' in result and 'data' in result and result_json['code'] == 0:
        check_message = 'checkin success,the message is: ' + result_json['data']['text']
    # 签到失败
    elif 'code' in result and result_json['code'] == 1011040:
        check_message = result_json['message']
    # 账号未登录,cookie过期
    elif 'code' in result and result_json['code'] == -101:
        check_message = result_json['message'] + ',cookie过期，请更新cookie'
    else:
        check_message = 'bilibili_Alive checkin error'
    check_message = 'The bilibili_Alive checkin message: ' + check_message
    print(check_message)
    return check_message


def bilibili_alive_checkin_main(bilibili_live_cookie=None, checkin_message=None):
    if bilibili_live_cookie is not None and len(bilibili_live_cookie) > 0:
        bilibili_live_cookies = bilibili_live_cookie.split(checkin_util.split_str)
        # 遍历cookie执行签到，并返回签到状态码和签到信息
        for idx, cookie in enumerate(bilibili_live_cookies):
            print(f"【Bilibili_Alive_Account_{idx + 1}】:")
            account_checkin_message = bilibili_checkin(cookie)

            # 存在账户签到信息，说明成功执行了签到
            if account_checkin_message is not None and len(account_checkin_message) > 0:
                checkin_message.append(f"【Bilibili_Alive_Account_{idx + 1}】 checkin message:" + str(account_checkin_message) + "      \n")
    return checkin_message
