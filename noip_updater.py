# Author: @IshaYokh

"""
    This is the main module that contains the main code to run the web driver,
    login to noip and update the host confirmation
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import time
import sys
import smtplib
from email.message import EmailMessage
from twilio.rest import Client
from config import settings
import os
import socket

# Updater class that contains the methods to run the web driver and handle website interaction
class Updater:
    def __init__(self, url, username, password, twilio_account_sid="", twilio_auth_token="", gmail_username="", gmail_password=""):
        self.url = url
        self.username = username
        self.password = password
        self.twilio_account_sid = twilio_account_sid
        self.twilio_auth_token = twilio_auth_token
        self.gmail_username = gmail_username
        self.gmail_password = gmail_password

        """
            Empty failed_hostnames list to be later used to store hostnames that were not updated
            because of some issues
        """
        self.failed_hostnames = []
        
        # Checking if firefox or chrome has been chosen in the settings and running selected web driver
        if settings.get("pref_webdriver").lower() == "firefox":
            try:
                print("[*] Launching Firefox")
                self.driver = webdriver.Firefox()
            except:
                print("""[X] Something went wrong with initialising the firefox web driver,
                        make sure the executable web driver for firefox has been added to
                        PATH in your system
                """)
                
                sys.exit()
        
        elif settings.get("pref_webdriver").lower() == "chrome":
            try:
                print("[*] Launching Chrome")
                self.driver = webdriver.Chrome()
            except:
                print("""[X] Something went wrong with initialising the chrome web driver,
                        make sure the executable web driver for chrome has been added to
                        PATH in your system
                """)

                sys.exit()

        else:
            print("[X] Given web browser name in settings is not recognised must be either firefox or chrome")
            sys.exit()

    # Logs in to NoIP main panel
    def login(self):
        print("[*] Logging in to NoIP panel")

        # Launches the web browser and navigates to noip main page using the driver object that was initialised earlier and the get method
        self.driver.get(self.url)
        time.sleep(3)

        # Finding the login button by link text name and clicking it to bring up the login menu
        login_button = self.driver.find_element_by_link_text("Sign In")
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
    
    # Navigates to confirmation page
    def navigate_to_confirmation_page(self, hostname, hostnames_counter):
        print("[*] Updating " + hostname)

        time.sleep(5)

        # Navigating to dynamic dns page
        self.driver.get("https://my.noip.com/#!/dynamic-dns")

        time.sleep(10)

        """
            Looking for the given hostname in settings on the web page and 
            validating if it exists
        """
        try:
            hostname_link = self.driver.find_element_by_link_text(hostname)
        except NoSuchElementException:
            self.failed_hostnames.append(hostname)
            return self.failed_hostnames

        self.confirm_hostname(hostname, hostnames_counter)

    # Confirms each hostname by clicking on confirm button
    def confirm_hostname(self, hostname, hostnames_counter):
        confirm_button = self.driver.find_element_by_xpath("//*[@id=\"host-panel\"]/table/tbody/tr[{tr_num}]/td[5]/button".format(tr_num=hostnames_counter))
        confirm_button.click()

    # Closes web driver/browser and clears all cookies
    def close(self):
        print("[*] Closing web driver")

        time.sleep(3)

        self.driver.delete_all_cookies()
        self.driver.quit()
    
    # Sends email and sms notification
    def send_notification(self, from_email="", to_email="", from_number="", to_number="", msg_head="", msg_body=""):
        print("[*] Sending update notification")

        # Validating if the user has chosen email option and sending email using EmailMessage() and smtplib
        if settings.get("send_email"):
            msg = EmailMessage()
            msg["Subject"] = msg_head
            msg["From"] = from_email
            msg["To"] = to_email
            msg.set_content(msg_body)

            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    try:
                        smtp.login(self.gmail_username, self.gmail_password)
                        smtp.send_message(msg)
                    except smtplib.SMTPAuthenticationError:
                        print( "[X] Error sending email - check receiver email or sender email and password\n\t \
                                [!] Make sure less secure apps is enabled on the sender email\n\t \
                                [!] Make sure you haven't been blocked")
            
            except socket.gaierror:
                print("[X] Error sending email - check your internet connection")

        # Validating if the user has chosen sms option and sending sms using twilio API
        if settings.get("send_sms"):
            twilio_client = Client(self.twilio_account_sid, self.twilio_auth_token)
            twilio_client.messages \
                .create(
                    body = msg_body,
                    from_= from_number,
                    to = to_number
                )

# Contains the main logic of the program and creates an instance object of the Updater class and uses its methods
def main():
    # Failed hostnames list for hostnames that were not updated
    failed_hostnames = []
    # Email message variable that will be given the message accordingly
    email_message = "The following hostnames have been sucessfuly updated:"

    # Validating settings before creating an Updater object
    validate_settings()

    noip_username, noip_password, twilio_sid, twilio_auth_token, gmail_username, gmail_password = read_creds()

    # Creating noip_updater object
    noip_updater = Updater("https://www.noip.com/", noip_username, noip_password, twilio_sid, twilio_auth_token, gmail_username, gmail_password)

    try:
        noip_updater.login()
    except WebDriverException:
        print("[X] Unable to connect to NoIP, check your internet connection")
        sys.exit()

    # Iterating through the given hostnames in settings
    hostnames_counter = 1
    for hostname in settings.get("hostnames"):
        failed_hostnames = noip_updater.navigate_to_confirmation_page(hostname, hostnames_counter)

        # Constructing email message that will be sent to the user based on sucessful/failed hostname updates
        if failed_hostnames:
            counter = 1
            email_message = "The following hostnames were not updated during the NoIP hostnames update:"
            
            for hostname in failed_hostnames:
                email_message += "\n\t{counter}. {hostname}".format(counter=counter, hostname= hostname)
                counter += 1

        else:
            email_message += "\n\t {hostname}".format(hostname=hostname)
        
        hostnames_counter += 1
    
    # Validating preferred notification method from settings
    if settings.get("send_sms") or settings.get("send_email"):
        # Sending notification
        noip_updater.send_notification( settings.get("notification_sender_email"), 
        settings.get("notification_receiver_email"), settings.get("notification_sender_number"),
        settings.get("notification_receiver_number"),
        settings.get("message_head"), email_message
        )
        
    # Closing web browser
    noip_updater.close()

# Uses the values from keys that are stored in the settings dict object to read environmental variables
def read_creds():
    # Reading environmental variables that are needed for authentication
    try:
        noip_username = os.environ[settings.get("noip_username_env_var_id")]
    except KeyError:
        print("[X] Unable to find environmental variable \"{env_var}\" for NoIP username".format(env_var=settings.get("noip_username_env_var_id")))
        sys.exit()
    
    try:
        noip_password = os.environ[settings.get("noip_password_env_var_id")]
    except KeyError:
        print("[X] Unable to find environmental variable \"{env_var}\" NoIP password".format(env_var=settings.get("noip_password_env_var_id")))
        sys.exit()

    try:
        twilio_sid = os.environ[settings.get("twilio_account_sid_env_var_id")]
    except KeyError:
        print("[X] Unable to find environmental variable \"{env_var}\" for twilio account SID".format(env_var=settings.get("twilio_account_sid_env_var_id")))
        twilio_sid = ""
    
    try:
        twilio_auth_token = os.environ[settings.get("twilio_auth_token_env_var_id")]
    except KeyError:
        print("[X] Unable to find environmental variable \"{env_var}\" for twilio authentication token".format(env_var=settings.get("twilio_auth_token_env_var_id")))
        twilio_auth_token = ""

    try:
        gmail_username = os.environ[settings.get("gmail_username_env_var_id")]
    except KeyError:
        print("[X] Unable to find environmental variable \"{env_var}\" for gmail username".format(env_var=settings.get("gmail_username_env_var_id")))
        gmail_username = ""

    try:
        gmail_password = os.environ[settings.get("gmail_password_env_var_id")]
    except KeyError:
        print("[X] Unable to find environmental variable \"{env_var}\" for gmail password".format(env_var=settings.get("gmail_password_env_var_id")))
        gmail_password = ""

    return noip_username, noip_password, twilio_sid, twilio_auth_token, gmail_username, gmail_password


# Validates values in the settings object and displays message/errors accordingly
def validate_settings():
    if not settings.get("noip_username_env_var_id") and not settings.get("noip_password_env_var_id"):
        print("[X] NoIP username or password could not be found using the environmental variables given in settings")
        sys.exit()
    
    if not settings.get("hostnames"):
        print("[X] No domain names found in settings, you must add at least one")
        sys.exit()

    if settings.get("pref_webdriver").lower() != "firefox" and settings.get("pref_webdriver").lower() != "chrome":
        print("[X] The preferred web browser specified in settings was not recognised, must be firefox or chrome")
        sys.exit()

    if settings.get("send_email") and not settings.get("gmail_username_env_var_id") and not settings.get("gmail_password_env_var_id") or not settings.get("send_email") and \
    settings.get("gmail_username_env_var_id") and settings.get("gmail_password_env_var_id"):
        print(""" [X] send_email function is enabled in settings but no credentials for gmail were provided, or it has been disabled and credentials are provided, 
        set send_email to false if there are no gmail credentials, remove the credentials if it is already on false, or set it to true and provide email credentials to use the email function """)
        sys.exit()
    
    if settings.get("send_sms") and not settings.get("twilio_account_sid_env_var_id") and not settings.get("twilio_auth_token_env_var_id") or not settings.get("send_sms") and \
    settings.get("twilio_account_sid_env_var_id") and settings.get("twilio_auth_token_env_var_id"):
        print(""" [X] send_sms function is enabled in settings but no credentials for twilio were provided, or it has been disabled and credentials are provided,
        set send_sms to false if there are no twilio credentials, remove the credentials if it is already on false, or set it to true and provide twilio credentials to use the sms function""")
        sys.exit()

    if settings.get("send_email") and settings.get("gmail_username_env_var_id") and not settings.get("gmail_password_env_var_id") or settings.get("send_email") and settings.get("gmail_password_env_var_id") and \
    not settings.get("gmail_username_env_var_id"):
        print("[X] Gmail username has been provided but password is missing or vice versa")
        sys.exit()

    if settings.get("send_sms") and settings.get("twilio_account_sid_env_var_id") and not settings.get("twilio_auth_token_env_var_id") or settings.get("send_sms") and settings.get("twilio_auth_token_env_var_id") and \
    not settings.get("twilio_account_sid_env_var_id"):
        print("[X] Twilio account SID has been provided but authentication token is missing or vice versa")
        sys.exit()

    if settings.get("send_email"):
        if not settings.get("notification_sender_email") or not settings.get("notification_receiver_email"):
            print("[X] send_email function has been enabled but email addresses are missing")
            sys.exit()

    if settings.get("send_sms"):
        if not settings.get("notification_sender_number") or not settings.get("notification_receiver_number"):
            print("[X] send_sms function has been enabled but phone numbers are missing")
            sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass


# Author: @IshaYokh