import time
import os
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from urllib.parse import quote  # Uncomment line below to use python 3

from time import sleep

# update css selector if you have any issues
css_selector = "#main > footer > div._2lSWV._3cjY2.copyable-area > div > span:nth-child(2) > div > div._1VZX7 > div._3Uu1_ > div > div > p > span"

# message to be sent to everyone
# msg = '''
# Hello, this is a test message sent from a python script.
# '''


CURR_SCRIPT_PATH = os.path.dirname(sys.executable)

# DRIVER_PATH = CURR_SCRIPT_PATH + "chromedriver.exe"
DRIVER_PATH = "chromedriver.exe"


failed_list = []


def init_driver():
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    return driver


def read_numbers():
    phones = []
    with open('numbers.txt') as numbers_file:  # read input from numbers.txt file
        for line in numbers_file:
            line = line.strip()
            if len(line) <= 13:
                phones.append(str(line))

    return phones


def send_to_all(driver, msg, phones):
    global failed_list
    msg = quote(msg)  # url-encode the message, use other functios for handling dictionaries, not recommended

    for phone in phones:
        url = "https://web.whatsapp.com/send?phone=" + phone + "&text=" + msg
        print(f'Opening : {phone}')
        driver.get(url)
        TRIES = 200

        sleep(5)  # any delay is okay, even 0, but 3-5 seems appropriate
        for i in range(TRIES):
            try:
                driver.find_element(By.CSS_SELECTOR, css_selector).send_keys(Keys.RETURN)
                sleep(1)  # in new WA Web, instantly clicking enter keeps message in typing and discards it
                driver.execute_script("window.onbeforeunload = function() {};")  # disable alert
                print(f'Sent to : {phone}')
                break
            except:
                print("not yet")
                sleep(1)

        else:
            failed_list.append(phone)

    print("Done")

    if len(failed_list) == 0:
        print(f'Message successfully sent to all {len(phones)} numbers.')
    else:
        print(f'Message sent to all numbers EXCEPT:')
        for number in failed_list:
            print(number)


def open_whatsapp(driver):
    driver.get("https://web.whatsapp.com")
    time.sleep(5)
    # input("Scan the QR code and press any key to continue")


def main():
    phones = read_numbers()
    driver = init_driver()
    open_whatsapp(driver)
    send_to_all(driver, "Hello, this is a test message sent from a python script.", phones)
    driver.quit()


if __name__ == '__main__':
    main()

