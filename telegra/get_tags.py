import os

def get_tags(cbr):
    """
    Вытаскиваем из комикса его название, автора(по возможности) и количество страниц
    Функция принимает имя файла, список файлов и выдает словарь с данными
    """
    pre_name = cbr.split('\\')
    # print()
    # print(*pre_name, sep='\n')
    # print(len(pre_name), 'элементов')
    # print()

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



cbr = "E:\Comics\Heavy Metal Magazine\Margot"
get_tags(cbr)

