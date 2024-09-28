import time

import cv2
import numpy as np
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_net():
    driver = setup()

    # 使用显式等待，确保页面元素加载完毕且按钮可点击
    wait = WebDriverWait(driver, 10)

    # 登录弹出
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-action="login"]'))).click()
    time.sleep(2)

    # 选择其他登录模式
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, '_3xIXD0Q6'))).click()
    time.sleep(2)

    # 勾选条款的 checkbox
    checkbox = wait.until(EC.element_to_be_clickable((By.ID, 'j-official-terms')))
    if not checkbox.is_selected():
        checkbox.click()
    time.sleep(2)

    # 手机号登录/注册
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, '_3fo6oHZe'))).click()
    time.sleep(2)

    # 选择密码登录
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, '密码登录'))).click()
    time.sleep(2)

    # 输入手机号
    phone_input = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, '_2OT0mQUQ')))
    phone_input.send_keys('15000840699')
    time.sleep(2)

    # 输入密码
    password_input = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'sR89MU1J')))
    password_input.send_keys('hf15000840699')
    time.sleep(2)

    # 点击登录
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, '_3fo6oHZe'))).click()
    time.sleep(2)

    # 获取两张图片
    url_s = driver.find_element(By.CLASS_NAME, 'yidun_jigsaw').get_attribute('src')
    url_b = driver.find_element(By.CLASS_NAME, 'yidun_bg-img').get_attribute('src')
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'
    }
    res_s = requests.get(url_s, headers=headers)
    data_s = res_s.content
    res_b = requests.get(url_b, headers=headers)
    data_b = res_b.content
    # 保存图片
    with open('pic_s.png', 'wb') as f:
        f.write(data_s)
    with open('pic_b.png', 'wb') as f:
        f.write(data_b)
    # 使用opencv读取两张图片
    simg = cv2.imread('pic_s.png')
    bimg = cv2.imread('pic_b.png')

    # 灰度处理，降低偏差
    s_img = cv2.cvtColor(simg, cv2.COLOR_BGR2GRAY)
    b_img = cv2.cvtColor(bimg, cv2.COLOR_BGR2GRAY)

    # 保存两张灰度处理的图片
    cv2.imwrite('hui_simg.png', s_img)
    cv2.imwrite('hui_bimg.png', b_img)

    # 处理滑块图片，保存有效部分
    s_img = s_img[s_img.any(1)]

    # opencv的匹配算法，匹配模块寻找两张图片的相似之处
    result = cv2.matchTemplate(b_img, s_img, cv2.TM_CCOEFF_NORMED)
    print('result', result)

    # 获取坐标
    # 获取最大索引
    index_max = np.argmax(result)
    # 获取到坐标
    y, x = np.unravel_index(index_max, result.shape)
    print("y:", y, "x:", x)

    # 拖动滑块的距离进行调整
    adjusted_x = x + 10  # 根据实际情况微调这个值

    # 定位到滑块
    ele = element = driver.find_element(By.XPATH,
                                        "//div[contains(@class, 'yidun_slider') and contains(@class, 'yidun_slider--hover')]")
    # 实例化对象
    action = ActionChains(driver)
    # 拖动滑块
    time.sleep(1)
    action.drag_and_drop_by_offset(ele, xoffset=adjusted_x, yoffset=0).perform()
    time.sleep(1)
    # 定位到验证成功
    time.sleep(2)

    # 点击我的音乐
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "我的音乐"))).click()
    time.sleep(2)

    # 点击关注
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "关注"))).click()
    time.sleep(2)

    teardown(driver)


def setup():
    driver = webdriver.Edge()
    driver.get("https://music.163.com")
    driver.maximize_window()
    return driver


def teardown(driver):
    driver.quit()


if __name__ == "__main__":
    test_net()
