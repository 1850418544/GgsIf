# 接口自动化测试框架

## 项目结构

```
GgsIf/
├── config/
│   ├── __init__.py
│   └── config.py              # 配置文件
├── utils/
│   ├── __init__.py
│   ├── logger.py              # 日志模块(loguru)
│   ├── http_client.py         # HTTP客户端封装
│   ├── excel_reporter.py      # Excel报告生成
│   └── txt_reporter.py        # TXT报告生成
├── testcases/
│   ├── __init__.py
│   └── test_httpbin.py        # 示例测试用例
├── reports/
│   ├── allure-results/        # Allure报告数据
│   ├── test_report.xlsx       # Excel报告
│   └── test_summary.txt      # TXT报告
├── logs/
│   └── test_*.log             # 日志文件
├── conftest.py                # pytest配置文件
├── pytest.ini                 # pytest配置
├── requirements.txt            # 依赖列表
└── run_tests.bat             # 运行脚本
```

## 功能特性

1. **日志管理** - 使用loguru记录详细日志
2. **Allure报告** - 生成美观的Allure HTML报告
3. **Excel报告** - 详细的Excel测试报告
4. **TXT报告** - 简洁的文本测试摘要
5. **参数化测试** - 支持数据驱动测试
6. **灵活的HTTP客户端** - 封装requests库

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行测试

### 方式1: 使用运行脚本
```bash
run_tests.bat
```

### 方式2: 直接运行pytest
```bash
python -m pytest testcases/ -v
```

### 方式3: 生成Allure报告
```bash
# 运行测试并生成allure数据
python -m pytest testcases/ -v --alluredir=reports/allure-results

# 生成HTML报告（需要安装allure-cli）
allure serve reports/allure-results
```

## 配置说明

修改 `config/config.py` 中的配置：

- `BASE_URL`: API基础URL
- `TIMEOUT`: 请求超时时间
- `HEADERS`: 默认请求头
- `LOG_DIR`: 日志目录
- `REPORT_DIR`: 报告目录

## 添加新测试用例

1. 在 `testcases/` 目录下创建新的测试文件
2. 使用 `HttpClient` 类发送请求
3. 使用 `allure` 装饰器标记测试
4. 编写断言验证响应

示例：
```python
import allure
from utils.http_client import HttpClient

client = HttpClient()

class TestMyAPI:
    @allure.feature('功能模块')
    @allure.story('测试场景')
    def test_example(self):
        response = client.get("/api/endpoint")
        assert response["status_code"] == 200
```

## 报告说明

### TXT报告 (test_summary.txt)
- 测试汇总统计
- 通过/失败接口数量
- 通过率

### Excel报告 (test_report.xlsx)
- 详细的测试数据
- 包含用例编号、名称、请求参数等
- 适合存档和数据分析

### Allure报告
- 美观的Web界面
- 支持分类筛选
- 详细的步骤和日志

## 依赖列表

- pytest==7.4.3
- allure-pytest==2.13.2
- requests==2.31.0
- loguru==0.7.2
- openpyxl==3.1.2
