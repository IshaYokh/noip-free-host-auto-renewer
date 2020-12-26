# Author: @IshaYokh

"""
    This is the main module that contains the main code to run the web driver,
    login to noip and update the host confirmation
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
import smtplib
from email.message import EmailMessage
from twilio.rest import Client
from config import settings
import os

# Updater class that contains the methods to run the web driver and handle website interaction
class Updater:
    def __init__(self, url, username, password, twilio_account_sid="", twilio_auth_token=""):
        self.url = url
        self.username = username
        self.password = password
        self.twilio_account_sid = twilio_account_sid
        self.twilio_auth_token = twilio_auth_token
        
        # Checking if firefox or chrome has been chosen in the settings and running selected web driver
        if settings.get("pref_webdriver").lower() == "firefox":
            self.driver = webdriver.Firefox()
        
        elif settings.get("pref_webdriver").lower() == "chrome":
            self.driver = webdriver.Chrome()

    # Logs in to NoIP main panel
    def login(self):
        # Launches the web browser and navigates to noip main page using the driver object that was initialised earlier and the get method
        self.driver.get(self.url)
        time.sleep(3)

        # Finding the login button by link text name and clicking it to bring up the login menu
        login_button = self.driver.find_element_by_link_text("Log In")
        login_button.send_keys(Keys.RETURN)

        # Finding username and password fields in the login box by name
        login_username_field = self.driver.find_element_by_name("username")
        login_password_field = self.driver.find_element_by_name("password")

        time.sleep(1)

        # Clearing text fields in case there is any text in them
        login_username_field.clear()
        login_password_field.clear()

        # Inserting the username and password
        login_username_field.send_keys(self.username)
        login_password_field.send_keys(self.password)

        time.sleep(1)

        # Logging in by sending RETURN in the password field
        login_password_field.send_keys(Keys.RETURN)
    
    # Navigates to confirmation page and confirms hostname
    def navigate_to_confirmation_page_and_confirm(self, hostname):
        time.sleep(5)

        # Navigating to dynamic dns page
        self.driver.get("https://my.noip.com/#!/dynamic-dns")

        time.sleep(10)

        # Clicking on the selected hostname/hostnames to bring up the hostname update menu
        hostname_link = self.driver.find_element_by_link_text(hostname)
        hostname_link.click()

        time.sleep(3)

        # Confirming hostname
        hostname_update_button = self.driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[4]/div/div/div/div[4]/button[1]/div")
        self.driver.maximize_window()
        time.sleep(3)
        hostname_update_button.click()

    
    # Sends email and sms notification
    def send_notification(self, email=False, sms=False, to_email="", to_number="", msg_head="", msg_body=""):
        pass

# Contains the main logic of the program and creates an instance object of the Updater class and uses its methods
def main():
    noip_username, noip_password, twilio_sid, twilio_auth_token = read_creds()

    # Creating noip_updater object
    noip_updater = Updater("https://www.noip.com/", noip_username, noip_password, twilio_sid, twilio_auth_token)

    noip_updater.login()

    # Iterating through the given hostnames in settings
    for hostname in settings.get("hostnames"):
        noip_updater.navigate_to_confirmation_page_and_confirm(hostname)

    noip_updater.send_notification(settings.get("send_email"), settings.get("send_sms"),
    settings.get("notification_receiver_email"), settings.get("notification_receiver_number"),
    settings.get("message_head"), settings.get("message_body")
    )

# Uses the values from keys that are stored in the settings dict object to read environmental variables
def read_creds():
    # Reading environmental variables that are needed for authentication
    noip_username = os.environ[settings.get("noip_username_env_var_id")]
    noip_password = os.environ[settings.get("noip_password_env_var_id")]
    twilio_sid = os.environ[settings.get("twilio_account_sid_env_var_id")]
    twilio_auth_token = os.environ[settings.get("twilio_auth_token_env_var_id")]

    return noip_username, noip_password, twilio_sid, twilio_auth_token


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass


# Author: @IshaYokh