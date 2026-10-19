# v3 设计规格 — Rifle 的场景 × Appointed 的克制

定位：一家街角纸品店的季节橱窗。先让中介看到吊牌系在派饼上、放在客户门口的画面，再让他买。
- **场景摄影（学 Rifle）**：首屏和关键段落用满版、暖色、节日感的礼物场景。每张图里都有我们真实的吊牌设计（AI 生成场景，空白吊牌用透视变换替换成站内产品图里裁出的单张吊牌，见 assets/scenes/tools/composite.py）。
- **排版（学 Appointed）**：小号衬线标题，留白多，文字少，左对齐，没有装饰。
- **导航（真实商店）**：深蓝促销条，下面是 Logo 居中的刊头，再下面一排按场合和品类的链接。

## 禁止
巨型标题（任何标题都不超过 44px）、倾斜样机、卡叠或拖拽手势、装饰性数字和罗马数字、圆角卡片、阴影卡片、渐变、emoji、全大写眉题在每段重复出现。

## 字体与颜色
- 字体：Instrument Serif（标题、价格，正体为主，斜体只点一个词）；Inter 400/500（正文 15–16px、导航 13px）。
- 颜色：纸色 #fbf8f2（页面），浅纸色 #f3eee4（商品图底），墨色 #1a2236，次要文字 #5b6170，深蓝 #14213a（促销条、Prompt 段、页脚），砖红 #a4472b（价格和"当季"链接，少量使用）。

## 版式（从上到下）
1. **促销条**（深蓝，12px，居中）："Instant download via Gumroad · Nothing ships; everything prints." 再加一个链接 "Get ten free prompts →"（free sample 的 Gumroad 链接）。
2. **刊头**：三栏网格。左边 "Shop on Gumroad"（店铺链接），中间 wordmark "MIDNIGHT PAGES STUDIO"（Inter 500，15px，字距 .34em），右边 "Buy the Library — $39"（文字链接，带下划线，始终可见）。下面一排导航，以细线分隔：Thanksgiving pop-bys（砖红，锚点到 #library）· Gift tags · The Tag Library · Prompt Pack · Free sample。刊头吸顶，背景是纸色。手机：促销条、wordmark 加右侧 "Buy · $39"；导航变成可横向滑动的一行。
3. **首屏（Thanksgiving）**：满版图片 assets/scenes/hero-thanksgiving.webp，高度 min(86vh, 760px)，object-fit cover，焦点在左边的派饼。文字压在图片右侧三分之一的柔焦桌面上，放在一块纸色面板里（不是卡片：纯色 #fbf8f2，无阴影，无圆角，padding 32px，宽约 380px）。面板内容依次是：小字 "The Pop-By Tag Library"；H1 衬线 40px "For the pie at *Thanksgiving*."；一句原文案 "Eight tag collections, 109 printable and editable designs, plus The Home Letter 2027: twelve monthly client newsletters, already written."；按钮 "Buy the Library $39"（深蓝底实心矩形）；小字 "Instant download via Gumroad. All eight sets bought separately cost $56."。
   手机：图片用 hero-thanksgiving-mobile.webp，高 70vh，面板放在图片下方，不叠在图上。
4. **Gift tag sets, $7 each**（标题 32px，左对齐，右边 "Shop all on Gumroad" 链接）：说明文字用现有的 section-head__note。8 个系列：电脑每行 4 个，手机每行 2 个。每格：方形产品图（img/*-480/800.webp，放在 #f3eee4 底上，无边框无阴影）→ 名称（衬线 20px）和右侧价格 $7 → 一行描述（14px，次要色，最多两行）→ 张数（12px）。整格是指向该系列 Gumroad 页面的链接。悬停时图片透明度 0.92，名称加下划线，不做位移。
5. **How agents use them**（标题 32px）：三张场景图横排（手机竖排），比例 4:3。每张下面是小标题加原文：
   - Pop-bys → use-popby-porch.webp
   - Client touches → use-closing-keys.webp
   - Open houses → use-openhouse-cookies.webp
6. **The Tag Library 详情**：左边 7 列，放现有的 library-800.webp（产品总览，放在 #f3eee4 底上，平放不倾斜）；右边 5 列：标题 "The Pop-By Tag Library"，两段原文（lede 和 lede--small），图注列出八个系列名，然后是按钮 $39 和价格说明。
7. **Prompt Pack**：满宽两栏，背景纸色，不用深蓝。左边是 prompt-desk.webp 场景图（Appointed 风桌面），右边是标题 "AI Listing & Marketing Prompt Pack"、两段原文、按钮 "Buy the Prompt Pack $24"。
8. **Free sample**：一条浅色横带 #f3eee4，左边标题 "Ten prompts, on the house" 加原文，右边按钮 "Get the free sample"。
9. **页脚**：深蓝，wordmark 加链接一行，加 "Digital downloads for US real estate agents. Nothing ships; everything prints."

## 间距
内容最大宽 1280px，左右边距 clamp(20px, 4vw, 48px)；段落之间 96px（手机 64px）；标题下方 24px。

## 动效（只有两种）
- 图片缓慢淡入：进入视口时 opacity 0→1，800ms，cubic-bezier(0.22,1,0.36,1)，只动 opacity，用 IntersectionObserver。理由：避免图片硬生生地蹦出来，保持安静。
- 首屏大图极轻的视差：图片 translateY 最多 40px，跟随滚动，用 requestAnimationFrame，只改 transform。理由：给满版大图一点景深，但不抢注意力。
- prefers-reduced-motion 时两者都关闭。不用 JS 时内容默认可见。

## v4 修订（2026-10-19，老板：首屏要一眼看出房产）
- 首屏场景：美国住宅门廊（海军蓝木门、黄铜门把/门牌、秋季菊花与南瓜），台阶上一只装苹果的牛皮纸袋，系真实 Curb Appeal「Thankful for clients like you」吊牌，旁边一串新房钥匙。文件 assets/scenes/v4-hero-porch.webp（2560×1440）/ v4-hero-porch-mobile.webp（竖裁）。
- 首屏标题改为现有文案中的「For the bag of apples on a past client’s porch.」（取自 The Pop-By Tag Library 段落原句，未新编）。
- 用法三张：Pop-bys 保留门廊苹果袋；Client touches 换为交房钥匙+蜡烛（竖放「Welcome home」吊牌，孔位上方留白不压字）；Open houses 换为样板房厨房岛台饼干罐。
- 手机首屏：图片约 44svh，图下紧接标题与购买按钮，按钮在 390×844 首屏内可见；说明文字放到按钮之后。
- 清晰度：AI 底图 1280×720 → Real-ESRGAN x4plus（ncnn-vulkan + Mesa lavapipe CPU，本地免费）手动分块放大到 2560×1440，再在高分辨率底图上贴吊牌（吊牌原图不经 AI 放大，避免文字被"脑补"）。
- 吊牌比例：场景里空白吊牌比原图更细长，采用"纵向最多拉伸 18% + 用吊牌底色向上/下延展"的方式适配，不压缩插画、不让打孔压到文字。
