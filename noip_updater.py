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
            self.driver = webdriver.Firefox(executable_path=settings.get("webdriver_path"))
        
        elif settings.get("pref_webdriver").lower() == "chrome":
            self.driver = webdriver.Chrome(executable_path=settings.get("webdriver_path"))

    # Logs in to NoIP
    def login(self):
        pass

    
    # Navigates to confirmation page
    def navigate_to_confirmation_page(self):
        pass


    # Confirms host name
    def confirm_hostname(self):
        pass

    
    # Gets host name from the NoIP panel
    def get_hostname(self):
        return ""

    
    # Sends email and sms notification
    def send_notification(self, email=False, sms=False, to_email="", to_number="", msg_head="", msg_body=""):
        pass

# Contains the main logic of the program and creates an instance object of the Updater class and uses its methods
def main():
    noip_username, noip_password, twilio_sid, twilio_auth_token = read_creds()

    # Creating noip_updater object
    noip_updater = Updater("https://www.noip.com/", noip_username, noip_password, twilio_sid, twilio_auth_token)

    noip_updater.login()
    noip_updater.navigate_to_confirmation_page()
    noip_updater.confirm_hostname()
    hostname = noip_updater.get_hostname()
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