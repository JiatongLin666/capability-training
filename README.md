# 信息安全基础能力训练

学号：2025303752

课程练习代码。每个练习一个目录，独立可运行。

## 目录

| 目录 | 说明 |
| --- | --- |
| `练习1-网页单词提取/` | 抓取网页、提取单词并按词频排序；支持输出到文件、生成密码候选变形、按深度爬取同域页面 |

## 练习1：网页单词提取

### 安装依赖

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r 练习1-网页单词提取/requirements.txt
```

### 运行

```bash
# 取网页中出现频率最高的 10 个单词，长度 ≥ 4
python 练习1-网页单词提取/webcrawler.py -u http://example.com -l 4 -n 10

# 结果写入文件
python 练习1-网页单词提取/webcrawler.py -u http://example.com -l 4 -o words.txt

# 生成密码候选变形
python 练习1-网页单词提取/webcrawler.py -u http://example.com -n 5 -e -o candidates.txt

# 按深度 2 爬取同一域名下的页面
python 练习1-网页单词提取/webcrawler.py -u http://example.com -d 2 -n 20
```

### 参数

| 参数 | 说明 |
| --- | --- |
| `-u, --url` | 起始网页 URL |
| `-l, --length` | 单词最小长度（默认 0，不限制） |
| `-n, --number` | 输出的单词个数（默认 10） |
| `-o, --output` | 输出文件名（默认打印到控制台） |
| `-d, --depth` | 爬取深度（默认 0，只抓起始页） |
| `-e, --encryption` | 生成密码候选变形（大小写、年份/数字/符号后缀） |
