
url = str(input("URL ~ "))
print('\n' * 300)

endinfo = []
if 'http://' in url:
    pass
elif 'https://' in url:
    pass
else:
    url = 'https://' + url

import os; os.system('cls')
banner = """\033[38;5;89m 
╔═════════════════════════════════════════════════════════════════════════════╗\033[38;5;125m 
║ .d8888b.           d8b                  .d8888b.                            ║\033[38;5;126m 
║d88P  Y88b          Y8P                 d88P  Y88b                           ║\033[38;5;162m 
║Y88b.                                   Y88b.                                ║\033[38;5;163m 
║ "Y888b.   88888b.  888  .d8888b .d88b.  "Y888b.    .d8888b  8888b.  88888b. ║\033[38;5;164m 
║    "Y88b. 888 "88b 888 d88P"   d8P  Y8b    "Y88b. d88P"        "88b 888 "88b║\033[38;5;165m
║      "888 888  888 888 888     88888888      "888 888      .d888888 888  888║\033[38;5;201m 
║Y88b  d88P 888 d88P 888 Y88b.   Y8b.    Y88b  d88P Y88b.    888  888 888  888║\033[38;5;165m 
║ "Y8888P"  88888P"  888  "Y8888P "Y8888  "Y8888P"   "Y8888P "Y888888 888  888║\033[38;5;164m 
║           888                                                               ║\033[38;5;163m 
║           888                                                               ║\033[38;5;162m 
║           888                                                               ║\033[38;5;126m 
╚═════════════════════════════════════════════════════════════════════════════╝\033[38;5;26m 
                         // Created By SpiceSouls //\033[0m             
"""
print(banner)
print("!!! I AM NOT RESPONSIBLE FOR ANY USE OF THIS TOOL, IT IS FOR EDUCATIONAL PURPOSES !!!\n\n")
print(f'                          \033[38;5;201m- {url} -\033[0m')
def green(message):
    print(f'[\u001b[32m+\u001b[0m] {message}')
def yellow(message):
    print(f'[\u001b[33m?\u001b[0m] {message}')
def red(message):
    print(f'[\u001b[31mx\u001b[0m] {message}')

# Checking Packages

yellow('Checking Packages...')
try:
    import requests
    from scapy.all import *
    from scapy.layers.inet import IP, ICMP
    import time
    import socket
    import threading
    from queue import Queue
    import sys
except:
    red('Packages partially/fully missing, have you installed the requirements?')
    exit()

green('Packages collected!')
validdirs = []
bads = [404, 400, 401, 402, 403]
def check(url, extension):
    r = requests.get(url + '/' + extension)
    if r.status_code in bads:
        red(f'/{extension} [{str(r.status_code)}]')
    else:
        green(f'/{extension} [{str(r.status_code)}]')
        validdirs.append(extension)




print('\n\n')
yellow('Starting Scan...')
time.sleep(1)

### SCANNING ###
## Machine

# IP
yellow('Attempting to resolve domain IP...')
urlraw = url.replace('http://', '')
urlraw = urlraw.replace('https://', '')
ipaddr = socket.gethostbyname(urlraw)
green(f'Success! {str(ipaddr)}\n')
endinfo.append(f'Domain - {urlraw}')
endinfo.append(f'IP - {str(ipaddr)}')
# OS
yellow('Attempting to fingerprint the OS...')
pack = IP(dst=ipaddr)/ICMP()
resp = sr1(pack, timeout=2)

if resp == None:
    red('No Response. Moving on.')
    endinfo.append('OS - Unknown')
elif IP in resp:
    if resp.getlayer(IP).ttl <= 64:
        green('Suspected Server OS: Linux\n')
        endinfo.append('OS - Possibly Linux')
    else:
        green('Suspected Server OS: Windows\n')
        endinfo.append('OS - Possibly Windows')



# Ports
yellow('Attempting to scan ports...\n')
openports = []
try:
    print_lock = threading.Lock()
    def portscan(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            con = s.connect((ipaddr, port))
            with print_lock:
                green(f'Port Discovered: {port}')
                openports.append(f'Open Port - {port}')
                con.close()
        except:
            pass
    def threader():
        while True:
            worker = q.get()
            portscan(worker)
            q.task_done()
    q = Queue()
    for x in range(1000):
         t = threading.Thread(target=threader)
         t.daemon = True
         t.start()
    start = time.time()
    for worker in range(1, 250):
        q.put(worker)
    q.join()
except KeyboardInterrupt:
    pass
print('\n\n')
green('Port Scanning Finished.\n\n')

## Web Dirs
# Robots.txt
yellow('Checking for robots.txt')
check(url, 'robots.txt')
r = requests.get(url, '/robots.txt')
if 'sitemap' in r.text:
    for line in r.text.splitlines():
        if 'Sitemap:' in line:
            print(line.replace('Sitemap: ', ''))
            break

# Humans.txt #
yellow('Checking for humans.txt')
check(url, 'humans.txt')

# TESTING KEYWORDS #
yellow('Checking for generic directories')
dir = ['api', 'API', 'src', 'source', 'js', 'java', 'python', 'html', 'db', 'sql', 'cfg', 'config', 'requests', 'login', 'admin']

for item in dir:
    check(url, item)

# DIR LIST #

try:
    with open('directory_list.txt', 'r') as f:
        lines = f.readlines()
        linecount = len(lines)
        print(f'\n--- Going Through directory_list.txt - Lines: {linecount} - Press CNTRL + C To Move On At Any Time ---\n')
        for line in lines:
            check(url, line[:-1])
except KeyboardInterrupt:
    print('\n' * 1000)
    


### RESULTS

banner = """\033[38;5;89m 
╔═════════════════════════════════════════════════════════════════════════════╗\033[38;5;125m 
║ .d8888b.           d8b                  .d8888b.                            ║\033[38;5;126m 
║d88P  Y88b          Y8P                 d88P  Y88b                           ║\033[38;5;162m 
║Y88b.                                   Y88b.                                ║\033[38;5;163m 
║ "Y888b.   88888b.  888  .d8888b .d88b.  "Y888b.    .d8888b  8888b.  88888b. ║\033[38;5;164m 
║    "Y88b. 888 "88b 888 d88P"   d8P  Y8b    "Y88b. d88P"        "88b 888 "88b║\033[38;5;165m
║      "888 888  888 888 888     88888888      "888 888      .d888888 888  888║\033[38;5;201m 
║Y88b  d88P 888 d88P 888 Y88b.   Y8b.    Y88b  d88P Y88b.    888  888 888  888║\033[38;5;165m 
║ "Y8888P"  88888P"  888  "Y8888P "Y8888  "Y8888P"   "Y8888P "Y888888 888  888║\033[38;5;164m 
║           888                                                               ║\033[38;5;163m 
║           888                                                               ║\033[38;5;162m 
║           888                                                               ║\033[38;5;126m 
╚═════════════════════════════════════════════════════════════════════════════╝\033[38;5;26m 
                         // Created By SpiceSouls //\033[0m             
"""
print(banner)
print("                       !!! RESULTS !!!\n\n")
print(f'                          \033[38;5;201m- {url} -\033[0m')
print('\n--- Basic Information ---')
for item in endinfo:
    green(item)
print('\n--- Open Ports ---')
for item in openports:
    green(item)
print('\n--- Discovered Directories ---')
for item in validdirs:
    green('/' + item)
