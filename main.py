"""
项目入口脚本
可以直接运行: python main.py
或者: python main.py -v (详细输出)

功能:
    1) 初始化日志和目录
    2) 调用 pytest 执行测试用例
    3) 生成报告(Excel、TXT、Allure 数据)
    4) 可选发送企业微信通知
"""
import sys
import os
from pathlib import Path

# 确保项目根目录在 Python 搜索路径中
BASE_DIR = Path(__file__).parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# 设置 UTF-8 编码(兼容 Windows)
os.environ["PYTHONIOENCODING"] = "utf-8"

from config.config import Config
from utils.logger import logger
import pytest


def print_banner():
    """打印启动横幅"""
    logger.info("=" * 60)
    logger.info("  接口自动化测试框架")
    logger.info(f"  API 地址: {Config.BASE_URL}")
    logger.info(f"  超时时间: {Config.TIMEOUT} 秒")
    logger.info(f"  企业微信通知: {'开启' if Config.SEND_WECHAT_NOTIFICATION else '关闭'}")
    logger.info("=" * 60)


def main():
    # 初始化：确保必要目录存在
    Config.ensure_dirs()

    # 打印启动信息
    print_banner()

    # 构造 pytest 参数：
    #   - 测试目录: testcases/
    #   - 详细输出: -v
    #   - pytest.ini 中的 addopts 会自动生效(如 --alluredir)
    pytest_args = ["testcases/", "-v"]

    # 将命令行中的额外参数透传给 pytest(例如: python main.py -k login)
    if len(sys.argv) > 1:
        pytest_args.extend(sys.argv[1:])

    logger.info(f"执行 pytest 命令参数: {pytest_args}")

    # 运行 pytest(pytest 会自动读取 conftest.py 和 pytest.ini)
    # conftest.py 中的 pytest_sessionfinish 钩子会负责生成报告和发通知
    exit_code = pytest.main(pytest_args)

    logger.info("=" * 60)
    if exit_code == 0:
        logger.info("全部测试执行完成，结果: 通过 ✅")
    else:
        logger.warning(f"测试执行完成，pytest 退出码: {exit_code}")
    logger.info("=" * 60)

    logger.info(f"报告目录: {Config.REPORT_DIR}")
    logger.info(f"日志目录: {Config.LOG_DIR}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
