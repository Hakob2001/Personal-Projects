from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np

target_dic = {
    'Россия': 0,
    'Бывший СССР': 3,
    'Экономика': 1,
    'Силовые структуры': 2,
    'Наука и техника': 8,
    'Спорт': 4,
    'Путешествия': 7,
    'Забота о себе': 5}
days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18',
        '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
mounts = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
mount = ['02']

for mm in mount:
    if mm == '02':
        days_m = days[:29]
    elif mm == '04' or '06' or '09' or '11':
        days_m = days[:30]
    else:
        days_m = days
    for dd in days_m:

        content_list = []
        target_list = []

        driver = webdriver.Chrome()

        try:
            for j in range(1, 25):  
                for i in range(1, 31):
                    driver.get(url=f'https://lenta.ru/2024/{mm}/{dd}/page/{j}/')
                    a = driver.find_element(By.CSS_SELECTOR,
                                            f'#body > div.layout.js-layout > div.layout__container > main > div.archive-page > section > ul > li:nth-child({i}) > a > div').text

                    if a[-1] != '4':
                        target = driver.find_element(By.CSS_SELECTOR,
                                                     f'#body > div.layout.js-layout > div.layout__container > main > div.archive-page > section > ul > li:nth-child({i}) > a > div > span').text

                        if target in target_dic:

                            driver.find_element(By.CSS_SELECTOR,
                                                f'#body > div.layout.js-layout > div.layout__container > main > div.archive-page > section > ul > li:nth-child({i}) > a').click()

                            content = driver.find_element(By.CSS_SELECTOR,
                                                          '#body > div.layout.js-layout > div.layout__container > main').text

                            if 'Что думаешь?' in content:
                                content = content[0:content.index('Что думаешь?')]
                            elif 'Комментарии отключены' in content:
                                content = content[0:content.index('Комментарии отключены')]
                            elif 'Последние новости' in content:
                                content = content[0:content.index('Последние новости')]
                            else:
                                content = content

                            content_list.append(content)
                            target_list.append(target_dic[target])









        except Exception as ex:
            print(ex.__class__.__name__)
            print('էռռոռ')
            df = pd.DataFrame(data=content_list, columns=['Content'])
            df['Target'] = target_list
            df.to_csv(f'train_{dd}_{mm}_2024.csv', encoding='utf-8', index=False, index_label=False)
        finally:
            driver.close()
            driver.quit()