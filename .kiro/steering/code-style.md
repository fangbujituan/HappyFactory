---
inclusion: auto
---

# 代码风格约束规则

在生成或修改代码时，必须遵循以下风格规范：

## 规则数据源

参考 #[[file:skills/code-style/style-rules.yaml]] 中定义的风格规范。

## 命名规范（必须遵循）

### Python
- 变量、函数、方法、模块：snake_case
- 类：PascalCase
- 常量：UPPER_SNAKE_CASE
- 布尔变量推荐 is_/has_/can_ 前缀

### JavaScript / TypeScript
- 变量、函数：camelCase
- 类、接口、类型：PascalCase
- 常量：UPPER_SNAKE_CASE
- React 组件：PascalCase

### 通用
- 名称必须有意义，禁止无意义的单字母变量（循环索引除外）
- 函数名用动词开头
- 避免缩写，除非是广泛认知的（id、url、api、db、config 等）

## 文档与注释（必须遵循）

1. 所有公共函数、类、方法必须有 docstring，格式用 Google Style
2. 模块文件顶部推荐有模块级 docstring
3. 注释解释 Why 不解释 What
4. TODO 注释格式：`# TODO(author, YYYY-MM-DD): 描述`
5. 禁止注释掉的代码提交到仓库

## 类型注解（必须遵循）

- Python：所有公共函数必须有参数和返回值类型注解
- TypeScript：禁止使用 any 类型（特殊场景需注释说明）

## 代码结构（推荐遵循）

1. 单函数不超过 50 行，超过应拆分
2. 函数参数不超过 5 个，超过考虑封装
3. 避免超过 3 层嵌套，用 early return 减少嵌套
4. 单文件不超过 400 行
5. 导入顺序：标准库 → 第三方库 → 本地模块，各组之间空一行

## 错误处理风格（必须遵循）

1. 禁止空的 except/catch 块
2. 捕获具体异常类型，禁止裸 except
3. 异常信息必须包含上下文（如具体的 ID、参数值）
