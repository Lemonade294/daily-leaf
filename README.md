# 拾页外刊 · The Daily Leaf

每日外刊风格的英文阅读网站。50 篇原创外刊文章（新闻 / 故事 / 评论 / 治愈，短中长搭配），书籍封面式卡片墙，单栏阅读模式，日间 / 夜间双主题，点词查义，生词本本地持久化。

## 功能

- **每日 20 篇**：以当天日期为种子，从文章池确定性选出 20 篇作为「今日外刊」（次日自动轮换），无需服务器
- **分类筛选**：新闻 14 / 故事 15 / 评论 11 / 治愈 10
- **篇幅筛选**：短篇 20 / 中篇 22 / 长篇 8
- **全文搜索**：标题、中文导读、正文、生词
- **点词查义**：点击正文任意英文单词，释义浮层出现在屏幕顶端，点任意处消失；可一键加入生词本
- **生词本**：收藏 / 标记掌握 / 删除，统计打卡天数，数据保存在浏览器 localStorage
- **阅读体验**：日间纸感 / 夜间深蓝双主题，字号调节，已读打卡，阅读进度条

## 目录结构

```
daily-leaf/
├── index.html           # 自包含站点（唯一交付物，直接打开即用）
├── build.py             # 构建脚本：合并文章数据与词库，注入 index.html
├── update.py            # 每日自我更新脚本：烧录当天日期进 index.html
├── data_common.py       # 通用查词词库（787 词）
├── data_part1~5.py      # 50 篇文章数据（可自行增改，改完跑 build.py）
├── .github/workflows/
│   ├── pages.yml        # 推送到 main 即自动部署 GitHub Pages
│   └── daily.yml        # 每天北京时间 05:00 自动烧录日期并推送（触发重建）
└── _shots/              # 自检截图（不入库）
```

## 本地使用

浏览器直接打开 `index.html` 即可，无需安装任何东西。

想改文章：编辑 `data_part*.py` → 运行 `python build.py` 重新生成。

## 自我更新机制（GitHub Actions）

站点通过两个工作流实现「每日轮换 + 自动部署」：

1. **`daily.yml`（Daily Self-Update）**：每天北京时间 05:00 自动运行 `update.py`，把当天日期烧录进 `index.html` 的 `TODAY_OVERRIDE` 并提交推送；
2. **`pages.yml`（Deploy to GitHub Pages）**：监听 `main` 分支推送，用官方 Actions 部署站点。

前端读取 `TODAY_OVERRIDE`（3 天内有效）作为当日的「发布日」，以它为种子选出当日 20 篇；超过 3 天（Actions 停更）则回退到浏览器当天日期，网站依然每天轮换。也可在 Actions 页面手动触发 `Daily Self-Update` 立即更新。

## 发布到 GitHub Pages

仓库设置 → Pages → Source 选 `GitHub Actions`，然后推送即可自动部署。

> 文章均为原创外刊风格内容，未抓取任何真实刊物的受版权内容。
