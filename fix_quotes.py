# -*- coding: utf-8 -*-
"""修复数据文件中的撇号转义：将字母后紧跟的 ' 转义为 \\'（字符串分隔符不受影响）"""
import re, os

BASE = os.path.dirname(os.path.abspath(__file__))
FILES = ['data_part1.py','data_part2.py','data_part3.py','data_part4.py','data_part5.py']

# 撇号前面是字母（词内所有格/缩写）→ 转义。分隔符前的 ' 前面是 : , [ 空格等，不受影响。
PAT = re.compile(r"(?<=[A-Za-z])'")

for name in FILES:
    p = os.path.join(BASE, name)
    with open(p, 'r', encoding='utf-8') as f:
        s = f.read()
    s2, n = PAT.subn(r"\\'", s)
    with open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(s2)
    print(name, '转义数量:', n)
print('done')
