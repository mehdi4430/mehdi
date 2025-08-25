import requests

def ilozi_send_otp(phone_number):
    """
    تابع برای ارسال کد تأیید از سایت ilozi.com
    شماره تلفن باید بدون صفر و بدون پیش‌وند کشوری باشد: 9173644430
    """

    # URL endpoint ثابت برای AJAX requests در وردپرس
    url = "https://ilozi.com/wp-admin/admin-ajax.php"
    
    # Payload دقیق بر اساس درخواست استخراج شده از DevTools
    payload = {
        "login_digt_countrycode": "+98",
        "digits_phone": phone_number,  # شماره بدون صفر و بدون +98
        "action_type": "phone",
        "sms_otp": "",
        "otp_step_1": "1",
        "digits_otp_field": "1",
        "digits": "1",
        "instance_id": "6fb17492e0d343df4e533a9deb8ba6b9",  # این مقدار ممکن است ثابت نباشد و نیاز به استخراج دینامیک داشته باشد
        "action": "digits_forms_ajax",
        "type": "login",
        "digits_step_1_type": "",
        "digits_step_1_value": "",
        "digits_step_2_type": "",
        "digits_step_2_value": "",
        "digits_step_3_type": "",
        "digits_step_3_value": "",
        "digits_login_email_token": "",
        "digits_redirect_page": "https://ilozi.com/my-account/?action=register",
        "digits_form": "3780032f76",  # این مقدار ممکن است ثابت نباشد
        "_wp_http_referer": "/?login=true&redirect_to=https%3A%2F%2Filozi.com%2Fmy-account%2F%3Faction%3Dregister&page=2",
        "show_force_title": "1",
        "otp_resend": "true",         # کلید اصلی برای درخواست ارسال مجدد کد
        "container": "digits_protected",
        "sub_action": "sms_otp"       # زیر-اکشن تعیین کننده نوع درخواست
    }

    # Headers دقیق برای شبیه‌سازی درخواست مرورگر
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9,fa;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://ilozi.com",
        "Referer": "https://ilozi.com/?login=true&redirect_to=https%3A%2F%2Filozi.com%2Fmy-account%2F%3Faction%3Dregister&page=2",
        "X-Requested-With": "XMLHttpRequest",  # مشخص کننده درخواست AJAX
        "Connection": "keep-alive"
    }

    try:
        # ارسال درخواست POST
        response = requests.post(url, data=payload, headers=headers, timeout=15)
        
        # بررسی پاسخ سرور
        if response.status_code == 200:
            response_data = response.json()
            
            # بررسی ساختار پاسخ JSON
            if response_data.get('success') is True:
                print(f"✅ (ilozi) کد تأیید برای {phone_number} ارسال شد.")
                print(f"   پاسخ سرور: {response_data}")
                return True
            else:
                error_message = response_data.get('message', 'Unknown error (no message in response)')
                print(f"❌ (ilozi) خطا: {error_message}")
                print(f"   پاسخ کامل: {response_data}")
                return False
        else:
            print(f"❌ (ilozi) خطای HTTP: {response.status_code}")
            print(f"   متن پاسخ: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ (ilozi) خطای اتصال: امکان ارتباط با سرور وجود ندارد.")
        return False
    except requests.exceptions.Timeout:
        print("❌ (ilozi) درخواست timeout شد.")
        return False
    except Exception as e:
        print(f"❌ (ilozi) یک خطای غیرمنتظره رخ داد: {str(e)}")
        return False

# مثال استفاده از تابع
if __name__ == "__main__":
    # شماره تلفن باید بدون صفر و بدون +98 باشد: 913644430
    result = ilozi_send_otp("9173644430")  # شماره مثال از درخواست شما
    print(f"نتیجه نهایی: {result}")
