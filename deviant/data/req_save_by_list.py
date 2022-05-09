import os
import requests
import shutil
from bs4 import BeautifulSoup
import datetime as d
import random
import time

start_time = d.datetime.now()

alpha_dir = "D:\Pictures"


header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'


img_pages = []

# Ввод поискового ключа для сбора ссылок
# key = input('Type a search term   ')
key = 'gb62da'

# Запрос количества скачиваемых картиночек
# qty = input('How many of img need to download?   ')
qty = 50

imgs_path = alpha_dir + '\\' + key + '\\' + 'images'


# Собираем ссылки на картиночки в файл
def save_image_link(img_link):
    with open(alpha_dir + '\\' + key + '_links_list.txt', 'a', encoding='UTF-8') as saved_text:
        saved_text.write(img_link)
        saved_text.write('\n')


# функция сохраняющая картиночки по заданным параметрам
def save_image(img_link, img_name, extension, img_page):
    response = requests.get(img_link, stream=True, headers=header)
    img_path = alpha_dir + '\\' + key + '\\' + 'images' + '\\' + img_name + '.' +  extension
    try:
        with open(img_path, "wb") as f:
            response.decode_content = True
            shutil.copyfileobj(response.raw, f)
            with open(alpha_dir + '\\' + key + '_saved_list.txt', 'a', encoding='UTF-8') as saved_text:
                saved_text.write(img_page)
            file_stats = os.stat(img_path)
            if int(file_stats.st_size) < 1024:
                print(f"Server don't response. Can't reach the file on page - {img_page}")
                with open(alpha_dir + '\\' + key + '_forbidden_list.txt', 'a', encoding='UTF-8') as forbidden_text:
                    forbidden_text.write(img_page)
    except Exception as ex:
        print(ex)
    finally:
        del response



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

    if string.find('-150.jpg') > 0:
        file_name = string[string.find("strp/") + 5 : string.find('-150.jpg')]
        link = pre_link[: pre_link.find(".jpg") + 4] + pre_link[pre_link.rfind(".jpg?") + 4 :]
        extension = 'jpg'
    else:
        file_name = string[string.find("strp/") + 5 : string.find('-150.png')]
        link = pre_link[: pre_link.find(".png") + 4] + pre_link[pre_link.rfind(".png?") + 4 :]
        extension = 'png'

    return (link, file_name, extension)


# Вытаскиваем со страницы данные картиночки
def analyze_page(images_links):

    print('Downloading...')

    if not os.path.exists(alpha_dir):
        os.mkdir(alpha_dir)

    if not os.path.exists(alpha_dir + '\\' + key):
        os.chdir(alpha_dir)
        os.mkdir(key)

    if not os.path.exists(alpha_dir + '\\' + key + '\\' + 'images'):
        os.chdir(alpha_dir + '\\' + key)
        os.mkdir('images')    
   
    # os.system(r"explorer.exe" + " " + imgs_path)

    counter = 0
 
    for img_page in images_links:
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
            # альтернативный способ анализа ссылки на файл
            # print(f'Error on page - {img_page}')
            items = soup.find_all('img', loading = False, srcset= False, title = False, style = False, height= False)
            items = str(items).split('"')

            try:
                img_name = items[1]
                img_link = items[-2]
                extension = 'jpg' 
            except IndexError:   # ошибка срабатывает если на странице видео вместо картинки или платный закрытый контент
                continue
            else: 
                img_name = check_filename(img_name)

        else:
            img_name = img_params[1]
            img_link = img_params[0]
            extension = img_params[2]


        save_image(img_link, img_name, extension, img_page) # вызываем функцию по сохранению файла
        # save_image_link(img_link) # сохраняем ссылки на картиночки в отдельный файл-список

    
    print(f' Downloaded {counter} files by search query - {key}')
    print(f' Script finished. Files in a folder ->  {imgs_path}')
    print(" Script running time " + str(d.datetime.now() - start_time)[:8])


if __name__ == "__main__":
    link_list = []
    saved_list = []

# подгружаем в массив ссылки с файла
    with open(alpha_dir + '\\' + '2022-05-08_gb62da_pages_list.txt', encoding = 'utf-8') as link_file:
    # with open(alpha_dir + '\\' + 'link_list.txt', encoding = 'utf-8') as link_file:
        for link_row in link_file:
            link_list.append(link_row)

# подгружаем в массив ссылки с файла
    try:
        with open(alpha_dir + '\\' + key + '_saved_list.txt', encoding = 'utf-8') as saved_file:
            for saved_row in saved_file:
                saved_list.append(saved_row)
    except FileNotFoundError:
        saved_list = []



    images_links = list(set(link_list).difference(set(saved_list)))

    analyze_page(images_links)


    


