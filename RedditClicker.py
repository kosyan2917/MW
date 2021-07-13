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


class GamerBot:
    
    def __init__(self, options, acc_name, login, password, window, queue):
        self.options = options
        self.driver = uc.Chrome(chrome_options=options)
        self.actions = ActionChains(self.driver)
        self.finder = CheckImage()
        self.mainWindowHandle = ''
        self.acc_name = acc_name
        self.password = password
        self.login = login
        self.window = window
        self.queue = queue
        self.stop = False

        self.startgame()
    
    def startgame(self):


        self.driver.get("https://aliens.artsy.nz/")
        element = self.driver.find_element_by_xpath("//button[@id='login']")
        time.sleep(2)
        element.click()
        time.sleep(2)
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
                        #


                        element[0].click()
                        element[0].clear()
                        element[0].send_keys(self.login)
                        element2 = self.driver.find_elements_by_xpath('//*[@name="password"]')
                        element2[0].click()
                        element2[0].clear()
                        element2[0].send_keys(self.password)
                        captcha.kok(self.driver, True, self.window, 'output_' + self.acc_name)
                        time.sleep(0.5)
                        element = self.driver.find_elements_by_xpath('//button[text()="Login"]')
                        element[0].click()
                        #
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
                    element = self.driver.find_elements_by_xpath('//*[text()="Approve"]')
                    if element:
                        self.driver.switch_to.window(window)
                        element[0].click()
                        time.sleep(2)
                        flag = False
                        break
                    time.sleep(0.5)
            except:
                pass

        self.driver.switch_to.window(self.mainWindowHandle)
        self.window['output_' + self.acc_name].update('Press Go to start farming')
        self.window['go_' + self.acc_name].update(disabled=False)
        speed = self.queue.get()
        self.window['go_' + self.acc_name].update(disabled=True)
        self.window['stop_' + self.acc_name].update(disabled=False)
        self.window['output_' + self.acc_name].update('Processing')
        threading.Thread(target=self.kill_thread).start()

        time.sleep(1)
        self.driver.execute_script('''document.querySelector("p").remove()

let div = document.createElement("div");
  div.className = "percdiv"
  div.innerHTML = '<div data-percent="9" class="ui progress blue"><div class="bar" style="width: 100%; transition-duration: 300ms;"><div class="progress"> <div class="content">loading...%</div> </div></div><div class="perclabel">CPU used - loading</div></div>';

  document.querySelector('p').before(div);

let myElements = document.querySelectorAll(".ui.progress.blue");

for (let i = 0; i < myElements.length; i++) {
    myElements[i].style.color= "black";
    //myElements[i].style.line-height= "1.4285em";
    myElements[i].style.display= "block";
    
    myElements[i].style.border= "none";
    myElements[i].style.padding= 0;
    myElements[i].style.color= "0 0 1.5em";
    myElements[i].style.background= "rgba(0,0,0,.35)";
    myElements[i].style.fontFamily= 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Ubuntu, "Helvetica Neue", sans-serif';
    myElements[i].style.fontWeight = 'bold'
    myElements[i].style.width = 'auto'
    myElements[i].style.right= '0.5em';

  
}

myElements = document.querySelectorAll(".bar");

for (let i = 0; i < myElements.length; i++) {
    myElements[i].style.backgroundColor = "#2185d0";
    myElements[i].style.borderRadius = "0.3047619rem";
    myElements[i].style.transitionDuration= '300ms';
    myElements[i].style.maxWidth= '340px';
}

myElements = document.querySelectorAll(".progress");

for (let i = 0; i < myElements.length; i++) {
     myElements[i].style.textAlign= "right";
     myElements[i].style.fontSize = "20px";

}

myElements = document.querySelectorAll(".percdiv");

for (let i = 0; i < myElements.length; i++) {
    myElements[i].style.width= "340px";
    myElements[i].style.marginTop= "10px";
    myElements[i].style.marginBottom= "30px";
}

myElements = document.querySelectorAll(".content");

for (let i = 0; i < myElements.length; i++) {
    myElements[i].style.marginRight= "7px";
}

myElements = document.querySelectorAll(".perclabel");

for (let i = 0; i < myElements.length; i++) {
    myElements[i].style.textAlign = "center";
    myElements[i].style.marginTop = "0.2em";
    myElements[i].style.right = "auto";
    myElements[i].style.left = "0%";
    myElements[i].style.color = "rgba(255, 255, 255, 0.9)";
    myElements[i].style.fontSize = "15px";
    myElements[i].style.position = "absolute";
    myElements[i].style.textAlign = "center";
    myElements[i].style.width = "340px"; 
}''')
        x = threading.Thread(target=self.captcha_thread)
        x.start()
        self.main_cycle()
    
    def main_cycle(self):
        # main
        while True:
            if self.stop:
                exit()
            try:

                if self.get_cpu():
                    try:
                        time_mas = self.driver.find_element_by_xpath('//span[@id=\'countdown\']').text.split(':')
                        time_to_sleep = int(time_mas[0]) * 360 + int(time_mas[1]) * 60 + int(time_mas[2])
                        end_time = time.time() + time_to_sleep
                        while time.time() < end_time:
                            if self.stop:
                                exit()
                            self.window['output_' + self.acc_name].update('cooldown - {}:{}'.format(int((end_time - time.time())//60), int((end_time - time.time())%60)))
                            time.sleep(1)
                        #time.sleep(time_to_sleep)
                        try:
                            element = self.driver.find_element_by_xpath('//button[@id=\'mine\']')
                            time.sleep(1)
                            element.click()
                            WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH,
                                                                                             '//button[@id=\'claim\']')))
                            time.sleep(3)
                        except Exception as Err:
                            pass
                            #print(f'Ошибка {Err}')
                    except:
                        pass
                    try:
                        if self.driver.find_element_by_xpath('//button[@id=\'claim\']').is_enabled():
                            try:
                                element = self.driver.find_element_by_xpath('//button[@id=\'claim\']')
                                time.sleep(1)
                                element.click()
                            except Exception as Err:
                                pass
                                # print(f'Ошибка {Err}')
                        else:
                            try:
                                element = self.driver.find_element_by_xpath('//button[@id=\'mine\']')
                                time.sleep(1)
                                element.click()
                            except Exception as Err:
                                pass
                                # print(f'Ошибка {Err}')
                    except Exception as Err:
                        pass
                        # print(f'Ошибка {Err}')
                else:
                    self.window['output_' + self.acc_name].update('Кажется кончилось цпу')
                    #print('Кажется кончилось цпу')
                    time.sleep(5)
            except Exception as Err:
                pass
                # print(f'Ошибка {Err}')
            time.sleep(5)
    
    def captcha_thread(self):
        while True:
            if self.stop:
                exit()
            windows = self.driver.window_handles
            if len(windows) > 1:
                try:
                    captcha.kok(self.driver, False, self.window, 'output_' + self.acc_name)
                except:
                    self.driver.close()
                time.sleep(2)
                self.driver.switch_to.window(self.mainWindowHandle)
                time.sleep(7)
            time.sleep(4)

    def kill_thread(self):
        while True:
            message = self.queue.get()
            print(message)
            if message == 'stop':
                self.stop = True
                print(self.stop)
                self.driver.quit();
                exit()

    
    def wait_for_find_button(self, button):
        while True:
            #print('ищу кнопку')
            # self.driver.save_screenshot(self.buttons[button])
            screenshot = self.driver.get_screenshot_as_png()
            cords = self.find_button(button, screenshot)
            if cords:
                return cords
            time.sleep(1)
    
    def click(self, cor1, cor2):
        # self.actions.move_by_offset(cor1, cor2).click().perform()
        # kekw = "document.elementFromPoint("+ str(cor1) +"," +  str(cor2) + ").click();"
        # self.driver.execute_script(kekw)
        self.actions.move_to_element_with_offset(self.driver.find_element_by_tag_name('html'), cor1,
                                                 cor2).click().perform()
        # self.actions.move_to_element(self.driver.find_element_by_tag_name('html')).move_by_offset(cor1, cor2).click().perform()
    
    def find_any_button(self):
        # self.driver.save_screenshot("screen.png")
        screenshot = self.driver.get_screenshot_as_png()
        for key in self.mainbuttons:
            cords = self.find_button(key, screenshot)
            if cords:
                return cords
        return ()
    
    def find_button(self, button, screenshot):
        self.finder.upload_image(screenshot)
        return self.finder.find_image(button)
    
    def get_cpu(self):
        response = requests.post('https://wax.cryptolions.io/v1/chain/get_account',
                                 data='{{"account_name": "{0}"}}'.format(self.acc_name))
        response = response.json()
        cpu_used = round(response['cpu_limit']['used']/1000, 2)
        cpu_max = round(response['cpu_limit']['max']/1000, 2)
        percentage = round(cpu_used / cpu_max * 100)
        self.driver.execute_script('document.querySelector(".bar").style.width = "{}%";'.format(percentage))
        self.driver.execute_script('document.querySelector(".content").innerHTML = "{}%";'.format(percentage))
        self.driver.execute_script('document.querySelector(".perclabel").innerHTML = "CPU used - {} ms / {} ms";'.format(cpu_used,cpu_max))

        if response["cpu_limit"]["available"] >= 2200:
            return True
        else:
            return False


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
    #print()
    bot = GamerBot(options, './chromedriver.exe')
    bot.startgame()
