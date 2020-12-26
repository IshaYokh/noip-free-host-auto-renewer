# Author: @IshaYokh

"""
    This module contains a dictionary object that holds some settings as keys and their values.
    Explanation of what each key is for:
        - noip_username_env_var_id - this key must have the enviroumental variable name that was used to store the NoIP account username as a value
        - noip_password_env_var_id - this key must have the enviroumental variable name that was used to store the NoIP account password as a value
        - twilio_account_sid_env_var_id - this key must have the enviroumental variable name that was used to store the twilio account SID
          (leave empty if sms won't be used)
        
        - twilio_auth_token_env_var_id - this key must have the enviroumental variable name that was used to store the twilio account authentication token
          (leave empty if sms won't be used)
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
    "twilio_account_sid_env_var_id":"",
    "twilio_auth_token_env_var_id":"",
    "send_email":False,
    "send_sms":False,
    "notification_receiver_number":"",
    "notification_receiver_email":"",
    "update_schedule":"30",
    "message_head":"NoIP hostname confirmation updated",
    "message_body":"Your hostname {hostname} confirmation has been updated on NoIP"
}

# Author: @IshaYokh