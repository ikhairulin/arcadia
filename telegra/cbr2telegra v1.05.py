"""Script for unpacking a cbr-comic archive and upload comics to telegra.ph"""

import os
import shutil
import time

import telegraph
import requests
import zipfile
import rarfile

from data.config import alpha_dir, my_token, UnRAR_path



def get_tags(cbr):
    """
    Вытаскиваем из комикса его название, автора(по возможности) и количество страниц
    Функция принимает имя файла, список файлов и выдает словарь с данными
    """
    pre_name = cbr.split('\\')
    if os.path.isdir(cbr):
        comic_name = pre_name[-1]
    else:
        not_publishing = ['English', 'Web Comics', 'Other', 'Manga']
        try:
            if pre_name[2] in not_publishing or len(pre_name) < 4:
                comic_name = pre_name[-1][:-4]
            else:
                comic_name = f'{pre_name[2]} - {pre_name[-1][:-4]}'
        except IndexError:
            comic_name = pre_name[-1][:-4]

    print('Analyzing file name...')
    print('Comic name is', comic_name)
    return comic_name


def cbr_to_list(cbr, alpha_dir):
    """Функция принимает абсолютный путь к архиву или к папке с комиксом в виде
     строки в переменной 'cbr',распаковывает его во временную папку.
     Возвращает список файлов
    """
    files_list = []
    extension = str(cbr)[-4:]


    if os.path.isdir(cbr):
        files_path = cbr
        for root, dirs, files in os.walk(str(cbr)):
            for file in files:
                files_list.append(os.path.join(root, file))
        print("Let's see what we have here...")


    elif extension in ['.cbz', '.zip']:
        files_path = str(alpha_dir + 'temp_dir')
        with zipfile.ZipFile(cbr) as z:
            z.extractall(str(alpha_dir + 'temp_dir'))
        print('Unpacking zip archive...')


    elif extension in ['.cbr', '.rar']:
        files_path = str(alpha_dir + 'temp_dir')
        rarfile.UNRAR_TOOL = UnRAR_path
        with rarfile.RarFile(cbr) as r:
            r.extractall(str(alpha_dir + 'temp_dir'))
        print('Unpacking rar archive...')


    else:
        print('Wrong file format. Please use .cbr, .cbz, rar, zip')

    for root, dirs, files in os.walk(files_path):
        for file in files:
            files_list.append(os.path.join(root, file))
    print('Received', len(files_list), 'pages')
    return files_list


def del_temp(alpha_dir):
    """Удаляет временные файлы с папкой после окончания закачки"""
    print('Deleting temp files...')
    time.sleep(5)
    shutil.rmtree(str(alpha_dir + 'temp_dir'))



def upload_imgs(filelist):
    """Принимает список файлов и по одному закачивает их на telegra.ph/upload
    Выдает список ссылок file_links
    Принимаются только файлы расширений image/gif, image/jpeg, image/jpg, image/png, video/mp4
    """
    upload_files = []
    counter = 1
    for file_name in filelist:
        with open(file_name, 'rb') as f:
            result_requests = requests.post(
                'https://telegra.ph/upload',
                files={'file': ('file', f, 'image/jpg')}
                ).json()
            upload_files.append(str(result_requests))
        print('Upload', counter, 'file. Link -  https://telegra.ph/' + str(result_requests)[10:-3])
        counter += 1
    return upload_files

def prepare_string(file_links):
    """ Принимает список ссылок на файлы, выдает строку в готовом для telegraph API виде"""
    pages = len(file_links)
    string = f'<p>{pages} страниц</p>'
    for i in range(len(file_links)):
        string += f'<img src="{file_links[i][10:-3]}">'
    return string


def create_telegra_page(token, title, page_string):
    """ Принимает токен, имя комикса как заголовок, список ссылок на файлы
    создает страницу и выдает ссылку на неё
    html_content принимает строку в виде
    <p>Hello, world!</p><img src="/file/1f49fad89f0d884d636a5.jpg">
    """
    print('Create a comic page on telegra.ph')
    session = telegraph.Telegraph(token)
    response = session.create_page(
    title,
    html_content=page_string
)
    print('https://telegra.ph/{}'.format(response['path'])) # распечатываем адрес страницы


def logging_script():
    """ Создает текстовый файл с логами работы программы"""
    pass


def main(cbr, alpha_dir):

    upload_file_list = upload_imgs(cbr_to_list(cbr, alpha_dir))

    title = get_tags(cbr)

    html_string = prepare_string(upload_file_list)

    create_telegra_page(my_token, title, html_string)


if __name__ == '__main__':

    # путь к файлу-архиву или к папке с картиночками
    cbr = "E:\Comics\Heavy Metal Magazine\Vampire Vixens of the Wehrmacht.cbr"

    try:
        main(cbr, alpha_dir)

        del_temp(alpha_dir)

    except Exception as ex:
        print("Error")
        print(ex)