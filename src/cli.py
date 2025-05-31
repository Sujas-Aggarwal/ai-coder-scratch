class CLI:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    def warning(text):
        return (CLI.WARNING + text + CLI.ENDC)
    def error(text):
        return (CLI.FAIL + text + CLI.ENDC)
    def success(text):
        return (CLI.OKGREEN + text + CLI.ENDC)
    def info(text):
        return (CLI.OKBLUE + text + CLI.ENDC)
    def header(text):
        return (CLI.HEADER + text + CLI.ENDC)
    def cyan(text):
        return (CLI.OKCYAN + text + CLI.ENDC)
    def bold(text):
        return (CLI.BOLD + text + CLI.ENDC)
    def underline(text):
        return (CLI.UNDERLINE + text + CLI.ENDC)
#---------------------------------------------------