# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

MODEL = 'Lenovo'


class TestSearchYandexMarket(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        # устанавливаем неявное ожидание в  5 секунд
        self.driver.implicitly_wait(5)
        # устанавливаем размер окна во весь экран
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)

        self.driver.get("https://market.yandex.ru/")
        self.driver.find_element(By.LINK_TEXT, 'Компьютерная техника').click()
        self.driver.find_element(By.LINK_TEXT, 'Ноутбуки').click()
        self.driver.find_element(
            By.XPATH,
            '//a/label/div[contains(.//span, "{0}")]'.format(MODEL)).click()

        self.driver.find_element(By.ID, "glpricefrom").send_keys("25000")
        self.driver.find_element(By.ID, "glpriceto").send_keys("30000")
        self.driver.find_element(By.ID, "glpriceto").send_keys(Keys.ENTER)

        # при установке фильтра появляется div.preloadable__preloader.preloadable__preloader_visibility_visible.preloadable__paranja
        # который делает область товаров неактивной. Ждем пока он появиться и пропадет
        self.wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'body > div.main > div:nth-child(7) > div.layout.layout_type_search.i-bem > div.layout__col.i-bem.layout__col_search-results_normal > div.n-filter-applied-results.metrika.b-zone.i-bem.n-filter-applied-results_js_inited.b-zone_js_inited > div > div.preloadable__preloader.preloadable__preloader_visibility_visible.preloadable__paranja'
            )))
        self.wait.until_not(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'body > div.main > div:nth-child(7) > div.layout.layout_type_search.i-bem > div.layout__col.i-bem.layout__col_search-results_normal > div.n-filter-applied-results.metrika.b-zone.i-bem.n-filter-applied-results_js_inited.b-zone_js_inited > div > div.preloadable__preloader.preloadable__preloader_visibility_visible.preloadable__paranja'
            )))

    def tearDown(self):
        self.driver.close()

    def test_search_by_price(self):
        # сохраняем html-код страницы в переменую и парсим с помощью BeautifulSoup
        html_source = self.driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')

        # получаем цены
        soup_prices_on_page = soup.find_all('div', {'class': 'price'})

        for i in soup_prices_on_page:
            price = int(
                i.text.replace('от', '').replace('₽', '').replace(' ',
                                                                  '').strip())
            isT = True if price >= 25000 and price <= 30000 else False
            self.assertTrue(isT)


if __name__ == "__main__":
    unittest.main()
