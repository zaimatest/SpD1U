#getCookies.py
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait #设置延迟需要用到
#from selenium.common.exceptions import TimeoutException

from setting import SELE_TIME_OUT, DOMAIN_NAME

#定义日志配置
import logging
logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(levelname)s : %(message)s')

def get_cookies_dict(BookName, Url):
    #这里拿cookie
    mobileEmulation = {"deviceName": "iPhone X"}
    options = webdriver.ChromeOptions()
    options.add_experimental_option("mobileEmulation", mobileEmulation)
    options.add_argument('--headless') #可以开无头
    #载入加载项
    browser = webdriver.Chrome(options=options)
    wait = WebDriverWait(browser, SELE_TIME_OUT) #超时设置：配置页面加载的最长等待时间

    browser.get(Url) 
    try:
        browser.find_element(By.CSS_SELECTOR, 'input[id="password"]').send_keys('1234')
        browser.find_element(By.CSS_SELECTOR, 'div.login a').click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="submit"]')))
    except:
        logging.info('无密码')

    #删除元素中style属性，使搜索节点可见
    script = "document.querySelector('body div[style]').removeAttribute('style')"
    browser.execute_script(script)
    DOMAIN_NAME = browser.current_url

    browser.find_element(By.CSS_SELECTOR, 'input[type="text"]').send_keys(BookName)
    browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
    

    _dict={"Booklen":0,
        "BookName":"",
        "Bookurl":"",
        "Cookies":"",
        "userAgent":"",
        "DOMAIN_NAME":DOMAIN_NAME}
    _Booklen=0
    IsNoSearch = False
    try:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.bd')))
    except:
        IsNoSearch = True
        logging.error('搜索无结果或未搜索词长度小于3', exc_info=True)
    
    if not IsNoSearch:
        elements_indexs = browser.find_elements(By.CSS_SELECTOR, 'div.bd div.right')
        if len(elements_indexs) > 0:
            for elements_index in elements_indexs:
                Booklen=int(elements_index.find_element(By.CSS_SELECTOR, 'span.words').text.replace('字数：', ''))
                if Booklen > _Booklen:
                    _Booklen = Booklen
                    _dict["Booklen"] = _Booklen
                    _dict["BookName"] = elements_index.find_element(By.CSS_SELECTOR, 'a.name').text
                    _dict["Bookurl"] = elements_index.find_element(By.CSS_SELECTOR, 'a.name').get_attribute('href')

    #拿请求头
    userAgent = browser.execute_script("return navigator.userAgent")    
    
    #拿cookies
    cookies=browser.get_cookies()
    _dict["Cookies"] = cookies
    _dict["userAgent"] = userAgent
    #print('Cookies: ', cookies, '\n')
    #print('Book: ', _dict, '\n')
    #print('userAgent: ', userAgent, '\n')
    
    # 关闭
    browser.close() 
    return _dict

def main():
    print(get_cookies_dict('何谓正邪', DOMAIN_NAME))

if __name__=='__main__':
    main()