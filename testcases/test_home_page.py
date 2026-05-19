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

test_result_details = {}

@pytest.fixture(scope="module")
def client():
    """创建共享的HTTP客户端实例"""
    client_instance = HttpClient()
    return client_instance

@pytest.fixture(scope="module")
def access_token(client):
    """获取登录token（fixture方式，不生成测试报告）"""
    payload = {"username": "fan", "password": "fan123"}
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
    
    @allure.feature('首页模块')
    @allure.story('home/statistics')
    def test_home_statistics(self, client, access_token):
        """首页统计接口"""
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        response = client.get("/home/statistics")
        response_text = response.get("response_text", "")
        is_success = response["status_code"] == 200 and "未经授权" not in response_text
        
        test_result_details["test_home_statistics"] = {
            "case_id": "007",
            "test_module": "首页模块",
            "case_name": "首页统计接口",
            "method": "GET",
            "url": "/home/statistics",
            "params": "{}",
            "expected_status": 200,
            "actual_status": response["status_code"],
            "actual_response": response_text,
            "response_time": f"{response.get('elapsed_time', 0):.2f}",
            "result": "PASS" if is_success else "FAIL",
            "test_time": start_time
        }
    
    @allure.feature('首页模块')
    @allure.story('home/orderProductCountStatistics')
    def test_order_product_count_statistics(self, client, access_token):
        """订单产品数量统计"""
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        response = client.get("/home/orderProductCountStatistics")
        response_text = response.get("response_text", "")
        is_success = response["status_code"] == 200 and "未经授权" not in response_text
        
        test_result_details["test_order_product_count_statistics"] = {
            "case_id": "008",
            "test_module": "首页模块",
            "case_name": "订单产品数量统计",
            "method": "GET",
            "url": "/home/orderProductCountStatistics",
            "params": "{}",
            "expected_status": 200,
            "actual_status": response["status_code"],
            "actual_response": response_text,
            "response_time": f"{response.get('elapsed_time', 0):.2f}",
            "result": "PASS" if is_success else "FAIL",
            "test_time": start_time
        }
    
    @allure.feature('首页模块')
    @allure.story('home/getListStatistics')
    def test_get_list_statistics(self, client, access_token):
        """列表统计接口（GET方法）"""
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        params = {"salesTimeRange": 0, "sortType": 0, "type": 0}
        response = client.get("/home/getListStatistics", params=params)
        response_text = response.get("response_text", "")
        is_success = response["status_code"] == 200 and "未经授权" not in response_text
        
        test_result_details["test_get_list_statistics"] = {
            "case_id": "009",
            "test_module": "首页模块",
            "case_name": "列表统计",
            "method": "GET",
            "url": "/home/getListStatistics",
            "params": str(params),
            "expected_status": 200,
            "actual_status": response["status_code"],
            "actual_response": response_text,
            "response_time": f"{response.get('elapsed_time', 0):.2f}",
            "result": "PASS" if is_success else "FAIL",
            "test_time": start_time
        }
    
    @allure.feature('首页模块')
    @allure.story('home/getPlatformData')
    def test_get_platform_data(self, client, access_token):
        """平台数据接口"""
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        response = client.get("/home/getPlatformData")
        response_text = response.get("response_text", "")
        is_success = response["status_code"] == 200 and "未经授权" not in response_text
        
        test_result_details["test_get_platform_data"] = {
            "case_id": "010",
            "test_module": "首页模块",
            "case_name": "平台数据",
            "method": "GET",
            "url": "/home/getPlatformData",
            "params": "{}",
            "expected_status": 200,
            "actual_status": response["status_code"],
            "actual_response": response_text,
            "response_time": f"{response.get('elapsed_time', 0):.2f}",
            "result": "PASS" if is_success else "FAIL",
            "test_time": start_time
        }
    
    @allure.feature('首页模块')
    @allure.story('home/recentSales')
    def test_recent_sales(self, client, access_token):
        """最近销售统计（7天）"""
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        params = {"days": 7}
        response = client.get("/home/recentSales", params=params)
        response_text = response.get("response_text", "")
        is_success = response["status_code"] == 200 and "未经授权" not in response_text
        
        test_result_details["test_recent_sales"] = {
            "case_id": "011",
            "test_module": "首页模块",
            "case_name": "最近销售(7天)",
            "method": "GET",
            "url": "/home/recentSales",
            "params": str(params),
            "expected_status": 200,
            "actual_status": response["status_code"],
            "actual_response": response_text,
            "response_time": f"{response.get('elapsed_time', 0):.2f}",
            "result": "PASS" if is_success else "FAIL",
            "test_time": start_time
        }
    
    @allure.feature('首页模块')
    @allure.story('home/orderStatistics/byRange')
    def test_order_statistics_by_range(self, client, access_token):
        """订单统计（按时间范围）"""
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        params = {"dateRange": "all"}
        response = client.get("/home/orderStatistics/byRange", params=params)
        response_text = response.get("response_text", "")
        is_success = response["status_code"] == 200 and "未经授权" not in response_text
        
        test_result_details["test_order_statistics_by_range"] = {
            "case_id": "012",
            "test_module": "首页模块",
            "case_name": "订单统计(全范围)",
            "method": "GET",
            "url": "/home/orderStatistics/byRange",
            "params": str(params),
            "expected_status": 200,
            "actual_status": response["status_code"],
            "actual_response": response_text,
            "response_time": f"{response.get('elapsed_time', 0):.2f}",
            "result": "PASS" if is_success else "FAIL",
            "test_time": start_time
        }
    
    @allure.feature('首页模块')
    @allure.story('home/homePageStatistics - type=0')
    def test_home_page_statistics_type_0(self, client, access_token):
        """首页统计POST（type=0）"""
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        payload = {"salesTimeRange": 0, "sortType": 0, "type": 0}
        response = client.post("/home/homePageStatistics", json=payload)
        response_text = response.get("response_text", "")
        is_success = response["status_code"] == 200 and "未经授权" not in response_text
        
        test_result_details["test_home_page_statistics_type_0"] = {
            "case_id": "013",
            "test_module": "首页模块",
            "case_name": "首页统计POST(type=0)",
            "method": "POST",
            "url": "/home/homePageStatistics",
            "params": str(payload),
            "expected_status": 200,
            "actual_status": response["status_code"],
            "actual_response": response_text,
            "response_time": f"{response.get('elapsed_time', 0):.2f}",
            "result": "PASS" if is_success else "FAIL",
            "test_time": start_time
        }
    
    @allure.feature('首页模块')
    @allure.story('home/homePageStatistics - type=1')
    def test_home_page_statistics_type_1(self, client, access_token):
        """首页统计POST（type=1）"""
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        payload = {"salesTimeRange": 0, "sortType": 0, "type": 1}
        response = client.post("/home/homePageStatistics", json=payload)
        response_text = response.get("response_text", "")
        is_success = response["status_code"] == 200 and "未经授权" not in response_text
        
        test_result_details["test_home_page_statistics_type_1"] = {
            "case_id": "014",
            "test_module": "首页模块",
            "case_name": "首页统计POST(type=1)",
            "method": "POST",
            "url": "/home/homePageStatistics",
            "params": str(payload),
            "expected_status": 200,
            "actual_status": response["status_code"],
            "actual_response": response_text,
            "response_time": f"{response.get('elapsed_time', 0):.2f}",
            "result": "PASS" if is_success else "FAIL",
            "test_time": start_time
        }