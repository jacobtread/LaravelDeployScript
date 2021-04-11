import sys

COLOR_RESET = '\033[0m'
COLOR_RED = '\033[1;31m'
COLOR_GREEN = '\033[1;32m'
COLOR_YELLOW = '\033[1;33m'
COLOR_BLUE = '\033[1;34m'
COLOR_PURPLE = '\033[1;35m'
COLOR_BOLD = '\033[1m'


def good(message: str):
    print('    ' + COLOR_GREEN + message + COLOR_RESET)


def bad(message: str):
    print('    ' + COLOR_RED + message + COLOR_RESET)


def fatal(message: str):
    print('    ' + COLOR_RED + message + COLOR_RESET)
    sys.exit(1)


def okay(message: str):
    print('    ' + COLOR_YELLOW + message + COLOR_RESET)

# \e[0;30m	Black
# \e[0;31m	Red
# \e[0;32m	Green
# \e[0;33m	Yellow
# \e[0;34m	Blue
# \e[0;35m	Purple
# \e[0;36m	Cyan
# \e[0;37m	White
# Background
# \e[40m	Black
# \e[41m	Red
# \e[42m	Green
# \e[43m	Yellow
# \e[44m	Blue
# \e[45m	Purple
# \e[46m	Cyan
# \e[47m	White
