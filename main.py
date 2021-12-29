import threading
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
import captcha
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import undetected_chromedriver as uc
import queue
from MailParser import MailParser

class GamerBot:

    def __init__(self, options, acc_name, login, password):
        self.forbidden = ['skunk']
        self.unit_dictionary = ['/_nuxt/img/wolf.de9bc8b.png', '/_nuxt/img/ant.5cc4b20.png',
                                '/_nuxt/img/skunk.b941207.png', '/_nuxt/img/raccoon.72fae59.png',
                                '/_nuxt/img/elephantor.94bc483.png', '/_nuxt/img/hamster.9100eb1.png']
        self.options = options
        self.driver = uc.Chrome(chrome_options=options, executable_path='C:\\Users\\Nik\\MW\\chromedriver.exe')
        self.actions = ActionChains(self.driver)
        self.mainWindowHandle = ''
        self.acc_name = acc_name
        self.password = password
        self.login = login
        self.actions = ActionChains(self.driver)
        self.stop = False
        self.mwm = 0
        self.units = {}
        self.parser = MailParser()
        self.startgame()
        

    def startgame(self):
        self.driver.get("https://game2.metal-war.com/")
        # while True:
        #     try:
        #         element = self.driver.find_element_by_xpath("//button[@id='ual-button']")
        #     except Exception:
        #         pass
        #     else:
        #         break
        element = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH,
                                                                                             '//button[@id=\'ual-button\']')))
        time.sleep(2)
        element.click()
        time.sleep(2)
        element = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH,
                                                                                   '(//div[@class=\'ual-auth-button  \'])[2]')))
        element.click()
        self.mainWindowHandle = self.driver.current_window_handle
        flag = True
        while flag:
            try:
                windows = self.driver.window_handles
                for window in windows:
                    self.driver.switch_to.window(window)
                    element_err = self.driver.find_elements_by_xpath('//div[@id="cf-error-details"]')
                    element = self.driver.find_elements_by_xpath('//*[@name="userName"]')
                    if element:
                        flag = False
                        break
                    if element_err:
                        self.driver.switch_to.window(window)
                        self.driver.get("https://all-access.wax.io/cloud-wallet/login/")
                        time.sleep(2)
                        flag = False
                        break

                    time.sleep(0.5)
            except:
                pass
        flag = True
        
        while flag:
            try:
                windows = self.driver.window_handles
                for window in windows:
                    self.driver.switch_to.window(window)
                    element = self.driver.find_elements_by_xpath('//*[@name="userName"]')
                    if element:
                        element[0].click()
                        element[0].clear()
                        element[0].send_keys(self.login)
                        element2 = self.driver.find_elements_by_xpath('//*[@name="password"]')
                        element2[0].click()
                        element2[0].clear()
                        element2[0].send_keys(self.password)
                        print('Вызвал капчу')
                        #captcha.kok(self.driver, True)
                        print('Капча кончилась')
                        time.sleep(0.5)
                        element = self.driver.find_elements_by_xpath('//button[text()="Login"]')
                        element[0].click()
                        flag = False
                        self.driver.switch_to_window(self.mainWindowHandle)
                        break
                    time.sleep(0.5)
            except:
                pass
        flag = True
        time.sleep(5)
        if len(self.driver.window_handles)!=1:
            while flag:
                try:
                    windows = self.driver.window_handles
                    for window in windows:
                        self.driver.switch_to.window(window)
                        element = self.driver.find_elements_by_xpath('//input')
                        if element:
                            element[0].click()
                            element[0].clear()
                            element[0].send_keys(self.parser.get_email_code())
                            element[0].send_keys(u'\ue007')
                            time.sleep(0.5)
                            flag = False
                            self.driver.switch_to_window(self.mainWindowHandle)
                            break
                except Exception:
                    pass
        element = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH,
                                                                                       '//div[@class=\'repair info_button\']')))
        time.sleep(2)
        element.click()
        
        element = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH,
                                                                                       '//div[@class=\'tabs\']')))
        tabs = element.find_elements_by_xpath(".//div")
        print(tabs)
        for tab in tabs:
            print(tab.text)
        tabs[4].click()
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH,
                                                                             '//input')))
        checkboxes = self.driver.find_elements_by_xpath('//input')
        checkboxes[1].click()
        checkboxes[2].click()
        tabs[1].click()
        
        x = threading.Thread(target=self.captcha_thread)
        while True:
                self.units = self.get_units()
            #print(self.units)
            #try:
                repair = []
                raid = []
                for unit in self.units:
                    # if self.units[unit][2] == '250/250':
                    #   continue
                    if self.units[unit]['raid'].find_element_by_xpath('.//*').text == 'MINE' or self.units[unit]['raid'].find_element_by_xpath('.//*').text == 'RAID':
                        raid.append(unit)
                    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[@class=\'units_line\']')))
                    if self.units[unit]['hp'] == 0:
                        repair.append(unit)
                for unit in repair:
                    if self.mwm <= self.units[unit]['cost']:
                        continue
                    self.driver.execute_script("arguments[0].scrollIntoView();", unit)
                    if not self.units[unit]['token'][0].find_element_by_xpath('.//input').is_selected() and not self.units[unit]['pioneer'][0].find_element_by_xpath('.//input').is_selected():
                        if self.units[unit]['token'][1] != 0:
                            self.units[unit]['token'][0].click()
                        else:
                            self.units[unit]['pioneer'][0].click()
                    (self.units[unit]['repair']).click()
                    time.sleep(3)
                for unit in raid:
                    if unit in repair:
                        continue
                    self.driver.execute_script("arguments[0].scrollIntoView();", unit)
                    self.units[unit]['raid'].click()
                    time.sleep(8)
                time.sleep(20)
            #except Exception as err:
             #   print(err)

    def get_units(self):
        self.mwm = int(self.driver.find_element_by_xpath('.//div[@class=\'shards_count\']').text.split()[0])
        units = {}
        #elements = self.driver.find_element_by_xpath('//div[@class=\'units_container\']')
        elements = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH,
                                                                                        '//div[@class=\'units_container\']')))
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[@class=\'units_line\']')))
        elements = elements.find_elements_by_xpath('//div[@class=\'units_line\']')
        for element in elements:
            try:
                unit_type = element.find_element_by_xpath('.//img').get_attribute('src')
                hp = element.find_element_by_xpath('.//div[@class=\'hp_text\']').text
                button_repair = element.find_element_by_xpath('.//div[@class=\'button raid\']')
                button_mine = element.find_element_by_xpath('(.//div[@class=\'units_action\'])[2]') \
                    .find_element_by_xpath('.//div[@class=\'button mine\']| .//div[@class=\'button raid\']')
                switches = element.find_elements_by_xpath('.//label')
            except Exception:
                continue
            if hp == '':
                continue
            units[element] = {'repair': button_repair, 'raid': button_mine, 'hp': int(hp.split('/')[0]),
                              'cost': int(hp.split('/')[1])/2, 'name': unit_type, 'pioneer': [switches[2], int(switches[2].text)],
                              'token': [switches[3], int(switches[3].text)]}
        return units

    def captcha_thread(self):
        while True:
            windows = self.driver.window_handles
            print(windows)
            if len(windows) > 1:
                try:
                    captcha.kok(self.driver, False)
                except:
                    self.driver.close()
                time.sleep(2)
                self.driver.switch_to.window(self.mainWindowHandle)
                time.sleep(7)
            time.sleep(4)

if __name__ == "__main__":
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--window-size=1600,900")
    #        chromeProfile = userdata
    #       options.add_argument(f"--user-data-dir={chromeProfile}")
    # options.add_argument("--profile-directory=Profile 1")

    except:
        pass
    # print()
    with open('auth.txt', 'r' ) as f:
        login = f.readline()
        pw = f.readline()
    bot = GamerBot(options, 'chromedriver.exe', login, pw)
