"""
登录接口测试用例
测试用户认证服务的登录接口
使用真实的测试环境和凭证
"""
import pytest
import allure
from datetime import datetime
from utils.http_client import HttpClient
from utils.logger import logger
from config.config import Config

# 创建HTTP客户端实例,使用默认配置
client = HttpClient()

# 全局变量,用于存储测试结果详情
test_result_details = {}


class TestAuthLogin:
    """用户登录接口测试类"""

    def _run_login_test(self, case_id, case_name, payload, expected_status=200, expected_code="200"):
        """通用的登录测试执行方法
        
        参数:
            case_id (str): 用例ID
            case_name (str): 用例名称
            payload (dict): 请求参数
            expected_status (int): 预期HTTP状态码,默认为200
            expected_code (str): 预期业务状态码,默认为"200"（成功）
                                设置为None表示不验证业务code
        
        返回:
            dict: 接口响应
        """
        # 记录测试开始时间
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 发送请求
        with allure.step(f"发送登录请求"):
            response = client.post("/service/boss/sysuser/authLogin", json=payload)
        
        # 获取响应状态码和业务code
        http_status = response["status_code"]
        response_data = response.get("response", {})
        business_code = str(response_data.get("code", ""))
        error_msg = response_data.get("message", "")
        
        # 记录响应日志
        logger.info(f"{case_name} - HTTP状态码: {http_status}, 业务code: {business_code}")
        
        # 判断测试结果
        http_pass = http_status == expected_status
        business_pass = True if expected_code is None else (business_code == expected_code)
        result = "PASS" if (http_pass and business_pass) else "FAIL"
        
        # 保存测试详情到全局变量
        test_result_details[f"test_login_{case_name.replace(' ', '_')}"] = {
            "case_id": case_id,
            "test_module": "登录模块",
            "case_name": case_name,
            "method": "POST",
            "url": "/service/boss/sysuser/authLogin",
            "params": str(payload),
            "expected_status": expected_status,
            "actual_status": http_status,
            "expected_code": expected_code,
            "actual_code": business_code,
            "actual_response": str(response.get("response_text", "")[:200]),
            "response_time": f"{response.get('elapsed_time', 0):.2f}",
            "error_msg": error_msg,
            "result": result,
            "test_time": start_time
        }
        
        # 添加断言，确保测试失败时pytest能识别
        with allure.step("验证HTTP状态码"):
            assert http_status == expected_status, \
                f"HTTP状态码断言失败: 预期{expected_status}, 实际{http_status}"
        
        # 如果需要验证业务code
        if expected_code is not None:
            with allure.step("验证业务状态码"):
                assert business_code == expected_code, \
                    f"业务状态码断言失败: 预期{expected_code}, 实际{business_code}"
        
        return response

    @allure.feature('用户认证')
    @allure.story('登录接口测试-正确凭证')
    def test_login_success(self):
        """测试使用正确凭证登录"""
        payload = {
            "username": Config.TEST_USERNAME,
            "password": Config.TEST_PASSWORD
        }
        
        response = self._run_login_test(
            case_id="001",
            case_name="登录成功",
            payload=payload,
            expected_status=200,
            expected_code="200"
        )
        
        # 登录成功特有的验证：检查响应数据结构和token
        response_data = response.get("response", {})
        with allure.step("验证响应数据结构"):
            assert isinstance(response_data, dict), "响应是JSON对象"
            assert "data" in response_data, "响应包含data字段"
            assert "token" in response_data.get("data", {}), "响应包含token"
        
        logger.info(f"登录成功响应: {response.get('response_text', '')[:500]}")

    @allure.feature('用户认证')
    @allure.story('登录接口测试-错误密码')
    def test_login_wrong_password(self):
        """测试使用错误密码登录"""
        payload = {
            "username": Config.TEST_USERNAME,
            "password": "wrongpassword"
        }
        
        self._run_login_test(
            case_id="002",
            case_name="错误密码登录",
            payload=payload,
            expected_status=200,
            expected_code="2002"  # 实际返回的业务失败码
        )

    @allure.feature('用户认证')
    @allure.story('登录接口测试-空用户名')
    def test_login_empty_username(self):
        """测试使用空用户名登录"""
        payload = {
            "username": "",
            "password": Config.TEST_PASSWORD
        }
        
        self._run_login_test(
            case_id="003",
            case_name="空用户名登录",
            payload=payload,
            expected_status=200,
            expected_code="2002"
        )

    @allure.feature('用户认证')
    @allure.story('登录接口测试-空密码')
    def test_login_empty_password(self):
        """测试使用空密码登录"""
        payload = {
            "username": Config.TEST_USERNAME,
            "password": ""
        }
        
        self._run_login_test(
            case_id="004",
            case_name="空密码登录",
            payload=payload,
            expected_status=200,
            expected_code="2002"
        )

    @allure.feature('用户认证')
    @allure.story('登录接口测试-缺少参数')
    def test_login_missing_params(self):
        """测试缺少必填参数登录"""
        payload = {
            "username": Config.TEST_USERNAME
            # 缺少 password 参数
        }
        
        self._run_login_test(
            case_id="005",
            case_name="缺少参数登录",
            payload=payload,
            expected_status=200,
            expected_code="500"  # 缺少参数服务器返回500
        )
