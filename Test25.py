import time
from selenium.webdriver.common.by import By
from selenium import webdriver
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome(r'C:/some_folder`/chromedriver.exe')
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield

   pytest.driver.quit()


def test_show_my_pets():
   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys('v.lexa.v@mail.ru')
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('Kentavr88')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
   #неявное ожидание
   pytest.driver.implicitly_wait(10)
   #явное ожидание
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[contains(text(),"Мои питомцы")]')))
   #явное ожидание
   WebDriverWait(pytest.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[contains(text(),"Выйти")]')))
   pytest.driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

   images = pytest.driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > th > img')
   names = pytest.driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > td')
   #descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

   for i in range(len(names)):
      assert images[i].get_attribute('src') != ''
      assert names[i].text != ''
      #assert descriptions[i].text != ''
      #assert ', ' in descriptions[i]
      #parts = descriptions[i].text.split(", ")
      #assert len(parts[0]) > 0
      #assert len(parts[1]) > 0

def test_check_animal_data():
   pytest.driver.find_element(By.ID, 'email').send_keys('v.lexa.v@mail.ru')
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('Kentavr88')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   pytest.driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()
   #driver.implicitly_wait(10)

   names = pytest.driver.find_elements(By.CSS_SELECTOR, '#all_my_pets .table tbody tr')
   print(len(names))
   for i in range(len(names)):
      parts = names[i].text.split(' ')
      print('Элемент в names: ', names[i].text.split(' '))
      assert len(parts[0]) > 0

   images = pytest.driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > th > img')
   count_not_photo = 0
   for i in range(len(names)):
      if images[i].get_attribute('src') != '':
         count_not_photo += 1
   assert count_not_photo >= (len(names) / 2)
