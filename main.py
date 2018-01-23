import re
import save_melon

#순위 커버 이미지

"""
print(chart)
[
    {
        'rank': 1,
        'title': '다른~',
        'artist': '수지'
        'album' : Faces of loe',
        'Like_content': '21.900'
    }
]
"""

save_melon.save()

PATTERN_DIV_RANK01 = re.compile(r'<div class="ellipsis rank01">.*?</div>', re.DOTALL)
PATTERN_A_CONTENT = re.compile(r'<a.*?>(.*?)</a>')

source = open('melon.html', 'rt').read()

match_list = re.finditer(PATTERN_DIV_RANK01, source)
print(match_list)

for index, match_object_div_rank01 in enumerate(match_list):
    title = re.search(PATTERN_A_CONTENT, match_object_div_rank01.group())
    print('========================================================================================================')
    print(f'{index+1}. {title.group(1)}')

#     div_rank01 = re.findall(PATTERN_DIV_RANK01, source)
# for index, item in enumerate(div_rank01):
#     title = re.search(PATTERN_A_CONTENT, item).group(1)
#     print('========================================================================================================')
#     print(f'{index+1}. {title}')