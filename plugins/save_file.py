import os

print("已成功加载【保存文件】插件")

plugin_name = "save_file"
plugin_description = "保存文件"
enable_content = f"""
需要保存或导出文件时，请以
%save_file%file_name
正文
%end%
的格式发送请求，其中file_name为文件名，正文为文件内容,请直接替换，不要加以解释。
正文部分不要使用任何Markdown语法，不要使用代码框，不要输出任何解释，只输出文件内容，以此法保存文件时不要省略任何内容。
文本类文件默认保存为html，脚本类文件默认保存为py文件。
"""


def main(fname, file_str):
    """把传入的文本保存为文件"""
    file_path = f"./output/{fname}"
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except Exception as e:
            print(f"创建目录失败: {e}")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(file_str)
    if any(file_path.endswith(ext) for ext in ['exe','sh','bat','bin','py']):
        choice = input("检测到生成的文件为可执行文件，是否要执行？(Y/n)")
        if choice == "n":
            return file_path
    os.system(f"start {os.getcwd()}/{file_path}")
    return file_path

def _open_file(fname):
    pass