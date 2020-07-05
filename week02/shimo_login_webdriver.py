from selenium import webdriver
import time

try:
    browser = webdriver.Chrome()
    browser.get('https://shimo.im/')
    time.sleep(2)

    loginpage_btn = browser.find_element_by_xpath(
        '//*[@id="homepage-header"]/nav/div[3]/a[2]/button')
    loginpage_btn.click()

    browser.find_element_by_xpath(
        '//*[@name="mobileOrEmail"]').send_keys('zrmpop@qq.com')
    browser.find_element_by_xpath(
        '//*[@name="password"]').send_keys('123456')
    time.sleep(1)
    login_btn = browser.find_element_by_xpath(
        '//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/button')
    login_btn.click()

    cookies = browser.get_cookies()  # 获取cookies
    print(cookies)

except Exception as e:
    print(e)
finally:
    time.sleep(5)
    browser.close()
