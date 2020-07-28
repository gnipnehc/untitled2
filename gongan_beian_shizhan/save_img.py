from PIL import Image
from gongan_beian_shizhan.chrome_run import bowser
import time


class save_screen(object):
    # 保存截图
    click_domain = bowser.find_element_by_xpath('//*[@id="searchtype"]').click()
    tags = bowser.find_element_by_xpath('//*[@id="searchtype"]/option[2]').click()
    bowser.find_element_by_xpath('//*[@id="searchImg"]').click()
    time.sleep(1)
    bowser.save_screenshot('chrome_img.png')

    code_Element = bowser.find_element_by_xpath('//*[@id="searchImg"]')
    # print(code_Element)

    img_size = code_Element.size
    img_location = code_Element.location
    # 计算验证码整体坐标
    rangle = (int(img_location['x']), int(img_location['y']), int(img_location['x'] +
                                                                  img_size['width']),
              int(img_location['y'] + img_size['height']))
    login = Image.open('chrome_img.png').convert('RGB')
    login_img = login.crop(rangle)
    pic = login_img.save('code.jpg')

