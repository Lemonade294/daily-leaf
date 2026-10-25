# -*- coding: utf-8 -*-
"""回滚被误转义的字符串结束分隔符：\\' 后跟 , : } ] 或行尾 → 恢复为 '（词内撇号保持转义）"""
import re, os

BASE = os.path.dirname(os.path.abspath(__file__))
FILES = ['data_part1.py','data_part2.py','data_part3.py','data_part4.py','data_part5.py']

# 被误转义的只有"结束分隔符"：\\' 后面是 : , } ] 或换行
PAT = re.compile(r"\\'(?=[:,}\]]|\n)")

for name in FILES:
    p = os.path.join(BASE, name)
    with open(p, 'r', encoding='utf-8') as f:
        s = f.read()
    s2, n = PAT.subn("'", s)
    with open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(s2)
    print(name, '恢复分隔符数量:', n)
print('done')
