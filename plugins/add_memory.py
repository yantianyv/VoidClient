import os
import datetime
from core import history
print("已成功加载【长期记忆】插件")

plugin_name = "add_memory"
plugin_description = "记忆特定内容"
enable_content = f"""
            当你需要长期记住某件事的时候，可以以以下格式保存记忆
            %add_memory%title
            正文
            %end%
            的格式发送请求，其中title为记忆的标题，正文为记忆内容,请直接替换，不要加以解释。
            由于每次对话都会先上传记忆，因此以此法保存的记忆要尽可能精简以节省token，但不能丢失重要信息。
            """

memory_path = './history'

def main(title, new_memory):
    if not os.path.exists(memory_path):
        os.makedirs(memory_path)
    with open(os.path.join(memory_path, title + '.txt'), 'w') as f:
        f.write(new_memory)
    
# 初始化时读取旧记忆
def init():
    old_memory = ""
    try:
        with open(f'{memory_path}/memory.txt', 'r') as f:
            old_memory = f.read()
            history.add("system",f"本条是你的长期记忆：\n{old_memory}")
    except:
        pass

init()