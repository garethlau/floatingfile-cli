class bcolors:
    HEADER = "\033[94m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    GRAY = "\033[37m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def p_sub(*args):
    print(bcolors.GRAY + " ".join(map(str, args)) + bcolors.ENDC)


def p_head():
    print()
    print(bcolors.BOLD + bcolors.HEADER + ">>> floatingfile" + bcolors.ENDC)
    print()


def p_ok(*args):
    print(bcolors.OKGREEN + " ".join(map(str, args)) + bcolors.ENDC)


def p_fail(*args):
    print(bcolors.FAIL + " ".join(map(str, args)) + bcolors.ENDC)


def p_question(*args):
    print(bcolors.OKBLUE + "? " + bcolors.ENDC + " ".join(map(str, args)))


def p_info(*args):
    print(bcolors.OKBLUE + "! " + bcolors.ENDC + " ".join(map(str, args)))


def xprint(*args):

    print(
        bcolors.BOLD,
        bcolors.OKBLUE + "  " + " ".join(map(str, args)) + bcolors.ENDC,
    )
