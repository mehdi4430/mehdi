def hajamooo(phone):
    """
    تابع برای ارسال کد تأیید از سایت hajamooo.ir
    شماره باید بدون صفر و بدون +98 باشد: 9173644430
    """
    import requests
    import random
    import string

    # تبدیل شماره از +989... به 9...
    digits_phone = phone.replace("+98", "")  

    # تولید یک nounce/csrf تصادفی (ممکنه نیاز به مقدار واقعی داشته باشه)
    random_nounce = ''.join(random.choices(string.hexdigits.lower(), k=10))

    url = "https://hajamooo.ir/wp-admin/admin-ajax.php"
    
    payload = {
        "action": "digits_check_mob",
        "countrycode": "+98",
        "mobileNo": digits_phone,
        "csrf": random_nounce,
        "login": "1",
        "username": "",
        "email": "",
        "captcha": "",
        "captcha_ses": "",
        "digits": "1",
        "json": "1",
        "whatsapp": "0",
        "mobmail": digits_phone,  # معمولاً همون mobileNo هست
        "dig_otp": "",
        "dig_nounce": random_nounce
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9,fa;q=0.8",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://hajamooo.ir",
        "Referer": "https://hajamooo.ir/",  # صفحه اصلی سایت
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            response_data = response.json()
            
            # بررسی ساختار پاسخ موفق
            if response_data.get("success") is True:
                print(f'{g}(hajamooo) {a}Code Sent')
                return True
            else:
                error_msg = response_data.get("message", "Unknown error")
                print(f'{r}[-] (hajamooo) Failed: {error_msg}{a}')
                return False
        else:
            print(f'{r}[-] (hajamooo) HTTP Error: {response.status_code}{a}')
            return False

    except Exception as e:
        print(f'{r}[!] hajamooo Exception: {e}{a}')
        return False
