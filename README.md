# noip-free-host-auto-renewer

## Table of contents:
- [DISCLAIMER](#DISCLAIMER)
- [Description](#Description)
- [How it works](#How-it-works)
- [Requirements](#Requirements)
- [Usage guide](#Usage-guide)
- [Running the script](#Running-the-script)
- [Running with headless mode](#Running-with-headless-mode)
- [LICENCE](#LICENCE)
- [Author](#Author)


## DISCLAIMER:
**THE SCRIPT WAS WRITTEN FOR EDUCATIONAL PURPOSES ONLY, THE AUTHOR DOES NOT HAVE ANY MALICIOUS INTENTIONS TOWARDS noip.com, USE AT YOUR OWN RISK. IF YOU DO NOT WANT TO CONFIRM YOUR HOSTNAMES MANUALLY, PLEASE GET THE PAID SUBSCRIPTION FROM noip.com**

## Description:
noip.com provides up to 3 free hostnames, but each must be confirmed manually by logging in to the panel monthly. This tool automatically confirms the hostnames that you defined in the settings based on a time that you defined, typically, every 30 days.

## How it works:
The tool uses selenium web drivers to automatically login to noip.com and confirm the hostnames and send a notification about hostnames that were successfully updated and those that were not updated due to an issue (notifications will be only sent if you choose so in the settings). All credentials, API keys, web driver preferred option, preferred notification method and other variables can be set in the settings (authentication details MUST NOT be stored in plain text, refer to Usage guide to find out how).

## Requirements:
- Linux/Unix based system or Windows
- Python3
- Pip3 (Python package manager)
- All libraries in requirements.txt which are selenium V3.141.0 and Twilio V6.46.0 (can be installed through pip, command depends on your operating system, "pip3 install -r requirements.txt" for Linux)
- Firefox or Chrome web driver executables (Must be compatible with your operating system)
    - URL for gecko webdriver (firefox): https://github.com/mozilla/geckodriver/releases
    - URL for chrome webdriver: https://chromedriver.chromium.org/downloads
- Access privilege to environmental variables and PATH in your system
- NoIP usersname and password
- At least one hostname registered with NoIP
- Gmail username and password (only required if email notification option is selected in settings)
- Twilio API key, authentication token, and a phone number (only required if SMS option is selected in settings)

## Usage guide:
The script's functionality will completely depend on the correct values defined in settings. Settings is a dictionary object initialised in the config.py module, it holds keys as a setting option and the value as a setting value that you will set, for example, "hostnames" variable holds a list value that will contain a list of string hostnames separated by a comma, ["example1.com", "example2.com"] and based on that, the script will confirm each hostname defined in that list during execution. NOTE: authentication details WILL NOT be written in plain text in config.py module for security purposes. Instead, you must store the authentication details in environmental variables in your system and then use the variable name as a value, for example, you store your NoIP username in an environmental variable called NOIP_USERNAME, then the value for "noip_username" key stored in settings will be "NOIP_USERNAME" (pointing to the real username value). Google how to define environment variables for your operating system if you are not sure how. Below is an explanation of all keys and what values they must hold. The explanation is also provided in the config.py module to make it easier to refer to it while storing values in settings.

**NOTE: The firefox or chrome web driver executable MUST be stored in PATH for the script to work properly (Google how to do that for your operating system if you are not sure how)**

**NOTE: The script supports scheduling to autorun for next time based on the time provided in settings, but a more efficient way is to use a task scheduler program for Linux or windows and a couple of lines of bash scripting, in case you don't want the script to be running in a loop the whole time which is not efficient itself (in case you need to reboot your system). Set the value of "update_schedule" in settings to 0 if you use another task scheduling tool, such as the method mentioned earlier.**

**Explanation of what each key is for:**
- noip_username_env_var_id - this key must have the environmental variable name that was used to store the NoIP account username as a value
- noip_password_env_var_id - this key must have the environmental variable name that was used to store the NoIP account password as a value        
- hostnames - This key holds a list of hostnames that need to be confirmed on NoIP, the list should look like the following:
    - ["example1.com", "example2.com", "example3.com"]
        
- twilio_account_sid_env_var_id - this key must have the environmental variable name that was used to store the Twilio Account SID (leave empty if SMS won't be used)        
- twilio_auth_token_env_var_id - this key must have the environmental variable name that was used to store the Twilio account authentication token (leave empty if SMS won't be used)
- gmail_username_env_var_id - this key must have the environmental variable name that was used to store the Gmail username (leave empty if email won't be used)
- gmail_password_env_var_id - this key must have the environmental variable name that was used to store the Gmail password (leave empty if email won't be used)
- pref_webdriver - Firefox or Chrome to be the value of this key
- send_email - must be True if the preferred notification method is via emails
- send_sms - must be True if the preferred notification method is via SMS
- notification_sender_number - this key must have the sender's number as a value (leave empty if SMS won't be used)
- notification_sender_email - this key must have the sender's email as a value (leave empty if email won't be used)
- notification_receiver_number - this key must have the user's number as a value (leave empty if SMS won't be used)
- notification_receiver_email - this key must have the user's email as a value (leave empty if email won't be used)
- update_schedule - This key must hold how frequent the script should run in Days (must be in Days) Default is every 30 days - set to 0 if you don't want the script to run automatically
- message_head - SMS or Email message head when a notification is sent
- message_body - SMS or Email message body when a notification is sent

## Running the script:
After fully configuring and providing all required values in settings, the script can be simply run with the below commands in the terminal or CMD:

- Linux/Unix:
    - python3 noip_updater.py

- Windows:
    - python noip_updater.py

### Running with headless mode:
To run the script with headless mode, simply add --headless argument from the terminal or CMD:

- Linux/Unix:
    - python3 noip_updater.py --headless

- Windows:
    - python noip_updater.py --headless

## LICENCE:
***NOT FOR COMMERCIAL USE If you intened to use any of my code for commercial use please contact me and get my permission. If you intend to make money using any of my code please ask my permission***

## Author:
- [Isha Yokh](https://github.com/IshaYokh)
- Repo for the project: https://github.com/IshaYokh/noip-free-host-auto-renewer
