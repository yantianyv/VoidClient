import os
import json
import sys
from colorama import Fore, Back, Style, init
import requests

CONFIG_PATH = 'config.json'

def _load_configs():
    """加载配置文件，支持多套配置"""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
            if "configs" not in data:
                raise ValueError("配置文件缺少 'configs' 字段")
            return data
        except (json.JSONDecodeError, ValueError) as e:
            print(f"配置文件损坏，将重新配置。错误：{e}")
            os.remove(CONFIG_PATH)
    return None

def _prompt_config(defaults: dict) -> dict:
    """Prompt user for configuration inputs."""
    try:
        config = {
            "api_key": input(f"Enter API Key [{defaults.get('api_key', '')}]: ").strip() or defaults.get("api_key", ""),
            "base_url": input(f"Enter API URL [default: {defaults.get('base_url', 'https://api.deepseek.com')}]: ").strip() or defaults["base_url"],
            "main_model": input(f"Enter main model [default: {defaults.get('main_model', 'deepseek-reasoner')}]: ").strip() or defaults["main_model"],
            "sub_model": input(f"Enter sub model [default: {defaults.get('sub_model', 'deepseek-chat')}]: ").strip() or defaults["sub_model"],
        }
        return config
    except KeyboardInterrupt:
        print("\nConfiguration cancelled")
        sys.exit(0)

def _get_config():
    """获取或创建配置文件"""
    configs_data = _load_configs()
    if configs_data is None:
        print("首次使用，请配置 API 信息（按 Ctrl+C 退出）")
        defaults = {
            "api_key": "",
            "base_url": "https://api.deepseek.com",
            "main_model": "deepseek-reasoner",
            "sub_model": "deepseek-chat",
        }
        new_config = _prompt_config(defaults)
        profile_name = "default"
        configs_data = {"configs": {profile_name: new_config}}
        os.makedirs(os.path.dirname(CONFIG_PATH) or ".", exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump(configs_data, f, indent=4)
        print("配置已保存至 config.json")
        return new_config, profile_name
    else:
        while True:
            configs = configs_data.get("configs", {})
            if not configs:
                print("配置文件为空，请配置 API 信息（按 Ctrl+C 退出）")
                defaults = {
                    "api_key": "",
                    "base_url": "https://api.deepseek.com",
                    "main_model": "deepseek-reasoner",
                    "sub_model": "deepseek-chat",
                }
                new_config = _prompt_config(defaults)
                profile_name = "default"
                configs_data["configs"] = {profile_name: new_config}
                with open(CONFIG_PATH, "w") as f:
                    json.dump(configs_data, f, indent=4)
                return new_config, profile_name
            print(Fore.GREEN + "配置列表：")
            profile_keys = list(configs.keys())
            default_choice = len(profile_keys)
            for idx, key in enumerate(profile_keys, start=1):
                try:
                    requests.get((configs[key])["base_url"], timeout=0.3)
                    print(Fore.GREEN + f"[{idx:^3d}]" + "\t[顺畅]" + Fore.CYAN + key)
                    default_choice = idx
                except:
                    print(Fore.GREEN + f"[{idx:^3d}]" + Fore.YELLOW + "\t[拥塞]" + Fore.CYAN + key)
            if len(profile_keys) > 1:
                print(Fore.LIGHTMAGENTA_EX + "[ d ]\t删除配置")
            print(Fore.LIGHTMAGENTA_EX + "[ n ]\t新建配置")
            print(Fore.GREEN + "直接回车自动选择：" + Fore.CYAN + profile_keys[default_choice - 1])
            choice = input(Fore.GREEN + "请选择操作：").strip()
            if not choice:
                choice = str(default_choice).strip()
            if choice.lower() == "n":
                profile_name = input(Fore.GREEN + "请输入新配置的名称：").strip()
                default_profile = configs[profile_keys[0]]
                print(Fore.GREEN + "请配置新配置项（直接回车使用默认值）：")
                new_config = _prompt_config(default_profile)
                configs_data["configs"][profile_name] = new_config
                with open(CONFIG_PATH, "w") as f:
                    json.dump(configs_data, f, indent=4)
                print(Fore.GREEN + "新配置已保存。")
                return new_config, profile_name
            elif choice.lower() == "d":
                if len(profile_keys) <= 1:
                    print(Fore.GREEN + "只有一个配置，无法删除。")
                    continue
                del_choice = input(Fore.GREEN + "请输入要删除的配置编号或名称：").strip()
                del_key = None
                if del_choice.isdigit():
                    index = int(del_choice) - 1
                    if 0 <= index < len(profile_keys):
                        del_key = profile_keys[index]
                elif del_choice in configs:
                    del_key = del_choice
                if del_key is None:
                    print(Fore.GREEN + "无效的选择。")
                    continue
                confirm = (input(Fore.RED + f"确认删除配置 '{del_key}'？(y/n): ").strip().lower())
                if confirm == "y":
                    del configs_data["configs"][del_key]
                    with open(CONFIG_PATH, "w") as f:
                        json.dump(configs_data, f, indent=4)
                    print(Fore.GREEN + f"配置 '{del_key}' 已删除。")
                else:
                    print(Fore.GREEN + "取消删除。")
                continue
            else:
                selected_config = None
                if choice.isdigit():
                    index = int(choice) - 1
                    if 0 <= index < len(profile_keys):
                        profile_name = profile_keys[index]
                        selected_config = configs[profile_name]
                elif choice in configs:
                    profile_name = choice
                    selected_config = configs[profile_name]
                if selected_config is None or not selected_config.get("api_key"):
                    print("无效选择或配置缺少 API Key，请重新选择。")
                    continue
                return selected_config, profile_name

config, profile_name = _get_config()
__all__ = ['config','profile_name']