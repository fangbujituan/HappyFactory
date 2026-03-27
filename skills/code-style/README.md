# 代码风格 Skill

## 目的

在自动编码过程中，确保 AI 生成的代码风格统一、可读性高、符合团队规范。覆盖命名、注释、类型注解、代码结构、格式化等方面。

## 使用方式

本 skill 作为 steering 规则自动生效，当 Kiro 生成或修改代码时会参考此风格规范。

## 核心规范

1. Python 命名：变量/函数 snake_case，类 PascalCase，常量 UPPER_SNAKE_CASE
2. 所有公共函数必须有 Google Style docstring 和类型注解
3. 注释解释 Why 不解释 What，禁止提交注释掉的代码
4. 单函数不超过 50 行，单文件不超过 400 行
5. 禁止空 except 块和裸 except

## 维护

编辑 `style-rules.yaml` 调整规则，修改 `level` 控制强制程度。
