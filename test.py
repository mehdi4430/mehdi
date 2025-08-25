import requests
from time import sleep
from threading import Thread

# رنگ‌ها
g = '\033[32;1m'
r = '\033[31;1m'
y = '\033[33;1m'
p = '\033[35;1m'
a = '\033[0m'

# تابع ارسال OTP از ilozi
def ilozi(phone):
    url = "https://ilozi.com/wp-admin/admin-ajax.php"
    payload = {
        "login_digt_countrycode": "+98",
        "digits_phone": phone,
        "action_type": "phone",
        "sms_otp": "",
        "otp_step_1": "1",
        "digits_otp_field": "1",
        "digits": "1",
        "instance_id": "6fb17492e0d343df4e533a9deb8ba6b9",
        "action": "digits_forms_ajax",
        "type": "login",
        "digits_redirect_page": "https://ilozi.com/my-account/?action=register",
        "digits_form": "3780032f76",
        "_wp_http_referer": "/?login=true&page=2",
        "show_force_title": "1",
        "otp_resend": "true",
        "container": "digits_protected",
        "sub_action": "sms_otp"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X)",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        if response.status_code == 200 and response.json().get("success"):
            print(f"{g}[+] Code sent to {phone}{a}")
            return True
        else:
            print(f"{y}[-] Failed or not sent: {phone}{a}")
            return False
    except Exception as e:
        print(f"{r}[!] Exception: {e}{a}")
        return False


