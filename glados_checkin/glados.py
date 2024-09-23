# -*- coding: utf-8 -*-
# @Author    :yaoys
# @Desc      :
# @Author    ：https://github.com/yaoysyao

import json
import time
import requests,os
from checkin_util.uc_driver import *

import checkin_util


def glados_checkin(driver):
    checkin_url = "https://glados.rocks/api/user/checkin"
    print('The print glados_checkin is: ' + checkin_url)
    # checkin_query = """
    #     (function (){
    #     var request = new XMLHttpRequest();
    #     request.open("POST","%s",false);
    #     request.setRequestHeader('content-type', 'application/json;charset=UTF-8');
    #     request.setRequestHeader('referer', 'https://glados.rocks/console/checkin');
    #     request.setRequestHeader('origin', 'https://glados.rocks');
    #     request.setRequestHeader('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36');
    #     request.send('{"token": "glados.one"}');
    #     return request;
    #     })();
    #     """ % checkin_url
    # checkin_query = checkin_query.replace("\n", "")
    # print('The print glados_checkin is: ' + checkin_query)
    # resp = driver.execute_script("return " + checkin_query)

    cookie = os.environ.get("GLADOS_COOKIE", []).split("&")[0]
    url= "https://glados.rocks/api/user/checkin"
    referer = 'https://glados.rocks/console/checkin'
    origin = "https://glados.rocks"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    payload={
        'token': 'glados.one'
    }
    checkin = requests.post(checkin_url,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent,'content-type':'application/json;charset=UTF-8'},data=json.dumps(payload))
    # resp = json.loads(checkin["response"])
    print('The print glados_checkin resp is: ' + checkin.text)
    return checkin.json()["code"], checkin.json()['message']


def glados_status(driver):
    # status_url = "https://glados.rocks/api/user/status"
    # status_query = """
    #     (function (){
    #     var request = new XMLHttpRequest();
    #     request.setRequestHeader('referer', 'https://glados.rocks/console/checkin');
    #     request.setRequestHeader('origin', 'https://glados.rocks');
    #     request.setRequestHeader('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36');
    #     request.open("GET","%s",false);
    #     request.send(null);
    #     return request;
    #     })();
    #     """ % (status_url)
    # status_query = status_query.replace("\n", "")
    # print('The print status_query is: ' + status_query)
    # resp = driver.execute_script("return " + status_query)
    cookie = os.environ.get("GLADOS_COOKIE", []).split("&")[0]
    url2= "https://glados.rocks/api/user/status"
    referer = 'https://glados.rocks/console/checkin'
    origin = "https://glados.rocks"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    state =  requests.get(url2,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent})
    # resp = json.loads(state["response"])
    print('The print resp is: ' + state)
    return state.json()["code"], state.json()['data']


def glados(cookie_string=None, driver=None):
    print(f"cookie_string:{cookie_string}")
    if cookie_string is None:
        raise Exception('The cookie is None')

    # if driver is None:
        # driver = get_driver()
    # Load cookie
    # driver.get("https://glados.rocks")
    print(f'Load cookie')

    # if cookie_string.startswith("cookie:"):
    #     cookie_string = cookie_string[len("cookie:"):]
    # cookie_dict = [
    #     {"name": x[:x.find('=')].strip(), "value": x[x.find('=') + 1:].strip()}
    #     for x in cookie_string.split(';')
    # ]

    # driver.delete_all_cookies()
    # for cookie in cookie_dict:
    #     if cookie["name"] in ["koa:sess", "koa:sess.sig"]:
    #         driver.add_cookie({
    #             "domain": "glados.rocks",
    #             "name": cookie["name"],
    #             "value": cookie["value"],
    #             "path": "/",
    #         })

    # driver.get("https://glados.rocks")
    print(f'driver.get("https://glados.rocks")')
    # WebDriverWait(driver, 240).until(
    #     lambda x: x.title != "Just a moment..."
    # )

    print(f'The print checkin_code checkin_message start: ')
    checkin_code, checkin_message = glados_checkin(driver)

    if checkin_code == -2: checkin_message = "Login fails, please check your cookie."
    print(f"[Checkin] {checkin_message}")

    message = ''
    if checkin_code != -2:
        status_code, status_data = glados_status(driver)
        left_days = int(float(status_data["leftDays"]))
        print(f"[Status] Left days:{left_days}")
        message = 'CheckIn time:' + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ', Checkin message:' + checkin_message + ', Status: Left days ' + str(left_days)
    else:
        message = 'The account login fails, please check your cookie. '

    # close_driver(driver=driver)

    return message


def glados_main(glados_cookie=None, checkin_message=None):
    # gloads 执行签到
    if glados_cookie is not None and len(glados_cookie) > 0:
        glados_cookies = glados_cookie.split(checkin_util.constants.split_str)
        # 遍历cookie执行签到，并返回签到状态码和签到信息
        for idx, cookie in enumerate(glados_cookies):
            print(f"【Gloads_Account_{idx + 1}】:")
            account_checkin_message = glados(cookie)

            # 存在账户签到信息，说明成功执行了签到
            if account_checkin_message is not None and len(account_checkin_message) > 0:
                checkin_message.append(f"【Gloads_Account_{idx + 1}】 checkin message:" + account_checkin_message + "\n")

    return checkin_message
