from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
}
url = "http://www.beian.gov.cn/portal/registerSystemInfo"

# 有头模式
# bowser = webdriver.Chrome()


# 无头模式
chrome_options = Options()
chrome_options.add_argument('--headless')
bowser = webdriver.Chrome(chrome_options=chrome_options)
bowser.set_window_size(1600, 1200)

bowser.get(url)
bowser.get(url)
time.sleep(1)

# time.sleep(3)
# bowser.close()
