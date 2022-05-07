from selenium import webdriver
import time
import pickle
from selenium.webdriver.common.keys import Keys

import os
import requests
import shutil
from bs4 import BeautifulSoup
import datetime as d
import random

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
qty = 50

imgs_path = 'D:\Pictures' + '\\' + key

# проверяем имя файла
def check_filename(filename):
    for i in list(filename):
        if str(i) in "/\\:;*?<>|":
            new_name = ''
            for k in range(len(filename)):
                if filename[k] in "/\\:;*?<>|":
                    continue
                else:
                    new_name += filename[k]
            filename = new_name
    return filename

def prepare_link(string):

    first_letter = string.find("url('")
    pre_link = string[first_letter + 5:-2]
    file_name = string[string.find("strp/") + 5 : string.find('-150.jpg')]
    link = pre_link[: pre_link.find(".jpg") + 4] + pre_link[pre_link.rfind(".jpg?") + 4 :]
    return (link, file_name)



# Скроллим поисковую выдачу и собираем в список ссылки на страницы с картинками
def scroll_pages(cycles):
    counter = 0
    for _ in range(cycles):
        counter += 1
        pass_input = driver.find_element_by_tag_name('body')
        pass_input.send_keys(Keys.END)
        time.sleep(1)
        items = driver.find_elements_by_xpath('//a[contains(@data-hook,"deviation_link")]')
        for item in items:
            img_pages.append(item.get_attribute('href'))
        print(f'{counter}. Количество проанализированных ссылок {len(img_pages)}')
    time.sleep(3)
    return img_pages


# Сам скрипт скачивающий по заданному списку
def download_img(images_links):

    print('Downloading...')

    if not os.path.exists(alpha_dir):
        os.mkdir(alpha_dir)

    if not os.path.exists(imgs_path):
        os.chdir(alpha_dir)
        os.mkdir(key)
   
    os.system(r"explorer.exe" + " " + imgs_path)

    counter = 0
    bad_list =[]
    global forbidden_list
    forbidden_list = []

    file = open(r'D:\OneDrive\Synh\Code\Python\My_projects\arcadia\Selenium\list.txt', encoding = 'utf-8')
    for img_page in file:
    # for img_page in images_links:
        counter += 1
        time.sleep(random.randint(0, 2))
        print(f'{counter}. Saving image from page - {img_page}')
        response = requests.Session()
        response = response.get(img_page, headers=header)
        soup = BeautifulSoup(response.text, 'html5lib')
        try:
            item = soup.find('div', class_ = '_2Py-J _287EP').get('style')
            img_params = prepare_link(item)
        except AttributeError:
            print(f'Error on page - {img_page}')
            bad_list.append(img_page)
            continue

    # ошибка срабатывает если на странице видео вместо картинки

        try:
            img_name = img_params[1]
            img_link = img_params[0]
        except IndexError:
             continue

        response = requests.get(img_link, stream=True, headers=header)
        img_path = alpha_dir + '/%s' % key + '/' + img_name + '.jpg'
        with open(img_path, "wb") as f:
            response.decode_content = True
            shutil.copyfileobj(response.raw, f)
            file_stats = os.stat(img_path)
            if int(file_stats.st_size) < 1024:
                print(f"Can't reach the file on page - {img_page}. Server don't response")
                forbidden_list.append(img_page)
        del response

# блок для необработанных первой волной ссылок. ИСПРАВИТЬ!!
    sec_counter = 0
    for img_page in bad_list:
        sec_counter += 1
        time.sleep(random.randint(0, 1))
        print(f'{sec_counter}. Saving image from page - {img_page}')
        response = requests.Session()
        response = response.get(img_page, headers=header)
        soup = BeautifulSoup(response.text, 'html5lib')
        items = soup.find_all('img', loading = False, srcset= False, title = False, style = False, height= False)
        items = str(items).split('"')

        try:
            img_name = items[1]
            img_link = items[-2]
        except IndexError:
            continue
        else: 
            img_name = check_filename(img_name)

        response = requests.get(img_link, stream=True, headers=header)
        img_path = alpha_dir + '/%s' % key + '/' + img_name + '.jpg'
        with open(img_path, "wb") as f:
            response.decode_content = True
            shutil.copyfileobj(response.raw, f)
        del response

    
    
    print(f' Downloaded {counter + sec_counter} files by search query - {key}')
    print(f' Script finished. Files in a folder ->  {imgs_path}')
    print(" Script running time " + str(d.datetime.now() - start_time)[:8])

    forbid_text = open(imgs_path + '\\' + 'forbidden_list.txt', 'w', encoding='UTF-8')
        for row in forbidden_list:
            forbid_text.write(row)
            forbid_text.write('\n')
        forbid_text.close


def parse_links(key, qty):

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

        text = open(imgs_path + '\\' + 'list.txt', 'w', encoding='UTF-8')
        for name in img_pages_list:
            text.write(name)
            text.write('\n')
        text.close


    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        # driver.quit()


parse_links(key, qty)

download_img(img_pages_list)

driver.quit()



