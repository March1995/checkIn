# -*- coding: utf-8 -*-
# @Author    :yaoys
# @Desc      :
# @Author    ：https://github.com/yaoysyao

import time

import requests
import checkin_util.constants as const

import checkin_util

__checkin_url_0 = 'http://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN_PHOTOS&activityId=ACT_SIGNIN&rand=%s'
__checkin_url_1 = 'http://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN&activityId=ACT_SIGNIN&rand=%s'


def __get_header(cookie_header):
    header = {
        'Connection': 'close',
        'Accept': '*/*',
        'Accept-Language': 'zh-cn',
        'Cookie': cookie_header,
        'Host': 'm.cloud.189.cn',
        'Content-Type': 'application/json;charset=UTF-8',
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-G930K Build/NRD90M; wv)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74"
                      ".0.3729.136 Mobile Safari/537.36 Ecloud/8.6.3 Android/22 clie"
                      "ntId/355325117317828 clientModel/SM-G930K imsi/46007111431782"
                      "4 clientChannelId/qq proVersion/1.0.6",
        "Referer": "https://m.cloud.189.cn/zhuanti/2016/sign/index.jsp?albumBackupOpened=1",
        "Accept-Encoding": "gzip, deflate",
    }
    return header


def cloud189_checkIn(cookie):
    header = __get_header(cookie)
    checkin_message = []

    for i in range(0, 2):
        rand = str(round(time.time() * 1000))
        if i == 0:
            url = __checkin_url_0 % rand
        elif i == 1:
            url = __checkin_url_1 % rand
        else:
            checkin_message.append('189 cloud checkin error,please check the code')
            return checkin_message

        resp = requests.get(url=url, headers=header, verify=False, timeout=const.request_timeout)
        result = resp.text
        result_json = resp.json()
        resp.close()
        # 说明返回了错误的签到信息
        if 'errorCode' in result:
            print('The 189 cloud is checkin,the message is:', result_json['errorCode'])
            checkin_message.append('The checkin url_' + str(i + 1) + ' result: ' + result_json['errorCode'])
        elif 'prizeName' in result:
            print('The 189 cloud is checkin,the message is: get ', result_json['prizeName'])
            checkin_message.append('The checkin url_' + str(i + 1) + ' result: ' + result_json['prizeName'])
        else:
            print('The 189 cloud checkin error')
            checkin_message.append('The checkin url_' + str(i + 1) + ' result: ' + result)
    return checkin_message


def cloud189_checkin_main(cloud189_cookie=None, checkin_message=None):
    if cloud189_cookie is not None and len(cloud189_cookie) > 0:
        cloud189_cookies = cloud189_cookie.split(checkin_util.split_str)
        # 遍历cookie执行签到，并返回签到状态码和签到信息
        for idx, cookie in enumerate(cloud189_cookies):
            print(f"【Cloud189_Account_{idx + 1}】:")
            account_checkin_message = cloud189_checkIn(cookie)

            # 存在账户签到信息，说明成功执行了签到
            if account_checkin_message is not None and len(account_checkin_message) > 0:
                cloud189_result = ''
                for i in range(0, len(account_checkin_message)):
                    cloud189_result += account_checkin_message[i] + ';'
                checkin_message.append(f"【Cloud189_Account_{idx + 1}】 checkin message:" + str(cloud189_result) + "      \n")
    return checkin_message
# 已经执行天翼云盘签到,返回签到信息: {"prizeId":"SIGNIN_CLOUD_50M","prizeName":"天翼云盘50M空间","prizeGrade":xxxxx,"prizeType":xxxx,"description":"xxxx","useDate":"2022-07-09 15:38:46","userId":xxxx,"isUsed":xxx,"activityId":"xxx","prizeStatus":xx,"showPriority":xx}
