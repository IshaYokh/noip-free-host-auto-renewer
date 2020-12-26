# Author: @IshaYokh

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
import smtplib
from email.message import EmailMessage
from twilio.rest import Client
from config import settings


class Updater:
    def __init__(self, url, username, password, twillo_account_sid="", twillo_auth_token=""):
        pass


    def login(self):
        pass


    def navigate_to_confirmation_page(self):
        pass


    def confirm_hostname(self):
        pass


    def get_hostname(self):
        pass


    def send_notification(self, email=True, sms=True, to_email="", to_number="", msg_head="", msg_body=""):
        pass


def main():
    pass


def read_settings(settings):
    pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass


# Author: @IshaYokh
