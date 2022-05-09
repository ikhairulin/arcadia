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

first_url = 'https://www.deviantart.com'

# Ввод поискового ключа для сбора ссылок
# key = input('Type a search term   ')
key = 'gb62da'


imgs_path = 'D:\Pictures' + '\\' + key

def save_forbidden(url_list):

    try:
        # заходим с уже заготовленными куками
        driver.get(first_url)
        time.sleep(2)

        for cookie in pickle.load(open(f'{username}_cookies', "rb")):
            driver.add_cookie(cookie)

        time.sleep(2)
        driver.refresh()

        for url in url_list:
            driver.get(url)
            time.sleep(3)
            save_button = driver.find_element_by_class_name('_1s9VZ _1EXgC').click()
            save_button.clear()
            time.sleep(2)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()


if __name__ == "__main__":

    forbid_list = []

    with open(alpha_dir + '\\' + key + '_new_forbidden_list.txt', encoding = 'utf-8') as link_file:
        for link_row in link_file:
            forbid_list.append(link_row)

    save_forbidden(forbid_list)

    driver.quit()

    print(f' Script finished. File with links in a folder ->  {alpha_dir}')
    print(" Script running time " + str(d.datetime.now() - start_time)[:8])