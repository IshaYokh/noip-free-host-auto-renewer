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

# Updater class that contains the methods to run the web driver and
class Updater:
    def __init__(self, url, username, password, twilio_account_sid="", twilio_auth_token=""):
        self.url = url
        self.username = username
        self.password = password
        self.twilio_account_sid = twilio_account_sid
        self.twilio_auth_token = twilio_auth_token
        
        # Checking if firefox or chrome has been chosen in the settings and running selected web driver
        if "".lower() == "firefox":
            self.driver = webdriver.Firefox()
        
        elif "".lower() == "chrome":
            self.driver = webdriver.Chrome()

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
        pass

    
    # Sends email and sms notification
    def send_notification(self, email=False, sms=False, to_email="", to_number="", msg_head="", msg_body=""):
        pass

# Contains the main logic of the program and creates an instance object of the Updater class and uses its methods
def main():
    pass

# Reads the keys and values from the settings dict object that is imported from the config module
def read_settings(settings):
    pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass


# Author: @IshaYokh
