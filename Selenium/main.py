from selenium import webdriver
import time
import pickle
from selenium.webdriver.common.keys import Keys


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




    time.sleep(2)
    img_pages_set = set(scroll_pages(10))
    print(*img_pages_set, sep = '\n')
    print(f'Количество элементов множества {len(img_pages_set)}')

    

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()

