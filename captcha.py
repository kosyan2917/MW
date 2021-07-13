from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with open('token.txt') as f:
    token = f.read()

def kok(driver, startflag):
    flag = True
    while flag:
        windows = driver.window_handles
        print('перед циклом')
        for window in windows:
            driver.switch_to.window(window)
            element_err = driver.find_elements_by_xpath('//div[@id="cf-error-details"]')
            element = driver.find_elements_by_xpath('//*[@id="g-recaptcha-response"]')
            if element:
                break
            if element_err:
                driver.get("https://all-access.wax.io/cloud-wallet/signing/")
                time.sleep(2)
        print('После циклаЯ')
        for window in windows:
            driver.switch_to.window(window)
            element = driver.find_elements_by_xpath('//*[@id="g-recaptcha-response"]')
            if element:
                lol = driver.execute_script('''function findRecaptchaClients() {
                                                                      // eslint-disable-next-line camelcase
                                                                      if (typeof (___grecaptcha_cfg) !== 'undefined') {
                                                                        // eslint-disable-next-line camelcase, no-undef
                                                                        return Object.entries(___grecaptcha_cfg.clients).map(([cid, client]) => {
                                                                          const data = { id: cid, version: cid >= 10000 ? 'V3' : 'V2' };
                                                                          const objects = Object.entries(client).filter(([_, value]) => value && typeof value === 'object');

                                                                          objects.forEach(([toplevelKey, toplevel]) => {
                                                                            const found = Object.entries(toplevel).find(([_, value]) => (
                                                                              value && typeof value === 'object' && 'sitekey' in value && 'size' in value
                                                                            ));

                                                                            if (typeof toplevel === 'object' && toplevel instanceof HTMLElement && toplevel['tagName'] === 'DIV'){
                                                                                data.pageurl = toplevel.baseURI;
                                                                            }

                                                                            if (found) {
                                                                              const [sublevelKey, sublevel] = found;

                                                                              data.sitekey = sublevel.sitekey;
                                                                              const callbackKey = data.version === 'V2' ? 'callback' : 'promise-callback';
                                                                              const callback = sublevel[callbackKey];
                                                                              if (!callback) {
                                                                                data.callback = null;
                                                                                data.function = null;
                                                                              } else {
                                                                                data.function = callback;
                                                                                const keys = [cid, toplevelKey, sublevelKey, callbackKey].map((key) => `['${key}']`).join('');
                                                                                data.callback = `___grecaptcha_cfg.clients${keys}`;
                                                                                //return(data.callback)
                                                                              }
                                                                            }
                                                                          });
                                                                          return data.callback;
                                                                        });
                                                                      }
                                                                      return [];
                                                                    }
                                                                    return (findRecaptchaClients())''')[0]
                while not lol:
                    #print('не нашел функцию капчи...')
                    lol = driver.execute_script('''function findRecaptchaClients() {
                                                                          // eslint-disable-next-line camelcase
                                                                          if (typeof (___grecaptcha_cfg) !== 'undefined') {
                                                                            // eslint-disable-next-line camelcase, no-undef
                                                                            return Object.entries(___grecaptcha_cfg.clients).map(([cid, client]) => {
                                                                              const data = { id: cid, version: cid >= 10000 ? 'V3' : 'V2' };
                                                                              const objects = Object.entries(client).filter(([_, value]) => value && typeof value === 'object');

                                                                              objects.forEach(([toplevelKey, toplevel]) => {
                                                                                const found = Object.entries(toplevel).find(([_, value]) => (
                                                                                  value && typeof value === 'object' && 'sitekey' in value && 'size' in value
                                                                                ));

                                                                                if (typeof toplevel === 'object' && toplevel instanceof HTMLElement && toplevel['tagName'] === 'DIV'){
                                                                                    data.pageurl = toplevel.baseURI;
                                                                                }

                                                                                if (found) {
                                                                                  const [sublevelKey, sublevel] = found;

                                                                                  data.sitekey = sublevel.sitekey;
                                                                                  const callbackKey = data.version === 'V2' ? 'callback' : 'promise-callback';
                                                                                  const callback = sublevel[callbackKey];
                                                                                  if (!callback) {
                                                                                    data.callback = null;
                                                                                    data.function = null;
                                                                                  } else {
                                                                                    data.function = callback;
                                                                                    const keys = [cid, toplevelKey, sublevelKey, callbackKey].map((key) => `['${key}']`).join('');
                                                                                    data.callback = `___grecaptcha_cfg.clients${keys}`;
                                                                                    //return(data.callback)
                                                                                  }
                                                                                }
                                                                              });
                                                                              return data.callback;
                                                                            });
                                                                          }
                                                                          return [];
                                                                        }
                                                                        return (findRecaptchaClients())''')[0]

                #print(driver.current_url)
                kekw = getKey(driver.current_url)
                while kekw == 0:
                    kekw = getKey(driver.current_url)
                    #raise Exception('3228')
                print(lol)
                lol = lol + "('"+kekw+"');"
                driver.execute_script(lol)
                if not startflag:
                    element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='button button-secondary button-large text-1-5rem text-bold mx-1']")))
                    element.click()

                flag = False

                break
            time.sleep(0.5)



def getKey(url):

    from selenium.webdriver.support.wait import WebDriverWait

    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(token)
    solver.set_website_url(url)
    solver.set_website_key("6LdaB7UUAAAAAD2w3lLYRQJqsoup5BsYXI2ZIpFF")
    # set optional custom parameter which Google made for their search page Recaptcha v2
    # solver.set_data_s('"data-s" token from Google Search results "protection"')
    g_response = solver.solve_and_return_solution()
    if g_response != 0:
        #print("g-response: " + g_response)
        return g_response
    else:
        #print("task finished with error " + solver.error_code)
        return 0