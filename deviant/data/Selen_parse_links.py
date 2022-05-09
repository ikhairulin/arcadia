from selenium import webdriver
import time
import pickle
from selenium.webdriver.common.keys import Keys

import datetime as d


start_time = d.datetime.now()

alpha_dir = "D:\Pictures"

header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'


# options
options = webdriver.ChromeOptions()
# options.add_argument(f'user-agent={random.choice(user_agent_list)}')
options.add_argument(f'user-agent={user_agent}')


# disable webdrivermode
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--start-maximized")

# работа в фоне
# options.add_argument('--headless')

# Адрес скачанного Chromedriver
driver = webdriver.Chrome(
    executable_path=r'D:\OneDrive\Synh\Code\Python\My_projects\arcadia\Selenium\chromedriver.exe',
    options=options
    )

# auth block
username = 'Zebul'


img_pages = []

# Ввод поискового ключа для сбора ссылок
# key = input('Type a search term   ')
key = 'gb62da'

# Запрос количества скачиваемых картиночек
# qty = input('How many of img need to download?   ')
qty = 50

imgs_path = 'D:\Pictures' + '\\' + key

# Скроллим поисковую выдачу и собираем в список ссылки на страницы с картинками
def scroll_pages(cycles):
    counter = 0
    for _ in range(cycles):
        counter += 1
        time.sleep(1)
        items = driver.find_elements_by_xpath('//a[contains(@data-hook,"deviation_link")]')
        for item in items:
            img_pages.append(item.get_attribute('href'))
        pass_input = driver.find_element_by_tag_name('body')
        pass_input.send_keys(Keys.END)
        time.sleep(1)
        print(f'{counter}. Количество проанализированных ссылок {len(img_pages)}')
    time.sleep(3)
    return img_pages


def parse_links(key, qty):

    kw_merged = ''
    for k in key.split(' '):
        if k != key.split(' ')[-1]:
            kw_merged += (k + '+')
        else:
            kw_merged += k

    url = f'https://www.deviantart.com/search/deviations?q={kw_merged}&page=0'

    try:
        # заходим с уже заготовленными куками
        driver.get(url)
        time.sleep(2)

        for cookie in pickle.load(open(f'{username}_cookies', "rb")):
            driver.add_cookie(cookie)

        time.sleep(2)
        driver.refresh()

        # time.sleep(10)
        scrolls = int(qty / 34)
        # scrolls = 1
     
        time.sleep(2)
        img_pages_set = set(scroll_pages(scrolls))
        # print(*img_pages_set, sep = '\n')
        print(f'Количество уникальных ссылок {len(img_pages_set)}')
        global img_pages_list
        img_pages_list = list(img_pages_set)
        # img_pages_list.sort()
        time.sleep(3)

        text = open(alpha_dir + '\\' + str(d.datetime.now())[:10] + '_' + key + '_pages_list.txt', 'w', encoding='UTF-8')
        for name in img_pages_list:
            text.write(name)
            text.write('\n')
        text.close


    except Exception as ex:
        print(ex)
    finally:
        driver.close()


if __name__ == "__main__":
    parse_links(key, qty)

    driver.quit()

    print(f' Script finished. File with links in a folder ->  {alpha_dir}')
    print(" Script running time " + str(d.datetime.now() - start_time)[:8])