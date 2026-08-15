# magnet-searcher

磁链聚合搜索命令行工具

![screenshot](https://raw.githubusercontent.com/akarrin/magnet-searcher/master/images/screenshot.gif)

自动从多个 BT 搜索源抓取磁力链接，按磁链去重后汇总展示，支持按大小/热度/时间排序、指定数量、导出 txt/csv。

## 目录

- [安装](#安装)
- [命令参数](#命令参数)
- [基本用法](#基本用法)
- [交互模式](#交互模式)
- [配置项](#配置项)
- [当前可用搜索源](#当前可用搜索源2026年验证)
- [常见问题](#常见问题)
- [新 Python 兼容性说明](#新-python-兼容性说明)

## 安装

### 方式一：源码运行（推荐）

```shell
$ git clone https://github.com/akarrin/magnet-searcher.git
$ cd magnet-searcher
$ python3 -m venv .venv
$ .venv/bin/pip install requests lxml click configparser arrow pysocks
$ .venv/bin/python magnet_search.py -k 上海堡垒
```

### 方式二：安装为全局命令

```shell
$ pip install requests lxml click configparser arrow pysocks
$ sudo python setup.py install
$ magnet-searcher -k 上海堡垒
```

## 命令参数

```
magnet_search.py [选项] [额外词]...

  -k, --keyword TEXT   搜索关键词, 必填; 空格分隔多个词
  -c, --count INTEGER  需要的结果数量, 默认 15
  -s, --sort TEXT      排序: size(大小) / hot(热度) / date(时间), 默认按源排序
  --source TEXT        优先来源: nyaa / piratebay / tokyotosho
  --help               获取命令帮助
```

## 基本用法

```shell
# 最简单的搜索（按规则顺序自动抓取多个源、去重、汇总）
$ magnet-searcher -k "shimoneta"

# 指定数量 + 按大小倒序
$ magnet-searcher -k "ubuntu" -c 10 -s size

# 按热度倒序
$ magnet-searcher -k "shimoneta" -c 5 -s hot

# 指定优先来源（先查该源，数量不足时再从其他源补充）
$ magnet-searcher -k "上海堡垒" --source piratebay

# 多词搜索（空格分隔，整体作为关键词发送）
$ magnet-searcher -k "shimoneta 1080p" -c 5
```

搜索结果展示格式：

```
----------------------------------------------------------------------
名称      1080P   [Tenrai-Sensei] SHIMONETA A Boring World Where The Concept...
磁链      magnet:?xt=urn:btih:670D5484F71B24674B017AEF2D9A7211DB2AA1B7&dn=...
大小      4.3GiB
日期      3年前
热度      114
来源      nyaa
----------------------------------------------------------------------
```

## 交互模式

每次搜索完成后进入交互循环：

| 输入 | 功能 |
| --- | --- |
| 输入新关键词 + Enter | 继续搜索新关键词 |
| 输入 `O` + Enter | 导出当前搜索结果（输入 txt/csv 路径） |
| 输入 `D` + Enter | 直接导出到默认位置 `~/Desktop/关键词.txt` |
| Ctrl+C | 退出 |

导出示例：

```
请输入搜索的关键词，或输入O+Enter导出搜索结果, 或按Ctrl+C退出: O
请输入导出路径，支持txt及csv格式，如'/home/usr/Desktop/output.txt', 或输入D+Enter键直接导出到默认位置: /tmp/result.txt
成功导出至/tmp/result.txt
```

## 配置项

### config.ini

代理、请求头、请求超时、debug 模式：

```ini
[PROXIES]
http = http://127.0.0.1:7890    ; 大陆访问境外源建议配置代理
https = http://127.0.0.1:7890

[FAKE HEADERS]
user-agent = Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0

[TIME OUT]
request_time_out = 30
```

### rules.json

搜索源规则（URL 模板、排序参数、XPath 提取规则）：

- 临时停用某源：把该源 `"active": true` 改为 `false`
- 新增源：参照 `piratebay` 规则块复制修改（base_url、query_tail、sorted_by 及各 XPath 需按目标站结构编写）

## 当前可用搜索源（2026年验证）

| --source 值 | 站点 | 内容倾向 | 备注 |
| --- | --- | --- | --- |
| nyaa | https://nyaa.si | 动画/日系 | 匿名限速约 10 次/分钟, 超时自动跳过 |
| piratebay | https://piratebayproxy.live | 通用资源 | 搜索结果页直接含磁链 |
| tokyotosho | https://www.tokyotosho.info | 动画聚合 | 部分关键词相关性一般 |

> 原配置的 btants/torrentkitty/ciliwang/zooqle/chazhongzi/ciliguo 等搜索源已失效(站点关闭或被反爬拦截)，已在 `rules.json` 中置为 `active: false`，如站点恢复可自行改回。

## 常见问题

- **提示"请求XX超时"**：该源响应慢或被限速，工具会自动跳过并尝试下一个源，属正常现象
- **提示"没有找到资源"**：所有可用源均无结果，换关键词重试
- **中国大陆直连超时**：境外源被墙，在 `config.ini` 的 `[PROXIES]` 配置代理后重新运行
- **想换回旧源**：把 `rules.json` 中对应源 `active` 改回 `true`（注意这些站点大多已关闭，改回通常无效）

## 新 Python 兼容性说明

- 旧版 `requirements.txt` 锁定的依赖（lxml 4.4.1 等）无法在现代 Python 上安装，建议直接安装最新版：
  `pip install requests lxml click configparser arrow pysocks`
- 已兼容新 setuptools（不再依赖已移除的 `pkg_resources` 模块）
- 已修复 3 处无效转义序列 SyntaxWarning
