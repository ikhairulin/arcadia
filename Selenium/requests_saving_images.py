from bs4 import BeautifulSoup
import requests
import datetime as d
import os
import shutil


start_time = d.datetime.now()
alpha_dir = "D:\Pictures"
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}


# не работающий пока блок авторизации

# url_login = 'https://www.deviantart.com/_sisu/do/signin'

# S = requests.Session()
# # response = session.get(url_login, headers=header)
# response = S.get(url_login, headers=header)
# print(S.get(url_login, headers=header))
# soup = BeautifulSoup(response.text, 'html5lib')
# print(response.text)

# inputs = soup.find_all('input', name = True, value = True)


r = session.get(url_login, headers=header)
r.html.render()
print(r.html.text)

# token = []

# for s in soup.body.find_all('input'):
#     print(str(s))
#     if str(s).startswith('<input type="hidden" name="csrf_token"'):
#         token.append(s.get('value'))

# print(token)

# datas = {
#     'referer': 'https://www.deviantart.com/',
#     'csrf_token': str(token),
#     'challenge': '0',
#     'username': 'Zebul',
#     'password': 'sNn@jNQ7Mc4cb7L',
#     'remember': 'on'
#     }
# url_login = 'https://www.deviantart.com/users/login'



# auth = response.post(url_login, headers=header, data=datas, allow_redirects = True)
# print(auth.status_code)

# with open('index.html', 'w') as f:
#     f.write(response.text)


def prepare_link(string):

    first_letter = string.find("url('")

    pre_link = string[first_letter + 5:-2]

    file_name = string[string.find("strp/") + 5 : string.find('-150.jpg')]

    link = pre_link[: pre_link.find(".jpg") + 4] + pre_link[pre_link.rfind(".jpg?") + 4 :]

    return (link, file_name)


# cycles = int(input('Type how many searchterms you will use: '))

cycles = int(1)

searchterm = []

for _ in range(cycles):
    # key = input('Type next searchterm: ')
    # qty = int(input('How many of them do you want? '))
    key = 'planescape torment'
    qty = 1
    pages = (qty // 23) + 1
    searchterm.append([key, qty])

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
def parse_links(key, qty, list):

    print()
    print(f'Analyze {pages} pages by search query {key}...'.format(qty, key))

    imgs_path = 'D:\Pictures' + '\\' + key

    if not os.path.exists(alpha_dir):
        os.mkdir(alpha_dir)

    if not os.path.exists(imgs_path):
        os.chdir(alpha_dir)
        os.mkdir(key)
    
    # разделяем поисковой запрос если он составной
    kw_merged = ''
    for k in key.split(' '):
        if k != key.split(' ')[-1]:
            kw_merged += (k + '+')
        else:
            kw_merged += k


    urls = []
    for number in [str(o) for o in list(range(1, pages + 1))]:
        urls.append(r'https://www.deviantart.com/search/deviations?q={0}&page={1}'.format(kw_merged, number))
    
    print('Prepairing urls...')
    images_links = []

    # блок отладки. Вставить сюда страницу с картинкой которая провоцирует ошибку
    # images_links = ['https://www.deviantart.com/murderousautomaton/art/Prey-133061554']
    
    for url in urls:
        response = requests.Session()
        response = response.get(url, headers=header)
        soup = BeautifulSoup(response.text, 'html5lib')
        for s in soup.body.find_all('a'):
            if str(s).startswith('<a data-hook="deviation_link"'):
                # # print(img_links)
                images_links.append(s.get('href'))
    print(*images_links, sep = '\n')
    print(f' Parsing {len(images_links)} img pages')
    response.close()
        
    print('Downloading...')

    os.system(r"explorer.exe" + " " + imgs_path)

    counter = 0

    for img_page in images_links:
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


# Старт программы с указанием количества циклов
# for key, qty in searchterm:
#     parse_deviant_art(key, qty)


if __name__ == "__main__":
    parse_links(key, qty, img_pages_list)