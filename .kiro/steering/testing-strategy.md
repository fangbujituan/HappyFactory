---
inclusion: auto
---

# 测试规范约束规则

在编写测试代码、设计测试策略时，必须遵循以下规则：

## 规则数据源

参考 #[[file:skills/testing-strategy/testing-rules.yaml]] 中定义的测试规范。

## 核心规则（必须遵循）

1. 遵循测试金字塔原则：单元测试数量最多，集成测试适中，E2E 测试聚焦关键流程
2. 测试文件命名：test_<被测模块名>.py
3. 测试函数命名：test_<方法名>_<场景>（如 test_login_with_invalid_password）
4. 每个测试函数遵循 AAA 模式：Arrange（准备）→ Act（执行）→ Assert（验证）
5. 每个测试只测一个行为，测试之间必须独立，不依赖执行顺序
6. 测试数据与测试逻辑分离，数据放 tests/testdata/，使用 YAML 格式优先
7. 数据驱动测试使用 pytest.mark.parametrize 注入外部数据
8. 所有测试必须标记类型：@pytest.mark.api / @pytest.mark.ui / @pytest.mark.unit 等
9. 公共 fixture 放 conftest.py，模块专用 fixture 放 fixtures/ 目录
10. 测试数据中禁止使用真实个人信息

## Mock 策略

- 应该 mock：外部 HTTP API、第三方服务、系统时间、随机数、文件系统（单元测试中）
- 不应该 mock：自己写的 Service 类（集成测试中）、简单数据类、纯函数工具
- Mock 要验证交互参数，不只是替换返回值
- 优先使用 pytest-mock 的 mocker fixture

## 覆盖率要求

- 整体不低于 80%，核心 Service 层不低于 90%
- 不追求 100%，getter/setter 等简单方法不需要单独测试
- 关注有意义的覆盖率，不为凑数字写无效测试

## CI 中的测试

- PR 合并前必须通过 unit 和 api 测试
- 执行顺序：smoke → unit → api → integration → ui → security → perf
- 必须生成 JUnit XML 报告，推荐同时生成 HTML 报告
- 测试失败时自动收集上下文（API 请求响应、UI 截图、错误堆栈）

## 场景匹配

- 新增业务功能 → 必须同时编写单元测试，覆盖正常和异常场景
- 新增 API 接口 → 编写 API 测试，使用数据驱动覆盖多种输入
- 新增页面 → 编写 UI 测试覆盖关键交互流程
- 修复 Bug → 先写复现 Bug 的测试用例，再修复，确保测试从红变绿
