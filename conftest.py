"""
pytest配置文件
包含测试前后的钩子函数，用于：
- 初始化日志和目录
- 收集测试结果
- 生成测试报告
- 发送企业微信通知
- 发送邮件通知
"""
import pytest
import os
from datetime import datetime
from config.config import Config
from utils.logger import logger
from utils.excel_reporter import ExcelReporter
from utils.txt_reporter import TxtReporter

# 存储所有测试结果的列表
test_results = []

def _generate_email_content(test_results):
    """生成邮件通知的HTML内容
    
    参数：
        test_results (list): 测试结果列表
    
    返回：
        str: HTML格式的邮件内容
    """
    total = len(test_results)
    passed = sum(1 for r in test_results if r.get("result") == "PASS")
    failed = total - passed
    pass_rate = passed / total * 100 if total > 0 else 0
    
    test_time = test_results[0].get('test_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S')) if test_results else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    failed_interfaces = [r for r in test_results if r.get("result") == "FAIL"]
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>接口自动化测试报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px; margin-bottom: 20px; }}
        .header h1 {{ margin: 0; font-size: 22px; }}
        .header p {{ margin: 8px 0 0; opacity: 0.9; font-size: 14px; }}
        .summary {{ background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
        .summary h3 {{ margin: 0 0 15px; color: #333; }}
        .stats {{ display: flex; gap: 15px; }}
        .stat-item {{ flex: 1; text-align: center; padding: 18px; background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
        .stat-value {{ font-size: 28px; font-weight: bold; }}
        .stat-label {{ font-size: 12px; color: #666; margin-top: 5px; }}
        .passed {{ color: #10b981; }}
        .failed {{ color: #ef4444; }}
        .total {{ color: #6366f1; }}
        .error-list {{ margin-top: 20px; }}
        .error-list h3 {{ color: #dc2626; margin: 0 0 15px; }}
        .error-item {{ padding: 15px; border-left: 4px solid #ef4444; background: #fef2f2; margin-bottom: 12px; border-radius: 0 6px 6px 0; }}
        .error-item strong {{ display: block; margin-bottom: 8px; color: #1f2937; }}
        .error-item p {{ margin: 5px 0; font-size: 14px; color: #4b5563; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb; color: #9ca3af; font-size: 13px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 接口自动化测试报告</h1>
        <p>测试时间: {test_time}</p>
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
        <p>详细测试结果请查看附件</p>
    </div>
</body>
</html>
"""
    return html_content

def pytest_configure(config):
    """pytest配置钩子 - 在测试会话开始前调用
    
    初始化日志配置和必要的目录结构
    """
    logger.info("=" * 80)
    logger.info("开始接口自动化测试")
    logger.info("=" * 80)
    # 确保所有必要目录存在
    Config.ensure_dirs()

def pytest_collection_modifyitems(items):
    """pytest收集钩子 - 修改收集到的测试用例
    
    可以在这里对测试用例进行过滤、排序等操作
    """
    for item in items:
        if "test_" in item.nodeid:
            logger.debug(f"收集测试用例: {item.nodeid}")

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """pytest测试报告钩子 - 在每个测试用例执行后调用
    
    收集测试结果，记录到test_results列表中
    """
    # 获取测试结果
    outcome = yield
    report = outcome.get_result()
    
    # 只处理测试执行阶段的结果（call阶段）
    if report.when == "call":
        # 尝试从测试模块获取详细的测试结果
        test_info = None
        
        # 获取测试用例所属的模块
        module = item.module
        
        # 检查模块是否有test_result_details字典
        if hasattr(module, 'test_result_details'):
            # 获取该测试用例的详细结果
            if item.name in module.test_result_details:
                test_info = module.test_result_details[item.name]
        
        # 如果没有获取到详细结果，使用默认值
        if test_info is None:
            test_info = {
                "case_id": f"{len(test_results) + 1:03d}",
                "case_name": item.name,
                "method": "POST",
                "url": "/service/boss/sysuser/authLogin",
                "params": "",
                "expected_status": 200,
                "actual_status": 200 if report.outcome == "passed" else "N/A",
                "expected_field": "",
                "actual_response": "",
                "result": "PASS" if report.outcome == "passed" else "FAIL",
                "response_time": "",
                "error_msg": str(report.longrepr.reprcrash.message) if hasattr(report, 'longrepr') and report.longrepr else "",
                "test_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        
        # 添加到结果列表
        test_results.append(test_info)
        
        # 记录日志
        case_name = test_info.get("case_name", item.name)
        if report.outcome == "passed":
            logger.info(f"✓ 测试通过: {case_name}")
        else:
            logger.error(f"✗ 测试失败: {case_name}")

def pytest_sessionfinish(session, exitstatus):
    """pytest会话结束钩子 - 在所有测试完成后调用
    
    生成测试报告（Excel、TXT、Allure）
    发送企业微信通知
    """
    logger.info("=" * 80)
    logger.info("测试执行完成，正在生成报告...")
    logger.info("=" * 80)
    
    try:
        # 生成Excel报告
        excel_reporter = ExcelReporter()
        for result in test_results:
            excel_reporter.add_test_case(result)
        excel_reporter.save_report(test_results)
        
        # 生成TXT报告
        TxtReporter.generate_report(test_results)
        
        # 输出报告位置信息
        logger.info("=" * 80)
        logger.info("报告生成完成!")
        logger.info(f"Allure报告: {Config.ALLURE_DIR}")
        logger.info(f"Excel报告: {Config.REPORT_DIR}")
        logger.info(f"TXT报告: {Config.TXT_REPORT}")
        logger.info("=" * 80)
        
        # 发送企业微信通知
        if Config.SEND_WECHAT_NOTIFICATION and Config.WECHAT_WEBHOOK_URL:
            logger.info("正在发送企业微信通知...")
            from utils.wechat_notifier import WeChatWorkNotifier
            notifier = WeChatWorkNotifier(Config.WECHAT_WEBHOOK_URL)
            notifier.send_test_report(test_results, str(Config.TXT_REPORT))
            logger.info("企业微信通知发送完成!")
        elif Config.SEND_WECHAT_NOTIFICATION and not Config.WECHAT_WEBHOOK_URL:
            logger.warning("未配置企业微信Webhook地址，跳过发送通知")
        
        # 发送邮件通知
        if Config.SEND_EMAIL_NOTIFICATION and Config.SMTP_USER and Config.SMTP_PASS and Config.EMAIL_TO:
            logger.info("正在发送邮件通知...")
            from utils.email_notifier import EmailNotifier
            
            # 收集附件（Excel报告和TXT报告）
            attachments = []
            
            # 添加Excel报告（查找最新生成的报告）
            excel_reports = list(Config.REPORT_DIR.glob("test_report_*.xlsx"))
            if excel_reports:
                latest_excel = max(excel_reports, key=os.path.getctime)
                attachments.append(str(latest_excel))
            
            # 添加TXT报告
            if Config.TXT_REPORT.exists():
                attachments.append(str(Config.TXT_REPORT))
            
            # 创建邮件通知器并发送
            email_notifier = EmailNotifier(
                smtp_host=Config.SMTP_HOST,
                smtp_port=Config.SMTP_PORT,
                smtp_user=Config.SMTP_USER,
                smtp_pass=Config.SMTP_PASS,
                smtp_from_name=Config.SMTP_FROM_NAME
            )
            
            # 设置收件人列表
            to_emails = [email.strip() for email in Config.EMAIL_TO.split(",") if email.strip()]
            
            email_notifier.send_email(
                to_emails=to_emails,
                subject=f"【接口自动化测试报告】测试完成",
                content=_generate_email_content(test_results),
                attachments=attachments
            )
            logger.info("邮件通知发送完成!")
        elif Config.SEND_EMAIL_NOTIFICATION:
            # 检查缺少哪些配置
            missing_configs = []
            if not Config.SMTP_USER:
                missing_configs.append("SMTP_USER")
            if not Config.SMTP_PASS:
                missing_configs.append("SMTP_PASS")
            if not Config.EMAIL_TO:
                missing_configs.append("EMAIL_TO")
            logger.warning(f"未配置邮件发送所需参数({', '.join(missing_configs)})，跳过发送邮件通知")
        
    except Exception as e:
        logger.error(f"生成报告或发送通知时出错: {e}")
        import traceback
        logger.error(traceback.format_exc())