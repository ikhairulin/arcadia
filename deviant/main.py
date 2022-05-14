"""
Парсер DeviantArt.com
если авторизация не пройдет успешно поисковая выдача будет иная, но скрипт отработает
"""

from bs4 import BeautifulSoup
import requests
import time
import re
from random import randint
import os, shutil
import datetime as d
from data.config import username, password, alpha_dir, key, qty, parametr, direct_url

# Технический блок
header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"}
alpha_dir = alpha_dir # материнская папка для сохранения файлов
start_time = d.datetime.now() # замеряем время для подсчета работы цикла
url = 'https://www.deviantart.com/'
url_login = 'https://www.deviantart.com/_sisu/do/signin'

key = key
qty = qty
pages = (qty // 23) + 1


def start_session():
    # Создаем сессию
    global S
    with requests.Session() as S:
        S.headers.update(header)
        S.headers.update({'Referer':url_login}) # Понять как это работает

    fake_user_activity = S.get(url, headers=header)
    print(f'Start script...')
    time.sleep(randint(0, 3))
    response = S.get(url_login, headers=header)
    soup = BeautifulSoup(response.text, 'lxml')
    token = soup.select('input[name="csrf_token"]')

    datas = {
        'referer': 'https://www.deviantart.com/',
        'csrf_token': extract_token(str(token)),
        'challenge': '0',
        'username': username,
        'password': password,
        'remember': 'on'
        }

    time.sleep(randint(0, 2))
    auth = S.post(url_login, headers=header, data=datas, allow_redirects = True)

    fake_user_activity = S.get(url, headers=header)
    if check_auth(fake_user_activity, username):
        print("Authorization successfully passed")
    else:
        print("Authorization NOT successfull")
    print(f'Connecting to site... Response code - {auth.status_code}')



def parse_deviant_links(key, pages, parametr, link, S):
    # Основная функция. # Надо бы наверно разделить

    print(f'Analyze {pages} pages by search query {key}...')

    urls = []

    if parametr == 'search':

        # разделяем поисковой запрос если он составной
        kw_merged = ''
        for k in key.split(' '):
            if k != key.split(' ')[-1]:
                kw_merged += (k + '+')
            else:
                kw_merged += k

        for number in [str(page) for page in list(range(1, pages + 1))]:
            urls.append(r'https://www.deviantart.com/search/deviations?q={0}&page={1}'.format(kw_merged, number))

    if parametr == 'all_gallery':
        for number in [str(page) for page in list(range(1, pages + 1))]:
            urls.append(r'https://www.deviantart.com/{0}/gallery/all?page={1}'.format(key, number))

    if parametr == 'favs':
        for number in [str(page) for page in list(range(1, pages + 1))]:
            urls.append(r'https://www.deviantart.com/{0}/favourites/all?page={1}'.format(key, number))

    if parametr == 'link':
        for number in [str(page) for page in list(range(1, pages + 1))]:
            urls.append(r'{0}&page={1}'.format(link, number))

    print('Prepairing urls...')
    images_links = []

    # блок отладки. Вставить сюда страницу с картинкой которая провоцирует ошибку
    # images_links = ['https://www.deviantart.com/murderousautomaton/art/Prey-133061554']

    for url in urls:
        response = S.get(url)
        soup = BeautifulSoup(response.text, 'html5lib')
        for row in soup.body.find_all('a'):
            if str(row).startswith('<a data-hook="deviation_link"'):
                img_page = row.get('href')
                # images_links.append(row.get('href'))
                images_links.append(img_page)
                with open(alpha_dir + '\\' + key + '\\' + 'url_pages_list.txt', 'a', encoding='UTF-8') as urls_text:
                    urls_text.write(img_page)
                    urls_text.write('\n')

    print(f'Parsing {len(images_links)} img pages')
    response.close()

    return images_links

def continue_save(urls_txt ,saved_txt):
    # функция для продолжения закачки, принимает список ссылок на скачку сравнивает со спсоком уже сохраненных и возвращает разницу
    link_list = []
    saved_list = []
    # подгружаем в массив ссылки с файла
    with open(urls_txt, encoding = 'utf-8') as link_file:

        for link_row in link_file:
            link_list.append(link_row)
    try:
        with open(saved_txt, encoding = 'utf-8') as saved_file:
            for saved_row in saved_file:
                saved_list.append(saved_row)
    except FileNotFoundError:
        saved_list = []

    images_links = list(set(link_list).difference(set(saved_list)))
    return images_links



def save_images(images_links):
    print('Downloading...')

    os.system(r"explorer.exe" + " " + imgs_path)

    counter = 0

    for img_page in images_links:
        time.sleep(randint(0, 2))
        counter += 1
        print(f'{counter}. Saving image from page - {img_page}')
        response = S.get(img_page, headers=header)
        soup = BeautifulSoup(response.text, 'html5lib')
        items = soup.find_all('img', loading = False, srcset= False, title = False, style = False, height= False)
        items = str(items).split('"')

        try:    # ошибка срабатывает если на странице видео вместо картинки
            img_name = items[1]
            img_link = items[-2]
        except IndexError:
            continue
        else:
            img_name = check_filename(img_name)

        response = S.get(img_link, stream=True, headers=header)
        try:
            save_path = imgs_path + '\\' + img_name + '.jpg'
            with open(save_path, "wb") as f:
                response.decode_content = True
                shutil.copyfileobj(response.raw, f)
        except OSError:
            img_name = check_filename(img_name)
            save_path = imgs_path + '\\' + img_name + '.jpg'
            with open(save_path, "wb") as f:
                response.decode_content = True
                shutil.copyfileobj(response.raw, f)

        finally:
            with open(alpha_dir + '\\' + key + '\\' + 'saved_list.txt', 'a', encoding='UTF-8') as saved_text:
                saved_text.write(img_page)
                saved_text.write('\n')
            del response

        if qty - counter == 0:
            break

    print(f'Downloaded {counter} files by search query - {key}')
    print(f'Script finished. Files in a folder ->  {imgs_path}')
    print("Script running time " + str(d.datetime.now() - start_time)[:8])


def extract_token(string):
    # вытаскиваем из строки html значение токена авторизации с помощью регулярки
    text = re.search(r'value=\".*?\"', string)
    result = str(text[0])[7:-1]
    return result

def check_auth(auth, username):
    soup = BeautifulSoup(auth.text, 'html5lib')
    for row in soup.header.find_all('a'):
        if str(row).startswith('<a class="user-link _1Zf8w _2dNZp" data-hook="user_link"'):
            usr_nme = row.get('data-username')
            if usr_nme == username:
                return True


def check_filename(filename):
    # проверяем имя файла на наличие недопустимых для Windows символов
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

def make_dirs():
    # создаем путь к рабочей папке
    if not os.path.exists(alpha_dir):
        os.mkdir(alpha_dir)

    if not os.path.exists(alpha_dir + '\\' + key):
        os.chdir(alpha_dir)
        os.mkdir(key)

    if not os.path.exists(alpha_dir + '\\' + key + '\\' + 'images'):
        os.chdir(alpha_dir + '\\' + key)
        os.mkdir('images')




if __name__ == "__main__":

    imgs_path = 'D:\Pictures' + '\\' + key + '\\' + 'images'

    if not os.path.exists(imgs_path):
        make_dirs()

    start_session()

    # dev_links = parse_deviant_links(key, pages, parametr, direct_url, S)


    url_list_txt = 'D:\\Pictures\\2022-05-08_gb62da_pages_list.txt'
    saved_list_txt = ''
    dev_links = continue_save(url_list_txt, saved_list_txt)

    if len(dev_links) > 0:
        save_images(dev_links)
    else:
        print(f'Nothing was found for your search query - {key}')
