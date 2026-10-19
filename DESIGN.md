# Midnight Pages Studio — 主页重设计规格 v2

目标：像纸品品牌的编辑式网页（Rifle Paper Co. / Papier / Minted）+ Apple 产品页的滚动叙事。不是卡片网格。
文案、产品、价格、Gumroad 链接全部沿用 v1（备份：git tag `backup-v1-cards`，目录 `/workspace/midnight-pages-site.backup-20261019`）。不新增任何评价、销量、客户数。

## 1. 禁止清单
网格卡片堆砌；圆角+阴影卡片；紫蓝渐变；emoji 图标；居中大标题+三个特性块；border-radius 一律 0（纸张允许 1px 圆角模拟裁切）。

## 2. 配色
| token | 值 | 用途 |
|---|---|---|
| --midnight | #111c33 | 深海军蓝：Prompt 段底色、正文墨色 |
| --midnight-2 | #1b2a4a | 深色段内层次 |
| --paper | #f2ece0 | 米白纸色：主背景 |
| --paper-2 | #e8dfcd | 纸色次级（Sets 段底） |
| --ink-soft | #4a5266 | 次要文字 |
| --gold | #b8914a | 细线、编号、深底上的强调 |
| --brick | #a4472b | 主要强调色：价格、眉题、购买按钮悬停 |
比例：纸色 70% / 海军蓝 25% / 金+砖红 ≤5%。

## 3. 字体
- 衬线：Instrument Serif（站内已有 woff，常规+斜体）——大标题、价格、斜体点题词。
- 无衬线：Inter 400/500（站内已有）——正文、导航、按钮、小号全大写眉题（字距 .22em）。
- 字号：Display clamp(3.4rem, 9vw, 8.5rem)/0.92；H2 clamp(2.6rem,6vw,5.2rem)/0.98；正文 1.0625rem/1.65；最大行宽 34rem。

## 4. 纸张与样机
- 纸张纹理：内联 SVG `feTurbulence`（baseFrequency .9, numOctaves 2）做噪点，作为 body 与纸张样机的 `::after` 背景，opacity .06–.09，mix-blend multiply。
- 样机：产品图放进 `.sheet`（米白边框 padding 4–6% 模拟印刷留白），轻微倾斜 −3°~+4°，双层真实阴影：
  `0 1px 1px rgba(17,28,51,.12), 0 18px 30px -12px rgba(17,28,51,.28), 0 50px 80px -30px rgba(17,28,51,.25)`。
- 礼卡叠：每张卡模拟吊牌——顶部打孔圆点 + CSS 绳子线（1px 金色）。
- Prompt Pack：封面图做成平放的装订册（左侧书脊阴影渐变 + 后方一张错位纸页）。

## 5. 版式与叙事（自上而下）
1. **刊头**：左 wordmark，右导航 + 常驻小号「Buy the Library $39」按钮（滚过首屏后出现底色），手机端只留 wordmark + 购买按钮。
2. **Hero（不对称 7/5）**：左侧超大衬线标题「The Pop-By / *Tag Library*」压在网格线上，lede + 购买按钮；右侧 library 大图做成倾斜纸张样机，后面叠一张错位纸页，压出页面右边界（出血）。图注斜体衬线。底部一条细金线 + 收录的八个系列名做成横向刊物目录行。
3. **How agents use them（编辑式，不是三个块）**：左侧固定小标题（sticky），右侧三段以罗马数字 I/II/III 为悬挂编号的长文段落，错落缩进，段间细线。
4. **Gift tag sets（核心）**：
   - 桌面：两栏。左栏 sticky：大标题「Eight sets, *$7 each*」+ 说明 + **礼卡叠**（可拖动翻看）。右栏：八个系列的编号目录（01–08），每行 = 编号、名称（衬线大字）、描述、张数、价格、「Buy X →」。目录行与卡叠双向同步：滚动/悬停/点击某行 → 卡叠切到该系列；翻卡叠 → 高亮对应行。
   - 手机：标题 → 卡叠（全宽，左右滑）→ 当前卡下方显示该系列名称/描述/购买链接 → 下面紧凑目录。
5. **Prompt Pack（深海军蓝段）**：左侧装订册样机（轻微 3D 倾斜，见手势 B），右侧文案 + 浅色按钮 $24。大号斜体「93」作为装饰性排版数字（是真实数据，来自现有文案）。
6. **Free sample**：不居中——左对齐窄栏，右侧一张撕边便签样式的纸片（CSS 做），按钮。
7. **页脚**：海军蓝细带，wordmark 大号衬线 + 链接一行。

## 6. 动效（每一处都有理由）
全局：缓动 `--ease: cubic-bezier(0.22,1,0.36,1)`；时长 400–900ms；只动 transform / opacity。

| # | 位置 | 效果 | 参数 | 为什么存在 |
|---|---|---|---|---|
| M1 | 段落与图片 | 进入视口渐显 + 上移 24px | IntersectionObserver threshold .15，700ms，同组错开 80ms | 引导阅读节奏，告诉用户「往下还有」，克制不抢戏 |
| M2 | Hero 纸张 | 首次加载落下：translateY(30px) rotate(-6°)→最终倾斜，900ms | 仅一次 | 第一眼建立「这是实物纸品」的印象 |
| M3 | 刊头购买按钮 | 滚过 Hero 后背景由透明变实色（opacity 层） | 400ms | 让购买入口始终显眼，帮助成交 |
| G1 | 礼卡叠 | 手势翻看（见 §7） | — | 八个系列是主要货品，翻看比网格更像在店里拿起吊牌，并把注意力集中在单个系列+其购买链接上 |
| G2 | Prompt 装订册 / Hero 主图 | 指针 3D 轻微倾斜 + 光泽 | 最大 6° | 只给主推产品，强化实物感；幅度小，不干扰点击 |
不做：视差满屏、鼠标跟随光标、文字逐字动画、滚动劫持。

## 7. 手势规格
统一 Pointer Events（pointerdown/move/up/cancel + setPointerCapture），鼠标和触摸同一套代码。
### G1 礼卡叠
- 结构：`.deck` 内 8 张 `.tag`，绝对定位叠放；当前卡在顶，其后 2 张露出（偏移 translate(8px·i, 6px·i) rotate(±2°·i)，scale 1−.04i），其余 opacity 0。
- `touch-action: pan-y`：只接管横向拖动，页面上下滚动不受影响；判定方向阈值 8px，若纵向位移先超过则放弃拖动。
- 拖动：卡片 translateX = dx，rotate = dx·0.05deg，rAF 中写入 transform。
- 松手：用最近 100ms 指针速度 v（px/ms）。若 |dx|>30% 卡宽 或 |v|>0.5 → 飞出到 ±1.4 卡宽（惯性：初速 v，摩擦 0.95/帧），换到下一/上一张，旧顶卡回到底部；否则弹簧回弹到 0（stiffness 0.12，damping 0.78，rAF 积分，|x|<0.5 且速度<0.05 停止）。
- 循环翻看（第 8 张后回到第 1 张）。另有「‹ ›」文字按钮 + 键盘 ←/→ + 计数「03 / 08」，保证无手势也能用。
- 点击（位移<6px）不触发拖动，卡上的 Buy 链接可正常点。
- 同步：切换时更新目录高亮与手机端信息栏（aria-live=polite）。
### G2 样机倾斜 + 光泽
- 仅 `@media (hover:hover) and (pointer:fine)` 启用；触屏设备不绑定（不出现悬停效果）。
- pointermove 记录相对坐标 (px,py)∈[−.5,.5]；rAF 中插值（lerp .12）写 `transform: perspective(1000px) rotateX(−py·6deg) rotateY(px·6deg)`，光泽层 `.gloss`（白色径向渐变，opacity 0→.35）用 translate 跟随，不改 background-position。
- pointerleave：lerp 回 0。
### 减少动效
`prefers-reduced-motion: reduce`：M1/M2/M3 直接显示终态；G1 无惯性、无弹簧——松手直接切换（无过渡）；G2 完全不绑定。

## 8. 响应式
断点 40rem / 64rem / 90rem。手机（390）：单栏，标题 clamp 下限，纸张倾斜减半，卡叠宽 78vw，购买按钮在刊头常驻（手机端用短文案「Buy · $39」）。所有可点区域 ≥44px。
## 9. 性能
图片 srcset 沿用；首图 fetchpriority=high；其余 lazy；JS 原生无依赖，< 8KB；will-change 只在拖动期间设置。
