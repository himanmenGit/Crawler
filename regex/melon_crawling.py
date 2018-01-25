import requests
import re

source = open('melon.html', 'rt').read()

PATTERN_DIV_RANK01 = re.compile(r'<div class="ellipsis rank01">.*?</div>', re.S)
PATTERN_A_CONTENT = re.compile(r'<a.*?>(.*?)</a>', re.S)

match_list = PATTERN_DIV_RANK01.finditer(source)

for match in match_list:
    a_list = PATTERN_A_CONTENT.search(match.group())
    print(a_list.group(1))
