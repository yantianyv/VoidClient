if __name__ == "__main__":
    import history,plugins
    from myconfig import config
else:
    from core import history,plugins
    from core.myconfig import config
from openai import OpenAI
import sys
from colorama import Fore, Back, Style, init
from rich.console import Console
from rich.markdown import Markdown

client = OpenAI(api_key=config["api_key"], base_url=config["base_url"])
temperature = 0.0 # 目前发现把temperature调高会出现DeepSeek无法正常使用插件的问题，qwen coder在插件调用的能力上要优于ChatGPT。
def user_ask(temperature=temperature,client=client, message_history = history.history):
    try:
        full_response = ""
        reasoning = ""
        if history.history[-1]['role'] != "user":
            history.add("user","")
        stream = client.chat.completions.create(
            model=config["main_model"],
            messages=message_history,
            stream=True,
            temperature=temperature,
        )
        content_switch = False
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                if not content_switch:
                    print("    #思考结束#")
                    print_color("AI： ", Fore.YELLOW, end="")
                    content_switch = True
                content = delta.content
                full_response += content
                print_color(content, end="")
                sys.stdout.flush()
            if hasattr(delta, "reasoning_content") and delta.reasoning_content:
                reasoning_part = delta.reasoning_content
                reasoning += reasoning_part
                print_color(reasoning_part, Fore.LIGHTBLACK_EX, end="")
                sys.stdout.flush()
        print()
        history.clear()
        print('检测是否调用插件')
        return full_response, reasoning
    #如果是用户主动按下Ctrl+C
    except KeyboardInterrupt:
        print(Fore.RED + "用户中断了回答")
        return full_response, reasoning
    except:
        print(Fore.RED + "回答出错")
        # 输出报错内容
        print(sys.exc_info()[0])
        return full_response, reasoning

def sys_ask(client=client, message_history = history.history):
    try:
        full_response = ""
        reasoning = ""
        if history.history[-1]['role'] != "user":
            history.add("user","")
        stream = client.chat.completions.create(
            model=config["sub_model"],
            messages=message_history,
            stream=True,
            temperature=0.1,
            max_tokens=512,
        )
        content_switch = False
        counter = 0
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                if not content_switch:
                    print("\r#思考结束#        ")
                    counter = 0
                    content_switch = True
                content = delta.content
                full_response += content
                print("\r处理中" + "." * counter + " " * (6 - counter), end="")
                counter = counter + 1 if counter < 6 else 0
                sys.stdout.flush()
            if hasattr(delta, "reasoning_content") and delta.reasoning_content:
                reasoning_part = delta.reasoning_content
                reasoning += reasoning_part
                print("\r思考中" + "." * counter + " " * (6 - counter), end="")
                counter = counter + 1 if counter < 6 else 0
                sys.stdout.flush()
        print()
        history.clear()
        return full_response, reasoning
    except:
        print("用户中断了处理")
        return full_response, reasoning

def print_color(text, color=Fore.WHITE, end="\n"):
    """带颜色打印文本"""
    print(color + text + Style.RESET_ALL, end=end, flush=True)

if __name__ == "__main__":
    history.add("user","你好")
    user_ask()