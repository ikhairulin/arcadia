from selenium import webdriver
import time
import pickle
from selenium.webdriver.common.keys import Keys
# from Requests_DA_img import *

from bs4 import BeautifulSoup
import requests
import datetime as d
import os
import shutil



start_time = d.datetime.now()
alpha_dir = "D:\Pictures"
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}


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


# Основная функция. # Надо бы наверно разделить
def parse_deviant_art(key, qty, img_pages_set):

    print()

    imgs_path = 'D:\Pictures' + '\\' + key

    if not os.path.exists(alpha_dir):
        os.mkdir(alpha_dir)

    if not os.path.exists(imgs_path):
        os.chdir(alpha_dir)
        os.mkdir(key)
    
       
    print('Downloading...')

    os.system(r"explorer.exe" + " " + imgs_path)

    counter = 0

    for img_page in img_pages_set:
        print(f'Saving image from page - {img_page}')
        response = requests.Session()
        response = response.get(img_page, headers=header)
        soup = BeautifulSoup(response.text, 'html5lib')
        items = soup.find_all('img', loading = False, srcset= False, title = False, style = False, height= False)
        items = str(items).split('"')

    # ошибка срабатывает если на странице видео вместо картинки
        try:
            img_name = items[1]
            img_link = items[-2]
        except IndexError:
            continue
        else: 
            img_name = check_filename(img_name)

    # Блок отладки. Debug block
        # print(items)
        # print()
        # print(*items, sep = "\n")
        # print(img_name, img_link, sep = "\n")

        response = requests.get(img_link, stream=True, headers=header)
        try:
            img_path = alpha_dir + '/%s' % key + '/' + img_name + '.jpg'
            with open(img_path, "wb") as f:
                response.decode_content = True
                shutil.copyfileobj(response.raw, f)
        except OSError:
            img_name = check_filename(img_name)
            img_path = alpha_dir + '/%s' % key + '/' + img_name + '.jpg'
            with open(img_path, "wb") as f:
                response.decode_content = True
                shutil.copyfileobj(response.raw, f)
        finally:
            counter += 1
            del response
    
    print(f' Downloaded {counter} files by search query - {key}')
    print(f' Script finished. Files in a folder ->  {imgs_path}')
    print(" Script running time " + str(d.datetime.now() - start_time)[:8])







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


url = 'https://www.deviantart.com/search/deviations?q=gb62da&page=1'
# url = f'https://www.deviantart.com/search/deviations?q=planescape&page=1'
url_login = 'https://www.deviantart.com/users/login'
driver = webdriver.Chrome(
    executable_path=r'D:\OneDrive\Synh\Code\Python\My_projects\arcadia\Selenium\chromedriver.exe',
    options=options
    )

# auth block
username = 'Zebul'
password = 'sNn@jNQ7Mc4cb7L'

img_pages = []

def scroll_pages(cycles):
    for _ in range(cycles):

        pass_input = driver.find_element_by_tag_name('body')
        pass_input.send_keys(Keys.END)
        time.sleep(2)

        items = driver.find_elements_by_xpath('//a[@data-hook="deviation_link"]')
        for item in items:
            img_pages.append(item.get_attribute('href'))
        print(f'Количество элементов в списке {len(img_pages)}')

    return img_pages


try:

    # заходим с уже заготовленными куками
    driver.get(url)
    time.sleep(2)

    for cookie in pickle.load(open(f'{username}_cookies', "rb")):
        driver.add_cookie(cookie)

    time.sleep(2)
    driver.refresh()


    # items = driver.find_elements_by_xpath('//a[@data-hook="deviation_link"]')
    # img_pages = []
    # for item in items:
    #     img_pages.append(item.get_attribute('href'))
    # print(f'Количество элементов в списке {len(img_pages)}')
    # img_pages_set = set(img_pages)
    #     # print(f"Ты ищешь страницу {item.get_attribute('href')}")
    # print(*img_pages_set, sep = '\n')
    # print(f'Количество элементов множества {len(img_pages_set)}')

    time.sleep(2)
    img_pages_set = set(scroll_pages(10))
    print(*img_pages_set, sep = '\n')
    print(f'Количество элементов множества {len(img_pages_set)}')



    key = 'gb62da'
    qty = 20

    parse_deviant_art(key, qty, img_pages_set)


except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()


