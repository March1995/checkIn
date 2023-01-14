# -*- coding: utf-8 -*-
# @Time      :2022/8/20 8:19
# @Author    :yaoys
# @Desc      :
# @Author    ：https://github.com/yaoysyao


import io
import platform
import subprocess
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait


def get_driver_version():
    global cmd
    system = platform.system()
    println(system)
    if system == "Darwin":
        cmd = r'''/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version'''
    elif system == "Windows":
        cmd = r'''powershell -command "&{(Get-Item 'C:\Program Files\Google\Chrome\Application\chrome.exe').VersionInfo.ProductVersion}"'''

    try:
        out, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    except IndexError as e:
        print('Check chrome version failed:{}'.format(e))
        return 0

    if system == "Darwin":
        out = out.decode("utf-8").split(" ")[2].split(".")[0]
    elif system == "Windows":
        out = out.decode("utf-8").split(".")[0]

    return out


def get_driver():
    options = uc.ChromeOptions()
    options.add_argument("--disable-popup-blocking")

    version = get_driver_version()
    driver = uc.Chrome(version_main=version, options=options)
    return driver


def close_driver(driver=None):
    if driver is None:
        raise Exception('The driver is None')

    driver.close()
    driver.quit()
