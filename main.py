import time
import difflib 
from selenium import webdriver
from webdriver_manager import driver
from webdriver_manager.driver import Driver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

url = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2'


def setup_driver():
    options = Options()
    # options.headless = True
    driver = webdriver.Firefox(options = options, executable_path=GeckoDriverManager().install())
    return driver

def find_country():
    driver = setup_driver()
    driver.get(url)
    table = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody')
    fields = table.find_elements(By.TAG_NAME, 'tr')[1:]
    # input_country = 'Испания'
    input_country = input("Выберите страну: ")

    i=1
    while i<len(fields):
        a = fields[i].find_elements(By.TAG_NAME, 'td')[2].text
        c = difflib.SequenceMatcher(None, a, input_country).ratio()
        d=c*100
        if d>80:
            print("Гимн ", a)
            link = fields[i].find_element(By.LINK_TEXT, a).get_attribute('href')

            driver.execute_script(f'window.open("{link}")')

            driver.switch_to_window(driver.window_handles[1])
            time.sleep(4)
            print(driver.current_url)
            desc2 = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody')
            gimn = desc2.find_element_by_tag_name('i').text
            print("Гимн ", a)
            print(gimn)
            driver.find_element_by_css_selector('span.ui-icon.ui-icon-play').click()

            break
        i=i+1
    else:
        print("Страны ", input_country, " не существует")



if __name__ == "__main__":
    find_country()