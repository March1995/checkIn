# -*- coding: utf-8 -*-
# @Author    :yaoys
# @Desc      :
# @Author    ：https://github.com/yaoysyao
import os

from ablesci_checkin.ableSci_checkin import ablesci_checkin_main
from bilibili_checkin import bilibili_alive_checkin_main, bilibili_checkin_main
from cloud_189_checkin import *
from glados_checkin.glados import glados_main
from gufenxueshu_checkin import gufen_checkin_main
from push_message.push_message import *

if __name__ == '__main__':
    # glados平台cookie
    glados_cookie = os.environ['GLADOS_COOKIE']
    # # 天翼云盘cookie
    # cloud189_cookie = os.environ['CLOUD189_COOKIE']
    # # bilibili直播 cookie
    # bilibili_live_cookie = os.environ['BILIBILI_COOKIE']
    # # bilibili请求获取硬币 cookie
    # bilibili_coin_cookie = os.environ['BILI_COIN_COOKIE']
    # pushplus平台token
    pushplus_token = os.environ['PUSHPLUS_TOKEN']
    # server酱token
    # server_token = os.environ['SERVER_TOKEN']
    # #
    # able_sci_cookie = os.environ['ABLESCI_COOKIE']
    # #
    # gufen_cookie = os.environ['GUFENXUESHU_COOKIE']

    checkin_message = []

    print('The print message is: ')
    try:
        checkin_message = glados_main(checkin_message=checkin_message, glados_cookie=glados_cookie)
    except Exception as e:
        checkin_message.append('main function: gloads checkin error, the error is ' + str(e))

    # try:
    #     # 天翼云盘执行签到
    #     checkin_message = cloud189_checkin_main(cloud189_cookie=cloud189_cookie, checkin_message=checkin_message)
    # except Exception as e:
    #     checkin_message.append('main function: cloud189 checkin error, the error is ' + str(e))
    #
    # try:
    #     # bilibili直播签到
    #     checkin_message = bilibili_alive_checkin_main(bilibili_live_cookie=bilibili_live_cookie, checkin_message=checkin_message)
    # except Exception as e:
    #     checkin_message.append('main function: bilibili_live checkin error, the error is ' + str(e))
    #
    # try:
    #     # bilibili请求,获取硬币
    #     checkin_message = bilibili_checkin_main(bilibili_cookie=bilibili_coin_cookie, checkin_message=checkin_message)
    # except Exception as e:
    #     checkin_message.append('main function: bilibili checkin error, the error is ' + str(e))
    #
    # try:
    #     # 科研通签到
    #     checkin_message = ablesci_checkin_main(able_sci_cookie=able_sci_cookie, checkin_message=checkin_message)
    # except Exception as e:
    #     checkin_message.append('main function: able_sci checkin error, the error is ' + str(e))
    #
    # try:
    #     # 谷粉学术签到
    #     checkin_message = gufen_checkin_main(gufen_cookie=gufen_cookie, checkin_message=checkin_message)
    # except Exception as e:
    #     checkin_message.append('main function: gufenxueshu checkin error, the error is ' + str(e))

    push_all_message(checkin_message=checkin_message, pushplus_token=pushplus_token, server_token='')
