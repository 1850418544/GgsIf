# pytest 教程

## 一、pytest 简介

pytest 是 Python 中最流行的测试框架之一，具有以下特点：

- **简单易用**：测试用例可以是简单的函数或类方法
- **丰富的断言**：支持 Python 标准断言，失败时提供详细的错误信息
- **自动发现**：自动发现测试文件和测试函数
- **fixture 系统**：强大的测试夹具系统，支持依赖注入
- **参数化测试**：支持数据驱动测试
- **插件生态**：丰富的插件支持（如 allure-pytest、pytest-html 等）

---

## 二、安装

```bash
# 安装 pytest
pip install pytest

# 安装常用插件
pip install pytest-allure  # Allure报告
pip install pytest-html    # HTML报告
pip install pytest-timeout # 超时控制
```

---

## 三、基本概念

### 3.1 测试文件命名规则

pytest 会自动发现符合以下规则的文件和函数：

| 类型 | 规则 | 示例 |
|------|------|------|
| 测试文件 | `test_*.py` 或 `*_test.py` | `test_login.py`, `auth_test.py` |
| 测试类 | 以 `Test` 开头，不含 `__init__` 方法 | `class TestAuth:` |
| 测试函数 | 以 `test_` 开头 | `def test_login_success():` |

### 3.2 基本测试用例

#### 简单函数测试

```python
# test_example.py

def test_add():
    """测试加法功能"""
    result = 2 + 3
    assert result == 5
```

#### 类方法测试

```python
# test_example.py

class TestMath:
    """数学运算测试类"""
    
    def test_add(self):
        """测试加法"""
        assert 2 + 3 == 5
    
    def test_multiply(self):
        """测试乘法"""
        assert 2 * 3 == 6
```

---

## 四、运行测试

### 4.1 基本命令

```bash
# 运行当前目录下所有测试
pytest

# 运行指定文件
pytest test_login.py

# 运行指定函数
pytest test_login.py::test_login_success

# 运行指定类的方法
pytest test_login.py::TestAuth::test_login_success

# 显示详细输出
pytest -v

# 显示更详细的输出（包括print内容）
pytest -s

# 只运行失败的测试
pytest --tb=short

# 设置超时时间（需要安装 pytest-timeout）
pytest --timeout=60
```

### 4.2 常用选项

| 选项 | 说明 |
|------|------|
| `-v` | 详细输出 |
| `-s` | 显示标准输出（print内容） |
| `-x` | 遇到第一个失败就停止 |
| `--tb=short` | 简化错误信息 |
| `--tb=no` | 不显示错误信息 |
| `-k` | 按关键字筛选测试 |
| `-m` | 按标记筛选测试 |

---

## 五、断言

pytest 使用 Python 标准断言，失败时会提供详细的错误信息。

### 5.1 基本断言

```python
def test_assertions():
    # 相等断言
    assert 1 + 1 == 2
    
    # 不等断言
    assert 1 + 1 != 3
    
    # 包含断言
    assert "hello" in "hello world"
    
    # 布尔断言
    assert True
    
    # 不为空断言
    assert len([1, 2, 3]) > 0
    
    # 异常断言
    with pytest.raises(ValueError):
        raise ValueError("test error")
```

### 5.2 自定义错误信息

```python
def test_with_message():
    result = 2 + 2
    assert result == 5, f"期望5，实际得到{result}"
```

---

## 六、Fixture 系统

Fixture 是 pytest 的核心特性，用于管理测试依赖和共享资源。

### 6.1 基本用法

```python
import pytest

@pytest.fixture
def setup_data():
    """准备测试数据"""
    data = {"username": "test", "password": "123456"}
    return data

def test_login(setup_data):
    """使用fixture"""
    assert setup_data["username"] == "test"
```

### 6.2 Fixture 作用域

```python
@pytest.fixture(scope="function")  # 默认，每个测试函数执行一次
@pytest.fixture(scope="class")     # 每个测试类执行一次
@pytest.fixture(scope="module")    # 每个模块执行一次
@pytest.fixture(scope="session")   # 整个测试会话执行一次
def my_fixture():
    # setup
    yield data
    # teardown（yield之后的代码在测试完成后执行）
```

### 6.3 Fixture 依赖

```python
@pytest.fixture
def user():
    return {"name": "test"}

@pytest.fixture
def order(user):
    """依赖于user fixture"""
    return {"user_id": user["name"], "amount": 100}

def test_order(order):
    assert order["user_id"] == "test"
```

### 6.4 带参数的 Fixture

```python
@pytest.fixture(params=[1, 2, 3])
def number(request):
    """参数化fixture"""
    return request.param

def test_number(number):
    """每个参数执行一次测试"""
    assert number > 0
```

---

## 七、参数化测试

参数化测试允许用不同的数据运行同一个测试用例。

### 7.1 使用 @pytest.mark.parametrize

```python
import pytest

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (2, 3, 5),
    (10, 20, 30),
])
def test_add(a, b, expected):
    """参数化测试加法"""
    assert a + b == expected
```

### 7.2 参数化测试类

```python
@pytest.mark.parametrize("username, password, should_pass", [
    ("fan", "fan123", True),
    ("fan", "wrong", False),
    ("", "fan123", False),
])
class TestLogin:
    def test_login(self, username, password, should_pass):
        """测试不同的登录场景"""
        result = login(username, password)
        assert result == should_pass
```

---

## 八、测试标记

使用标记可以对测试进行分类和筛选。

### 8.1 定义标记

```python
import pytest

@pytest.mark.smoke
def test_login():
    """冒烟测试：登录功能"""
    pass

@pytest.mark.regression
def test_order():
    """回归测试：订单功能"""
    pass

@pytest.mark.skip(reason="功能尚未实现")
def test_feature():
    """跳过测试"""
    pass

@pytest.mark.skipif(True, reason="条件不满足")
def test_conditional():
    """条件跳过"""
    pass
```

### 8.2 使用标记运行测试

```bash
# 只运行冒烟测试
pytest -m smoke

# 排除冒烟测试
pytest -m "not smoke"

# 运行多个标记
pytest -m "smoke or regression"
```

### 8.3 注册自定义标记

在 `pytest.ini` 或 `setup.cfg` 中注册标记：

```ini
[pytest]
markers =
    smoke: 冒烟测试
    regression: 回归测试
    api: API测试
```

---

## 九、pytest.ini 配置

```ini
[pytest]
# 测试目录
testpaths = 
    testcases

# 文件匹配规则
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# 添加标记
markers =
    smoke: 冒烟测试
    regression: 回归测试
    api: API测试

# 添加命令行参数
addopts = -v --tb=short
```

---

## 十、钩子函数（Hook Functions）

### 10.1 什么是钩子函数

钩子函数（Hook Functions）是 pytest 提供的回调机制，允许在测试执行的不同阶段插入自定义逻辑。钩子函数通常定义在 `conftest.py` 文件中，对该目录及其子目录下的所有测试生效。

### 10.2 常用钩子函数

#### 10.2.1 会话级别钩子

```python
# conftest.py

def pytest_sessionstart(session):
    """测试会话开始时执行（在收集测试之前）"""
    print("=== 测试会话开始 ===")

def pytest_sessionfinish(session, exitstatus):
    """测试会话结束时执行（在所有测试完成后）"""
    print(f"=== 测试会话结束，退出状态: {exitstatus} ===")
```

#### 10.2.2 测试收集钩子

```python
def pytest_collection_modifyitems(session, config, items):
    """修改收集到的测试用例列表"""
    # 例如：按名称排序
    items.sort(key=lambda x: x.name)
    
    # 例如：添加标记
    for item in items:
        if "login" in item.name:
            item.add_marker(pytest.mark.login)

def pytest_collect_file(parent, path):
    """自定义测试文件收集逻辑"""
    # 返回 None 表示不收集该文件
    if "skip" in str(path):
        return None
```

#### 10.2.3 测试执行钩子

```python
def pytest_runtest_protocol(item, nextitem):
    """测试用例执行协议（控制测试执行流程）"""
    # 返回 True 表示跳过默认执行
    return None  # 使用默认行为

def pytest_runtest_makereport(item, call):
    """自定义测试报告"""
    if call.when == "call":
        # 测试执行阶段
        if call.excinfo is not None:
            print(f"测试失败: {item.name}")
```

#### 10.2.4 测试函数级别钩子

```python
def pytest_runtest_setup(item):
    """每个测试用例执行前调用"""
    print(f"准备测试: {item.name}")

def pytest_runtest_teardown(item, nextitem):
    """每个测试用例执行后调用"""
    print(f"清理测试: {item.name}")
```

#### 10.2.5 配置相关钩子

```python
def pytest_addoption(parser):
    """添加自定义命令行参数"""
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="测试环境: test, staging, prod"
    )

def pytest_configure(config):
    """配置 pytest（在命令行参数解析后）"""
    env = config.getoption("--env")
    print(f"当前测试环境: {env}")
```

### 10.3 使用钩子函数的实际场景

#### 场景1：统一日志配置

```python
# conftest.py
import logging

def pytest_sessionstart(session):
    """配置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
```

#### 场景2：收集测试结果

```python
# conftest.py
test_results = []

def pytest_runtest_makereport(item, call):
    """收集测试结果"""
    if call.when == "call":
        result = {
            "name": item.name,
            "status": "PASS" if call.excinfo is None else "FAIL",
            "duration": call.duration
        }
        test_results.append(result)

def pytest_sessionfinish(session, exitstatus):
    """输出测试总结"""
    passed = [r for r in test_results if r["status"] == "PASS"]
    failed = [r for r in test_results if r["status"] == "FAIL"]
    print(f"\n测试总结: {len(passed)} 通过, {len(failed)} 失败")
```

#### 场景3：根据环境选择测试用例

```python
# conftest.py
def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="test")

def pytest_collection_modifyitems(config, items):
    env = config.getoption("--env")
    skip_env = pytest.mark.skip(reason=f"不运行在 {env} 环境")
    
    for item in items:
        # 如果测试标记了 @pytest.mark.prod，但当前不是prod环境
        if "prod" in item.keywords and env != "prod":
            item.add_marker(skip_env)
```

### 10.4 钩子函数执行顺序

```
pytest_sessionstart()
    │
    ├─> pytest_collection_modifyitems()
    │
    ├─> 对于每个测试用例:
    │       │
    │       ├─> pytest_runtest_setup()
    │       │
    │       ├─> pytest_runtest_protocol()
    │       │       │
    │       │       └─> pytest_runtest_makereport(when="call")
    │       │
    │       └─> pytest_runtest_teardown()
    │
    └─> pytest_sessionfinish()
```

### 10.5 钩子函数的作用域

| 文件位置 | 作用域 |
|---------|--------|
| 项目根目录的 `conftest.py` | 整个项目 |
| 子目录的 `conftest.py` | 该目录及其子目录 |

---

## 十一、异常处理

### 11.1 测试异常抛出

```python
def test_raise_exception():
    """测试函数是否抛出预期异常"""
    with pytest.raises(ValueError) as exc_info:
        raise ValueError("test")
    
    # 检查异常消息
    assert "test" in str(exc_info.value)
```

### 10.2 测试警告

```python
import warnings

def test_warning():
    """测试警告"""
    with pytest.warns(DeprecationWarning):
        warnings.warn("deprecated", DeprecationWarning)
```

---

## 十一、测试报告

### 11.1 使用 allure-pytest

```bash
# 安装
pip install allure-pytest

# 生成报告数据
pytest --alluredir=allure-results

# 查看报告（需要安装 allure 命令行工具）
allure serve allure-results
```

### 11.2 使用 pytest-html

```bash
# 安装
pip install pytest-html

# 生成HTML报告
pytest --html=report.html
```

---

## 十二、实用技巧

### 12.1 临时目录

```python
def test_temp_dir(tmpdir):
    """使用临时目录"""
    file = tmpdir / "test.txt"
    file.write("hello")
    assert file.read() == "hello"
```

### 12.2 临时文件

```python
def test_temp_file(tmp_path):
    """使用临时路径"""
    file = tmp_path / "data.json"
    file.write_text('{"key": "value"}')
    content = file.read_text()
    assert "key" in content
```

### 12.3 运行特定测试

```bash
# 按名称匹配
pytest -k "login"

# 排除特定测试
pytest -k "not login"

# 使用正则表达式
pytest -k "test_login_.*_success"
```

---

## 十三、与其他工具集成

### 13.1 与 requests 集成（API测试）

```python
import requests

@pytest.fixture
def api_client():
    session = requests.Session()
    session.base_url = "https://api.example.com"
    return session

def test_api_login(api_client):
    response = api_client.post("/login", json={"user": "test"})
    assert response.status_code == 200
```

### 13.2 与 unittest 集成

pytest 可以直接运行 unittest 测试：

```python
import unittest

class TestMyUnitTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(2 + 2, 4)
```

---

## 十四、常见问题

### Q1: 如何跳过测试？

```python
@pytest.mark.skip(reason="原因")
def test_skip():
    pass
```

### Q2: 如何让测试失败时继续运行？

```bash
pytest --tb=short  # 不停止，显示简化的错误信息
```

### Q3: 如何测试异步代码？

安装 `pytest-asyncio`：

```bash
pip install pytest-asyncio
```

```python
@pytest.mark.asyncio
async def test_async():
    result = await async_function()
    assert result == "expected"
```

---

## 十五、项目结构示例

```
project/
├── config/
│   └── config.py
├── testcases/
│   ├── test_auth.py
│   ├── test_api.py
│   └── test_ui.py
├── utils/
│   └── helpers.py
├── pytest.ini
└── requirements.txt
```

---

## 十六、总结

pytest 是一个功能强大且易于使用的测试框架，主要特点包括：

1. **简单直观**：测试用例编写简单
2. **fixture 系统**：强大的依赖管理
3. **参数化测试**：支持数据驱动
4. **丰富的插件**：扩展功能丰富
5. **良好的文档**：社区活跃，文档完善

掌握 pytest 可以大大提高测试效率和代码质量！