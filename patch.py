# -*- coding: utf-8 -*-
"""对 daily-mag.html 做样式修补"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(BASE, 'daily-mag.html')
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

def rep(old, new):
    global s
    assert s.count(old) == 1, '锚点不唯一或缺失: ' + old[:50]
    s = s.replace(old, new)

# 1. cover-num 缩小并右移，标题右侧让位
rep(""".cover-num{
  position:absolute; right:16px; bottom:10px;
  font-family:var(--font-en); font-size:54px; font-weight:700; line-height:1;
  color:rgba(255,255,255,.16); letter-spacing:.02em;
}""", """.cover-num{
  position:absolute; right:12px; bottom:8px;
  font-family:var(--font-en); font-size:38px; font-weight:700; line-height:1;
  color:rgba(255,255,255,.2); letter-spacing:.02em;
}""")

rep(""".cover-title{
  position:absolute; left:18px; right:18px; bottom:14px;""", """.cover-title{
  position:absolute; left:18px; right:62px; bottom:14px;""")

# 2. dict-close 放大
rep(""".dict-close{
  position:absolute; right:12px; top:12px; width:26px; height:26px; border-radius:8px;""",
""".dict-close{
  position:absolute; right:12px; top:12px; width:30px; height:30px; border-radius:8px;""")

# 3. 移动端断点增强：nav/pill 触控与字号
rep(""".nav-btn{padding:7px 12px; font-size:13.5px}""",
""".nav-btn{padding:8px 12px; font-size:13px}""")

rep(""".dict-hint{font-size:11.5px; color:var(--text-3); margin-left:auto}""",
""".dict-hint{font-size:12.5px; color:var(--text-3); margin-left:auto}""")

# 移动端 pill 与 dict-btn
rep("""@media(max-width:520px){
  .brand-name{font-size:15px; letter-spacing:.08em}""",
"""@media(max-width:520px){
  .pill{padding:10px 15px; font-size:13.5px}
  .dict-btn{font-size:13.5px; padding:9px 16px}
  .brand-name{font-size:15px; letter-spacing:.08em}""")

with open(p, 'w', encoding='utf-8', newline='') as f:
    f.write(s)
print('patch OK, size:', round(len(s)/1024,1), 'KB')
