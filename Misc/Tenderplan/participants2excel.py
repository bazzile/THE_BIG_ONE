from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
from selenium import webdriver
from Misc.Tenderplan.password import get_passwd


def waiter(expression, method='xpath', delay=10, click=0, event='presence'):
    try:
        if method == 'xpath':
            if event == 'presence':
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, expression)))
            elif event == 'visibility':
                WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, expression)))
        elif method == 'css':
            if event == 'presence':
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, expression)))
            if event == 'visibility':
                WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CSS_SELECTOR, expression)))
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

# TODO собрать всех участников в сет и устранить дубликаты
# TODO выявить победителя
# TODO добавить ссылку на тендер (берётся из адресной строки)
# TODO экспорт в Excel

counter = 0

seen_companies = set()
participants_list = []

while True:
    counter += 1
    try:
        participant_dict = {}
        # Перебираем список лидов, ожидая (visibility), пока прогрузятся новые
        waiter(
            "//*[@id='slidepanel-left-wrapper']/div/div/div/div[2]/div[" + str(counter) + "]",
            click=1, event='visibility')
        # Название тендера
        tender_name = driver.find_element_by_xpath(
            "//*[@id='slidepanel-left-wrapper']/div/div/div/div[2]/div[" + str(counter) + "]/div/div[2]/div[1]").text
        participant_dict['tender_name'] = [tender_name]
        print('\nЛид {}: {}'.format(counter, tender_name))
    except NoSuchElementException:
        print('Конец списка лидов')
        break

    try:
        if waiter('.col-sm-12.notification-title.notification-header-mark', 'css', event='visibility') is True:
            # Страница с тендером полностью прогрузилась, можно искать таблицу участников
            table_presence_tag = waiter('table.participants-table', method='css', delay=0)
            if table_presence_tag is True:
                # таблица участников присутствует, обрабатываем
                # waiter('table.participants-table', method='css')
                table = driver.find_element_by_css_selector(
                    '.table.table-striped.table-condensed.participants-table>tbody')
                print('\n')
                for row in table.find_elements_by_css_selector('.deflink-button>span'):
                    if len(row.text) > 0:
                        company = row.text.strip()
                        print(company)
                        if company not in seen_companies:
                            seen_companies.add(company)
                            participant_dict['company'] = company
                            participants_list.append(participant_dict)
                        else:
                            for item in participants_list:
                                if item['company'] == company:
                                    item['tender_name'].append(tender_name)

            else:
                print('Таблицы участников нету, переходим к следующему тендеру...')

    except (NoSuchElementException, StaleElementReferenceException):
        print('{}\nОшибка приполучении списка, пробуем заново...'.format(80 * '='))
        del participant_dict
        counter -= 1
        # sleep(1)
        continue

for item in participants_list:
    print(item)

