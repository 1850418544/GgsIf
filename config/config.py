"""
项目配置文件
包含全局配置项，如 API 地址、超时时间、目录路径、企业微信配置、邮件配置等
配置项的读取优先级：环境变量 > .env 文件 > 代码中的默认值
"""
import os
from pathlib import Path

# 尝试加载 .env 文件(可选，如果没有安装 python-dotenv 或文件不存在则忽略)
try:
    from dotenv import load_dotenv
    load_dotenv()  # 从项目根目录加载 .env 文件
except ImportError:
    pass

# 获取项目根目录，该文件位于 config 目录下，所以 parent.parent 指向项目根
BASE_DIR = Path(__file__).parent.parent


def _env_bool(key: str, default: bool) -> bool:
    """从环境变量读取布尔值
    支持的值: true/false/yes/no/1/0(不区分大小写)
    """
    value = os.getenv(key, "").strip().lower()
    if not value:
        return default
    return value in ("true", "yes", "1")


class Config:
    """配置类，管理项目的所有配置参数"""

    # API 基础地址，测试环境的认证服务地址
    BASE_URL = os.getenv("API_BASE_URL", "https://pehss.sfrtlce.cn/service-boss")

    # 请求超时时间，单位：秒
    TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))

    # 默认请求头，模拟浏览器发送请求
    HEADERS = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    # 测试账号(从环境变量读取，方便在不同环境中配置不同账号)
    TEST_USERNAME = os.getenv("TEST_USERNAME", "fan")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD", "fan123")

    # 日志文件目录
    LOG_DIR = BASE_DIR / "logs"
    # 报告文件目录
    REPORT_DIR = BASE_DIR / "reports"
    # Allure 报告数据目录
    ALLURE_DIR = REPORT_DIR / "allure-results"
    # Excel 报告路径(实际使用时会添加时间戳)
    EXCEL_REPORT = REPORT_DIR / "test_report.xlsx"
    # TXT 报告路径
    TXT_REPORT = REPORT_DIR / "test_summary.txt"

    # ============ 企业微信配置 ============
    # 是否启用企业微信通知 (true/false)
    SEND_WECHAT_NOTIFICATION = _env_bool("SEND_WECHAT_NOTIFICATION", False)
    # 企业微信机器人 Webhook 地址
    WECHAT_WEBHOOK_URL = os.getenv("WECHAT_WEBHOOK_URL", "")

    # ============ 邮件通知配置 ============
    # 是否启用邮件通知 (true/false)
    SEND_EMAIL_NOTIFICATION = _env_bool("SEND_EMAIL_NOTIFICATION", False)
    # SMTP 服务器配置
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.qq.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))  # 465=SSL, 587=TLS
    SMTP_USER = os.getenv("SMTP_USER", "")           # 发件人邮箱
    SMTP_PASS = os.getenv("SMTP_PASS", "")           # 邮箱密码或授权码
    SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "API自动化测试")  # 发件人显示名称
    # 收件人邮箱(支持多个，用逗号分隔)
    EMAIL_TO = os.getenv("EMAIL_TO", "")

    # 是否生成 Allure 报告
    GENERATE_ALLURE_REPORT = _env_bool("GENERATE_ALLURE_REPORT", True)

    @classmethod
    def ensure_dirs(cls):
        """确保所有必要的目录存在，如果不存在则创建

        使用示例：
            Config.ensure_dirs()  # 在项目启动时调用一次即可
        """
        for dir_path in [cls.LOG_DIR, cls.REPORT_DIR, cls.ALLURE_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)
