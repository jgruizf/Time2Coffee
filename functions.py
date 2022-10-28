import hashlib
import binascii

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printBanner():

    print(bcolors.OKGREEN + "                                                                                                                                        " + bcolors.ENDC)
    print(bcolors.OKGREEN + "@@@  @@@  @@@@@@@  @@@@@@@    @@@@@@    @@@@@@   @@@@@@@@   @@@@@@   @@@@@@@    @@@@@@@  @@@  @@@     @@@  @@@    @@@        @@@@@@@@   " + bcolors.ENDC)
    print(bcolors.OKGREEN + "@@@@ @@@  @@@@@@@  @@@@@@@@  @@@@@@@   @@@@@@@   @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@  @@@     @@@  @@@   @@@@       @@@@@@@@@@  " + bcolors.ENDC)
    print(bcolors.OKGREEN + "@@!@!@@@    @@!    @@!  @@@  !@@       !@@       @@!       @@!  @@@  @@!  @@@  !@@       @@!  @@@     @@!  @@@  @@@!!       @@!   @@@@  " + bcolors.ENDC)
    print(bcolors.OKGREEN + "!@!!@!@!    !@!    !@!  @!@  !@!       !@!       !@!       !@!  @!@  !@!  @!@  !@!       !@!  @!@     !@!  @!@    !@!       !@!  @!@!@  " + bcolors.ENDC)
    print(bcolors.OKGREEN + "@!@ !!@!    @!!    @!@  !@!  !!@@!!    !!@@!!    @!!!:!    @!@!@!@!  @!@!!@!   !@!       @!@!@!@!     @!@  !@!    @!@       @!@ @! !@!  " + bcolors.ENDC)
    print(bcolors.OKGREEN + "!@!  !!!    !!!    !@!  !!!   !!@!!!    !!@!!!   !!!!!:    !!!@!!!!  !!@!@!    !!!       !!!@!!!!     !@!  !!!    !@!       !@!!!  !!!  " + bcolors.ENDC)
    print(bcolors.OKGREEN + "!!:  !!!    !!:    !!:  !!!       !:!       !:!  !!:       !!:  !!!  !!: :!!   :!!       !!:  !!!     :!:  !!:    !!:       !!:!   !!!  " + bcolors.ENDC)
    print(bcolors.OKGREEN + ":!:  !:!    :!:    :!:  !:!      !:!       !:!   :!:       :!:  !:!  :!:  !:!  :!:       :!:  !:!      ::!!:!     :!:  :!:  :!:    !:!  " + bcolors.ENDC)
    print(bcolors.OKGREEN + " ::   ::     ::     :::: ::  :::: ::   :::: ::    :: ::::  ::   :::  ::   :::   ::: :::  ::   :::       ::::      :::  :::  ::::::: ::  " + bcolors.ENDC)
    print(bcolors.OKGREEN + "::    :      :     :: :  :   :: : :    :: : :    : :: ::    :   : :   :   : :   :: :: :   :   : :        :         ::  :::   : : :  :   " + bcolors.ENDC)
    print(bcolors.OKGREEN + "                                                                                                                                        " + bcolors.ENDC)

def repeated(dict, string=None):
    rev_dict = {}
    for key, value in dict.items():
        rev_dict.setdefault(value, set()).add(key)

    result = [key for key, values in rev_dict.items()
              if len(values) > 1]
    cont = 0
    for i in result:
        it = getUsernameByHash(dict, i, string=string)
        cont += it
    return result, cont

def getUsernameByHash(dict, hash, password=None, string=None):
    a = 0
    for key, value in dict.items():
        if hash == value:
            if a == 0:
                print(f"Hash: {value} : {password}")
            if string is not None and string in key.lower():
                print(f"{bcolors.UNDERLINE} {bcolors.OKGREEN}\t {key} {bcolors.ENDC}")
            else:
                print(f"\t {key}")
            a = a + 1
    return a


def getNTLM(password):
    genhash = hashlib.new('md4', password.encode('utf-16le')).digest()
    genHash = binascii.hexlify(genhash)
    return genHash
