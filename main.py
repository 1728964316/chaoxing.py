import json
import re
import time

import pyautogui
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--mute-audio")#静音
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation','enable-logging'])

url = 'https://www.zhihuishu.com/'

class p():
    def start(self):
        # self.Denglu()
        # input('输入:')
        # self.Save_cookie()

        self.Send_cookie()
        self.JingRu()
        self.Judget1()
        self.getlist()
        time.sleep(1)
        self.start_time = time.time()
        self.end_time = 0
        self.播放时间 = 0
        self.播放时间 = 0
        视频时间 = self.Get_time()
        now_time=''
        while True:
            if self.播放时间 >= 30*60:
                print('到达规定时间')
                break;
            self.get_now_num()
            self.当前下标 = self.number_list0.index(self.now_num)
            print('当前' + self.number_list0[self.当前下标])
            self.Finish_pro()
            self.Bofang()
            while True:
                pre_time = self.播放时间
                if pre_time == now_time != 视频时间[1]:
                    self.Bofang()
                pre_time = now_time
                self.end_time = time.time()
                self.播放时间 = int(self.end_time - self.start_time)
                if self.播放时间 >= 30 * 60:
                    break;
                print('已播放'+str(int(self.播放时间/60))+'分'+str(int(self.播放时间%60))+'秒')
                视频时间 = self.Get_time()
                if 视频时间[0] == 视频时间[1]:
                    self.Next()
                    break;

                now_time = 视频时间
                # time.sleep(10)
                self.Judget2()
        self.driver2.quit()

    #第一次登录
    def Denglu(self):
        self.driver1 = webdriver.Chrome(options=chrome_options, executable_path="chromedriver.exe")  # 启动浏览器
        self.driver1.get(url)
        self.driver1.execute_script('arguments[0].click();',self.driver1.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/ul/li[5]/span/a[1]'))
        self.driver1.implicitly_wait(3)
        self.driver1.execute_script('arguments[0].click();',self.driver1.find_element(By.XPATH,'/html/body/div[4]/a[1]'))

    #保存cookie
    def Save_cookie(self):
        self.driver1.implicitly_wait(5)
        self.driver1.execute_script('arguments[0].click();',self.driver1.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/ul/li[4]/a/span'))

        dictCookies = self.driver1.get_cookies()  # 获取list的cookies
        jsonCookies = json.dumps(dictCookies)  # 转换成字符串保存

        with open('cookies.txt', 'w') as f:
            f.write(jsonCookies)
        print('cookies保存成功！')
        self.driver1.quit()
    #传递cookie 自动登录
    def Send_cookie(self):
        self.driver2 = webdriver.Chrome(options=chrome_options, executable_path="chromedriver.exe")
        # self.driver2.maximize_window()
        self.driver2.set_window_position(y=0, x=1850)
        self.driver2.set_window_size(1900, 1080)

        self.driver2.get('https://www.zhihuishu.com/')
        self.driver2.implicitly_wait(5)
        self.driver2.execute_script('arguments[0].click();',self.driver2.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/ul/li[4]/a/span'))
        time.sleep(1)
        self.driver2.delete_all_cookies()
        with open('cookies.txt', 'r') as f:
            listCookies = json.load(f)
        for cookie in listCookies:
            if 'expiry' in cookie:
                del cookie['expiry']
            self.driver2.add_cookie(cookie)

        # for cookie in listCookies:
        #     print(cookie)
        #     cookie_dict = {
        #         'domain': '.zhihuishu.com',
        #         # 'expiry': cookie.get('expiry'),
        #         'name': cookie.get('name'),
        #         'value': cookie.get('value'),
        #         'path': '/',
        #
        #         'httpOnly': cookie.get('httpOnly'),
        #         'secure': False
        #     }
        #
        #     driver.add_cookie(cookie_dict)

        # 更新cookies后进入目标网页
        self.driver2.refresh()
        print('登陆成功')

    #进入课程
    def JingRu(self):
        try:
            self.driver2.implicitly_wait(5)
            self.driver2.execute_script('arguments[0].click();',self.driver2.find_element(By.XPATH,'/html/body/div[1]/section/div[2]/section[2]/section/div/div/div/div[2]/div[1]/div[2]/ul/div/dl/dt/div[1]/div[1]'))
        except:
            print('进入课程失败，正在重试...')
            self.JingRu()

    #判断学前须知
    def Judget1(self):
        try:
            我知道了 = self.driver2.find_element(By.XPATH,'/html/body/div[1]/div/div[6]/div/div[3]/span/button')
            # driver2.execute_script('arguments[0].click();',我知道了)
            # 我知道了.click()
            ActionChains(self.driver2).click(我知道了).perform()
            print('点击我知道了')
            # time.sleep(1.5)
            取消 = self.driver2.find_element(By.XPATH,'/html/body/div[1]/div/div[7]/div[2]/div[1]/i')
            self.driver2.execute_script('arguments[0].click();',取消)
            # ActionChains(self.driver2).click(取消).perform()
            # 取消.click()
            print('点击取消')
        except:
            print('错误,正在重试...')

    def Finish_pro(self):
        try:
            题目list = self.driver2.find_elements(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div[3]/ul/li')
            i = 0
            for 题目 in 题目list:
                i += 1
                time.sleep(1)
                self.driver2.execute_script('arguments[0].click();', 题目)
                time.sleep(1)
                print('第' + str(i) + '题完成')
                选项 = self.driver2.find_element(By.XPATH,
                                                 '/html/body/div[1]/div/div[7]/div/div[2]/div/div[1]/div/div/div[2]/ul/li[1]')
                # self.driver2.execute_script('arguments[0].click();',self.driver2.find_element(By.XPATH,'/html/body/div[1]/div/div[7]/div/div[2]/div/div[1]/div/div/div[2]/ul/li[1]'))
                ActionChains(self.driver2).click(选项).perform()
                time.sleep(1)

            time.sleep(1.5)
            # 使用js语法被检测
            关闭 = self.driver2.find_element(By.XPATH, '/html/body/div[1]/div/div[7]/div/div[3]/span/div')
            # self.driver2.find_element(By.XPATH, '/html/body/div[1]/div/div[7]/div/div[3]/span/div').click()
            ActionChains(self.driver2).click(关闭).perform()
        except:
            pass

    #播放
    def Bofang(self):
        try:
            time.sleep(1)
            self.视频 = self.driver2.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div/div[8]')
            ActionChains(self.driver2).move_to_element(self.视频).perform()
            # time.sleep(1)
            播放 = self.driver2.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div/div[10]/div[2]')
            ActionChains(self.driver2).click(self.视频).perform()
            # 播放.click()
            print('开始播放')
        except:
            print('播放失败，正在重试...')
            self.Bofang()


    #判断题目
    def Judget2(self):
        try:
            self.driver2.find_element(By.XPATH, '/html/body/div[1]/div/div[7]/div/div[3]/span/div').click()
            time.sleep(1)
            self.视频 = self.driver2.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div/div[8]')
            ActionChains(self.driver2).move_to_element(self.视频).perform()
            time.sleep(1)
            播放 = self.driver2.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div/div[10]/div[2]')
            播放.click()
            print('关闭题目开始播放')
        except:
            pass

    #获取视频时间
    def Get_time(self):
        time.sleep(1)
        视频当前时间 = self.driver2.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div/div[10]/div[4]/span[1]').get_attribute('textContent')
        视频结束时间 = self.driver2.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div/div[10]/div[4]/span[2]').get_attribute('textContent')
        print(视频当前时间)
        print(视频结束时间)
        return 视频当前时间,视频结束时间

    #切换下一集
    def Next(self):

        self.getXpth()
        ActionChains(self.driver2).click(self.driver2.find_element(By.XPATH,self.xpath)).perform()
        print('切换到下一集')

    # 获得能点击交互列表的标号  用来获得xpath地址
    def getlist(self):
        text = self.driver2.page_source
        self.number_list0 = re.findall('class="pl5  hour">(.*?)</b>',text)
        # print(number_list0)
        # 存放拥有三级列表的二级列表
        number_list1 = []
        for i in self.number_list0:
            if i.count('.') == 2:
                list0 = i.split('.')
                del list0[len(list0) - 1]
                str0 = '.'.join(list0)
                if str0 not in number_list1:
                    number_list1.append(str0)
        for j in number_list1:
            index0 = self.number_list0.index(j)
            del self.number_list0[index0]

        # print(self.number_list0)

    #获取当前视频序号
    def get_now_num(self):
        self.now_num = self.driver2.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[1]/div[1]/div[1]/span[2]').get_attribute('textContent')
        self.now_num = self.now_num.split('、')[0]
        # print(self.now_num)

    # 获得下一视频的xpath地址
    def getXpth(self):
        list0 = self.number_list0[self.当前下标+1].split('.')
        if self.number_list0[self.当前下标+1].count('.') == 2:

            self.xpath = '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[1]/div/ul[' + list0[0] + ']/div[' + list0[
                1] + ']/ul/li[' \
                    + list0[2] + ']/div '
        else:
            self.xpath = '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[1]/div/ul[' + list0[0] + ']/div[' + list0[
                1] + ']/li/div'
        # print(self.xpath)




if __name__ == '__main__':
    p0 = p()
    p0.start()

























