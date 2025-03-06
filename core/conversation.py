import sys
from core import input_lines,history,api,plugins
# from core import command_handler
from colorama import Fore, Back, Style, init
from datetime import datetime

def handle(max_turns):
    """处理对话流程"""
    for _ in range(max_turns):
        _process_conversation_turn()
    history.display()
    try:
        input(Fore.RED + "对话已达最大轮数，按 Enter 键压缩历史记录继续对话")
    except:
        pass

def _process_conversation_turn():
    """处理单次对话轮次"""
    current_time = datetime.now().strftime("%y%m%d%H%M")
    history.add("system",f"{current_time}")
    user_input = input_lines.input_lines(Fore.CYAN + "我：")
    if user_input is None:
        _print_color("取消输入", Fore.RED)
        return
    if user_input.lower() in ["exit", "quit"]:
        sys.exit(0)
    history.add("user",user_input)
    print("\n" + Fore.YELLOW + "AI 正在思考...")
    response, _ = api.user_ask()
    history.add("assistant",response)
    if not plugins.sniff(response):
        history.display()
    
def _print_color(text, color=Fore.WHITE, end="\n"):
    """带颜色打印文本"""
    print(color + text + Style.RESET_ALL, end=end, flush=True)