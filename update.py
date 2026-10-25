# -*- coding: utf-8 -*-
"""每日自我更新：把当天日期（UTC+8）烧录进 index.html 的 TODAY_OVERRIDE。
由 GitHub Actions 每天定时调用；本地运行亦可。"""
import re, os, sys, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(BASE, 'index.html')

# 固定按北京时间取日期，不依赖服务器时区
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
today = now.strftime('%Y-%m-%d')

with open(html_path, 'r', encoding='utf-8') as f:
    s = f.read()

pat = re.compile(r"const TODAY_OVERRIDE = '[^']*';")
m = pat.search(s)
if not m:
    print('ERROR: 找不到 TODAY_OVERRIDE 声明', file=sys.stderr)
    sys.exit(1)

old = m.group(0)
new = "const TODAY_OVERRIDE = '%s';" % today
if old == new:
    print('no change, already', today)
else:
    s2 = pat.sub(new, s, count=1)
    with open(html_path, 'w', encoding='utf-8', newline='') as f:
        f.write(s2)
    print('stamped TODAY_OVERRIDE =', today)
