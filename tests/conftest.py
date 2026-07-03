"""测试配置文件。

在测试运行时将项目根目录加入 ``sys.path``，以便能够导入 ``nilo`` 包。
"""

import sys
from pathlib import Path

# 将仓库根目录添加到 Python 模块搜索路径
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))