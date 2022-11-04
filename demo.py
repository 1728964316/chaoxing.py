import json
import re
import sys
import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from myui import Ui_Form

url = 'https://www.zhihuishu.com/'


# 扫码登录
class Mythread1(QThread):
    # mythread1_signal1 = pyqtSignal(str)
    def __init__(self):
        super(Mythread1, self).__init__()
        self.driver = None

    def run(self):
        chrome_options = Options()
        chrome_options.add_argument("--mute-audio")  # 静音
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        self.driver = webdriver.Chrome(options=chrome_options, executable_path="chromedriver.exe")  # 启动浏览器
        self.driver.set_window_size(width=500, height=1000)
        self.driver.set_window_position(x=0, y=0)
        self.driver.get(url)
        self.driver.execute_script('arguments[0].click();', self.driver.find_element(By.XPATH,
                                                                                     '/html/body/div[1]/div/div[1]/div/ul/li[5]/span/a[1]'))
        self.driver.implicitly_wait(3)
        self.driver.execute_script('arguments[0].click();',
                                   self.driver.find_element(By.XPATH, '/html/body/div[4]/a[1]'))


# 保存cookie
class Mythread2(QThread):
    mythread2_signal1 = pyqtSignal(str)

    def __init__(self):
        super(Mythread2, self).__init__()

    def Save_cookie(self):
        self.driver = self.data
        self.driver.implicitly_wait(5)
        self.driver.execute_script('arguments[0].click();', self.driver.find_element(By.XPATH,
                                                                                     '/html/body/div[1]/div/div[1]/div/ul/li[4]/a/span'))
        dictCookies = self.driver.get_cookies()  # 获取list的cookies
        jsonCookies = json.dumps(dictCookies)  # 转换成字符串保存
        with open('cookies.txt', 'w') as f:
            f.write(jsonCookies)
        self.mythread2_signal1.emit('cookies保存成功！')
        # print('cookies保存成功！')
        self.driver.quit()

    def run(self):
        self.Save_cookie()


class Mythread3(QThread):
    mythread3_signal1 = pyqtSignal(str)
    mythread3_signal2 = pyqtSignal(str)
    mythread3_signal3 = pyqtSignal(str)
    mythread3_signal4 = pyqtSignal(str)
    mythread3_signal5 = pyqtSignal(int)
    mythread3_signal6 = pyqtSignal(str)
    mythread3_signal7 = pyqtSignal(str)

    def __init__(self):
        super(Mythread3, self).__init__()

    def pre(self):
        chrome_options = Options()
        chrome_options.add_argument("--mute-audio")  # 静音
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        self.driver = webdriver.Chrome(options=chrome_options, executable_path="chromedriver.exe")  # 启动浏览器
        self.driver.set_window_position(x=1850, y=0)
        self.driver.set_window_size(height=1000, width=1000)

    def Send_cookie(self):
        self.driver.get(url)
        self.driver.implicitly_wait(5)
        self.driver.execute_script('arguments[0].click();', self.driver.find_element(By.XPATH,
                                                                                     '/html/body/div[1]/div/div[1]/div/ul/li[4]/a/span'))
        time.sleep(1)
        self.driver.delete_all_cookies()
        with open('cookies.txt', 'r') as f:
            listCookies = json.load(f)
        for cookie in listCookies:
            if 'expiry' in cookie:
                del cookie['expiry']
            self.driver.add_cookie(cookie)
        self.driver.refresh()
        self.mythread3_signal1.emit('登录成功')

    # 进入课程
    def JingRu(self):
        try:
            self.driver.implicitly_wait(5)
            self.driver.execute_script('arguments[0].click();', self.driver.find_element(By.XPATH,
                                                                                         '/html/body/div[1]/section/div[2]/section[2]/section/div/div/div/div[2]/div[1]/div[2]/ul/div/dl/dt/div[1]/div[1]'))
        except:
            # print('进入课程失败，正在重试...')
            self.mythread3_signal1.emit('进入课程失败，正在重试...')
            self.JingRu()

    # 判断学前须知
    def Judget1(self):
        try:
            我知道了 = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[6]/div/div[3]/span/button')
            # driver2.execute_script('arguments[0].click();',我知道了)
            # 我知道了.click()
            ActionChains(self.driver).click(我知道了).perform()
            # print('点击我知道了')
            self.mythread3_signal1.emit('点击我知道了')
            # time.sleep(1.5)
            取消 = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[7]/div[2]/div[1]/i')
            self.driver.execute_script('arguments[0].click();', 取消)
            # ActionChains(self.driver2).click(取消).perform()
            # 取消.click()
            # print('点击取消')
            self.mythread3_signal1.emit('点击取消')
        except:
            # print('错误,正在重试...')
            self.mythread3_signal1.emit('发现错误,正在重试...')

    def Finish_pro(self):
        try:
            题目list = self.driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div[3]/ul/li')
            i = 0
            for 题目 in 题目list:
                i += 1
                time.sleep(1)
                self.driver.execute_script('arguments[0].click();', 题目)
                time.sleep(1)
                self.mythread3_signal1.emit('第' + str(i) + '题完成')
                # print('第' + str(i) + '题完成')
                选项 = self.driver.find_element(By.XPATH,
                                                '/html/body/div[1]/div/div[7]/div/div[2]/div/div[1]/div/div/div[2]/ul/li[1]')
                # self.driver2.execute_script('arguments[0].click();',self.driver2.find_element(By.XPATH,'/html/body/div[1]/div/div[7]/div/div[2]/div/div[1]/div/div/div[2]/ul/li[1]'))
                ActionChains(self.driver).click(选项).perform()
                time.sleep(1)

            time.sleep(1.5)
            # 使用js语法被检测
            关闭 = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[7]/div/div[3]/span/div')
            # self.driver2.find_element(By.XPATH, '/html/body/div[1]/div/div[7]/div/div[3]/span/div').click()
            ActionChains(self.driver).click(关闭).perform()
        except:
            pass

    # 播放
    def Bofang(self):
        try:
            time.sleep(1)
            self.视频 = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div/div[8]')
            ActionChains(self.driver).move_to_element(self.视频).perform()
            # time.sleep(1)
            播放 = self.driver.find_element(By.XPATH,
                                            '/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div/div[10]/div[2]')
            ActionChains(self.driver).click(self.视频).perform()
            # 播放.click()
            self.mythread3_signal1.emit('开始播放')
            # print('开始播放')
        except:
            # print('播放失败，正在重试...')
            self.mythread3_signal1.emit('播放失败，正在重试...')
            self.Bofang()

    # 判断题目
    def Judget2(self):
        try:
            选项 = self.driver.find_element(By.XPATH,
                                            '/html/body/div[1]/div/div[7]/div/div[2]/div/div[1]/div/div/div[2]/ul/li[1]')
            # self.driver2.execute_script('arguments[0].click();',self.driver2.find_element(By.XPATH,'/html/body/div[1]/div/div[7]/div/div[2]/div/div[1]/div/div/div[2]/ul/li[1]'))
            ActionChains(self.driver).click(选项).perform()
            time.sleep(2)
            关闭 = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[7]/div/div[3]/span/div')
            # self.driver2.find_element(By.XPATH, '/html/body/div[1]/div/div[7]/div/div[3]/span/div').click()
            ActionChains(self.driver).click(关闭).perform()
            # print('关闭题目开始播放')
            self.mythread3_signal1.emit('关闭题目开始播放')
        except:
            pass

        try:
            关闭 = self.driver.find_element(By.XPATH,'/html/body/div[5]/div/div[1]/button/i')
            ActionChains(self.driver).click(关闭).perform()
            time.sleep(2)
            self.Judget2()
        except:
            pass

    def Judegt3(self):
        try:
            # /html/body/div[1]/div/div[8]/div/div[1]/button
            取消 = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[8]/div/div[1]/button/i')
            self.driver.execute_script('arguments[0].click();', 取消)
        except:
            pass

    # 判断播放状态
    def Judegt4(self):
        try:
            play_class = self.driver.find_element(By.XPATH,
                                                  '/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div/div[10]/div[2]').get_attribute(
                'class')
            if play_class == 'playButton':
                self.mythread3_signal7.emit('当前状态：暂停中')
                self.Bofang()
                self.mythread3_signal1.emit('当前暂停，正在开始播放')
            else:
                self.mythread3_signal7.emit('当前状态：播放中')
                pass
        except:
            self.Judegt4()

    # 获取视频时间
    def Get_time(self):
        time.sleep(1)
        视频当前时间 = self.driver.find_element(By.XPATH,
                                                '/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div/div[10]/div[4]/span[1]').get_attribute(
            'textContent')
        视频结束时间 = self.driver.find_element(By.XPATH,
                                                '/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div/div[10]/div[4]/span[2]').get_attribute(
            'textContent')
        self.mythread3_signal2.emit(视频当前时间 + '\n' + 视频结束时间)
        self.a = 视频当前时间
        self.b = 视频结束时间
        self.a = self.a.split(':')
        self.b = self.b.split(':')
        # print(self.a)
        # print(self.b)
        num = (int(self.a[1]) * 60 + int(self.a[2])) / (int(self.b[1]) * 60 + int(self.b[2]))
        num1 = (int(self.b[1]) * 60 + int(self.b[2]))-(int(self.a[1]) * 60 + int(self.a[2]))
        # print(num)
        # print(int(self.b[1]) * 60 + int(self.b[2]))
        # print(int(self.a[1]) * 60 + int(self.a[2]))
        self.mythread3_signal5.emit(int(num * 100))
        return num1

    # 切换下一集
    def Next(self):
        try:
            self.Judegt3()
            self.getXpth()
            ActionChains(self.driver).click(self.driver.find_element(By.XPATH, self.xpath)).perform()
            # print('切换到下一集')
            self.mythread3_signal2.emit('切换到下一集')
        except:
            self.Next()


    # 获得能点击交互列表的标号  用来获得xpath地址
    def getlist(self):
        text = self.driver.page_source
        self.number_list0 = re.findall('class="pl5  hour">(.*?)</b>', text)
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

    # 获取当前视频序号
    def get_now_num(self):
        try:
            self.now_num = self.driver.find_element(By.XPATH,
                                                    '/html/body/div[1]/div/div[2]/div[1]/div[1]/div[1]/span[2]').get_attribute(
                'textContent')
            self.now_num = self.now_num.split('、')[0]
        except:
            pass
        # print(self.now_num)

    # 获得下一视频的xpath地址
    def getXpth(self):
        list0 = self.number_list0[self.当前下标 + 1].split('.')
        if self.number_list0[self.当前下标 + 1].count('.') == 2:

            self.xpath = '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[1]/div/ul[' + list0[0] + ']/div[' + list0[
                1] + ']/ul/li[' \
                         + list0[2] + ']/div '
        else:
            self.xpath = '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[1]/div/ul[' + list0[0] + ']/div[' + list0[
                1] + ']/li/div'

    def run(self):
        self.pre()
        self.Send_cookie()
        self.JingRu()
        self.Judget1()
        self.getlist()
        time.sleep(1)
        self.start_time = time.time()
        self.end_time = 0
        self.播放时间 = 0
        self.播放时间 = 0
        while True:
            if self.播放时间 >= 30 * 60:
                # print('到达规定时间')
                self.mythread3_signal1.emit('到达规定时间')
                break
            self.Bofang()
            while True:
                self.get_now_num()
                self.当前下标 = self.number_list0.index(self.now_num)
                self.mythread3_signal3.emit(self.number_list0[self.当前下标])
                self.Judegt3()
                self.end_time = time.time()
                self.播放时间 = int(self.end_time - self.start_time)
                if self.播放时间 >= 30 * 60:
                    break
                # print('已播放'+str(int(self.播放时间/60))+'分'+str(int(self.播放时间%60))+'秒')
                self.mythread3_signal4.emit(str(int(self.播放时间 / 60)) + ':' + str(int(self.播放时间 % 60)))
                num1 = self.Get_time()
                # print(num1)
                if num1<35:
                    self.Next()
                    break
                # time.sleep(10)
                else:
                    self.Judget2()
                    self.Judegt4()
        self.driver.quit()
        self.mythread3_signal6.emit('今天已播放完成')


class Mywindow(QWidget, Ui_Form):
    def __init__(self):
        super(Mywindow, self).__init__()
        self.setupUi(self)
        self.display()
        self.Connected()

    def display(self):
        self.mythread1 = Mythread1()
        self.mythread2 = Mythread2()
        self.mythread3 = Mythread3()
        self.pushButton.clicked.connect(self.FirstDenglu)
        self.pushButton_2.clicked.connect(self.Save_cookie)
        self.pushButton_3.clicked.connect(self.Start_work)
        self.pushButton_4.clicked.connect(self.Close_bro)

    def Connected(self):
        self.mythread2.mythread2_signal1.connect(self.Input1)

        self.mythread3.mythread3_signal1.connect(self.Input2)
        self.mythread3.mythread3_signal2.connect(self.Input3)
        self.mythread3.mythread3_signal3.connect(self.Input4)
        self.mythread3.mythread3_signal4.connect(self.Input5)
        self.mythread3.mythread3_signal5.connect(self.Input6)
        self.mythread3.mythread3_signal6.connect(self.Input7)
        self.mythread3.mythread3_signal7.connect(self.Input8)

    def FirstDenglu(self):
        self.mythread1.start()

    def Save_cookie(self):
        self.mythread2.data = self.mythread1.driver
        self.mythread2.start()

    def Start_work(self):
        self.mythread3.start()

    def Close_bro(self):
        try:
            self.mythread3.driver.quit()
        # self.mythread3.quit()
        except Exception as e:
            try:
                # self.mythread1.driver.quit()
                self.mythread1.quit()
            except:
                pass
        else:
            self.textBrowser.setText('已关闭')

    # 保存成功
    def Input1(self, str):
        # self.mythread1.quit()
        # print('...')
        # self.mythread2.quit()
        self.textBrowser.append(str)

    def Input2(self, str):
        self.textBrowser.append(str)

    def Input3(self, str):
        self.textBrowser_2.setText(str)

    def Input4(self, str):
        self.textBrowser_3.setText(str)

    def Input5(self, str):
        self.lcdNumber.display(str)

    def Input6(self, int):
        self.progressBar.setValue(int)
        # print(int)

    def Input7(self, str):
        QMessageBox.information(self, "提示", str)

    def Input8(self, str):
        self.textBrowser_4.setText(str)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = Mywindow()
    mywindow.show()
    sys.exit(app.exec_())
