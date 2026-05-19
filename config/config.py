"""
项目配置文件
包含全局配置项,如API地址、超时时间、目录路径等
"""
import os
from pathlib import Path

# 获取项目根目录，该文件位于config目录下，所以parent.parent指向项目根
BASE_DIR = Path(__file__).parent.parent

class Config:
    """配置类，管理项目的所有配置参数"""
    
    # API基础地址，测试环境的认证服务地址
    BASE_URL = "https://pehss.sfrtlce.cn/service-boss"
    
    # 请求超时时间，单位：秒
    TIMEOUT = 30
    
    # 默认请求头，模拟浏览器发送请求
    HEADERS = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # 日志文件目录
    LOG_DIR = BASE_DIR / "logs"
    # 报告文件目录
    REPORT_DIR = BASE_DIR / "reports"
    # Allure报告数据目录
    ALLURE_DIR = REPORT_DIR / "allure-results"
    # Excel报告路径（实际使用时会添加时间戳）
    EXCEL_REPORT = REPORT_DIR / "test_report.xlsx"
    # TXT报告路径
    TXT_REPORT = REPORT_DIR / "test_summary.txt"
    
    # 企业微信配置
    WECHAT_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8eebb96d-d57e-4ffa-8fb9-52e0c6b2c50d"  # 请在此填写企业微信机器人的Webhook地址
    SEND_WECHAT_NOTIFICATION = True  # 是否发送企业微信通知（调试时关闭）
    
    @classmethod
    def ensure_dirs(cls):
        """确保所有必要的目录存在，如果不存在则创建
        
        使用示例：
            Config.ensure_dirs()  # 在项目启动时调用一次即可
        """
        for dir_path in [cls.LOG_DIR, cls.REPORT_DIR, cls.ALLURE_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)
