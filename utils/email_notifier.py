"""
邮件通知模块
支持发送测试报告到指定邮箱
使用 SMTP 协议，支持 SSL/TLS 加密
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formataddr
from datetime import datetime
from utils.logger import logger


class EmailNotifier:
    """邮件通知类"""
    
    def __init__(self, smtp_host, smtp_port, smtp_user, smtp_pass, smtp_from_name="API自动化测试"):
        """初始化邮件通知器
        
        参数：
            smtp_host (str): SMTP 服务器地址(如 smtp.qq.com, smtp.163.com)
            smtp_port (int): SMTP 端口(SSL通常是465，TLS通常是587)
            smtp_user (str): 发件人邮箱账号
            smtp_pass (str): 发件人邮箱密码或授权码
            smtp_from_name (str): 发件人显示名称
        
        使用示例：
            notifier = EmailNotifier(
                smtp_host="smtp.163.com",
                smtp_port=465,
                smtp_user="your_email@163.com",
                smtp_pass="your_auth_code",
                smtp_from_name="API自动化测试"
            )
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass
        self.smtp_from_name = smtp_from_name
    
    def send_email(self, to_emails, subject, content, attachments=None):
        """发送邮件
        
        参数：
            to_emails (list): 收件人邮箱列表，如 ["a@example.com", "b@example.com"]
            subject (str): 邮件主题
            content (str): 邮件内容(支持HTML格式)
            attachments (list, 可选): 附件文件路径列表，如 ["reports/test_report.xlsx"]
        
        返回：
            bool: 是否发送成功
        
        使用示例：
            notifier.send_email(
                to_emails=["test@example.com"],
                subject="测试报告",
                content="<h1>测试完成</h1>",
                attachments=["reports/test_report.xlsx"]
            )
        """
        try:
            # 创建邮件对象
            msg = MIMEMultipart()
            
            # 设置发件人
            msg['From'] = formataddr([self.smtp_from_name, self.smtp_user])
            
            # 设置收件人
            msg['To'] = ", ".join(to_emails)
            
            # 设置主题
            msg['Subject'] = subject
            
            # 添加正文
            msg.attach(MIMEText(content, 'html', 'utf-8'))
            
            # 添加附件
            if attachments and isinstance(attachments, list):
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                            msg.attach(part)
                        logger.info(f"添加附件: {file_path}")
                    else:
                        logger.warning(f"附件文件不存在，已跳过: {file_path}")
            
            # 连接SMTP服务器并发送
            with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
                server.login(self.smtp_user, self.smtp_pass)
                server.sendmail(self.smtp_user, to_emails, msg.as_string())
            
            logger.info(f"邮件发送成功，收件人: {to_emails}")
            return True
            
        except Exception as e:
            logger.error(f"发送邮件失败: {e}")
            return False
    
    def send_test_report(self, test_results, attachments=None):
        """发送测试报告摘要到邮箱
        
        参数：
            test_results (list): 测试结果列表
            attachments (list, 可选): 附件文件路径列表
        
        使用示例：
            notifier.send_test_report(test_results, ["reports/test_report.xlsx", "reports/test_summary.txt"])
        """
        # 计算统计数据
        total = len(test_results)
        passed = sum(1 for r in test_results if r.get("result") == "PASS")
        failed = total - passed
        pass_rate = passed / total * 100 if total > 0 else 0
        
        # 获取测试时间
        test_time = test_results[0].get('test_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S')) if test_results else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 筛选失败的接口
        failed_interfaces = [r for r in test_results if r.get("result") == "FAIL"]
        
        # 构建HTML格式的邮件内容
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>接口自动化测试报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; }}
        .summary {{ margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 8px; }}
        .stats {{ display: flex; gap: 20px; margin-top: 15px; }}
        .stat-item {{ text-align: center; padding: 15px 25px; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .stat-value {{ font-size: 24px; font-weight: bold; }}
        .stat-label {{ font-size: 12px; color: #666; }}
        .passed {{ color: #10b981; }}
        .failed {{ color: #ef4444; }}
        .total {{ color: #6366f1; }}
        .error-list {{ margin-top: 20px; }}
        .error-item {{ padding: 12px; border-left: 4px solid #ef4444; background: #fef2f2; margin-bottom: 10px; border-radius: 0 4px 4px 0; }}
        .footer {{ margin-top: 30px; padding-top: 15px; border-top: 1px solid #eee; color: #999; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 接口自动化测试报告</h1>
        <p style="opacity: 0.9;">测试时间: {test_time}</p>
    </div>
    
    <div class="summary">
        <h3>📊 测试统计</h3>
        <div class="stats">
            <div class="stat-item">
                <div class="stat-value total">{total}</div>
                <div class="stat-label">总接口数</div>
            </div>
            <div class="stat-item">
                <div class="stat-value passed">{passed}</div>
                <div class="stat-label">成功</div>
            </div>
            <div class="stat-item">
                <div class="stat-value failed">{failed}</div>
                <div class="stat-label">失败</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" style="color: {'#10b981' if pass_rate >= 90 else '#f59e0b'}">{pass_rate:.1f}%</div>
                <div class="stat-label">通过率</div>
            </div>
        </div>
    </div>
"""
        
        # 如果有失败接口，列出详情
        if failed_interfaces:
            html_content += """
    <div class="error-list">
        <h3>❌ 失败接口详情</h3>
"""
            for idx, result in enumerate(failed_interfaces, 1):
                html_content += f"""
        <div class="error-item">
            <strong>{idx}. {result.get('case_name', '未知')}</strong>
            <p><strong>URL:</strong> {result.get('url', '')}</p>
            <p><strong>方法:</strong> {result.get('method', '')}</p>
            <p><strong>状态码:</strong> {result.get('actual_status', 'N/A')}</p>
            <p><strong>错误信息:</strong> {result.get('error_msg', '')[:200]}</p>
        </div>
"""
            html_content += """
    </div>
"""
        
        html_content += """
    <div class="footer">
        <p>本邮件由接口自动化测试框架自动发送</p>
        <p>报告附件包含详细的测试结果和日志</p>
    </div>
</body>
</html>
"""
        
        # 构建主题(包含通过率)
        subject = f"【接口自动化测试】{'✅' if failed == 0 else '⚠️'} {passed}/{total} 通过 ({pass_rate:.0f}%)"
        
        return self.send_email(
            to_emails=self._get_to_emails(),
            subject=subject,
            content=html_content,
            attachments=attachments
        )
    
    def _get_to_emails(self):
        """获取收件人列表(从配置或环境变量读取)"""
        # 优先从环境变量读取
        to_emails_str = os.getenv("EMAIL_TO", "")
        if to_emails_str:
            return [email.strip() for email in to_emails_str.split(",") if email.strip()]
        
        # 默认收件人
        return ["test@example.com"]
