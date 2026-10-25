# -*- coding: utf-8 -*-
"""构建脚本：合并文章数据与词库，注入 index.html
支持两种状态：占位符（/*__ARTICLES_DATA__*/）或已注入的数据（正则替换单行 const 声明）"""
import io, sys, json, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))
def load(name):
    ns = {}
    src = os.path.join(BASE, name)
    with open(src, 'r', encoding='utf-8') as f:
        code = f.read()
    exec(compile(code, name, 'exec'), ns)
    return ns

p1 = load('data_part1.py')['PART']
p2 = load('data_part2.py')['PART']
p3 = load('data_part3.py')['PART']
p4 = load('data_part4.py')['PART']
p5 = load('data_part5.py')['PART']
COMMON_DICT = load('data_common.py')['COMMON_DICT']

ARTICLES = p1 + p2 + p3 + p4 + p5

# ---- 校验 ----
ids = [a['id'] for a in ARTICLES]
assert len(ids) == len(set(ids)), '存在重复 id'
for a in ARTICLES:
    assert a['category'] in ('news','story','essay','soul'), a['id'] + ' 分类非法'
    assert a['len'] in ('short','medium','long'), a['id'] + ' 长度非法'
    assert a.get('title') and a.get('cn') and a.get('intro'), a['id'] + ' 缺字段'
    assert isinstance(a.get('paras'), list) and len(a['paras']) >= 2, a['id'] + ' 正文不足'
    for p in a['paras']:
        assert p.get('c') and p.get('t') in ('p','h'), a['id'] + ' 段落格式非法'
    assert isinstance(a.get('words'), int) and a['words'] > 0, a['id'] + ' 词数非法'
    assert isinstance(a.get('vocab'), list) and a['vocab'], a['id'] + ' 生词表为空'
    for v in a['vocab']:
        assert v.get('w') and v.get('def'), a['id'] + ' 生词缺字段'

cat_cnt = {}
len_cnt = {}
for a in ARTICLES:
    cat_cnt[a['category']] = cat_cnt.get(a['category'], 0) + 1
    len_cnt[a['len']] = len_cnt.get(a['len'], 0) + 1
print('文章总数:', len(ARTICLES))
print('分类分布:', cat_cnt)
print('长度分布:', len_cnt)
print('词库词数:', len(COMMON_DICT))

# ---- 生成 JS（转义 < 防止 </script> 提前闭合）----
def to_js(obj):
    s = json.dumps(obj, ensure_ascii=False, separators=(',',':'))
    return s.replace('<', '\\u003c')

js_articles = 'const ARTICLES = ' + to_js(ARTICLES) + ';'
js_dict = 'const COMMON_DICT = ' + to_js(COMMON_DICT) + ';'

html_path = os.path.join(BASE, 'index.html')
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

if '/*__ARTICLES_DATA__*/' in html and '/*__DICT_DATA__*/' in html:
    # 占位符模式（全新模板）
    html = html.replace('/*__ARTICLES_DATA__*/', js_articles)
    html = html.replace('/*__DICT_DATA__*/', js_dict)
else:
    # 已注入模式：正则替换单行数据声明
    assert re.search(r'const ARTICLES = ', html), '找不到 ARTICLES 声明'
    assert re.search(r'const COMMON_DICT = ', html), '找不到 COMMON_DICT 声明'
    html = re.sub(r'(?s)const ARTICLES = .*?(?=\nconst COMMON_DICT)',
                  'const ARTICLES = ' + to_js(ARTICLES) + ';', html, count=1)
    html = re.sub(r'(?s)const COMMON_DICT = .*?(?=\n</script>)',
                  'const COMMON_DICT = ' + to_js(COMMON_DICT) + ';', html, count=1)
assert '</script' not in html.lower().replace('</script>', ''), '存在未转义的闭合标签'

with open(html_path, 'w', encoding='utf-8', newline='') as f:
    f.write(html)
print('注入完成, HTML 大小:', round(len(html)/1024, 1), 'KB')
