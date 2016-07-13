from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep
from selenium import webdriver
from Misc.Tenderplan.password import get_passwd


def waiter(expression, method='xpath', delay=10, click=0):
    try:
        if method == 'xpath':
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, expression)))
        elif method == 'css':
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, expression)))
        # print("Page is ready!")
        if click == 1:
            driver.find_element_by_xpath(expression).click()
        return True
    except TimeoutException:
        # print("Loading took too much time!")
        return False
# запрашиваем пароль к tenderplan.ru
pwd = get_passwd().strip()
driver = webdriver.Firefox()
driver.get("http://tenderplan.ru/account/logon")
username = driver.find_element_by_name("EmailAddress")
password = driver.find_element_by_name("Password")
username.send_keys("lobanov@innoter.com")
password.send_keys(pwd)
driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/section/div/div/form/div[3]/button").click()
# Жмём "Лиды отработать"
print('Запрашиваем список лидов...')
waiter("//*[contains(text(), 'Лиды отработать')]", click=1)
# ждём, пока лиды прогрузятся
sleep(3)

# Перебираем список лидов
# TODO разобраться, как получить общее число тендеров в списке
# TODO собрать всех участников в сет и устранить дубликаты
# TODO выявить победителя
# TODO экспорт в Excel
for i in range(9, 21):
    waiter("//*[@id='slidepanel-left-wrapper']/div/div/div/div[2]/div[" + str(i) + "]/div/div[2]/div[1]", click=1)
    # Название тендера
    tender_name = driver.find_element_by_xpath("//*[@id='slidepanel-left-wrapper']/div/div/div/div[2]/div[" + str(i) + "]/div/div[2]/div[1]").text
    print('\nЛид {}: {}'.format(i, tender_name))

    if waiter('.col-sm-12.notification-title.notification-header-mark', 'css') is True:
        # Страница с тендером полностью прогрузилась, можно искать таблицу участников
        table_presence_tag = waiter('table.participants-table', method='css', delay=0)
        if table_presence_tag is True:
            # таблица участников присутствует, обрабатываем
            # waiter('table.participants-table', method='css')
            table = driver.find_element_by_css_selector('.table.table-striped.table-condensed.participants-table>tbody')
            for row in table.find_elements_by_css_selector('.deflink-button>span'):
                print(row.text)
        else:
            print('Таблицы участников нету, переходим к следующему тендеру...')
