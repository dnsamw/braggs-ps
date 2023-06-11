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


def getHelp():
    print("\n======HELP======\n")
    print("1. version - Displays Current version of ScrapeX.")
    print("2. info - Displays information regarding how to consume this tool")
    print("3. path - Displays the current save path.")
    print("4. list - Displays the currently Supported site list.")
    print("5. exit - Exit the tool.\n")


def getInfo():
    print(bcolors.WARNING + "=====================================INFO=====================================" + bcolors.ENDC)
    print("")
    print("(*) This is a comand line tool for scraping data from braggsschoolwear.co.uk")
    print("(*) Developed by @dnsamw")
    print(bcolors.WARNING + "===============================================================================" + bcolors.ENDC + "\n")


def getList():
    print("\n==================SUPPORTED SITES==================\n")
    print("(1) braggsschoolwear.co.uk")
