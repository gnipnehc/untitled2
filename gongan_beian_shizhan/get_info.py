
from gongan_beian_shizhan.save_img import save_screen
from gongan_beian_shizhan.reginize_codes import soc_code
import time
from PIL import Image
from gongan_beian_shizhan.chrome_run import bowser
from gongan_beian_shizhan.create_table import url_all_info, db

count = 0


def into_url(domain_name):
    # bowser.find_element_by_xpath('//*[@id="searchtype"]').click()
    bowser.find_element_by_xpath('//*[@id="searchtype"]/option[2]').click()
    input_name = bowser.find_element_by_xpath('//*[@id="searchname"]')
    input_name.clear()
    input_name.send_keys(domain_name)
    time.sleep(0.5)
    input_code = bowser.find_element_by_id('searchVer')
    input_code.clear()
    input_code.send_keys(soc_code())
    time.sleep(0.5)

    error = bowser.find_element_by_xpath('//*[@id="searcherror"]').text  # 验证码识别失败
    if error:
        # 清空验证码输入框并点击验证码刷新图片
        input_code.clear()
        click_img = bowser.find_element_by_xpath('//*[@id="searchImg"]')
        click_img.click()
        time.sleep(0.5)

        bowser.save_screenshot('chrome_img.png')  # 截取整个屏幕
        # 找到验证码图片的位置
        code_Element = bowser.find_element_by_xpath('//*[@id="searchImg"]')

        img_size = code_Element.size
        img_location = code_Element.location
        # 计算验证码整体坐标
        rangle = (int(img_location['x']), int(img_location['y']), int(img_location['x'] +
                                                                      img_size['width']),
                  int(img_location['y'] + img_size['height']))
        login = Image.open('chrome_img.png').convert('RGB')
        login_img = login.crop(rangle)
        login_img.save('code.jpg')  # 保存验证码图片
        time.sleep(1)

        input_code.send_keys(soc_code())
        right = bowser.find_element_by_xpath('//*[@id="searchright"]')  # 验证码识别正确
        if right:
            # 点击查询按钮
            bowser.find_element_by_xpath('//*[@id="searchform"]/a').click()
            try:
                try:
                    basic_info = bowser.find_element_by_xpath('/html/body/div[1]/div[2]/div[3]/div[1]/table')
                    content = basic_info.find_elements_by_tag_name('td')
                    list = []
                    for td in content:
                        list.append(td.text)
                    # print(list)

                    if domain_name.strip('\n') == list[3]:
                        name = list[1]
                        domain = list[3]
                        if list[4] == '网站二级域名':
                            most = list[7]
                            wtype = list[9]
                            with open('have_second_domain.txt', 'a+') as f:
                                f.write(domain_name)
                        else:
                            most = list[5]
                            wtype = list[7]

                        user_message = bowser.find_element_by_xpath('/html/body/div[1]/div[2]/div[3]/div[2]/table')
                        user_content = user_message.find_elements_by_tag_name('td')
                        shuju = []
                        for td in user_content:
                            shuju.append(td.text)
                        # print(shuju)

                        uname = shuju[1]
                        case_number = shuju[3]
                        record_address = shuju[5]
                        filing_time = shuju[7]

                        massage = url_all_info(
                            main_domain=domain, url_name=name, main_body=most, url_type=wtype, use_name=uname,
                            recode_number=case_number, public_address=record_address, recode_time=filing_time,
                            is_code=True)
                        db.session.add(massage)
                        db.session.commit()
                        time.sleep(1)
                    else:
                        name = list[1]
                        domain = domain_name
                        if list[4] == '网站二级域名':
                            most = list[7]
                            wtype = list[9]
                            with open('have_second_domain.txt', 'a+') as f:
                                f.write(domain_name)
                        else:
                            most = list[5]
                            wtype = list[7]
                        # 两个域名不一致，则存入两条数据
                        second_domain = list[3]
                        with open('two_domain_name.txt', 'a+') as f:
                            f.write(domain+second_domain+'\n')

                        user_message = bowser.find_element_by_xpath('/html/body/div[1]/div[2]/div[3]/div[2]/table')
                        user_content = user_message.find_elements_by_tag_name('td')
                        shuju = []
                        for td in user_content:
                            shuju.append(td.text)
                        # print(shuju)

                        uname = shuju[1]
                        case_number = shuju[3]
                        record_address = shuju[5]
                        filing_time = shuju[7]

                        massage1 = url_all_info(
                            main_domain=domain.strip('\n'), url_name=name, main_body=most, url_type=wtype, use_name=uname,
                            recode_number=case_number, public_address=record_address, recode_time=filing_time,
                            is_code=True)

                        message2 = url_all_info(
                            main_domain=second_domain, url_name=name, main_body=most, url_type=wtype, use_name=uname,
                            recode_number=case_number, public_address=record_address, recode_time=filing_time,
                            is_code=True
                        )
                        db.session.add(massage1)
                        db.session.add(message2)
                        db.session.commit()
                        time.sleep(1)

                    bowser.back()
                    bowser.refresh()
                    bowser.find_element_by_xpath('//*[@id="searchtype"]').click()
                    bowser.find_element_by_xpath('//*[@id="searchtype"]/option[2]').click()
                    time.sleep(0.5)
                except:
                    if bowser.find_element_by_xpath('//*[@id="kong_wzym"]'):
                        info = url_all_info(
                            main_domain=domain_name.strip('\n'), url_name='', main_body='', url_type='', use_name='',
                            recode_number='', public_address='', recode_time='', is_code=False)
                        db.session.add(info)
                        db.session.commit()
                        bowser.refresh()
                        bowser.find_element_by_xpath('//*[@id="searchtype"]').click()
                        bowser.find_element_by_xpath('//*[@id="searchtype"]/option[2]').click()
                        time.sleep(0.5)
            except:
                print('500 error')
                info = url_all_info(
                    main_domain=domain_name.strip('\n'), url_name='', main_body='', url_type='', use_name='',
                    recode_number='', public_address='', recode_time='', is_code=False
                )
                db.session.add(info)
                db.session.commit()
                with open('weihuing_domain.txt', 'a+') as f:
                    f.write(domain_name)
                    time.sleep(0.5)
                bowser.refresh()
                bowser.find_element_by_xpath('//*[@id="searchtype"]').click()
                bowser.find_element_by_xpath('//*[@id="searchtype"]/option[2]').click()
                time.sleep(1)
        # else:
        #     # 清空验证码输入框并点击验证码刷新图片
        #     input_code.clear()
        #     click_img = bowser.find_element_by_xpath('//*[@id="searchImg"]')
        #     click_img.click()
        #     time.sleep(0.5)
        #
        #     bowser.save_screenshot('chrome_img.png')  # 截取整个屏幕
        #     # 找到验证码图片的位置
        #     code_Element = bowser.find_element_by_xpath('//*[@id="searchImg"]')
        #
        #     img_size = code_Element.size
        #     img_location = code_Element.location
        #     # 计算验证码整体坐标
        #     rangle = (int(img_location['x']), int(img_location['y']), int(img_location['x'] +
        #                                                                   img_size['width']),
        #               int(img_location['y'] + img_size['height']))
        #     login = Image.open('chrome_img.png').convert('RGB')
        #     login_img = login.crop(rangle)
        #     login_img.save('code.jpg')  # 保存验证码图片
        #     time.sleep(0.5)
        #
        #     input_code.send_keys(soc_code())
        #     if right:
        #         # 点击查询按钮
        #         bowser.find_element_by_xpath('//*[@id="searchform"]/a').click()
        #         try:
        #             try:
        #                 basic_info = bowser.find_element_by_xpath('/html/body/div[1]/div[2]/div[3]/div[1]/table')
        #                 content = basic_info.find_elements_by_tag_name('td')
        #                 list = []
        #                 for td in content:
        #                     list.append(td.text)
        #                 # print(list)
        #
        #                 if domain_name.strip('\n') == list[3]:
        #                     name = list[1]
        #                     domain = list[3]
        #                     if list[4] == '网站二级域名':
        #                         most = list[7]
        #                         wtype = list[9]
        #                         with open('have_second_domain.txt', 'a+') as f:
        #                             f.write(domain_name)
        #                     else:
        #                         most = list[5]
        #                         wtype = list[7]
        #
        #                     user_message = bowser.find_element_by_xpath('/html/body/div[1]/div[2]/div[3]/div[2]/table')
        #                     user_content = user_message.find_elements_by_tag_name('td')
        #                     shuju = []
        #                     for td in user_content:
        #                         shuju.append(td.text)
        #                     # print(shuju)
        #
        #                     uname = shuju[1]
        #                     case_number = shuju[3]
        #                     record_address = shuju[5]
        #                     filing_time = shuju[7]
        #
        #                     massage = url_all_info(
        #                         main_domain=domain, url_name=name, main_body=most, url_type=wtype, use_name=uname,
        #                         recode_number=case_number, public_address=record_address, recode_time=filing_time,
        #                         is_code=True)
        #                     db.session.add(massage)
        #                     db.session.commit()
        #                     time.sleep(0.5)
        #                 else:
        #                     name = list[1]
        #                     domain = domain_name
        #                     if list[4] == '网站二级域名':
        #                         most = list[7]
        #                         wtype = list[9]
        #                         with open('have_second_domain.txt', 'a+') as f:
        #                             f.write(domain_name)
        #                     else:
        #                         most = list[5]
        #                         wtype = list[7]
        #                     # 两个域名不一致，则存入两条数据
        #                     second_domain = list[3]
        #                     with open('two_domain_name.txt', 'a+') as f:
        #                         f.write(domain + second_domain + '\n')
        #
        #                     user_message = bowser.find_element_by_xpath('/html/body/div[1]/div[2]/div[3]/div[2]/table')
        #                     user_content = user_message.find_elements_by_tag_name('td')
        #                     shuju = []
        #                     for td in user_content:
        #                         shuju.append(td.text)
        #                     # print(shuju)
        #
        #                     uname = shuju[1]
        #                     case_number = shuju[3]
        #                     record_address = shuju[5]
        #                     filing_time = shuju[7]
        #
        #                     massage1 = url_all_info(
        #                         main_domain=domain.strip('\n'), url_name=name, main_body=most, url_type=wtype,
        #                         use_name=uname,
        #                         recode_number=case_number, public_address=record_address, recode_time=filing_time,
        #                         is_code=True)
        #
        #                     message2 = url_all_info(
        #                         main_domain=second_domain, url_name=name, main_body=most, url_type=wtype,
        #                         use_name=uname,
        #                         recode_number=case_number, public_address=record_address, recode_time=filing_time,
        #                         is_code=True
        #                     )
        #                     db.session.add(massage1)
        #                     db.session.add(message2)
        #                     db.session.commit()
        #                     time.sleep(1)
        #
        #                 bowser.back()
        #                 bowser.refresh()
        #                 bowser.find_element_by_xpath('//*[@id="searchtype"]').click()
        #                 bowser.find_element_by_xpath('//*[@id="searchtype"]/option[2]').click()
        #                 time.sleep(0.5)
        #             except:
        #                 if bowser.find_element_by_xpath('//*[@id="kong_wzym"]'):
        #                     info = url_all_info(
        #                         main_domain=domain_name.strip('\n'), url_name='', main_body='', url_type='',
        #                         use_name='',
        #                         recode_number='', public_address='', recode_time='', is_code=False)
        #                     db.session.add(info)
        #                     db.session.commit()
        #                     bowser.refresh()
        #                     bowser.find_element_by_xpath('//*[@id="searchtype"]').click()
        #                     bowser.find_element_by_xpath('//*[@id="searchtype"]/option[2]').click()
        #                     time.sleep(0.5)
        #         except:
        #             print('500 error')
        #             info = url_all_info(
        #                 main_domain=domain_name.strip('\n'), url_name='', main_body='', url_type='', use_name='',
        #                 recode_number='', public_address='', recode_time='', is_code=False
        #             )
        #             db.session.add(info)
        #             db.session.commit()
        #             with open('weihuing_domain.txt', 'a+') as f:
        #                 f.write(domain_name)
        #                 time.sleep(0.5)
        #             bowser.refresh()
        #             bowser.find_element_by_xpath('//*[@id="searchtype"]').click()
        #             bowser.find_element_by_xpath('//*[@id="searchtype"]/option[2]').click()
        #             time.sleep(1)

    else:
        bowser.find_element_by_xpath('//*[@id="searchform"]/a').click()
        try:
            try:
                basic_info = bowser.find_element_by_xpath('/html/body/div[1]/div[2]/div[3]/div[1]/table')
                content = basic_info.find_elements_by_tag_name('td')
                list = []
                for td in content:
                    list.append(td.text)
                # print(list)

                if domain_name.strip('\n') == list[3]:
                    name = list[1]
                    domain = list[3]
                    if list[4] == '网站二级域名':
                        most = list[7]
                        wtype = list[9]
                        with open('have_second_domain.txt', 'a+') as f:
                            f.write(domain_name)
                    else:
                        most = list[5]
                        wtype = list[7]

                    user_message = bowser.find_element_by_xpath('/html/body/div[1]/div[2]/div[3]/div[2]/table')
                    user_content = user_message.find_elements_by_tag_name('td')
                    shuju = []
                    for td in user_content:
                        shuju.append(td.text)
                    # print(shuju)

                    uname = shuju[1]
                    case_number = shuju[3]
                    record_address = shuju[5]
                    filing_time = shuju[7]

                    massage = url_all_info(
                        main_domain=domain, url_name=name, main_body=most, url_type=wtype, use_name=uname,
                        recode_number=case_number, public_address=record_address, recode_time=filing_time,
                        is_code=True)
                    db.session.add(massage)
                    db.session.commit()
                    time.sleep(0.5)
                else:
                    name = list[1]
                    domain = domain_name
                    if list[4] == '网站二级域名':
                        most = list[7]
                        wtype = list[9]
                        with open('have_second_domain.txt', 'a+') as f:
                            f.write(domain_name)
                    else:
                        most = list[5]
                        wtype = list[7]
                    # 两个域名不一致，则存入两条数据
                    second_domain = list[3]
                    with open('two_domain_name.txt', 'a+') as f:
                        f.write(domain+second_domain+'\n')

                    user_message = bowser.find_element_by_xpath('/html/body/div[1]/div[2]/div[3]/div[2]/table')
                    user_content = user_message.find_elements_by_tag_name('td')
                    shuju = []
                    for td in user_content:
                        shuju.append(td.text)
                    # print(shuju)

                    uname = shuju[1]
                    case_number = shuju[3]
                    record_address = shuju[5]
                    filing_time = shuju[7]

                    massage1 = url_all_info(
                        main_domain=domain.strip('\n'), url_name=name, main_body=most, url_type=wtype, use_name=uname,
                        recode_number=case_number, public_address=record_address, recode_time=filing_time,
                        is_code=True)

                    message2 = url_all_info(
                        main_domain=second_domain, url_name=name, main_body=most, url_type=wtype, use_name=uname,
                        recode_number=case_number, public_address=record_address, recode_time=filing_time,
                        is_code=True
                    )
                    db.session.add(massage1)
                    db.session.add(message2)
                    db.session.commit()
                    time.sleep(1)

                bowser.back()
                bowser.refresh()
                bowser.find_element_by_xpath('//*[@id="searchtype"]').click()
                bowser.find_element_by_xpath('//*[@id="searchtype"]/option[2]').click()
                time.sleep(0.5)
            except:
                if bowser.find_element_by_xpath('//*[@id="kong_wzym"]').text:
                    info = url_all_info(
                        main_domain=domain_name.strip('\n'), url_name='', main_body='', url_type='', use_name='',
                        recode_number='', public_address='', recode_time='', is_code=False)
                    db.session.add(info)
                    db.session.commit()
                    bowser.refresh()
                    bowser.find_element_by_xpath('//*[@id="searchtype"]').click()
                    bowser.find_element_by_xpath('//*[@id="searchtype"]/option[2]').click()
                    time.sleep(0.5)
        except:
            print('500 error')
            info = url_all_info(
                main_domain=domain_name.strip('\n'), url_name='', main_body='', url_type='', use_name='',
                recode_number='', public_address='', recode_time='', is_code=False
            )
            db.session.add(info)
            db.session.commit()
            with open('weihuing_domain.txt', 'a+') as f:
                f.write(domain_name)
                time.sleep(0.5)
            bowser.refresh()
            bowser.find_element_by_xpath('//*[@id="searchtype"]').click()
            bowser.find_element_by_xpath('//*[@id="searchtype"]/option[2]').click()
            time.sleep(1)


if __name__ == '__main__':
    d_data = open('domain1.txt', 'r')
    for i in d_data:
        domain_name = i
        count += 1
        into_url(domain_name)
        save_screen()
        soc_code()
    print('已爬取{}个域名'.format(count))
