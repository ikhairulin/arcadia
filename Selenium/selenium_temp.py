from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pickle


user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
    'Chrome/101.0.4951.41'
]

# options
options = webdriver.ChromeOptions()
# options.add_argument(f'user-agent={random.choice(user_agent_list)}')
options.add_argument(f'user-agent={user_agent_list[0]}')


# disable webdrivermode
options.add_argument('--disable-blink-features=AutomationControlled')

# # работа в фоне
# options.add_argument('--headless')


url = 'https://www.deviantart.com/search/deviations?q=gb62da&page=1'
url_login = 'https://www.deviantart.com/users/login'
driver = webdriver.Chrome(
    executable_path=r'D:\OneDrive\Synh\Code\Python\My_projects\arcadia\Selenium\chromedriver.exe',
    options=options
    )

# auth block
username = 'Zebul'
password = 'sNn@jNQ7Mc4cb7L'

try:

    # авторизуемся и получаем куки

    driver.get(url_login)
    time.sleep(5)

    print('Проходим идентификацию...')
    email_input = driver.find_element_by_id('username')
    email_input.clear()
    email_input.send_keys(username)

    pass_input = driver.find_element_by_id('password')
    pass_input.clear()
    pass_input.send_keys(password)
    time.sleep(3)

    pass_input.send_keys(Keys.ENTER)

    # login_button = driver.find_element_by_id('loginbutton').click()
    time.sleep(5)

    # cookies
    pickle.dump(driver.get_cookies(),open(f"{username}_cookies", "wb"))
    time.sleep(3)


    # заходим с уже заготовленными куками

    # driver.get(url)
    # driver.get('https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html')
    # time.sleep(5)

    # for cookie in pickle.load(open(f'{username}_cookies', "rb")):
    #     driver.add_cookie(cookie)

    # time.sleep(5)
    # driver.refresh()
    # time.sleep(10)





except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()


# Список опций Chromium
# https://peter.sh/experiments/chromium-command-line-switches/




    # items = driver.find_elements_by_xpath('//a[@data-hook="deviation_link"]')
    # img_pages = []
    # for item in items:
    #     img_pages.append(item.get_attribute('href'))
    # print(f'Количество элементов в списке {len(img_pages)}')
    # img_pages_set = set(img_pages)
    #     # print(f"Ты ищешь страницу {item.get_attribute('href')}")
    # print(*img_pages_set, sep = '\n')
    # print(f'Количество элементов множества {len(img_pages_set)}')





    