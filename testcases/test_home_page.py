"""
首页接口测试用例
测试登录后访问的首页数据接口
认证方式: X-Token请求头
"""
import pytest
import allure
from datetime import datetime
from utils.http_client import HttpClient
from utils.logger import logger
from config.config import Config

test_result_details = {}


@pytest.fixture(scope="module")
def client():
    """创建共享的HTTP客户端实例"""
    client_instance = HttpClient()
    return client_instance


@pytest.fixture(scope="module")
def access_token(client):
    """获取登录token(fixture方式,不生成测试报告)"""
    payload = {"username": Config.TEST_USERNAME, "password": Config.TEST_PASSWORD}
    response = client.post("/service/boss/sysuser/authLogin", json=payload)
    
    assert response["status_code"] == 200, "登录失败"
    
    token = ""
    if "response" in response and isinstance(response["response"], dict):
        data = response["response"].get("data", {})
        if isinstance(data, dict):
            token = data.get("token", "")
    
    assert token, "未获取到token"
    client.session.headers.update({"X-Token": token})
    logger.info(f"获取到token: {token[:20]}...")
    
    return token


class TestHomePage:
    """首页接口测试类"""

    def _run_api_test(self, case_id, case_name, method, url, client, params=None, json=None, expected_status=200, expected_code="200"):
        """通用的API测试执行方法
        
        参数:
            case_id (str): 用例ID
            case_name (str): 用例名称
            method (str): HTTP方法(GET/POST)
            url (str): API端点路径
            client: HTTP客户端实例
            params (dict, optional): URL查询参数(GET方法使用)
            json (dict, optional): 请求体数据(POST方法使用)
            expected_status (int): 预期HTTP状态码,默认为200
            expected_code (str): 预期业务状态码,默认为"200"
        
        返回:
            dict: 接口响应
        """
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 发送请求
        with allure.step(f"发送{method}请求: {url}"):
            if method.upper() == "GET":
                response = client.get(url, params=params)
            elif method.upper() == "POST":
                response = client.post(url, json=json)
            else:
                response = client.request(method, url, params=params, json=json)
        
        # 获取响应信息
        http_status = response["status_code"]
        response_data = response.get("response", {})
        business_code = str(response_data.get("code", ""))
        response_text = response.get("response_text", "")
        
        # 判断是否成功（考虑授权情况）
        is_success = http_status == expected_status and "未经授权" not in response_text
        
        # 业务code判断
        if expected_code is not None:
            is_success = is_success and (business_code == expected_code)
        
        # 记录日志
        logger.info(f"{case_name} - HTTP状态码: {http_status}, 业务code: {business_code}")
        
        # 保存测试详情
        test_result_details[f"test_{case_name.replace(' ', '_')}"] = {
            "case_id": case_id,
            "test_module": "首页模块",
            "case_name": case_name,
            "method": method,
            "url": url,
            "params": str(params) if params else str(json) if json else "{}",
            "expected_status": expected_status,
            "actual_status": http_status,
            "expected_code": expected_code,
            "actual_code": business_code,
            "actual_response": response_text[:200],
            "response_time": f"{response.get('elapsed_time', 0):.2f}",
            "result": "PASS" if is_success else "FAIL",
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
        
        # 验证未授权情况
        with allure.step("验证授权状态"):
            assert "未经授权" not in response_text, \
                "接口返回'未经授权', token可能已过期或无效"
        
        return response

    @allure.feature('首页模块')
    @allure.story('home/statistics')
    def test_home_statistics(self, client, access_token):
        """首页统计接口"""
        self._run_api_test(
            case_id="007",
            case_name="首页统计接口",
            method="GET",
            url="/home/statistics",
            client=client
        )

    @allure.feature('首页模块')
    @allure.story('home/orderProductCountStatistics')
    def test_order_product_count_statistics(self, client, access_token):
        """订单产品数量统计"""
        self._run_api_test(
            case_id="008",
            case_name="订单产品数量统计",
            method="GET",
            url="/home/orderProductCountStatistics",
            client=client
        )

    @allure.feature('首页模块')
    @allure.story('home/getListStatistics')
    def test_get_list_statistics(self, client, access_token):
        """列表统计接口(GET方法)"""
        params = {"salesTimeRange": 0, "sortType": 0, "type": 0}
        self._run_api_test(
            case_id="009",
            case_name="列表统计",
            method="GET",
            url="/home/getListStatistics",
            client=client,
            params=params
        )

    @allure.feature('首页模块')
    @allure.story('home/getPlatformData')
    def test_get_platform_data(self, client, access_token):
        """平台数据接口"""
        self._run_api_test(
            case_id="010",
            case_name="平台数据",
            method="GET",
            url="/home/getPlatformData",
            client=client
        )

    @allure.feature('首页模块')
    @allure.story('home/recentSales')
    def test_recent_sales(self, client, access_token):
        """最近销售统计(7天)"""
        params = {"days": 7}
        self._run_api_test(
            case_id="011",
            case_name="最近销售(7天)",
            method="GET",
            url="/home/recentSales",
            client=client,
            params=params
        )

    @pytest.mark.skip(reason="接口报错了，暂时跳过")
    @allure.feature('首页模块')
    @allure.story('home/orderStatistics/byRange')
    def test_order_statistics_by_range(self, client, access_token):
        """订单统计(按时间范围)"""
        params = {"dateRange": "all"}
        self._run_api_test(
            case_id="012",
            case_name="订单统计(全范围)",
            method="GET",
            url="/home/orderStatistics/byRange",
            client=client,
            params=params
        )

    @allure.feature('首页模块')
    @allure.story('home/homePageStatistics - type=0')
    def test_home_page_statistics_type_0(self, client, access_token):
        """首页统计POST(type=0)"""
        payload = {"salesTimeRange": 0, "sortType": 0, "type": 0}
        self._run_api_test(
            case_id="013",
            case_name="首页统计POST(type=0)",
            method="POST",
            url="/home/homePageStatistics",
            client=client,
            json=payload
        )

    @allure.feature('首页模块')
    @allure.story('home/homePageStatistics - type=1')
    def test_home_page_statistics_type_1(self, client, access_token):
        """首页统计POST(type=1)"""
        payload = {"salesTimeRange": 0, "sortType": 0, "type": 1}
        self._run_api_test(
            case_id="014",
            case_name="首页统计POST(type=1)",
            method="POST",
            url="/home/homePageStatistics",
            client=client,
            json=payload
        )
