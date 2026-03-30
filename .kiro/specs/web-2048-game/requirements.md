# 需求文档

## 简介

本文档定义了网页版2048滑动拼图游戏的功能需求。2048是一款经典的单人益智游戏，玩家在4x4的网格上通过滑动操作合并相同数字的方块，目标是创建一个值为2048的方块。游戏需要在现代浏览器中运行，支持键盘和触屏操作，并具备响应式设计以适配不同设备。

## 术语表

- **Game_Grid（游戏网格）**: 4x4的二维网格，用于放置和移动数字方块
- **Tile（方块）**: 网格中带有数字值的单元，数值为2的幂次方（2, 4, 8, 16, ... 2048）
- **Move（移动操作）**: 玩家通过键盘方向键或触屏滑动触发的方块整体移动，方向为上、下、左、右之一
- **Merge（合并）**: 两个相同数值的方块在移动方向上相遇时合并为一个方块，新方块数值为原数值的两倍
- **Score（分数）**: 玩家的累计得分，每次合并时增加合并后方块的数值
- **Best_Score（最高分）**: 玩家历史最高分数，持久化存储在浏览器本地
- **Game_Over（游戏结束）**: 网格已满且无法进行任何合并操作的状态
- **Game_Engine（游戏引擎）**: 负责处理游戏核心逻辑的模块，包括移动、合并、生成方块和状态判断
- **UI_Renderer（界面渲染器）**: 负责将游戏状态渲染到网页上的模块

## 需求

### 需求 1：游戏网格初始化

**用户故事：** 作为玩家，我希望游戏启动时显示一个4x4的网格并随机放置初始方块，以便我可以开始游戏。

#### 验收标准

1. WHEN 游戏启动时, THE Game_Engine SHALL 创建一个4x4的空网格
2. WHEN 游戏网格创建完成后, THE Game_Engine SHALL 在随机空位置生成2个初始方块
3. WHEN 生成初始方块时, THE Game_Engine SHALL 以90%的概率生成数值为2的方块，以10%的概率生成数值为4的方块
4. THE UI_Renderer SHALL 将Game_Grid以居中对齐的方式渲染到页面上

### 需求 2：方块移动

**用户故事：** 作为玩家，我希望通过键盘方向键或触屏滑动来移动方块，以便我可以控制游戏进程。

#### 验收标准

1. WHEN 玩家按下上、下、左、右方向键时, THE Game_Engine SHALL 将所有方块沿对应方向移动到最远的空位置
2. WHEN 玩家在触屏设备上滑动时, THE Game_Engine SHALL 识别滑动方向并将所有方块沿该方向移动
3. WHEN 一次移动操作导致至少一个方块位置发生变化时, THE Game_Engine SHALL 在一个随机空位置生成一个新方块
4. WHEN 一次移动操作未导致任何方块位置变化时, THE Game_Engine SHALL 忽略该操作且不生成新方块
5. WHILE 游戏处于Game_Over状态时, THE Game_Engine SHALL 忽略所有移动操作输入

### 需求 3：方块合并

**用户故事：** 作为玩家，我希望相同数值的方块在移动时能够合并，以便我可以创建更大数值的方块。

#### 验收标准

1. WHEN 两个相同数值的方块在移动方向上相邻时, THE Game_Engine SHALL 将两个方块合并为一个方块，新方块数值为原数值的两倍
2. WHEN 一次移动中同一行或列有多对可合并的方块时, THE Game_Engine SHALL 仅合并移动方向上最先相遇的一对方块
3. WHEN 一次移动中一个方块已参与合并时, THE Game_Engine SHALL 阻止该方块在同一次移动中再次合并
4. WHEN 合并产生数值为2048的方块时, THE Game_Engine SHALL 触发胜利提示，同时允许玩家继续游戏

### 需求 4：分数系统

**用户故事：** 作为玩家，我希望看到当前分数和历史最高分，以便我可以追踪自己的游戏表现。

#### 验收标准

1. WHEN 游戏启动时, THE Game_Engine SHALL 将当前分数初始化为0
2. WHEN 方块合并发生时, THE Game_Engine SHALL 将合并后方块的数值累加到当前分数
3. THE UI_Renderer SHALL 在游戏网格上方实时显示当前分数
4. WHEN 当前分数超过Best_Score时, THE Game_Engine SHALL 更新Best_Score的值
5. THE Game_Engine SHALL 将Best_Score存储到浏览器localStorage中，确保页面刷新后数据不丢失
6. THE UI_Renderer SHALL 在当前分数旁边显示Best_Score

### 需求 5：游戏结束检测

**用户故事：** 作为玩家，我希望游戏能在无法继续操作时提示我游戏结束，以便我知道本局游戏已结束。

#### 验收标准

1. WHEN 每次移动操作完成后, THE Game_Engine SHALL 检查游戏是否结束
2. WHEN Game_Grid中没有空位置且没有任何相邻方块数值相同时, THE Game_Engine SHALL 将游戏状态设置为Game_Over
3. WHEN 游戏状态变为Game_Over时, THE UI_Renderer SHALL 在Game_Grid上方显示"游戏结束"的提示信息
4. WHEN 游戏状态变为Game_Over时, THE UI_Renderer SHALL 显示一个"重新开始"按钮

### 需求 6：游戏重启

**用户故事：** 作为玩家，我希望可以随时重新开始游戏，以便我可以重新挑战。

#### 验收标准

1. THE UI_Renderer SHALL 在页面上始终显示一个"新游戏"按钮
2. WHEN 玩家点击"新游戏"按钮时, THE Game_Engine SHALL 清空Game_Grid中所有方块并将当前分数重置为0
3. WHEN Game_Grid清空后, THE Game_Engine SHALL 按照需求1的规则重新生成初始方块

### 需求 7：动画效果

**用户故事：** 作为玩家，我希望方块移动和合并时有流畅的动画效果，以便获得良好的视觉体验。

#### 验收标准

1. WHEN 方块移动时, THE UI_Renderer SHALL 以平滑过渡动画展示方块从原位置到目标位置的移动过程
2. WHEN 方块合并时, THE UI_Renderer SHALL 以缩放弹跳动画展示合并效果
3. WHEN 新方块生成时, THE UI_Renderer SHALL 以淡入缩放动画展示新方块的出现
4. THE UI_Renderer SHALL 确保所有动画在150毫秒内完成，避免影响玩家操作节奏

### 需求 8：响应式设计

**用户故事：** 作为玩家，我希望游戏在不同设备和屏幕尺寸上都能正常显示和操作，以便我可以在手机、平板或电脑上游玩。

#### 验收标准

1. THE UI_Renderer SHALL 使Game_Grid在320px至1920px的屏幕宽度范围内自适应缩放
2. WHILE 屏幕宽度小于600px时, THE UI_Renderer SHALL 将Game_Grid宽度设置为屏幕宽度的90%
3. WHILE 屏幕宽度大于等于600px时, THE UI_Renderer SHALL 将Game_Grid宽度固定为500px
4. THE UI_Renderer SHALL 根据方块数值大小动态调整方块内文字的字号，确保数字完整显示
5. THE UI_Renderer SHALL 为不同数值的方块分配不同的背景颜色，以便玩家快速区分

### 需求 9：键盘与触屏输入处理

**用户故事：** 作为玩家，我希望游戏能准确识别我的操作输入，以便游戏响应符合我的预期。

#### 验收标准

1. WHEN 玩家按下方向键（上、下、左、右）时, THE Game_Engine SHALL 在当前动画完成后执行对应方向的移动操作
2. WHEN 玩家在触屏上滑动距离超过30px时, THE Game_Engine SHALL 根据滑动的主方向（水平或垂直中位移较大的方向）执行移动操作
3. WHEN 玩家在触屏上滑动距离不超过30px时, THE Game_Engine SHALL 忽略该触屏事件
4. WHILE 游戏正在处理一次移动操作时, THE Game_Engine SHALL 将后续输入加入队列，待当前操作完成后依次处理
5. THE Game_Engine SHALL 阻止方向键的默认页面滚动行为

### 需求 10：游戏状态序列化

**用户故事：** 作为玩家，我希望刷新页面后游戏进度不会丢失，以便我可以随时继续之前的游戏。

#### 验收标准

1. WHEN 游戏状态发生变化时, THE Game_Engine SHALL 将当前Game_Grid状态和分数序列化为JSON格式并存储到浏览器localStorage中
2. WHEN 页面加载时且localStorage中存在有效的游戏存档时, THE Game_Engine SHALL 从存档中反序列化恢复Game_Grid状态和分数
3. WHEN 页面加载时且localStorage中不存在有效存档时, THE Game_Engine SHALL 按照需求1的规则初始化新游戏
4. FOR ALL 有效的游戏状态对象, 序列化后再反序列化 SHALL 产生与原始状态等价的游戏状态（往返一致性）
