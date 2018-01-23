import re
import save_melon

save_melon.save()

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
    PATTERN_RANK = re.compile(r'<span.*?>(\d*)</span>.*?<span.*?>', re.DOTALL)
    rank = re.search(PATTERN_RANK, td_rank).group(1)
    dic['rank'] = int(rank)

    ##title_artist
    td_title_artist = td_all[5]

    ## title
    PATTERN_DIV_RANK01 = re.compile(r'<div class="ellipsis rank01">.*?</div>', re.DOTALL)
    PATTERN_A_CONTENT = re.compile(r'<a.*?>(.*?)</a>')
    title_content = re.search(PATTERN_DIV_RANK01, td_title_artist).group()
    title = re.search(PATTERN_A_CONTENT, title_content).group(1)
    dic['title'] = title

    ## artist
    PATTERN_DIV_RANK02 = re.compile(r'<div class="ellipsis rank02">.*?</div>', re.DOTALL)
    PATTERN_A_ARTIST = re.compile(r'<a.*?>(.*?)</a>')
    artist_content= re.search(PATTERN_DIV_RANK02, td_title_artist).group()
    artist = re.search(PATTERN_A_ARTIST, artist_content).group(1)
    dic['artist'] = artist

    ## album
    td_album = td_all[6]

    PATTERN_DIV_RANK03 = re.compile(r'<div class="ellipsis rank03">.*?</div>', re.DOTALL)
    PATTERN_A_ALBUM = re.compile(r'<a.*?>(.*?)</a>')
    album_content = re.search(PATTERN_DIV_RANK03, td_album).group()
    album = re.search(PATTERN_A_ALBUM, album_content).group(1)
    dic['album'] = album

    chart.append(dic)

print_chart(chart)