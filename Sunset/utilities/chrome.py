from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from win32api import GetSystemMetrics
from selenium import webdriver
from utilities import log
import os

current_proxy = 0
use_proxy = False
proxy_list = []
timeout = 0

def start(driver_version):
    driver_directory = os.getenv("appdata") + f"/Sunset/drivers/{driver_version}.exe"

    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument("--log-level=OFF")
    driver_options.add_experimental_option("prefs", {
        "credentials_enable_service" : False,
        "profile.password_manager_enabled" : False
    })
    driver_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    if len(proxy_list) != 0 and use_proxy:
        global current_proxy
        proxy = proxy_list[current_proxy]
        driver_options.add_argument(f"--proxy-server={proxy}")
    
    size = (450, 600)
    position = (round(GetSystemMetrics(0) / 2 - size[0] / 2), round(GetSystemMetrics(1) / 2 - size[1] / 2))
    
    try:
        driver = webdriver.Chrome(executable_path=driver_directory, options=driver_options)
    except Exception as data:
        log.crash(data)
        exit()
    driver.set_window_position(position[0], position[1])
    driver.set_window_size(size[0], size[1])

    return driver

def wait_for_element(driver, id):
    try:
        return WebDriverWait(driver, timeout).until(expected_conditions.visibility_of_element_located((By.ID, id)))
    except Exception as data:
        log.crash(data)
        exit()

def is_displayed(driver, id):
    try:
        WebDriverWait(driver, 5).until(expected_conditions.visibility_of_element_located((By.ID, id)))
        return True
    except:
        return False

def get_proxies():
    global proxy_list
    with open("proxies.txt") as proxies_file:
        proxy_list = proxies_file.readlines()
        proxies_file.close()
