import os
from functions import *
import signal
import sys

try:
    import readline
except:
    pass  # readline not available


def signal_handler(sig, frame):
    print('Interrupt: use the "exit" or "quit"')


signal.signal(signal.SIGINT, signal_handler)

printBanner()

decorator = bcolors.OKCYAN + "[]> " + bcolors.ENDC
fileInfo = None
username_contains = None
dict = {}

while True:
    code = input(decorator)
    print("")

    args = code.split(" ")

    if args[0] == "exit" or args[0] == "quit":
        break

    elif args[0] == "":
        pass

    elif args[0] == "help":
        print(bcolors.WARNING + "help\t\t\t\t\tDisplay this help")
        print("exit/quit\t\t\t\tExit the program")
        print("back\t\t\t\t\tGo back from the function")
        print("")

        print("setfile\t\t\t\t\tSet the output file from secretsdump")
        print("setfileSecretsdump\t\t\tSet the output running secretsdump")
        print("")

        print("setUsernameContains\t\t\tSet the string in username you want to highlight (case insensitive)")
        print("removeHistory\t\t\t\tRemove history hashes from list")
        print(
            "repeated\t\t\t\tGet repeated hashes with his usernames. if you specify an argument, it will be the path where the hashes will be exported")
        print("")

        print("getUsernameByHash\t\t\tGet all usernames that have the same hash")
        print("getUsernameByPassword\t\t\tGet all usernames that have the same password")
        print("getUsernameByPasswordList\t\tGet all usernames that have the same password from a list")
        print("getUsernameByHashList\t\t\tGet all usernames that have the same hash from a list" + bcolors.ENDC)

    elif args[0].lower() == 'setfile':

        if len(args) == 2:
            if os.path.isfile(args[1]):
                file = args[1]
                dict = {}

                # file info in file variable
                f = open(file, "r")
                fileInfo = f.readlines()
                f.close()

                # create dict
                for line in fileInfo:
                    try:
                        if "$" not in line and "[*]" not in line and "31d6cfe0d16ae931b73c59d7e0c089c0" not in line:
                            split = line.split(":")
                            dict[split[0]] = split[3]
                    except:
                        pass

                file = file.split("/")[-1]
                print("File set to: " + file)
                decorator = (bcolors.OKCYAN + "[{}]> " + bcolors.ENDC).format(file)

            else:
                print(bcolors.FAIL + "File not found" + bcolors.ENDC)
        else:
            print(bcolors.FAIL + "Usage: SETFILE <file>" + bcolors.ENDC)

    elif args[0].lower() == 'setfilesecretsdump':

        if len(args) > 3:
            domain = args[1].lower()
            user = args[2].lower()
            password = args[3]
            dc_ip = args[4]
            os.system(
                f"python3 /opt/impacket/examples/secretsdump.py -just-dc {domain}/{user}:{password}@{dc_ip} > ntds_temp")

            if os.path.isfile("ntds_temp"):
                file = "ntds_temp"

                # file info in file variable
                f = open(file, "r")
                fileInfo = f.readlines()
                f.close()

                # create dict
                for line in fileInfo:
                    try:
                        if "$" not in line and "[*]" not in line and "31d6cfe0d16ae931b73c59d7e0c089c0" not in line:
                            split = line.split(":")
                            dict[split[0]] = split[3]
                            os.remove("ntds_temp")
                    except:
                        pass

                file = f"secretsdump - {domain}"
                print(bcolors.OKGREEN + "File set " + file + bcolors.ENDC)
                decorator = (bcolors.OKCYAN + "[{}]> " + bcolors.ENDC).format(file)

        else:
            print(bcolors.FAIL + "Usage: SETFILESECRETSDUMP <domain> <user> <password> <dc_ip>" + bcolors.ENDC)

    elif args[0].lower() == 'setusernamecontains':

        if len(args) > 1:
            username_contains = args[1].lower()
        else:
            print(bcolors.FAIL + "Usage: SETUSERNAMECONTAINS <string>" + bcolors.ENDC)

    elif args[0].lower() == 'removehistory':

        if fileInfo is not None:
            for line in fileInfo:
                try:
                    if "$" not in line and "_history" not in line:
                        split = line.split(":")
                        dict[split[0]] = split[3]
                except:
                    pass
        else:
            print(bcolors.FAIL + "File not set" + bcolors.ENDC)


    elif args[0].lower() == 'gethistory':
        if fileInfo is not None:
            for line in fileInfo:
                try:
                    if "_history" in line:
                        split = line.split(":")
                        print(dict[split[0]].replace('_history"',''))
                except:
                    pass
        else:
            print(bcolors.FAIL + "File not set" + bcolors.ENDC)


    elif args[0].lower() == 'repeated':
        if dict != {}:
            hash_list, cont = repeated(dict, string=username_contains)
            print("\n-----------------------------------------------------------")
            print("Repeated passwords: " + str(hash_list.__len__()) )
            print("Number of users with repeated passwords: " + str(cont))
            print("-----------------------------------------------------------")
            if len(args) == 2:
                path = args[1]
                if hash_list is not [] and path != "":
                    f = open(path, "a")
                    for i in hash_list:
                        f.write(i + "\n")
                    f.close()
                    print(bcolors.OKGREEN + "\nHashes dump to " + path + bcolors.ENDC)
        else:
            print(bcolors.FAIL + "File not set" + bcolors.ENDC)

    elif args[0].lower() == 'getusernamebyhash':
        if dict != {}:
            decorator = (bcolors.OKCYAN + "[{} > getUsernameByHash]> " + bcolors.ENDC).format(file)

            while True:
                code = input(decorator)
                if code == "back":
                    decorator = (bcolors.OKCYAN + "[{}]> " + bcolors.ENDC).format(file)
                    break
                elif code == "exit" or code == "quit":
                    exit()
                elif code == "":
                    pass
                elif code == "help":
                    print(bcolors.WARNING + "Get all usernames that have the same hash." + bcolors.ENDC)
                    print(bcolors.WARNING + "usage ex: <hash>" + bcolors.ENDC)
                else:
                    if not (getUsernameByHash(dict, code, string=username_contains)):
                        print(f"{bcolors.FAIL}Hash \"{code}\" not found in ntds.dit file{bcolors.ENDC}")

        else:
            print(bcolors.FAIL + "File not set" + bcolors.ENDC)

    elif args[0].lower() == 'getusernamebypassword':
        if dict != {}:
            decorator = (bcolors.OKCYAN + "[{} > getUsernameByPassword]> " + bcolors.ENDC).format(file)

            while True:
                code = input(decorator)
                if code == "back":
                    decorator = (bcolors.OKCYAN + "[{}]> " + bcolors.ENDC).format(file)
                    break
                elif code == "exit" or code == "quit":
                    exit()
                elif code == "":
                    pass
                elif code == "help":
                    print(bcolors.WARNING + "Get all usernames that have the same password." + bcolors.ENDC)
                    print(bcolors.WARNING + "usage ex: <password>" + bcolors.ENDC)
                else:
                    genHash = getNTLM(code)
                    if not (getUsernameByHash(dict, genHash.decode(), code, string=username_contains)):
                        print(f"{bcolors.FAIL}Password \"{code}\" not found in ntds.dit file{bcolors.ENDC}")

        else:
            print(bcolors.FAIL + "File not set" + bcolors.ENDC)

    elif args[0].lower() == 'getusernamebypasswordlist':
        if dict != {}:

            decorator = (bcolors.OKCYAN + "[{} > getUsernameByPasswordList]> " + bcolors.ENDC).format(file)

            while True:
                code = input(decorator)
                if code == "back":
                    decorator = (bcolors.OKCYAN + "[{}]> " + bcolors.ENDC).format(file)
                    break
                elif code == "exit" or code == "quit":
                    exit()
                elif code == "":
                    pass
                elif code == "help":
                    print(
                        bcolors.WARNING + "Get all usernames that have the same password from a list. if you enter only one argument, it will be the file that will check against the passwords. If you enter two, the second argument will be the path where the passwords that are in the ntds.dit file are exported. " + bcolors.ENDC)
                    print(bcolors.WARNING + "usage ex1: <password_list>" + bcolors.ENDC)
                    print(bcolors.WARNING + "usage ex2: <password_list> <password_export>" + bcolors.ENDC)
                else:
                    arguments = code.split(" ")
                    if os.path.isfile(arguments[0]):

                        f = open(arguments[0], "r")
                        Lines = f.read().split("\n")
                        f.close()
                        contpass = 0
                        contusers = 0
                        hash_list = []
                        for line in Lines:
                            it = 0
                            if line != "":
                                genHash = getNTLM(line)
                                it += getUsernameByHash(dict, genHash.decode(), line, string=username_contains)
                                if it > 0:
                                    contusers += it
                                    contpass += 1
                                    hash_list.append(line)

                        if not contpass:
                            print(
                                f"{bcolors.FAIL}Passwords from \"{arguments[0]}\" not found in ntds.dit file{bcolors.ENDC}")
                        else:
                            print("\n-----------------------------------------------------------")
                            print( "Passwords loaded: " + str(Lines.__len__() - 1))
                            print("Repeated passwords: " + str(contpass))
                            print("Number of users with repeated passwords: " + str(contusers))
                            print("-----------------------------------------------------------\n")

                            if arguments.__len__() == 2:
                                f = open(arguments[1], "a")
                                for i in hash_list:
                                    f.write(i + "\n")
                                f.close()
                                print("Hashes dump to " + arguments[1] )
                    else:
                        print(bcolors.FAIL + "Password list not found" + bcolors.ENDC)
        else:
            print(bcolors.FAIL + "File not set" + bcolors.ENDC)

    elif args[0].lower() == 'getusernamebyhashlist':
        if dict != {}:
            decorator = (bcolors.OKCYAN + "[{} > getUsernameByHashList]> " + bcolors.ENDC).format(file)

            while True:
                code = input(decorator)
                if code == "back":
                    decorator = (bcolors.OKCYAN + "[{}]> " + bcolors.ENDC).format(file)
                    break
                elif code == "exit" or code == "quit":
                    exit()
                elif code == "":
                    pass
                elif code == "help":
                    print(
                        bcolors.WARNING + "Get all usernames that have the same hash from a list. if you enter only one argument, it will be the file that will check against the hashes. If you enter two, the second argument will be the path where the hashes that are in the ntds.dit file are exported. " + bcolors.ENDC)
                    print(bcolors.WARNING + "usage ex1: <hash_list>" + bcolors.ENDC)
                    print(bcolors.WARNING + "usage ex2: <hash_list> <hash_export>" + bcolors.ENDC)
                else:
                    arguments = code.split(" ")

                    if os.path.isfile(arguments[0]):
                        f = open(arguments[0], "r")
                        Lines = f.read().split("\n")
                        f.close()
                        conthashes = 0
                        contusers = 0
                        hash_list = []
                        for line in Lines:
                            it = 0
                            if line != "":
                                it = getUsernameByHash(dict, line.lower(), None, string=username_contains)
                                if it > 0:
                                    contusers += it
                                    conthashes += 1
                                    hash_list.append(line)

                        if not conthashes:
                            print(
                                f"{bcolors.FAIL}Hashes from \"{arguments[0]}\" not found in ntds.dit file{bcolors.ENDC}")
                        else:
                            print("\n-----------------------------------------------------------" + bcolors.ENDC)
                            print("Hashes loaded: " + str(Lines.__len__() - 1) + bcolors.ENDC)
                            print("Repeated passwords: " + str(conthashes) + bcolors.ENDC)
                            print("Number of users with repeated passwords: " + str(contusers))
                            print("-----------------------------------------------------------\n")

                        if arguments.__len__() == 2:
                            f = open(arguments[1], "a")
                            for i in hash_list:
                                f.write(i + "\n")
                            f.close()
                            print("Hashes dump to " + arguments[1])
                    else:
                        print(bcolors.FAIL + "Hash list not found" + bcolors.ENDC)

        else:
            print(bcolors.FAIL + "File not set" + bcolors.ENDC)

    else:
        print(bcolors.FAIL + "Command not found" + bcolors.ENDC)
    print("")
