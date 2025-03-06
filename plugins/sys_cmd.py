import os

print("已成功加载【系统指令】插件")

plugin_name = "sys_cmd"
plugin_description = "调用系统指令"
enable_content = f"""
需要执行系统命令时，可以使用
%sys_cmd%execute
commands
%end%
来调用，其中'execute'为关键字，你无需替换。commands为指令的具体内容，依据用户当前的系统使用bat或sh格式。（当前系统为{os.name}）
"""



def main(arg1, shell):
    """执行系统命令"""
    if 'execute' in arg1:
        cmd = shell
        if os.name == 'nt':
            os.system(f"cmd /c {cmd}")
        else:
            os.system(f"sh -c {cmd}")
    return ""
