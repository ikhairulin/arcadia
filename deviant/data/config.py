"""Параметры для работы парсера"""

"""Поисковой запрос и ориентировочное количество скачиваемых файлов."""
key = 'Sun'

"""Указываем так же в кавычках. Можно несколько слов, например 'planescape torment'"""
qty = 1000

"""
Цикл прекратится когда будет сохранено это количество файлов
Поиск выдает по 23-25 картинки на страницу, парсер собирает их все и количество может варьироваться.
Формула расчета для количества спарсенных страниц (qty // 23) + 1
"""

"""указать свои данные для авторизации на сайте. Без этого поисковая выдача будет неполная"""
username = ''
password = ''


""" Материнская папка где будут созданы поддиректории с поисковыми запросами и скачанными файлами
"""
alpha_dir = "D:\Pictures"



""" Параметры скачивания:
1. 'search' - обычный режим, сохраняются все картинки из поисковой выдачи сайта по ключевому слову key
2. 'all' - скачать все работы одного автора, необходимо указать в графе key имя автора из профиля, например по ссылке https://www.deviantart.com/jpryno будет 'jpryno'
3. 'favs' - подборка из папки Favorites автора под именем key
4. 'link' - парсится отдельная подборка автора по ссылке. Например https://www.deviantart.com/jpryno/gallery/73050711/traditional-art. Записывается в direct_url
"""
parametr = 'link'
direct_url = 'https://www.deviantart.com/jambe/favourites/1894595/photo-favs'