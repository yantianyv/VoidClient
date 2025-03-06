from colorama import Fore, Back, Style, init
import os

def input_lines(prompt_message):
    """支持多行输入"""
    print(Fore.MAGENTA + "（输入多行内容，输入 '/send' '发送' 或四击enter发送，'/del' '删除' 删除上一行，'/cancel' '取消' 取消）")
    print(prompt_message)
    lines = []
    empty_count = 0
    while True:
        line = input()
        if line.strip() == "":
            empty_count += 1
            if empty_count > 2:
                print(Fore.LIGHTBLACK_EX + f"(已发送)", end="\r")
                break
            print(Fore.LIGHTBLACK_EX + f"(再按{3-empty_count}次发送)", end="\r")
        elif empty_count > 0:
            empty_count = 0
        if line.strip() == "/send" or line.strip() == "发送":
            break
        if line.strip() == "/cancel" or line.strip() == "取消":
            return None
        if line.strip() == "/del" or line.strip() == "删除":
            lines.pop()
            os.system("cls" if os.name == "nt" else "clear")
            print(Fore.MAGENTA + "（输入多行内容，输入 '/send' '发送' 或四击enter发送，'/del' '删除' 删除上一行，'/cancel' '取消' 取消）")
            for line in lines:
                print(line)
            continue
        lines.append(line)
    return "\n".join(lines)