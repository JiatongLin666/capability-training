# 信息安全基础能力训练

学号：2025303752

课程练习代码。每个练习一个目录，独立可运行。

> 代码仅用于课程实验环境（自建虚拟机 / 靶场），请勿用于未授权的系统。

## 目录

| 目录 | 说明 |
| --- | --- |
| `练习1-网页单词提取/` | 抓取网页、提取单词并按词频排序；支持输出到文件、生成密码候选变形、按深度爬取同域页面 |
| `练习2-bind-shell/` | bind shell：在目标主机监听指定端口，建立 TCP 连接后提供命令执行通道 |

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

## 练习2：bind shell

在目标主机（虚拟机）上监听指定端口，等待客户端连接；连上后把收到的每条命令交给 shell 执行，并把输出回传。

### 安装依赖

```bash
pip install -r 练习2-bind-shell/requirements.txt
```

### 运行

```bash
# 在目标主机上启动，监听 4444 端口
python 练习2-bind-shell/bindshell.py --port 4444
```

### 参数

| 参数 | 说明 |
| --- | --- |
| `-p, --port` | 监听端口（默认 4444） |

### 客户端连接

```bash
# 攻击机（宿主机）执行
ncat <目标IP> 4444
```

- Linux 客户端：`nc <目标IP> <端口>`
- Windows 客户端：`winget install Insecure.Nmap` 后使用 `ncat`
- 目标机为 Ubuntu 且启用了 ufw 时需先放行端口：`sudo ufw allow 4444/tcp`（测试后删除）

### 实现说明

在课件示例的基础上修正了命令收发的边界问题：

- 以 `\n` 作为命令结束符，用缓冲区切分，正确处理 TCP 的粘包 / 拆包；
- 兼容客户端发送 `\r\n` 行尾；
- 客户端断开（`recv` 返回 `b''`）时退出线程，避免空转；
- 每个连接一个线程，支持多客户端并发连接。
