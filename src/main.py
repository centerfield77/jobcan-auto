#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from secretManager import get_secret_version
import jpholiday
import os,time,datetime


def main(event, context):

    # URL
    TOP_PAGE_URL = 'https://id.jobcan.jp/users/sign_in'

    # cloud functionの環境変数からproject_idを取得
    PROJECT_ID = os.environ.get('PROJECT_ID')

    # ログイン情報
    MAIL_ADDRESS = get_secret_version(PROJECT_ID, 'secret_mail')
    PASSWORD = get_secret_version(PROJECT_ID, 'secret_password')

    # CSSセレクタ
    MAIL_INPUT_SELECTOR = '#user_email'
    PASSWORD_INPUT_SELECTOR = '#user_password'
    LOGIN_BUTTON_SELECTOR = '#login_button'
    KINTAI_PAGE_LINK_TAB_SELECTOR = '#jbc-app-links > ul > li:nth-child(3) > a'
    DAKOKU_BUTTON_SELECTOR = '#adit-button-push'


    # 祝日だったら何もせず終了
    is_holiday = jpholiday.is_holiday(datetime.date.today()) 
    if is_holiday:
        print('Today is holiday.')
        return
    

    # seleniumの初期化
    path = os.getcwd()
    driverPath = path + '/bin/chromedriver'
    headlessPath = path + '/bin/headless-chromium'
    options = Options()
    options.binary_location = headlessPath
    driver = webdriver.Chrome(driverPath, options=options)

    # ページを開く
    driver.get(TOP_PAGE_URL)
    time.sleep(2)

    # ログイン
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, MAIL_INPUT_SELECTOR)))
    mail_input = driver.find_element_by_css_selector(MAIL_INPUT_SELECTOR)
    password_input = driver.find_element_by_css_selector(PASSWORD_INPUT_SELECTOR)
    login_button = driver.find_element_by_css_selector(LOGIN_BUTTON_SELECTOR)
    mail_input.send_keys(MAIL_ADDRESS)
    password_input.send_keys(PASSWORD)
    login_button.click()
    time.sleep(2)

    # 勤怠ページへ
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, KINTAI_PAGE_LINK_TAB_SELECTOR)))
    kintai_page_link_tab = driver.find_element_by_css_selector(KINTAI_PAGE_LINK_TAB_SELECTOR)
    kintai_page_link_tab.click()
    time.sleep(2)

    # 打刻
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, DAKOKU_BUTTON_SELECTOR)))
    dakoku_button = driver.find_element_by_css_selector(DAKOKU_BUTTON_SELECTOR)
    print(dakoku_button.text)
    dakoku_button.click()

    driver.quit()