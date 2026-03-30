# 实现计划：网页版2048游戏

## 概述

基于纯HTML/CSS/JavaScript实现2048滑动拼图游戏，采用关注点分离架构：Game Engine负责纯逻辑，UI Renderer负责DOM渲染和动画。实现顺序为：项目结构 → 数据模型 → 核心算法 → 游戏管理 → UI渲染 → 输入处理 → 持久化 → 动画 → 响应式 → 测试。

## Tasks

- [x] 1. 搭建项目基础结构
  - [x] 1.1 创建项目目录结构和HTML入口文件
    - 创建 `index.html`，包含游戏容器、分数面板、新游戏按钮、消息覆盖层的DOM结构
    - 创建 `css/style.css` 基础样式文件（网格背景、布局框架）
    - 创建 `js/` 目录，包含各模块的空JS文件：`tile.js`、`grid.js`、`game-manager.js`、`ui-renderer.js`、`input-handler.js`、`storage-manager.js`、`app.js`
    - 在 `index.html` 中按依赖顺序引入所有JS文件
    - _Requirements: 1.4, 8.1_

- [x] 2. 实现数据模型层（Tile 和 Grid）
  - [x] 2.1 实现 Tile 类
    - 在 `js/tile.js` 中实现 Tile 类，包含 `position`、`value`、`previousPosition`、`mergedFrom` 属性
    - 实现 `savePosition()`、`updatePosition(pos)`、`serialize()` 方法
    - _Requirements: 1.3_

  - [x] 2.2 实现 Grid 类
    - 在 `js/grid.js` 中实现 Grid 类，构造函数接受 `size` 和可选的 `previousState`
    - 实现 `emptyCells()`、`randomAvailableCell()`、`cellAvailable(pos)`、`cellContent(pos)` 方法
    - 实现 `insertTile(tile)`、`removeTile(tile)`、`eachCell(callback)`、`serialize()` 方法
    - `cells` 使用 `cells[x][y]` 坐标系（第x列第y行）
    - _Requirements: 1.1, 1.2_

  - [ ]* 2.3 编写 Grid 和 Tile 的单元测试
    - 测试 Grid 创建4x4空网格、`emptyCells` 返回16个空位
    - 测试 `insertTile`/`removeTile` 正确操作、`cellContent` 返回正确内容
    - 测试 Tile 的 `savePosition`、`updatePosition`、`serialize`
    - _Requirements: 1.1, 1.2_

- [x] 3. 实现移动与合并核心算法
  - [x] 3.1 实现单行向左移动合并函数
    - 在 `js/game-manager.js` 中实现 `moveLine(line)` 纯函数，输入为一行方块值数组，返回合并后的数组和本次合并得分
    - 算法：过滤空位 → 从左到右扫描相邻相同值合并 → 已合并方块不再参与后续合并 → 填充0至原长度
    - 示例：`[2,2,2,0]` → `[4,2,0,0]`，得分4；`[2,2,4,4]` → `[4,8,0,0]`，得分12
    - _Requirements: 3.1, 3.2, 3.3_

  - [x] 3.2 实现四方向移动的坐标变换
    - 实现 `buildTraversals(direction, size)` 函数，返回各方向的遍历顺序
    - 在 GameManager 中实现 `move(direction)` 方法，通过坐标变换将四个方向统一处理
    - 方向映射：0=上, 1=右, 2=下, 3=左
    - 移动后检测是否有变化，有变化则调用 `addRandomTile()` 生成新方块
    - _Requirements: 2.1, 2.3, 2.4_

  - [x] 3.3 实现新方块生成逻辑
    - 实现 `addRandomTile()` 方法，在随机空位生成新方块
    - 生成概率：90%为2，10%为4
    - _Requirements: 1.3, 2.3_

  - [ ]* 3.4 编写移动合并算法的属性测试
    - **Property 2: 移动压缩性** — 移动后方块紧贴移动方向边界，无中间空隙
    - **Validates: Requirements 2.1**

  - [ ]* 3.5 编写合并正确性的属性测试
    - **Property 6: 合并正确性** — (a) 合并后数值为原数值两倍；(b) 同一次移动中方块最多参与一次合并
    - **Validates: Requirements 3.1, 3.3**

  - [ ]* 3.6 编写移动合并的单元测试
    - 测试 `[2,2,2,0]` 向左合并为 `[4,2,0,0]`（方向优先合并）
    - 测试 `[2,2,4,4]` 向左合并为 `[4,8,0,0]`
    - 测试空行移动不变、单元素行移动到边界
    - _Requirements: 3.1, 3.2, 3.3_

- [x] 4. 实现 GameManager 游戏管理器
  - [x] 4.1 实现 GameManager 核心逻辑
    - 在 `js/game-manager.js` 中实现 GameManager 类，构造函数接受 `size`、`renderer`、`storageManager`
    - 实现 `setup()` 方法：清空网格、重置分数、生成2个初始方块、通知渲染器
    - 实现 `getState()` 返回当前游戏状态快照
    - 管理 `score`、`bestScore`、`over`、`won`、`keepPlaying` 状态
    - _Requirements: 1.1, 1.2, 4.1, 6.2, 6.3_

  - [x] 4.2 实现分数计算和最高分更新
    - 在 `move()` 方法中累加合并得分到 `score`
    - 当 `score > bestScore` 时更新 `bestScore`
    - 通过回调通知渲染器更新分数显示
    - _Requirements: 4.2, 4.3, 4.4_

  - [x] 4.3 实现游戏结束和胜利检测
    - 实现 `isGameOver()` 方法：网格无空位且无相邻相同方块时返回true
    - 实现胜利检测：合并产生2048时设置 `won = true`
    - 游戏结束时设置 `over = true`，阻止后续移动
    - 支持 `keepPlaying` 模式：达到2048后可继续游戏
    - _Requirements: 5.1, 5.2, 3.4, 2.5_

  - [ ]* 4.4 编写游戏状态相关的属性测试
    - **Property 1: 方块值约束** — 新生成方块数值只能是2或4
    - **Validates: Requirements 1.3**

  - [ ]* 4.5 编写有效/无效移动的属性测试
    - **Property 3: 有效移动生成新方块** — 有效移动后方块总数恰好多1
    - **Validates: Requirements 2.3**
    - **Property 4: 无效移动为空操作** — 无效移动后网格状态不变，不生成新方块
    - **Validates: Requirements 2.4**

  - [ ]* 4.6 编写游戏结束和分数的属性测试
    - **Property 5: 游戏结束状态阻止移动** — Game_Over状态下移动不改变状态
    - **Validates: Requirements 2.5**
    - **Property 7: 分数与合并一致性** — 分数增量等于所有合并新方块数值之和
    - **Validates: Requirements 4.2**
    - **Property 8: 最高分单调性** — bestScore >= score 且只增不减
    - **Validates: Requirements 4.4**
    - **Property 9: 游戏结束检测正确性** — 当且仅当无空位且无相邻相同方块时返回true
    - **Validates: Requirements 5.2**

  - [ ]* 4.7 编写 GameManager 单元测试
    - 测试新游戏初始化：4x4网格、2个初始方块、分数为0
    - 测试合并产生2048时触发胜利
    - 测试游戏重启后网格清空、分数归零
    - _Requirements: 1.1, 1.2, 4.1, 3.4, 6.2, 6.3_

- [x] 5. Checkpoint - 确保核心逻辑正确
  - 确保所有测试通过，如有问题请向用户确认。

- [x] 6. 实现 StorageManager 存储管理器
  - [x] 6.1 实现 StorageManager 类
    - 在 `js/storage-manager.js` 中实现 localStorage 封装
    - 实现 `getGameState()`、`setGameState(state)`、`clearGameState()` 方法
    - 实现 `getBestScore()`、`setBestScore(score)` 方法
    - 处理 localStorage 不可用（隐私模式）：捕获异常，游戏正常运行但不持久化
    - 处理存档数据损坏：JSON.parse 失败时清除存档
    - _Requirements: 10.1, 10.2, 10.3, 4.5_

  - [x] 6.2 在 GameManager 中集成 StorageManager
    - 构造函数中尝试从 localStorage 恢复游戏状态
    - 每次移动后自动保存游戏状态
    - 新游戏时清除旧存档
    - _Requirements: 10.1, 10.2, 10.3_

  - [ ]* 6.3 编写序列化往返一致性属性测试
    - **Property 11: 游戏状态序列化往返一致性** — 序列化后再反序列化产生等价状态
    - **Validates: Requirements 10.4**

  - [ ]* 6.4 编写 StorageManager 单元测试
    - 测试存档保存和恢复正确性
    - 测试无存档时返回null
    - 测试损坏数据处理
    - _Requirements: 10.2, 10.3_

- [x] 7. 实现 UIRenderer 界面渲染器
  - [x] 7.1 实现 UIRenderer 类
    - 在 `js/ui-renderer.js` 中实现 UIRenderer 类
    - 实现 `render(state)` 方法：清除旧方块DOM，根据状态创建新方块DOM元素
    - 每个方块DOM元素设置对应的位置class（`tile-position-x-y`）和数值class（`tile-value`）
    - 实现 `updateScore(score)` 和 `updateBestScore(best)` 更新分数显示
    - 实现 `showMessage(won)` 显示游戏结束/胜利消息覆盖层
    - 实现 `clearMessage()` 清除消息
    - _Requirements: 1.4, 4.3, 4.6, 5.3, 5.4, 6.1_

  - [x] 7.2 实现方块颜色和样式系统
    - 在 `css/style.css` 中为每个方块数值（2~2048）定义背景色和文字色
    - 根据数值动态调整文字字号（≥1000时缩小字号）
    - 实现网格背景（圆角方格底色）
    - _Requirements: 8.4, 8.5_

- [x] 8. 实现 InputHandler 输入处理器
  - [x] 8.1 实现键盘输入处理
    - 在 `js/input-handler.js` 中实现 InputHandler 类
    - 监听 `keydown` 事件，映射方向键（ArrowUp/Down/Left/Right）到方向值（0/1/2/3）
    - 调用 `event.preventDefault()` 阻止方向键的默认页面滚动
    - 绑定"新游戏"和"继续游戏"按钮的点击事件
    - _Requirements: 9.1, 9.5_

  - [x] 8.2 实现触屏滑动输入处理
    - 监听 `touchstart` 和 `touchend` 事件
    - 记录触摸起点坐标，计算滑动距离和方向
    - 滑动距离 > 30px 时触发移动，比较水平/垂直位移绝对值取主方向
    - 滑动距离 ≤ 30px 时忽略
    - _Requirements: 9.2, 9.3_

  - [ ]* 8.3 编写触屏方向识别属性测试
    - **Property 10: 触屏方向识别** — 距离>30px时识别位移较大轴方向，距离≤30px时不触发
    - **Validates: Requirements 2.2, 9.2, 9.3**

  - [ ]* 8.4 编写输入处理单元测试
    - 测试方向键正确映射到移动方向
    - 测试非方向键被忽略
    - _Requirements: 9.1_

- [x] 9. 实现动画效果
  - [x] 9.1 实现CSS过渡动画
    - 在 `css/style.css` 中为方块位置变化添加 CSS transition（150ms）
    - 实现方块合并时的缩放弹跳动画（CSS @keyframes）
    - 实现新方块出现时的淡入缩放动画（CSS @keyframes）
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

  - [x] 9.2 在 UIRenderer 中集成动画
    - 渲染时为移动方块设置 `previousPosition` 对应的初始位置class，触发CSS过渡
    - 为合并方块添加 `tile-merged` class 触发弹跳动画
    - 为新生成方块添加 `tile-new` class 触发淡入动画
    - _Requirements: 7.1, 7.2, 7.3_

- [x] 10. 实现响应式设计
  - [x] 10.1 实现响应式CSS布局
    - 使用CSS媒体查询：屏幕宽度 < 600px 时网格宽度为90vw，≥ 600px 时固定500px
    - 方块尺寸和间距随网格尺寸等比缩放
    - 分数面板和按钮在小屏幕上自适应排列
    - 设置 viewport meta 标签确保移动端正确缩放
    - _Requirements: 8.1, 8.2, 8.3_

- [x] 11. 应用入口和模块集成
  - [x] 11.1 实现 app.js 入口文件
    - 在 `js/app.js` 中实例化 StorageManager、UIRenderer、InputHandler、GameManager
    - 连接各模块：InputHandler 的回调调用 GameManager 的方法
    - GameManager 状态变更时调用 UIRenderer 渲染
    - 页面加载时自动初始化游戏（从存档恢复或新游戏）
    - _Requirements: 10.2, 10.3, 1.1, 1.2_

  - [x] 11.2 实现输入队列机制
    - 在动画进行中将输入加入队列
    - 动画完成后依次处理队列中的输入
    - _Requirements: 9.4_

- [x] 12. Checkpoint - 确保完整功能可用
  - 确保所有测试通过，如有问题请向用户确认。

- [x] 13. 测试框架搭建和剩余测试补充
  - [x] 13.1 搭建测试环境
    - 安装 fast-check 和测试运行器（如 vitest 或 jest）
    - 创建 `tests/game/` 目录结构
    - 配置测试脚本，确保可通过命令行运行所有测试
    - 创建共用的 fast-check 生成器（`tileValueArb`、`gridArb`、`directionArb`、`gameStateArb`）

  - [ ]* 13.2 补充集成测试
    - 测试完整游戏流程：初始化 → 移动 → 合并 → 分数更新 → 存档 → 恢复
    - 测试游戏结束流程：填满网格 → 检测Game_Over → 显示消息 → 重新开始
    - _Requirements: 1.1, 1.2, 2.1, 3.1, 4.2, 5.2, 6.2, 10.2_

- [x] 14. 最终检查点 - 确保所有测试通过
  - 确保所有测试通过，如有问题请向用户确认。

## Notes

- 标记 `*` 的任务为可选任务，可跳过以加速MVP开发
- 每个任务引用了对应的需求编号，确保可追溯性
- 检查点任务用于阶段性验证，确保增量开发的正确性
- 属性测试验证通用正确性属性，单元测试验证具体示例和边界情况
- 所有11个正确性属性均已分配到对应的属性测试任务中
