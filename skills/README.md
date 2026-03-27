# AI 驱动开发：概念体系与应用指南

## 一、核心概念

### 1. Spec（规格化开发流程）

Spec 是一次具体开发任务的结构化流程，分三个阶段迭代推进：

| 阶段 | 产出文件 | 作用 |
|------|----------|------|
| 需求 | requirements.md | 结构化的用户故事和验收标准 |
| 设计 | design.md | 技术架构、组件接口、数据模型 |
| 任务 | tasks.md | 可执行的实施任务列表，逐个交付 |

每个阶段人都可以介入审查和调整，确保产出可控。

### 2. Skill（技能 / Steering 规则）

Skill 是预先定义的规则集，在所有对话中持续生效，约束 AI 的行为。

结构：
```
skills/<skill-name>/           # 数据和文档
.kiro/steering/<skill-name>.md # 入口文件（inclusion: auto）
```

Steering 文件通过 `#[[file:...]]` 引用 skill 目录下的数据文件，Kiro 启动时自动加载。

### 3. Ontology（本体）

本体是对某个领域的概念、关系和规则的结构化描述。在 AI 开发场景下分为三层：

- **业务本体**：项目做什么，有哪些领域概念和流程
- **技术本体**：用什么技术，遵循什么架构原则
- **工程本体**：怎么写代码，怎么测试，怎么协作

Skill 是本体的载体，每写一条 steering 规则，就是在构建你的本体。

### 4. Agent Factory（Agent 工厂）

Agent Factory 是根据任务需求，从本体（skill 库）中自动组装专用 Agent 的机制。

核心闭环：
```
需求 → spec 执行 → 产出代码 → 发现规则缺失 → 补充 skill → 本体进化 → 下次更精准
```

---

## 二、本体分层与应用建议

### 业务本体

定义项目的领域知识，让 AI 理解你的业务语境。

**建议沉淀的内容：**

- 领域术语表：核心业务概念的定义和关系（如 spec 中的术语表）
- 业务流程：关键流程的步骤描述（如用户注册流程、订单生命周期）
- 数据模型：核心实体及其字段、关系（如 User、Order、Product 的 ER 关系）
- 业务规则：领域约束（如"订单金额不能为负"、"用户名唯一"）
- API 契约：接口规范文档（OpenAPI spec、GraphQL schema）

**Skill 示例：**
```
skills/domain-model/
├── entities.yaml          # 核心实体定义
├── business-rules.yaml    # 业务规则清单
├── glossary.yaml          # 术语表
└── README.md
```

**Steering 规则示例：**
```markdown
- 生成代码时，实体命名必须与 entities.yaml 中的定义一致
- 新增 API 接口时，必须遵循 OpenAPI spec 中的命名和响应格式规范
- 涉及金额计算时，必须使用 Decimal 类型，禁止使用浮点数
```

---

### 技术本体

定义技术选型和架构决策，避免 AI 引入不合适的技术。

**建议沉淀的内容：**

- 框架选型清单：按语言和场景分类，标注 preferred / accepted / excluded（你已有的 tech-stack-guide）
- 架构模式偏好：你倾向的分层方式、设计模式
- 依赖管理规则：版本约束、许可证白名单
- 性能约束：响应时间要求、并发量预期
- 安全基线：认证方案、加密要求、敏感数据处理

**Skill 示例：**
```
skills/tech-stack-guide/        # 已有：框架选型
skills/architecture/
├── patterns.yaml               # 偏好的设计模式
├── layering-rules.yaml         # 分层架构规则
└── README.md
```

**Steering 规则示例：**
```markdown
- 后端项目必须采用分层架构：Controller → Service → Repository
- 禁止在 Controller 层直接操作数据库
- 所有外部服务调用必须通过独立的 Client 类封装
- 配置信息必须通过环境变量或配置文件注入，禁止硬编码
- 数据库访问必须使用 ORM，禁止裸 SQL（安全审计场景除外）
```

---

### 工程本体

定义"怎么写代码"，统一团队的工程实践。

**建议沉淀的内容：**

#### 代码风格
- 命名规范：变量、函数、类、文件的命名规则
- 目录结构偏好：项目骨架模板
- 注释风格：何时写注释、注释格式、docstring 规范
- 导入顺序：标准库 → 第三方 → 本地模块
- 代码长度约束：单函数最大行数、单文件最大行数

#### 测试规范
- 测试覆盖率要求：最低覆盖率阈值
- 测试命名规则：test_<功能>_<场景>_<预期结果>
- 测试分层：单元测试 / 集成测试 / E2E 测试的边界
- Mock 策略：什么该 mock，什么不该 mock
- 测试数据管理：fixture 和 testdata 的组织方式

#### Git 与协作
- 分支策略：Git Flow / Trunk Based
- Commit 规范：Conventional Commits 格式
- PR 规范：描述模板、Review 检查项
- 版本号规则：SemVer 策略

#### CI/CD
- 流水线阶段：lint → test → build → deploy
- 质量门禁：哪些检查必须通过才能合并
- 部署策略：蓝绿 / 滚动 / 金丝雀

**Skill 示例：**
```
skills/code-style/
├── naming.yaml                 # 命名规范
├── structure-template.yaml     # 目录结构模板
├── comment-rules.yaml          # 注释规范
└── README.md

skills/testing-strategy/
├── coverage-rules.yaml         # 覆盖率要求
├── naming-convention.yaml      # 测试命名规则
├── mock-policy.yaml            # Mock 策略
└── README.md

skills/git-workflow/
├── branch-strategy.yaml        # 分支策略
├── commit-convention.yaml      # Commit 规范
└── README.md
```

**Steering 规则示例：**
```markdown
## 代码风格
- Python 项目：变量和函数用 snake_case，类用 PascalCase
- 所有公共函数必须有 docstring，格式用 Google Style
- 单个函数不超过 50 行，超过必须拆分
- 文件顶部必须有模块级 docstring 说明文件用途

## 测试
- 每个新功能必须附带单元测试，覆盖率不低于 80%
- 测试文件命名：test_<被测模块名>.py
- 测试函数命名：test_<方法名>_<场景>（如 test_login_with_invalid_password）
- 外部服务调用必须 mock，数据库操作使用测试专用 fixture

## Git
- Commit 格式：<type>(<scope>): <description>
- type 取值：feat / fix / refactor / test / docs / chore
- 每个 PR 必须关联 Issue，描述中包含改动原因和影响范围
```

---

## 三、Spec + Skill 协作模型

```
┌─────────────────────────────────────────────────┐
│                  你的本体（Ontology）              │
│                                                   │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐          │
│  │ 业务本体 │  │ 技术本体 │  │ 工程本体 │          │
│  │ 领域模型 │  │ 框架选型 │  │ 代码风格 │          │
│  │ 业务规则 │  │ 架构模式 │  │ 测试规范 │          │
│  │ API 契约 │  │ 安全基线 │  │ Git 规范 │          │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
│       └──────────────┼──────────────┘              │
│                      ↓                             │
│            .kiro/steering/*.md                     │
│          （inclusion: auto 自动加载）               │
└──────────────────────┬──────────────────────────────┘
                       ↓
              ┌────────────────┐
              │   Spec 开发流程  │
              │                │
              │  需求 → 设计 → 任务 → 代码
              │    ↑              │
              │    │   本体约束    │
              │    │   全程生效    │
              └────────────────┘
                       ↓
              发现新的规则缺失？
                       ↓
              补充到 skill → 本体进化
```

---

## 四、落地建议

### 从小处开始
不要试图一次建完所有本体。从你最常纠正 AI 的地方开始：
1. 如果你总是改 AI 的技术选型 → 先建技术本体（你已经做了）
2. 如果你总是改 AI 的代码风格 → 建工程本体中的代码风格 skill
3. 如果你总是改 AI 的架构设计 → 建技术本体中的架构 skill

### 迭代优化
每次 spec 执行后回顾：
- AI 哪里做得不对？→ 补充规则
- AI 哪里做得好？→ 确认规则有效
- 有没有新的模式可以提炼？→ 新增 skill

### 保持简洁
- 每个 skill 聚焦一个领域，不要做大而全的万能 skill
- 规则用自然语言写，不需要复杂的格式
- YAML 数据文件用于结构化的清单（如框架列表），steering 规则用于描述行为约束
