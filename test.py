from threading import Thread
from time import sleep
import requests

# ------------------------------
# Colors
# ------------------------------
r = '\033[31;1m'
g = '\033[32;1m'
y = '\033[33;1m'
p = '\033[35;1m'
a = '\033[0m'

# ------------------------------
# Slow print
# ------------------------------
def print_slow(text, delay=0.005):
    for char in text:
        print(char, end='', flush=True)
        sleep(delay)
    print()

# ------------------------------
# Ilozi SMS API Test
# ------------------------------
def ilozi_test(phone):
    url = "https://ilozi.com/wp-admin/admin-ajax.php"
    payload = {
        "login_digt_countrycode": "+98",
        "digits_phone": phone,
        "action_type": "phone",
        "digits": "1",
        "instance_id": "6fb17492e0d343df4e533a9deb8ba6b9",  # ممکن است تغییر کند
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
        "digits_form": "3780032f76",
        "_wp_http_referer": "/?login=true&redirect_to=https%3A%2F%2Filozi.com%2Fmy-account%2F%3Faction%3Dregister&page=2",
        "show_force_title": "1"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    session = requests.Session()
    try:
        session.get("https://ilozi.com", headers=headers, timeout=5)  # گرفتن کوکی اولیه
        resp = session.post(url, data=payload, headers=headers, timeout=5)
        if resp.status_code == 200 and ("success" in resp.text.lower() or "sent" in resp.text.lower()):
            print(f"{g}[+] Test SMS Sent to {phone}{a}")
        else:
            print(f"{y}[-] Request sent but response may not be successful{a}")
    except Exception as e:
        print(f"{r}[!] Exception: {e}{a}")

# ------------------------------
# Run multiple threads safely
# ------------------------------
def run_test(phone, delay=1, count=3):
    print_slow(f"{p}╔═════[ Ilozi SMS Test ]═════╗")
    print_slow(f"{g}Target: {y}{phone}")
    print_slow(f"{g}Delay between requests: {y}{delay}s")
    print_slow(f"{g}Total Attempts: {y}{count}")
    print_slow(f"{p}╚════════════════════════════╝")
    
    for i in range(count):
        Thread(target=ilozi_test, args=(phone,)).start()
        sleep(delay)

# ------------------------------
# Main
# ------------------------------
if __name__ == "__main__":
    phone = input("Enter your phone (e.g. 9173644430): ")
    run_test(phone, delay=1, count=3)
