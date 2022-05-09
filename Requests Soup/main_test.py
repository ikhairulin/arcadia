from bs4 import BeautifulSoup
import requests
import datetime as d
import os
import shutil
import imghdr


start_time = d.datetime.now()
alpha_dir = "D:\Pictures"
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

img_page = 'https://www.deviantart.com/gb62da/art/Sweet-Home-ala-Dana-2-753657901'
# img_page = 'index.html'

key = 'gb62da2'


def prepare_link(string):

    first_letter = string.find("url('")

    pre_link = string[first_letter + 5:-2]

    file_name = string[string.find("strp/") + 5 : string.find('-150.jpg')]

    link = pre_link[: pre_link.find(".jpg") + 4] + pre_link[pre_link.rfind(".jpg?") + 4 :]

    return (link, file_name)


imgs_path = 'D:\Pictures' + '\\' + key

if not os.path.exists(alpha_dir):
    os.mkdir(alpha_dir)

if not os.path.exists(imgs_path):
    os.chdir(alpha_dir)
    os.mkdir(key)
    
print('Downloading...')

os.system(r"explorer.exe" + " " + imgs_path)

counter = 0

print(f'Saving image from page - {img_page}')
response = requests.Session()
response = response.get(img_page, headers=header)
soup = BeautifulSoup(response.text, 'html5lib')
items = soup.find('div', class_ = '_2Py-J _287EP').get('style')
# items = str(items).split('"')
# print(response.text)
# with open('index.html', "w") as f:
#    f.write(response.text)

# Блок отладки. Debug block
# print(items)
# print()
# print(*items, sep = "\n")


img_params = prepare_link(items)

img_name = img_params[1]
img_link = img_params[0]
# print(img_link)


# # Блок отладки. Debug block
# print(items)
# print()
# print(*items, sep = "\n")
# print(img_name, img_link, sep = "\n")

response = requests.get(img_link, stream=True, headers=header)
img_path = alpha_dir + '/%s' % key + '/' + img_name + '.jpg'
with open(img_path, "wb") as f:
    response.decode_content = True
    shutil.copyfileobj(response.raw, f)
    file_stats = os.stat(img_path)
    if int(file_stats.st_size) < 1024:
        print("Косяк")
    print(file_stats.st_size)
counter += 1
del response

print(f' Downloaded {counter} files by search query - {key}')
print(f' Script finished. Files in a folder ->  {imgs_path}')
print(" Script running time " + str(d.datetime.now() - start_time)[:8])


# Старт программы с указанием количества циклов
# for key, qty in searchterm:
#     parse_deviant_art(key, qty)
