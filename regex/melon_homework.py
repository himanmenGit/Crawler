import re

from regex.utils import *

source = open('melon.html', 'rt').read()

def print_chart(chart):
    print('\n=================================================================\n')
    print('[')
    for info in chart:
        print(f'\t{info}')
    print(']')

chart = list()

PATTERN_TR = re.compile(r'<tr.*?>.*?</tr>', re.DOTALL)
PATTERN_TD = re.compile(r'<td.*?>.*?</td>', re.DOTALL)

tr_all = re.findall(PATTERN_TR, source)

for index, tr in enumerate(tr_all):
    dic = dict()

    if index == 0:
        continue

    td_all = re.findall(PATTERN_TD, tr)

    #rank
    td_rank = td_all[1]
    # PATTERN_RANK = re.compile(r'<span.*?>(\d*)</span>.*?<span.*?>', re.DOTALL)
    # rank = re.search(PATTERN_RANK, td_rank).group(1)
    rank_content = find_tag('span', td_rank, class_='rank ')
    rank = get_tag_content(rank_content)
    dic['rank'] = int(rank)

    ##title_artist
    td_title_artist = td_all[5]

    ## title
    # PATTERN_DIV_RANK01 = re.compile(r'<div class="ellipsis rank01">.*?</div>', re.DOTALL)
    # PATTERN_A_CONTENT = re.compile(r'<a.*?>(.*?)</a>')
    # title_content = re.search(PATTERN_DIV_RANK01, td_title_artist).group()
    # title = re.search(PATTERN_A_CONTENT, title_content).group(1)
    title_content = find_tag('div', td_title_artist, class_='rank01')
    title_a_tag = find_tag('a', title_content)
    title = get_tag_content(title_a_tag)
    dic['title'] = title

    ## artist
    # PATTERN_DIV_RANK02 = re.compile(r'<div class="ellipsis rank02">.*?</div>', re.DOTALL)
    # PATTERN_A_ARTIST = re.compile(r'<a.*?>(.*?)</a>')
    # artist_content= re.search(PATTERN_DIV_RANK02, td_title_artist).group()
    # artist = re.search(PATTERN_A_ARTIST, artist_content).group(1)
    artist_content = find_tag('div', td_title_artist, class_='rank02')
    artist_a_tag = find_tag('a', artist_content)
    artist = get_tag_content(artist_a_tag)
    dic['artist'] = artist
    # break;

    ## album
    td_album = td_all[6]

    # PATTERN_DIV_RANK03 = re.compile(r'<div class="ellipsis rank03">.*?</div>', re.DOTALL)
    # PATTERN_A_ALBUM = re.compile(r'<a.*?>(.*?)</a>')
    # album_content = re.search(PATTERN_DIV_RANK03, td_album).group()
    # album = re.search(PATTERN_A_ALBUM, album_content).group(1)
    album_content = find_tag('div', td_album, class_='rank03')
    album_a_tag = find_tag('a', album_content)
    album = get_tag_content(album_a_tag)
    dic['album'] = album

    chart.append(dic)

print_chart(chart)