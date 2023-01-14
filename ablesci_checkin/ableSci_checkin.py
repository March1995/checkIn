# -*- coding: utf-8 -*-
# @FileName  :ableSci_checkin.py
# @Time      :2022/8/20 8:19
# @Author    :yaoys
# @Desc      :
# @Author    ：https://github.com/yaoysyao
import json

import checkin_util
from checkin_util.uc_driver import *


def __able_sci_checkin(driver):
    checkin_url = "https://www.ablesci.com/user/sign"
    checkin_query = """
            (function (){
                var request = new XMLHttpRequest();
                request.open("GET","%s",false);
                request.setRequestHeader('accept', 'application/json, text/javascript, */*; q=0.01');
                request.setRequestHeader('x-requested-with', 'XMLHttpRequest');
                request.setRequestHeader('sec-ch-ua-mobile', '?0');
                request.setRequestHeader('sec-ch-ua-platform', "Windows");
                request.setRequestHeader('sec-fetch-site', 'same-origin');
                request.setRequestHeader('sec-fetch-mode', 'cors');
                request.setRequestHeader('sec-fetch-dest', 'empty');
                request.setRequestHeader('referer', 'https://www.ablesci.com/');
                request.setRequestHeader('accept-encoding', 'gzip, deflate, br');
                request.setRequestHeader('accept-language', 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7');
                request.setRequestHeader('cache-control', 'no-cache');
                request.setRequestHeader('pragma', 'no-cache');
                request.send();
                return request;
        })();
        """ % checkin_url
    checkin_query = checkin_query.replace("\n", "")
    resp = driver.execute_script("return " + checkin_query)
    resp = json.loads(resp["response"])
    code = -1
    msg = ''
    signcount = 0
    signpoint = 0
    code = resp['code']
    msg = resp['msg']
    if 'data' in resp:
        signcount = resp['data']['signcount']
        signpoint = resp['data']['signpoint']

    return code, msg, signcount, signpoint


def able_sci(cookie_string=None, driver=None):
    if cookie_string is None:
        raise Exception('The cookie is None')

    if driver is None:
        driver = get_driver()

    # Load cookie
    driver.get("https://www.ablesci.com/")

    if cookie_string.startswith("cookie:"):
        cookie_string = cookie_string[len("cookie:"):]
    cookie_dict = [
        {"name": x[:x.find('=')].strip(), "value": x[x.find('=') + 1:].strip()}
        for x in cookie_string.split(';')
    ]

    driver.delete_all_cookies()
    for cookie in cookie_dict:
        driver.add_cookie({
            "domain": "www.ablesci.com",
            "name": cookie["name"],
            "value": cookie["value"],
            "path": "/",
        })

    driver.get("https://www.ablesci.com/")
    WebDriverWait(driver, 240).until(
        lambda x: x.title != "Just a moment..."
    )
    message = ''
    checkin_code, checkin_message, signcount, signpoint = __able_sci_checkin(driver)
    message = 'The checkin code is ' + str(checkin_code) + ',the checkin message is ' + checkin_message

    print(message)

    close_driver(driver=driver)
    return message


def ablesci_checkin_main(able_sci_cookie=None, checkin_message=None):
    if able_sci_cookie is not None and len(able_sci_cookie) > 0:
        able_sci_cookies = able_sci_cookie.split(checkin_util.split_str)
        # 遍历cookie执行签到，并返回签到状态码和签到信息
        for idx, cookie in enumerate(able_sci_cookies):
            print(f"【Ableaci_Account_{idx + 1}】:")
            account_checkin_message = able_sci(cookie_string=cookie)

            # 存在账户签到信息，说明成功执行了签到
            if account_checkin_message is not None and len(account_checkin_message) > 0:
                checkin_message.append(f"【Ableaci_Account_{idx + 1}】 checkin message:" + str(account_checkin_message) + "      \n")
    return checkin_message
