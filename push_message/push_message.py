# -*- coding: utf-8 -*-
# @Author    :yaoys
# @Desc      :
# @Author    ：https://github.com/yaoysyao

import requests
from checkin_util.constants import request_timeout


def push_all_message(checkin_message=None, pushplus_token=None, server_token=None):
    # 所有账号签到完毕，判断是否有签到信息，如果有签到信息说明账号执行了签到
    if checkin_message is not None and len(checkin_message) > 0:
        print('The push message is:', checkin_message)
        try:
            # 推送签到消息至pushplus平台
            if pushplus_token is not None and len(pushplus_token) > 0:
                pushplus_message(pushplus_token, ''.join(checkin_message))
            else:
                print('The push plus token is none')
        except Exception as e:
            print('push push plus message error:', str(e))

        try:
            #     推送至server酱
            if server_token is not None and len(server_token) > 0:
                server_messgae(token=server_token, title='checkIn status', message=''.join(checkin_message))
            else:
                print('The server token is none')
        except Exception as e:
            print('push server message error:', str(e))
    else:
        print('The checkin_message is none')


def pushplus_message(token, message):
    payload = {'token': token, "channel": "wechat", "template": "html", "content": message, "title": "checkin status"}
    resp = requests.post("http://www.pushplus.plus/send", params=payload, timeout=request_timeout)
    if resp.status_code == 200:
        print('push plus success code:', resp.status_code)
    else:
        print('push message to push plus error,the code is:', resp.status_code)
    resp.close()


def server_messgae(token, title, message):
    payload = {"title": title, "desp": message, }
    resp = requests.post(f"https://sctapi.ftqq.com/{token}.send", params=payload, timeout=request_timeout)
    result = resp.json()
    if result["code"] == 0:
        print("Push the message to server success(code:0),the code is:" + str(result["code"]))
    if result["code"] != 0:
        print("Push the message to server error(code!=0),The error message is " + str(result["code"]) + str(result["message"]))
    code = resp.status_code
    resp.close()
    return code
