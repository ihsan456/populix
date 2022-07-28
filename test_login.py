import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pytest
import pandas as pd
from pytest_html_reporter import attach

df1 = pd.read_excel('validdata.xlsx', na_filter=False)
validdata = df1.values

df2 = pd.read_excel('invaliddata.xlsx', na_filter=False)
invaliddata = df2.values

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.populix.co/login')
    driver.maximize_window()
    yield driver

    attach(data=driver.get_screenshot_as_png())
    driver.quit()


@pytest.mark.parametrize("email, password", validdata)
def test_validlogin(driver, email, password):
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID, 'input_email'))).send_keys(email)
    driver.find_element(By.ID, 'input_password').send_keys(password)
    driver.find_element(By.ID, 'submit_login').click()
    assert WebDriverWait(driver,20).until(EC.invisibility_of_element_located((By.ID, 'input_email')))

@pytest.mark.parametrize("email, password, condition", invaliddata)
def test_invalidlogin(driver, email, password, condition):
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID, 'input_email'))).send_keys(email)
    driver.find_element(By.ID, 'input_password').send_keys(password)
    driver.find_element(By.ID, 'submit_login').click()
    if condition == 'Invalid Email':
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'input_email-helper-text')))
        warningEmail = driver.find_element(By.ID, 'input_email-helper-text')
        assert warningEmail.text == 'Email yang anda masukan salah atau tidak terdaftar'
    elif condition == 'Invalid Password':
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'input_password-helper-text')))
        warningPassword = driver.find_element(By.ID, 'input_password-helper-text')
        assert warningPassword.text == 'Password yang anda masukan salah'
    elif condition == 'Blank':
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'input_email-helper-text' and 'input_password-helper-text')))
        warningEmail = driver.find_element(By.ID, 'input_email-helper-text')
        warningPassword = driver.find_element(By.ID, 'input_password-helper-text')
        assert warningEmail.text == 'Email yang anda masukan salah atau tidak terdaftar' and warningPassword.text == 'Password yang anda masukan salah'

def test_moveToRegister(driver):
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID, 'btn_to-register'))).click()
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h4.MuiTypography-root')))
    assert driver.find_element(By.CSS_SELECTOR, 'h4.MuiTypography-root').text == 'Daftar Akun Populix'

def test_moveToLupaPassword(driver):
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID, 'btn_to-forgot-password'))).click()
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h4.MuiTypography-root')))
    assert driver.find_element(By.CSS_SELECTOR, 'h4.MuiTypography-root').text == 'Lupa kata sandi? Tetap tenang'

def test_googlePlayButton(driver):
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID, 'btn_to-playstore'))).click()
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '/html/body/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[1]/div/h1/span')))
    assert driver.find_element(By.XPATH, '/html/body/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[1]/div/h1/span').text == 'Populix'

def test_appStoreButton(driver):
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.ID, 'btn_to-appstore'))).click()
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/main/div[2]/section[1]/div/div[2]/header/h1')))
    assert driver.find_element(By.XPATH, '/html/body/div[5]/main/div[2]/section[1]/div/div[2]/header/h1').text == 'Populix 4+'