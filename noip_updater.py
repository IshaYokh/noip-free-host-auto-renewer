# Author: @IshaYokh

"""
    This is the main module that contains the main code to run the web driver,
    login to noip and update the host confirmation
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
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
        print("[*] Updating " + hostname)

        time.sleep(5)

        # Navigating to dynamic dns page
        self.driver.get("https://my.noip.com/#!/dynamic-dns")

        time.sleep(10)

        """
            Clicking on the selected hostname/hostnames to bring up the hostname update menu 
            and validating if given hostname in settings exists on the panel
        """
        try:
            hostname_link = self.driver.find_element_by_link_text(hostname)
        except NoSuchElementException:
            self.failed_hostnames.append(hostname)
            return self.failed_hostnames

        hostname_link.click()

        time.sleep(3)

        # Confirming hostname
        hostname_update_button = self.driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[4]/div/div/div/div[4]/button[1]/div")

        time.sleep(3)

        hostname_update_button.click()

        # Validating if hostname wasn't updated sucessfully and adding the hostname to failed hostnames list if it failed
        if not self.validate_host_confirmation(hostname):
            self.failed_hostnames.append(hostname)
            print("[*] {hostname} wasn't updated sucessfully".format(hostname=hostname))
        else:
            print("[*] {hostname} updated sucessfully".fomrat(hostname=hostname))

        return self.failed_hostnames

    # Validates if the message of a sucessful host confirmation popped up
    def validate_host_confirmation(self, hostname):
        time.sleep(2)

        try:
            update_feedback_msg = self.driver.find_element_by_class_name("growl-message")
            return True

        except NoSuchElementException:
            return False

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

    noip_updater.login()

    # Iterating through the given hostnames in settings
    for hostname in settings.get("hostnames"):
        failed_hostnames = noip_updater.navigate_to_confirmation_page_and_confirm(hostname)

        # Constructing email message that will be sent to the user based on sucessful/failed hostname updates
        if failed_hostnames:
            counter = 1
            email_message = "The following hostnames were not updated during the NoIP hostnames update:"
            
            for hostname in failed_hostnames:
                email_message += "\n\t{counter}. {hostname}".format(counter=counter, hostname= hostname)
                counter += 1

        else:
            email_message += "\n\t {hostname}".format(hostname=hostname)
    
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
        print("[X] Unable to find environmental \"{env_var}\"".format(env_var=settings.get("noip_username_env_var_id")))
        sys.exit()
    
    try:
        noip_password = os.environ[settings.get("noip_password_env_var_id")]
    except KeyError:
        print("[X] Unable to find environmental \"{env_var}\"".format(env_var=settings.get("noip_password_env_var_id")))
        sys.exit()

    try:
        twilio_sid = os.environ[settings.get("twilio_account_sid_env_var_id")]
    except KeyError:
        print("[X] Unable to find environmental \"{env_var}\"".format(env_var=settings.get("twilio_account_sid_env_var_id")))
        sys.exit()
    
    try:
        twilio_auth_token = os.environ[settings.get("twilio_auth_token_env_var_id")]
    except KeyError:
        print("[X] Unable to find environmental \"{env_var}\"".format(env_var=settings.get("twilio_auth_token_env_var_id")))
        sys.exit()

    try:
        gmail_username = os.environ[settings.get("gmail_username_env_var_id")]
    except KeyError:
        print("[X] Unable to find environmental \"{env_var}\"".format(env_var=settings.get("gmail_username_env_var_id")))
        sys.exit()

    try:
        gmail_password = os.environ[settings.get("gmail_password_env_var_id")]
    except KeyError:
        print("[X] Unable to find environmental \"{env_var}\"".format(env_var=settings.get("gmail_password_env_var_id")))
        sys.exit()

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

    if not settings.get("send_email") and not settings.get("send_sms"):
        print("[X] Both values for twilio or/and gmail options were not set to true in settings, at least one must be selected, email/sms")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass


# Author: @IshaYokh