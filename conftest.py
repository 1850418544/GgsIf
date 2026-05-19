"""
pytest配置文件
包含测试前后的钩子函数，用于：
- 初始化日志和目录
- 收集测试结果
- 生成测试报告
- 发送企业微信通知
"""
import pytest
from datetime import datetime
from config.config import Config
from utils.logger import logger
from utils.excel_reporter import ExcelReporter
from utils.txt_reporter import TxtReporter

# 存储所有测试结果的列表
test_results = []

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
        
    except Exception as e:
        logger.error(f"生成报告或发送通知时出错: {e}")
        import traceback
        logger.error(traceback.format_exc())