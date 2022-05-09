from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pickle
import os

user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'

# options
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={user_agent}')

# disable webdrivermode
options.add_argument('--disable-blink-features=AutomationControlled')

# # работа в фоне
# options.add_argument('--headless')

url_login = 'https://www.deviantart.com/users/login'

path = os.path.abspath(__file__) # возвращает путь до исполняемого скрипта
executable_path = path[: path.rindex('\\') + 1] + 'chromedriver.exe'

driver = webdriver.Chrome(
    executable_path = executable_path,
    options=options
    )

# driver = webdriver.Chrome(
#     executable_path=r'D:\OneDrive\Synh\Code\Python\My_projects\arcadia\deviant\chromedriver.exe',
#     options=options
#     )

# auth block
username = 'Zebul'
password = 'sNn@jNQ7Mc4cb7L'


def grab_cookies():         # авторизуемся и получаем куки
    try:
        # авторизуемся и получаем куки

        driver.get(url_login)
        time.sleep(3)

        print('Проходим идентификацию...')
        email_input = driver.find_element_by_id('username')
        email_input.clear()
        email_input.send_keys(username)

        pass_input = driver.find_element_by_id('password')
        pass_input.clear()
        pass_input.send_keys(password)
        time.sleep(2)

        pass_input.send_keys(Keys.ENTER)

        # login_button = driver.find_element_by_id('loginbutton').click()
        time.sleep(3)

        # сохраняем cookies в файл
        pickle.dump(driver.get_cookies(),open(f"{username}_cookies", "wb"))
        time.sleep(3)



    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":
    grab_cookies()