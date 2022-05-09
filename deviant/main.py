from selenium import webdriver
import time
import pickle
from selenium.webdriver.common.keys import Keys

import requests
import shutil


alpha_dir = "D:\\"
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

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

# работа в фоне
# options.add_argument('--headless')


url_login = 'https://www.deviantart.com/users/login'

# Адрес скачанного Chromedriver
driver = webdriver.Chrome(
    executable_path=r'D:\OneDrive\Synh\Code\Python\My_projects\arcadia\Selenium\chromedriver.exe',
    options=options
    )

# auth block
username = 'Zebul'
password = 'sNn@jNQ7Mc4cb7L'

img_pages = []

# Ввод поискового ключа для сбора ссылок
# key = input('Type a search term   ')
key = 'gb62da'

# Запрос количества скачиваемых картиночек
# qty = input('How many of img need to download?   ')
qty = 100

# Скроллим поисковую выдачу и собираем в список ссылки на страницы с картинками
def scroll_pages(cycles):
    for _ in range(cycles):

        pass_input = driver.find_element_by_tag_name('body')
        pass_input.send_keys(Keys.END)
        time.sleep(2)

        items = driver.find_elements_by_xpath('//a[contains(@data-hook,"deviation_link")]')
        for item in items:
            img_pages.append(item.get_attribute('href'))
        print(f'Количество элементов в списке {len(img_pages)}')

    return img_pages


try:
    # авторизуемся и получаем куки

    driver.get(url_login)
    time.sleep(3)

    print('Проходим идентификацию...')
    email_input = driver.find_element_by_id('username')
    email_input.clear()
    email_input.send_keys(username)

    pass_input = driver.find_element_by_id('password')
    pass_input.clear()
    pass_input.send_keys(password)
    time.sleep(2)

    pass_input.send_keys(Keys.ENTER)

    # login_button = driver.find_element_by_id('loginbutton').click()
    time.sleep(3)

    # сохраняем cookies в файл
    pickle.dump(driver.get_cookies(),open(f"{username}_cookies", "wb"))
    time.sleep(3)



except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()







def parse_links(key, qty, img_pages_set):

    kw_merged = ''
    for k in key.split(' '):
        if k != key.split(' ')[-1]:
            kw_merged += (k + '+')
        else:
            kw_merged += k

    url = f'https://www.deviantart.com/search/deviations?q={kw_merged}&page=1'

    try:
        # заходим с уже заготовленными куками
        driver.get(url)
        time.sleep(2)

        for cookie in pickle.load(open(f'{username}_cookies', "rb")):
            driver.add_cookie(cookie)

        time.sleep(2)
        driver.refresh()

        # time.sleep(10)
        scrolls = qty / 23
        # scrolls = 1
        

        time.sleep(2)
        img_pages_set = set(scroll_pages(scrolls))
        # print(*img_pages_set, sep = '\n')
        print(f'Количество элементов множества {len(img_pages_set)}')
        global img_pages_list
        img_pages_list = list(img_pages_set)
        time.sleep(3)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

parse_links(key, qty, img_pages_list)


