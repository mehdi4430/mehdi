import requests

def ilozi(phone):
    url = "https://ilozi.com/wp-admin/admin-ajax.php"
    payload = {
        "login_digt_countrycode": "+98",
        "digits_phone": phone,  # شماره بدون صفر و بدون +98
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
        "show_force_title": "1",
        "otp_resend": "true",
        "container": "digits_protected",
        "sub_action": "sms_otp"
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        r = requests.post(url, data=payload, headers=headers, timeout=5)
        if r.status_code == 200 and r.json().get("success"):
            print(f"{g}(Ilozi) {a}Code Sent")
            return True
        else:
            print(f"{r}[-] (Ilozi) Failed or No Response{a}")
            return False
    except Exception as e:
        print(f"{r}[!] Ilozi Exception: {e}{a}")
        return False
