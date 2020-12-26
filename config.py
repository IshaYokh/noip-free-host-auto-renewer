# Author: @IshaYokh

"""
    This module contains a dictionary object that holds some settings as keys and their values.
    Explanation of what each key is for:
        - noip_username_env_var_id - this key must have the enviroumental variable name that was used to store the NoIP account username as a value
        - noip_password_env_var_id - this key must have the enviroumental variable name that was used to store the NoIP account password as a value
        
        - hostnames - This key holds a list of hostnames that need to be confirmed on NoIP, the list should look like the following:
          ["example1.com", "example2.com", "example3.com"]
        
        - twilio_account_sid_env_var_id - this key must have the enviroumental variable name that was used to store the twilio account SID
          (leave empty if sms won't be used)
        
        - twilio_auth_token_env_var_id - this key must have the enviroumental variable name that was used to store the twilio account authentication token
          (leave empty if sms won't be used)
        - pref_webdriver - Firefox or Chrome to be the value of this key
        - webdriver_path - system path to the executable web driver that is compatible with your system
        - send_email - must be True if the preferred notification method is via emails
        - send_sms - must be True if the preferred notification method is via sms
        - notification_receiver_number - this key must have the user's number as a value (if sms is being used)
        - notification_receiver_email - this key must have the user's email as a value (if email is being used)
        - update_schedule - This key must hold how frequent the script should run in Days (must be in Days) Default is every 30 days
        - message_head - SMS or Email message head when notification is sent
        - message_body - SMS or Email message body when notification is sent
"""

settings = {
    "noip_username_env_var_id":"",
    "noip_password_env_var_id":"",
    "hostnames":[],
    "twilio_account_sid_env_var_id":"",
    "twilio_auth_token_env_var_id":"",
    "pref_webdriver":"",
    "webdriver_path":"",
    "send_email":False,
    "send_sms":False,
    "notification_receiver_number":"",
    "notification_receiver_email":"",
    "update_schedule":"30",
    "message_head":"NoIP hostname confirmation updated",
    "message_body":"Your hostname {hostname} confirmation has been updated on NoIP"
}

# Author: @IshaYokh