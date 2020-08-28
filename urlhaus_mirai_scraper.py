# this scraper is made by checksum (0xchecksum on github)
# i just added something that checks if port 3306

import socket, requests, colorama

from colorama import Fore

ips = []

def Log(txt:str):
    '''
    sexy logs
    '''
    print(f"[{Fore.BLUE}+{Fore.RESET}] {txt}")


def CheckMysql(ip:str):
    '''
    connect to the ip with 3306 port
    '''

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2) # man fuck ur waiting

    try:
        s.connect((ip,3306))
        return True

    except:
        return False


def main():
    Log("Starting scraper.")

    try:
        res = requests.get('https://urlhaus.abuse.ch/downloads/csv_recent/')

        for line in res.text.split('\n'):
            if not "mirai" in line.lower():
                continue

            ip = line.split(",")[2].split("://")[1].split("/")[0]

            if ip.count(".") != 4:
                try:
                    ip = socket.gethostbyname(ip)
                except:
                    continue
            
            if ip in ips:
                continue

            if not CheckMysql(ip):
                continue

            ips.append(ip)

            Log(f"Scraped valid ip [{ip}]")
    except:
        pass




if __name__ == "__main__":
    main()