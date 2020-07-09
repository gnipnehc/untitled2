from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options as FOptions


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
}
url = "http://www.beian.gov.cn/portal/registerSystemInfo"

# 有头模式
# options = FOptions()
# bowser = webdriver.Chrome(options=options)

# 无头模式
options = webdriver.ChromeOptions()
options.set_headless()
bowser = webdriver.Chrome(chrome_options=options)

bowser.get(url)
bowser.get(url)
time.sleep(1)

# time.sleep(3)
# bowser.close()
