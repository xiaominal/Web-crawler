import urllib, time
from lxml import etree
import urllib.request
from selenium import webdriver


def get_url(url):  # 国内高匿代理的链接
    url_list = []
    for i in range(1, 4):
        url_new = url + '?page=' + str(i)
        url_list.append(url_new)
    return url_list


def get_content(url):  # 获取网页内容
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    headers = {'User-Agent': user_agent}
    req = urllib.request.Request(url=url, headers=headers)
    res = urllib.request.urlopen(req)
    content = res.read()
    return content.decode('utf-8')


# 提取网页信息 / ip 端口
def get_info(content):
    datas_ip = etree.HTML(content).xpath(
        '//table[contains(@class,"table table-hover table-bordered table-striped")]/tbody/tr/td[2]/text()')
    datas_port = etree.HTML(content).xpath(
        '//table[contains(@class,"table table-hover table-bordered table-striped")]/tbody/tr/td[3]/text()')
    iplist = []
    for i in range(len(datas_ip)):
        # print(datas_ip[i],type(datas_ip[i]),datas_port[i],type(datas_port[i]))
        a = datas_ip[i] + ":" + datas_port[i]
        iplist.append(a)
    return iplist


def verif_ip(ip):  # 验证ip有效性

    try:
        print("当前代理IP " + ip)
        proxy = urllib.request.ProxyHandler({"http": ip})
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        url = "http://www.baidu.com"
        data = urllib.request.urlopen(url).read().decode('utf-8', 'ignore')
        print("通过ip")
        with open("d:\IPdata.txt", "a", encoding='utf-8') as fd:  # 有效ip保存到data2文件夹
            fd.write(ip + u"\n")
        print("-----------------------------")
    except Exception as err:
        print(err)
        print("-----------------------------")


if __name__ == '__main__':
    time_start = time.time()
    url = 'http://ip.jiangxianli.com/'
    url_list = get_url(url)
    data_ip_all = []
    data_port_all = []

    for i in url_list:
        print(i)
        content = get_content(i)
        time.sleep(3)
        data = get_info(content)
        data_ip_all.append(data)

    for ipdata in data_ip_all:
        for data in ipdata:
            print('0', data.split(u":")[0], '1', data.split(u":")[1])
            verif_ip(data)

    with open("d:\IPdata.txt", "r") as fd:
        datas = fd.readlines()

        for data in datas:
            print(data)
            data.strip('\n')
            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.add_argument(('--proxy-server=http://' + data))
            driver = webdriver.Chrome(chrome_options=chromeOptions)
            driver.get('https://xin.baidu.com/')
            time.sleep(20)

            if '输入企业名、注册号、法定代表人等' in driver.page_source:
                print("通过")
                with open("d:\IPdataok.txt", "a", encoding='utf-8') as fd:
                    fd.write(data)
    time_end = time.time()
    print('totally cost', time_end - time_start)