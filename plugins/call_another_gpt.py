import os
from core import api
from openai import OpenAI

print("已成功加载【调用gpt】插件")

plugin_name = "call_another_gpt"
plugin_description = "调用另一个gpt模型（暂不可用）"
enable_content = f"""
当你遇到不太擅长的事时，可以通过
%call_another_gpt%modle
content
%end%
的形式调用另一个gpt。其中modle是另一个gpt的名称，content是你发送给它的指令。
这个功能通常用于让高性能模型做指挥家设计架构，让低性能模型依照架构填充具体实现
可用modle如下：
coder：专门用于编写代码的gpt
reasoner：专门用于做推理的gpt
"""


def main(modle, content):
    pass

def _init_modle(modle):
    if modle == 'coder':
        pass
    elif modle == 'reasoner':
        pass
