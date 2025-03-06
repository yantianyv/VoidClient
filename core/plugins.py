import os,importlib,datetime,re
from colorama import Fore, Back, Style, init
from core.printcolor import print_color
from core import history,api
def _system_prompt():
    """系统提示"""
    plugin_list = ""
    for plugin in os.listdir('./plugins'):
        if plugin.endswith(".py") and plugin != "__init__.py":
            module = importlib.import_module(f"plugins.{plugin[:-3]}")
            plugin_list += str("模型名称："+str(module.plugin_name)+"\t模型功能："+str(module.plugin_description)+"\n")
    history.add("system",f"""
            当前时间是{datetime.datetime.now()}，聊天中的时间戳为系统自动添加的用户当前时区时间。
            当用户需要你执行插件提供的功能时，除非你启用过该插件，否则你需要中止你的回复，并用下面的指令激活插件
            %plugin%plugin_name
            enable
            %end%
            激活单个插件的指令必须单独占据一次回复，插件激活成功后才能继续处理用户的要求。
            在你激活插件之前，不能擅自调用插件。%plugin%指令只能用于激活插件，调用插件的指令以系统提示为准。
            以下为插件列表：
            {plugin_list}
            接下来的内容是你与用户的聊天记录：
            """)

def sniff(text):
    pattern = r'%([^%\n]+)%([^%\n]+)\n([^%]+)%end%'  # 修改后的正则表达式
    matches = re.finditer(pattern, text, re.DOTALL)
    for match in matches:
        arg1, arg2, arg3 = match.groups()
        arg1 = arg1.replace(" ", "")
        arg2 = arg2.replace(" ", "")
        print(Fore.GREEN + f"检测到插件{arg1}被调用，正在执行插件")
        _use_plugin(arg1, arg2, arg3)
    if matches:
        return True
    else:
        return False

def _enable_plugin(plugin_name):
    """启用插件"""
    plugin_name = f"plugins.{plugin_name}"
    plugin=importlib.import_module(plugin_name,package='plugins')
    history.add('system',plugin.enable_content)
    response, _ = api.user_ask()
    history.add("assistant",response)
    if not sniff(response):
        history.display()

def _use_plugin(plugin_name, plugin_arg1, plugin_arg2):
    print(plugin_name, plugin_arg1, plugin_arg2)
    if plugin_name == 'plugin':
        if 'enable' in plugin_arg2:
            _enable_plugin(plugin_arg1)
        else:
            print_color(f"插件{plugin_name}不支持{plugin_arg2}操作", Fore.RED)
        return
    """使用插件"""
    plugin_name = f"plugins.{plugin_name}"
    try:
        plugin=importlib.import_module(plugin_name,package='plugins')
    except:
        print_color(f"插件{plugin_name}不存在", Fore.RED)
        history.add("system",f"插件{plugin_name}不存在，请正确调用")
        return
    plugin.main(plugin_arg1, plugin_arg2)
    return

_system_prompt()