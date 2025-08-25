from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import time

# شماره موبایل
phone = "9173644430"

# تنظیمات کروم بدون GUI
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)

try:
    # 1️⃣ باز کردن صفحه ورود
    driver.get("https://ilozi.com/?login=true")

    time.sleep(2)  # صبر برای لود شدن کامل

    # 2️⃣ استخراج مقادیر داینامیک
    instance_id = driver.find_element(By.NAME, "instance_id").get_attribute("value")
    digits_form = driver.find_element(By.NAME, "digits_form").get_attribute("value")
    wp_referer = driver.find_element(By.NAME, "_wp_http_referer").get_attribute("value")

    print("instance_id:", instance_id)
    print("digits_form:", digits_form)
    print("_wp_http_referer:", wp_referer)

finally:
    driver.quit()

# 3️⃣ ارسال درخواست POST واقعی
url = "https://ilozi.com/wp-admin/admin-ajax.php"

payload = {
    "login_digt_countrycode": "+98",
    "digits_phone": phone,
    "action_type": "phone",
    "sms_otp": "",
    "otp_step_1": "1",
    "digits_otp_field": "1",
    "digits": "1",
    "instance_id": instance_id,
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
    "digits_form": digits_form,
    "_wp_http_referer": wp_referer,
    "show_force_title": "1",
    "container": "digits_protected",
    "sub_action": "sms_otp"
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0"
}

response = requests.post(url, data=payload, headers=headers)
print(response.json())
