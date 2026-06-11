"""
TXT报告生成模块
生成简洁的文本测试报告，包含测试汇总和详细结果
便于快速查看测试结果概览
"""
from datetime import datetime
from config.config import Config
from utils.logger import logger

class TxtReporter:
    """TXT报告生成器类"""
    
    @staticmethod
    def generate_report(test_results):
        """生成TXT格式的测试报告
        
        参数：
            test_results (list): 测试结果列表，每个元素是一个测试用例字典
        
        使用示例：
            TxtReporter.generate_report(test_results)
        
        报告内容包括：
            - 测试时间
            - 测试汇总(总用例数、通过数、失败数、通过率)
            - 失败接口详情(如果有失败)
            - 详细测试结果列表(包含用例编号、模块、名称、URL、参数、状态码、响应、响应时间、测试时间、结果)
        """
        # 确保目录存在
        Config.ensure_dirs()
        
        # 计算统计数据
        passed = sum(1 for r in test_results if r.get("result") == "PASS")
        failed = len(test_results) - passed
        pass_rate = (passed / len(test_results) * 100) if test_results else 0
        
        # 构建报告内容
        report_lines = []
        
        # 报告标题
        report_lines.append("=" * 80)
        report_lines.append("接口自动化测试报告".center(80))
        report_lines.append("=" * 80)
        report_lines.append("")
        
        # 测试时间
        report_lines.append(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # 测试汇总
        report_lines.append("-" * 80)
        report_lines.append("测试汇总")
        report_lines.append("-" * 80)
        report_lines.append(f"总接口数: {len(test_results)}")
        report_lines.append(f"通过接口: {passed}")
        report_lines.append(f"失败接口: {failed}")
        report_lines.append(f"通过率: {pass_rate:.2f}%")
        report_lines.append("")
        
        # 失败接口详情(如果有失败)
        if failed > 0:
            report_lines.append("-" * 80)
            report_lines.append("失败接口详情")
            report_lines.append("-" * 80)
            
            for idx, result in enumerate(test_results, 1):
                if result.get("result") == "FAIL":
                    report_lines.append(f"\n{idx}. {result.get('case_name', 'Unknown')}")
                    report_lines.append(f"   用例编号: {result.get('case_id', '')}")
                    report_lines.append(f"   测试模块: {result.get('test_module', '')}")
                    report_lines.append(f"   接口URL: {result.get('url', '')}")
                    report_lines.append(f"   请求方法: {result.get('method', '')}")
                    report_lines.append(f"   请求参数: {result.get('params', '')}")
                    report_lines.append(f"   预期状态码: {result.get('expected_status', '')}")
                    report_lines.append(f"   实际状态码: {result.get('actual_status', '')}")
                    report_lines.append(f"   实际响应: {result.get('actual_response', '')}")
                    report_lines.append(f"   响应时间: {result.get('response_time', '')} ms")
                    report_lines.append(f"   测试时间: {result.get('test_time', '')}")
                    report_lines.append(f"   错误信息: {result.get('error_msg', '')}")
        
        # 详细测试结果
        report_lines.append("")
        report_lines.append("=" * 80)
        report_lines.append("详细测试结果")
        report_lines.append("=" * 80)
        
        # 遍历所有测试用例
        for idx, result in enumerate(test_results, 1):
            report_lines.append(f"\n【{idx}】{result.get('case_name', 'Unknown')}")
            report_lines.append(f"  用例编号: {result.get('case_id', '')}")
            report_lines.append(f"  测试模块: {result.get('test_module', '')}")
            report_lines.append(f"  接口URL: {result.get('url', '')}")
            report_lines.append(f"  请求方法: {result.get('method', '')}")
            report_lines.append(f"  请求参数: {result.get('params', '')}")
            report_lines.append(f"  预期状态码: {result.get('expected_status', '')}")
            report_lines.append(f"  实际状态码: {result.get('actual_status', '')}")
            report_lines.append(f"  实际响应: {result.get('actual_response', '')}")
            report_lines.append(f"  响应时间: {result.get('response_time', '')} ms")
            report_lines.append(f"  测试时间: {result.get('test_time', '')}")
            report_lines.append(f"  测试结果: {result.get('result', '')}")
            if result.get('error_msg'):
                report_lines.append(f"  错误信息: {result.get('error_msg', '')}")
        
        # 报告结尾
        report_lines.append("")
        report_lines.append("=" * 80)
        
        # 写入文件
        try:
            with open(Config.TXT_REPORT, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report_lines))
            logger.info(f"TXT报告已生成: {Config.TXT_REPORT}")
        except Exception as e:
            logger.error(f"生成TXT报告失败: {e}")
            raise