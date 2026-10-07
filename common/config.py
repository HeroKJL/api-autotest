"""读取 config.yaml（项目里所有地方都通过这里拿配置）"""
from pathlib import Path

import yaml

# 项目根目录 = 本文件所在目录(common)的上一级
ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT_DIR / "config.yaml"


def load_config():
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)
