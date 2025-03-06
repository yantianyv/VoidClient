from colorama import Fore, Back, Style, init

def print_color(text, color=Fore.WHITE, end="\n"):
    """带颜色打印文本"""
    print(color + text + Style.RESET_ALL, end=end, flush=True)