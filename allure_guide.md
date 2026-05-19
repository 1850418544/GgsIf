# Allure 测试报告使用手册

## 一、Allure 简介

Allure 是一个开源的测试报告框架，能够生成清晰、美观、交互式的测试报告。它支持多种测试框架（如 pytest、JUnit、TestNG 等），提供丰富的测试结果展示和分析功能。

### 主要特点

- **可视化报告**：直观的图表和统计信息
- **分层展示**：支持 Feature → Story → Test 的层级结构
- **测试步骤**：详细记录每个测试步骤的执行情况
- **附件支持**：可附加截图、日志、文件等
- **历史趋势**：支持测试历史数据对比

***

## 二、安装与配置

### 2.1 安装 Allure 命令行工具

#### Windows 系统

```bash
# 使用 Scoop 安装（推荐）
scoop install allure

# 或手动下载安装
# 1. 下载 https://github.com/allure-framework/allure2/releases
# 2. 解压到本地目录
# 3. 将 bin 目录添加到系统环境变量 PATH
```

#### Linux/MacOS

```bash
# 使用 Homebrew（MacOS）
brew install allure

# 使用 SDKMAN
sdk install allure
```

### 2.2 安装 pytest-allure-adaptor

```bash
pip install allure-pytest
```

### 2.3 验证安装

```bash
allure --version
# 输出示例：2.25.0
```

***

## 三、基本使用

### 3.1 在 pytest 中使用 Allure

#### 3.1.1 基础注解

```python
import pytest
import allure

@allure.feature("登录模块")  # 功能模块
@allure.story("登录成功")    # 用户故事/场景
@allure.title("测试登录成功场景")  # 测试标题
def test_login_success():
    """测试使用正确凭证登录"""
    with allure.step("准备登录数据"):
        username = "fan"
        password = "fan123"
    
    with allure.step("发送登录请求"):
        # 执行登录请求
        pass
    
    with allure.step("验证登录结果"):
        assert True
```

#### 3.1.2 运行测试并生成报告

```bash
# 运行测试并生成 Allure 报告数据
pytest testcases/ --alluredir=allure-results

# 生成 HTML 报告
allure generate allure-results -o allure-report --clean

# 启动本地服务查看报告
allure serve allure-results
```

***

## 四、常用注解说明

### 4.1 层级注解

| 注解                      | 作用        | 使用场景        |
| ----------------------- | --------- | ----------- |
| `@allure.feature()`     | 定义功能模块    | 如：登录模块、首页模块 |
| `@allure.story()`       | 定义用户故事/场景 | 如：登录成功、登录失败 |
| `@allure.title()`       | 定义测试用例标题  | 自定义测试显示名称   |
| `@allure.description()` | 添加测试描述    | 详细说明测试目的    |

### 4.2 步骤注解

```python
# 方式1：使用 with 语句
with allure.step("步骤描述"):
    # 执行操作
    pass

# 方式2：使用装饰器
@allure.step("步骤描述")
def my_step():
    # 执行操作
    pass
```

### 4.3 优先级注解

```python
@allure.severity(allure.severity_level.CRITICAL)  # 严重
@allure.severity(allure.severity_level.HIGH)       # 高
@allure.severity(allure.severity_level.MEDIUM)     # 中
@allure.severity(allure.severity_level.LOW)        # 低
@allure.severity(allure.severity_level.MINOR)      # 轻微
def test_example():
    pass
```

### 4.4 附件注解

```python
# 添加文本附件
allure.attach("这是一段文本内容", name="文本日志", attachment_type=allure.attachment_type.TEXT)

# 添加图片附件
allure.attach(file.read(), name="截图", attachment_type=allure.attachment_type.PNG)

# 添加 JSON 数据
allure.attach(json.dumps(data), name="响应数据", attachment_type=allure.attachment_type.JSON)
```

***

## 五、报告生成命令

### 5.1 生成报告

```bash
# 生成 HTML 报告到指定目录
allure generate <results_dir> -o <output_dir>

# 强制覆盖已有报告
allure generate <results_dir> -o <output_dir> --clean
```

### 5.2 启动预览服务

```bash
# 直接启动服务（无需先生成 HTML）
allure serve <results_dir>

# 指定端口
allure serve <results_dir> -p 8080
```

### 5.3 打开已生成的报告

```bash
allure open <report_dir>
```

***

## 六、报告结构说明

### 6.1 报告首页

- **统计概览**：总测试数、通过数、失败数、跳过数
- **趋势图表**：历史测试趋势（需配置历史数据）
- **分类统计**：按 severity、feature 等维度统计

### 6.2 测试结果页面

- **测试列表**：按 feature/story 层级展示
- **测试详情**：点击查看具体测试步骤和附件
- **失败详情**：显示断言失败信息和堆栈跟踪

***

## 七、高级特性

### 7.1 参数化测试支持

```python
import pytest

@allure.feature("登录模块")
@pytest.mark.parametrize("username,password,expected", [
    ("fan", "fan123", "success"),
    ("fan", "wrong", "fail"),
    ("", "fan123", "fail"),
])
def test_login_parametrize(username, password, expected):
    allure.dynamic.title(f"登录测试: {username}")
    # 测试逻辑
    pass
```

### 7.2 动态修改测试信息

```python
def test_dynamic_info():
    allure.dynamic.title("动态标题")
    allure.dynamic.description("动态描述")
    allure.dynamic.severity(allure.severity_level.HIGH)
```

### 7.3 链接到外部资源

```python
@allure.link("https://example.com", name="需求文档")
@allure.issue("BUG-123", name="关联缺陷")
@allure.testcase("TC-456", name="测试用例")
def test_with_links():
    pass
```

***

## 八、与框架集成

### 8.1 与 conftest.py 集成

```python
import allure
import pytest

@pytest.fixture(scope="function")
def setup(request):
    """每个测试用例执行前的前置操作"""
    with allure.step(f"设置测试环境: {request.function.__name__}"):
        yield
        # 清理操作
```

### 8.2 pytest 钩子函数集成

```python
import allure

@pytest.fixture(autouse=True)
def attach_test_name(request):
    """自动记录测试用例名称"""
    allure.attach(request.node.name, "测试用例名称", allure.attachment_type.TEXT)
```

***

## 九、最佳实践

### 9.1 测试结构建议

```
testcases/
├── test_auth_login.py    # 登录相关测试
├── test_home_page.py     # 首页相关测试
└── conftest.py           # 共享配置
```

### 9.2 注解使用规范

1. **Feature**：按业务模块划分（如：登录模块、订单模块）
2. **Story**：按具体场景划分（如：成功登录、密码错误）
3. **Step**：每个关键操作都应封装为 step
4. **Severity**：根据业务重要性标注优先级

### 9.3 报告存储策略

```bash
# 按日期生成报告目录
allure generate allure-results -o reports/allure-report-$(date +%Y%m%d)
```

***

## 十、常见问题

### 10.1 报告生成失败

**问题**：`allure generate` 命令报错

**解决方案**：

```bash
# 检查 Java 版本（需要 Java 8+）
java -version

# 清理缓存后重新生成
rm -rf allure-results/*
pytest --alluredir=allure-results
```

### 10.2 中文乱码

**问题**：报告中中文显示为乱码

**解决方案**：

```python
# 在 conftest.py 中添加
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

### 10.3 附件无法显示

**问题**：添加的附件在报告中无法查看

**解决方案**：

```python
# 确保附件数据正确
allure.attach(
    data=content, 
    name="附件名称", 
    attachment_type=allure.attachment_type.TEXT  # 使用正确的类型
)
```

***

## 十一、附录

### 11.1 常用命令速查

| 命令                 | 说明         |
| ------------------ | ---------- |
| `allure serve`     | 启动预览服务     |
| `allure generate`  | 生成 HTML 报告 |
| `allure open`      | 打开已生成的报告   |
| `allure --version` | 查看版本       |

### 11.2 附件类型常量

| 类型     | 常量                            |
| ------ | ----------------------------- |
| 文本     | `allure.attachment_type.TEXT` |
| JSON   | `allure.attachment_type.JSON` |
| PNG 图片 | `allure.attachment_type.PNG`  |
| JPG 图片 | `allure.attachment_type.JPG`  |
| PDF 文件 | `allure.attachment_type.PDF`  |

### 11.3 严重级别说明

| 级别       | 说明 | 应用场景    |
| -------- | -- | ------- |
| CRITICAL | 严重 | 核心功能不可用 |
| HIGH     | 高  | 主要功能受影响 |
| MEDIUM   | 中  | 次要功能异常  |
| LOW      | 低  | 轻微问题    |
| MINOR    | 轻微 | 建议性改进   |

