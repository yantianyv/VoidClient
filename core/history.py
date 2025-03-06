import json
import os
from colorama import Fore, Back, Style, init
from rich.console import Console
from rich.markdown import Markdown
import time
import markdown

console = Console()

__all__ = ['history','history_file']
history = []
history_file = "default.history"
'''
choose()    # 用户手动选择历史记录文件
load()      # 读取历史记录文件
save()      # 保存历史记录文件
'''

def add(role,content):
    global history
    history.append({"role":role,"content":content})
    if role not in ['user','assistant','system']:
        input("警告，角色名不合法，请检查源码")
    return True

def clear():
    for i in history:
        if i["content"] == "":
            history.remove(i)
        if '%end%' in i["content"] and i["role"] == "assistant":
            history.remove(i)

def choose():   #用户通过命令行选择一个历史记录文件或新建一个
    global history
    global history_file
    time.sleep(0.2)
    history_file = str(_choose())
    return history_file
    
def load(file_name=history_file):
    global history
    if os.path.exists("./history/"+file_name):
        with open("./history/"+file_name, "r") as f:
            history = json.load(f)
        return True
    else:
        if not os.path.exists("./history/"):
            os.makedirs("./history")
        with open("./history/"+file_name, "w") as f:
            f.write('[]')
        history = []
        return False

def save(file_name=history_file):
    global history
    with open("./history/"+file_name, "w") as f:
        json.dump(history, f)
    return True

def display():
    """显示对话历史"""
    os.system("cls" if os.name == "nt" else "clear")
    for msg in history:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            color = Fore.CYAN
            prefix = "我："
        elif role == "assistant":
            color = Fore.WHITE
            prefix = Fore.YELLOW + "AI：" + Fore.WHITE
        else:
            color = Fore.LIGHTBLACK_EX
            prefix = "系统："
        if "```" in content or "*" in content and prefix != "系统：":
            _print_color(f"{prefix} ", color, end="")
            markdown = Markdown(content)
            console.print(markdown)
        else:
            _print_color(f"{prefix} {content}", color)
        print()

def pop():
    global history
    return history.pop()

def _choose():   #用户通过命令行选择一个历史记录文件或新建一个
    global history
    history_list = []
    print(Fore.CYAN + "历史记录列表：")
    for idx, file in enumerate([f for f in os.listdir('./history/') if f.endswith('.history')], start=1):
        print(Fore.GREEN + f"[{idx:^3d}]" + Fore.CYAN + file)
        history_list.append(file)
    print(Fore.LIGHTMAGENTA_EX + "[ n ]\t新建历史记录")
    print(Fore.LIGHTMAGENTA_EX + "[ d ]\t删除历史记录")
    print(Fore.GREEN + "直接回车使用临时对话")
    choice = input(Fore.GREEN + "请选择历史记录：").strip()
    if not choice:
        return None
    elif choice.lower() == "n":
        file_name = input("请输入历史记录名称：")
        with open('./history/'+file_name+'.history','w') as f:
            f.write('[]')
        history = []
        return file_name
    elif choice.lower() == "d":
        del_choice = input(Fore.GREEN + "请输入要删除的历史记录编号或名称：").strip()
        del_key = None
        if del_choice.isdigit():
            index = int(del_choice) - 1
            if 0 <= index < len(history_list):
                del_key = history_list[index]
        elif del_choice in history_list:
            del_key = del_choice
        if del_key:
            os.remove('./history/'+del_key+'.json')
            print(Fore.GREEN + "历史记录已删除。")
        else:
            print(Fore.GREEN + "无效的选择。")
    elif choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(history_list):
            file_name = history_list[index]
            load(file_name)
            return file_name
        else:
            print(Fore.GREEN + "无效的选择。")
    elif choice in history_list:
        file_name = choice
        load(file_name)
        return file_name
    else:
        print(Fore.GREEN + "无效的选择。")
        return None
    
def _print_color(text, color=Fore.WHITE, end="\n"):
    """带颜色打印文本"""
    print(color + text + Style.RESET_ALL, end=end, flush=True)

if __name__ == "__main__":
    history_file = choose()
    print(history)
    history.insert(0, {"role": "system", "content": "example"})
    save()
    load()
