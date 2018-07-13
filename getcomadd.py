
from PIL import Image
from ctypes import *
from selenium.common.exceptions import NoSuchElementException
import time
from random import choice
from selenium import webdriver


# 验证码截屏
def screen_shot(driver):
    driver.get_screenshot_as_file('d:\yzm.png')

    # 获取指定元素位置
    element = driver.find_element_by_class_name('check-img-pic')
    left = int(element.location['x'])
    top = int(element.location['y'])
    right = int(element.location['x'] + element.size['width'])
    bottom = int(element.location['y'] + element.size['height'])

    # 通过Image处理图像
    im = Image.open('d:\yzm.png')
    im = im.crop((left, top, right, bottom))
    im.save('d:\yzmsave.png')

# 获取验证码
def get_yzm():
    YDMApi = windll.LoadLibrary('yundamaAPI-x64')

    # 1. http://www.yundama.com/index/reg/developer 注册开发者账号
    # 2. http://www.yundama.com/developer/myapp 添加新软件
    # 3. 使用添加的软件ID和密钥进行开发，享受丰厚分成

    appId = 4758  # 软件ＩＤ，开发者分成必要参数。登录开发者后台【我的软件】获得！
    appKey = b'acfcb069eb8b5e562ecab06cacb74ea0'  # 软件密钥，开发者分成必要参数。登录开发者后台【我的软件】获得！

    # 注意这里是普通会员账号，不是开发者账号，注册地址 http://www.yundama.com/index/reg/user
    # 开发者可以联系客服领取免费调试题分

    username = b'xiaomin_huang'
    password = b'@@@@@@@@@@@'

    if username == b'test':
        exit('\r\n>>>请先设置用户名密码')

    ####################### 一键识别函数 YDM_EasyDecodeByPath #######################

    # 例：1004表示4位字母数字，不同类型收费不同。请准确填写，否则影响识别率。在此查询所有类型 http://www.yundama.com/price.html
    codetype = 1004

    # 分配30个字节存放识别结果
    result = c_char_p(b"                              ")

    # 识别超时时间 单位：秒
    timeout = 60

    # 验证码文件路径
    filename = b'd:\yzmsave.png'

    # 一键识别函数，无需调用 YDM_SetAppInfo 和 YDM_Login，适合脚本调用
    captchaId = YDMApi.YDM_EasyDecodeByPath(username, password, appId, appKey, filename, codetype, timeout,
                                            result)
    yzm = result.value
    return yzm

def setip(ip_list,chromeOptions):
    ALL = True
    ip = choice(ip_list)
    chromeOptions.add_argument(('--proxy-server=http://' + ip))
    driver = webdriver.Chrome(chrome_options=chromeOptions)
    # 查看本机ip，查看代理是否起作用
    driver.get("https://xin.baidu.com/")
    time.sleep(30)
    if '输入企业名、注册号、法定代表人等' in driver.page_source:
        ALL = False

    else:
        ALL = True
    return  ALL,driver


def setip1(ip_list,chromeOptions):
    ALL = True
    while ALL:
        ip = choice(ip_list)
        chromeOptions.add_argument(('--proxy-server=http://' + ip))
        driver = webdriver.Chrome(chrome_options=chromeOptions)
        # 查看本机ip，查看代理是否起作用
        driver.get("https://xin.baidu.com/")
        time.sleep(30)
        if '输入企业名、注册号、法定代表人等' in driver.page_source:
            ALL = False

        else:
            ALL = True
    return driver


def main():
    #ip_list = ['93.171.25.202:53281', '39.104.53.175:8080', '36.81.203.228:8080','171.10.31.74 1:8080',]
    # ip_list =['103.23.134.106:8080','93.171.25.202:53281','47.104.88.127:8088']
    ######################################3# 读取公司名称################
    companulist = []
    file = open('D:\COMPANYlist1t.txt', encoding="utf-8")
    list1 = list(file)
    for line in list1:
        linelist = line.strip('\n')
        companulist.append(linelist)

    ####################################### 读取ip地址###################3
    fp = open('D:\IPdataok.txt', encoding="utf-8")
    lines = fp.readlines()
    ip_list = []
    for line in lines:
        line.strip('\n')
        ip_list.append(line)

    chromeOptions = webdriver.ChromeOptions()
    ip = choice(ip_list)
    chromeOptions.add_argument(('--proxy-server=http://' + ip))
    driver = webdriver.Chrome(chrome_options=chromeOptions)
    driver.get('https://xin.baidu.com/')

    #############################验证IP是否可用#############################
    ALL = True
    if '输入企业名、注册号、法定代表人等' in driver.page_source:
        print('ip ok')
    else:
        while ALL:
            ALL, driver = setip(ip_list, chromeOptions)

    for i in companulist:
        tab = True
        input_str = driver.find_element_by_class_name('search-text')
        input_str.send_keys(i)
        button = driver.find_element_by_class_name('search-btn')
        button.click()
        while tab:
            time.sleep(10)
            try:
                address = driver.find_element_by_xpath("//div[@class='zx-ent-address']/span[1]").text
                print(address, i)
                tab = False

            except NoSuchElementException as e:
                if '抱歉，没有找到相关结果...' in driver.page_source:
                    address = '无结果'
                    print(i,'抱歉，没有找到相关结果...')
                    tab = False
                elif '验证码' in driver.page_source:
                    screen_shot(driver)
                    yzm_get = get_yzm()
                    yzm1 = str(yzm_get)
                    yzm2 = yzm1[2:6]
                    print(yzm2)
                    input_str1 = driver.find_element_by_class_name('check-img-ipt')
                    input_str1.send_keys(yzm2)
                    time.sleep(12)
                    tab = True
                else:
                    driver = setip1(ip_list,chromeOptions)
                    print("重新设置IP")
                    time.sleep(30)
                    input_str = driver.find_element_by_class_name('search-text')
                    input_str.send_keys(i)
                    button = driver.find_element_by_class_name('search-btn')
                    button.click()
                    tab = True

        time.sleep(15)
        input_str = driver.find_element_by_class_name('search-text')
        input_str.clear()
        with open("d:\datatest1.txt", "a", encoding='utf-8') as fd:
            fd.write(i+ u":" + address)
            fd.write("\n")

if __name__ == '__main__':
    main()
