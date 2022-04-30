from selenium import webdriver
import time
import random
from fake_useragent import UserAgent


user_agent_list = [
    'hello_world',
    'best_of_the_best',
    'python_today',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'
]

# options
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={random.choice(user_agent_list)}')


url = 'https://www.deviantart.com/search/deviations?q=gb62da&page=1'
driver = webdriver.Chrome(
    executable_path=r'D:\OneDrive\Synh\Code\Python\My_projects\arcadia\Selenium\chromedriver.exe',
    options=options
    )
get_user_agent = 'https://www.whatismybrowser.com/detect/what-is-my-user-agent'

try:
    driver.get(url=get_user_agent)

    time.sleep(5)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()