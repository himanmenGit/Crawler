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

"""
[
	{'rank': 1, 'title': '다른사람을 사랑하고 있어', 'artist': '수지 (SUZY)', 'album': 'Faces of Love'}
	{'rank': 2, 'title': '그날처럼', 'artist': '장덕철', 'album': '그날처럼'}
	{'rank': 3, 'title': '주인공', 'artist': '선미', 'album': '주인공'}
	{'rank': 4, 'title': '#첫사랑', 'artist': '볼빨간사춘기', 'album': '#첫사랑'}
	{'rank': 5, 'title': '빛이 나 (Shinin`)', 'artist': '종현 (JONGHYUN)', 'album': 'Poet｜Artist'}
	{'rank': 6, 'title': '비행운', 'artist': '문문 (MoonMoon)', 'album': 'LIFE IS BEAUTY FULL'}
	{'rank': 7, 'title': 'instagram', 'artist': 'DEAN', 'album': 'instagram'}
	{'rank': 8, 'title': 'Havana (Feat. Young Thug)', 'artist': 'Camila Cabello', 'album': 'Camila'}
	{'rank': 9, 'title': '선물', 'artist': '멜로망스', 'album': 'Moonlight'}
	{'rank': 10, 'title': '답장', 'artist': '김동률', 'album': '답장'}
	{'rank': 11, 'title': 'Roller Coaster', 'artist': '청하', 'album': 'Offset'}
	{'rank': 12, 'title': 'Heart Shaker', 'artist': 'TWICE (트와이스)', 'album': 'Merry & Happy'}
	{'rank': 13, 'title': '밤이 되니까', 'artist': '펀치 (Punch)', 'album': '밤이 되니까'}
	{'rank': 14, 'title': 'Universe', 'artist': 'EXO', 'album': 'Universe - 겨울 스페셜 앨범, 2017'}
	{'rank': 15, 'title': 'Lonely (Feat. 태연)', 'artist': '종현 (JONGHYUN)', 'album': '종현 소품집 `이야기 Op.2`'}
	{'rank': 16, 'title': '환상통 (Only One You Need)', 'artist': '종현 (JONGHYUN)', 'album': 'Poet｜Artist'}
	{'rank': 17, 'title': '기억의 빈자리', 'artist': '나얼', 'album': '기억의 빈자리'}
	{'rank': 18, 'title': '좋니', 'artist': '윤종신', 'album': 'LISTEN 010 좋니'}
	{'rank': 19, 'title': 'DNA', 'artist': '방탄소년단', 'album': 'LOVE YOURSELF 承 `Her`'}
	{'rank': 20, 'title': '좋아', 'artist': '민서', 'album': '2017 월간 윤종신 11월호'}
	{'rank': 21, 'title': '피카부 (Peek-A-Boo)', 'artist': 'Red Velvet (레드벨벳)', 'album': 'Perfect Velvet - The 2nd Album'}
	{'rank': 22, 'title': 'LIKEY', 'artist': 'TWICE (트와이스)', 'album': 'twicetagram'}
	{'rank': 23, 'title': 'all of my life', 'artist': '박원', 'album': '0M'}
	{'rank': 24, 'title': '뿜뿜', 'artist': '모모랜드 (MOMOLAND)', 'album': 'GREAT!'}
	{'rank': 25, 'title': 'Ko Ko Bop', 'artist': 'EXO', 'album': 'THE WAR - The 4th Album'}
	{'rank': 26, 'title': 'Beautiful', 'artist': 'Wanna One (워너원)', 'album': '1-1=0 (NOTHING WITHOUT YOU)'}
	{'rank': 27, 'title': '겨울소리', 'artist': '박효신', 'album': '겨울소리'}
	{'rank': 28, 'title': '와플 (#Hashtag)', 'artist': '종현 (JONGHYUN)', 'album': 'Poet｜Artist'}
	{'rank': 29, 'title': '이 별', 'artist': '길구봉구', 'album': 'Star'}
	{'rank': 30, 'title': 'Tell Me', 'artist': '인피니트', 'album': 'TOP SEED'}
	{'rank': 31, 'title': '우린 봄이 오기 전에 (Before Our Spring)', 'artist': '종현 (JONGHYUN)', 'album': 'Poet｜Artist'}
	{'rank': 32, 'title': '그리워하다', 'artist': '비투비', 'album': 'Brother Act.'}
	{'rank': 33, 'title': 'Power', 'artist': 'EXO', 'album': 'The Power of Music - The 4th Album Repackage'}
	{'rank': 34, 'title': '비밀정원', 'artist': '오마이걸', 'album': '비밀정원'}
	{'rank': 35, 'title': '밤편지', 'artist': '아이유', 'album': '밤편지'}
	{'rank': 36, 'title': '시차 (We Are) (Feat. 로꼬 & GRAY)', 'artist': '우원재', 'album': '시차 (We Are)'}
	{'rank': 37, 'title': '썸 탈꺼야', 'artist': '볼빨간사춘기', 'album': 'Red Diary Page.1'}
	{'rank': 38, 'title': '봄날', 'artist': '방탄소년단', 'album': 'YOU NEVER WALK ALONE'}
	{'rank': 39, 'title': '그때의 나, 그때의 우리', 'artist': '어반자카파', 'album': '그때의 나, 그때의 우리'}
	{'rank': 40, 'title': '기름때 (Grease)', 'artist': '종현 (JONGHYUN)', 'album': 'Poet｜Artist'}
	{'rank': 41, 'title': '가시나', 'artist': '선미', 'album': 'SUNMI SPECIAL EDITION `가시나`'}
	{'rank': 42, 'title': 'Take The Dive', 'artist': '종현 (JONGHYUN)', 'album': 'Poet｜Artist'}
	{'rank': 43, 'title': '지나갈 테니 (Been Through)', 'artist': 'EXO', 'album': 'Universe - 겨울 스페셜 앨범, 2017'}
	{'rank': 44, 'title': '가을 안부', 'artist': '먼데이 키즈', 'album': '가을 안부'}
	{'rank': 45, 'title': '바보야', 'artist': '허각', 'album': '바보야'}
	{'rank': 46, 'title': '사람 구경 중 (Sightseeing)', 'artist': '종현 (JONGHYUN)', 'album': 'Poet｜Artist'}
	{'rank': 47, 'title': 'Stay', 'artist': 'EXO', 'album': 'Universe - 겨울 스페셜 앨범, 2017'}
	{'rank': 48, 'title': 'Shape of You', 'artist': 'Ed Sheeran', 'album': '÷ (Deluxe)'}
	{'rank': 49, 'title': '에너제틱 (Energetic)', 'artist': 'Wanna One (워너원)', 'album': '1X1=1(TO BE ONE)'}
	{'rank': 50, 'title': '노력', 'artist': '박원', 'album': '1/24'}
	{'rank': 51, 'title': 'Fall', 'artist': 'EXO', 'album': 'Universe - 겨울 스페셜 앨범, 2017'}
	{'rank': 52, 'title': '고민보다 Go', 'artist': '방탄소년단', 'album': 'LOVE YOURSELF 承 `Her`'}
	{'rank': 53, 'title': 'Good Night', 'artist': 'EXO', 'album': 'Universe - 겨울 스페셜 앨범, 2017'}
	{'rank': 54, 'title': '연애소설 (Feat. 아이유)', 'artist': '에픽하이 (EPIK HIGH)', 'album': 'WE`VE DONE SOMETHING WONDERFUL'}
	{'rank': 55, 'title': '하루만이라도 (Just for a day)', 'artist': '종현 (JONGHYUN)', 'album': 'Poet｜Artist'}
	{'rank': 56, 'title': 'Lights Out', 'artist': 'EXO', 'album': 'Universe - 겨울 스페셜 앨범, 2017'}
	{'rank': 57, 'title': 'There`s Nothing Holdin` Me Back', 'artist': 'Shawn Mendes', 'album': 'Illuminate (New Deluxe Ver.)'}
	{'rank': 58, 'title': '어떤 기분이 들까 (I`m So Curious)', 'artist': '종현 (JONGHYUN)', 'album': 'Poet｜Artist'}
	{'rank': 59, 'title': 'Rewind', 'artist': '종현 (JONGHYUN)', 'album': 'Poet｜Artist'}
	{'rank': 60, 'title': '그 사람을 아나요', 'artist': '임창정', 'album': '그 사람을 아나요'}
	{'rank': 61, 'title': '눈 (Feat. 이문세)', 'artist': 'Zion.T', 'album': '눈'}
	{'rank': 62, 'title': 'Sentimental', 'artist': '종현 (JONGHYUN)', 'album': 'Poet｜Artist'}
	{'rank': 63, 'title': '나의 사춘기에게', 'artist': '볼빨간사춘기', 'album': 'Red Diary Page.1'}
	{'rank': 64, 'title': 'MIC Drop', 'artist': '방탄소년단', 'album': 'LOVE YOURSELF 承 `Her`'}
	{'rank': 65, 'title': '첫눈처럼 너에게 가겠다', 'artist': '에일리', 'album': '도깨비 OST Part.9'}
	{'rank': 66, 'title': '비도 오고 그래서 (Feat. 신용재)', 'artist': '헤이즈 (Heize)', 'album': '/// (너 먹구름 비)'}
	{'rank': 67, 'title': '한숨', 'artist': '이하이', 'album': 'SEOULITE'}
	{'rank': 68, 'title': '마지막처럼', 'artist': 'BLACKPINK', 'album': '마지막처럼'}
	{'rank': 69, 'title': '짙어져', 'artist': '멜로망스', 'album': 'Yellow OST Part.2'}
	{'rank': 70, 'title': '덜덜덜', 'artist': 'EXID', 'album': 'Full Moon'}
	{'rank': 71, 'title': 'REALLY REALLY', 'artist': 'WINNER', 'album': 'FATE NUMBER FOR'}
	{'rank': 72, 'title': 'HandClap (영화 `슈퍼배드 3` 삽입곡)', 'artist': 'Fitz & The Tantrums', 'album': 'Fitz and The Tantrums (Deluxe)'}
	{'rank': 73, 'title': 'Blue', 'artist': '볼빨간사춘기', 'album': 'Red Diary Page.1'}
	{'rank': 74, 'title': '빨간 맛 (Red Flavor)', 'artist': 'Red Velvet (레드벨벳)', 'album': 'The Red Summer - Summer Mini Album'}
	{'rank': 75, 'title': '미안해', 'artist': '양다일', 'album': 'inside'}
	{'rank': 76, 'title': '꽃이야', 'artist': 'JBJ', 'album': 'True Colors'}
	{'rank': 77, 'title': '눈 떠보니 이별이더라', 'artist': '포맨', 'album': 'REMEMBER ME'}
	{'rank': 78, 'title': '매일 듣는 노래 (A Daily Song)', 'artist': '황치열', 'album': 'Be ordinary'}
	{'rank': 79, 'title': 'WHERE YOU AT', 'artist': '뉴이스트 W', 'album': 'W, HERE'}
	{'rank': 80, 'title': '갖고 싶어', 'artist': 'Wanna One (워너원)', 'album': '1-1=0 (NOTHING WITHOUT YOU)'}
	{'rank': 81, 'title': '피 땀 눈물', 'artist': '방탄소년단', 'album': 'WINGS'}
	{'rank': 82, 'title': '여보세요', 'artist': 'NU`EST', 'album': 'THE SECOND MINI ALBUM `여보세요`'}
	{'rank': 83, 'title': '폰서트', 'artist': '10cm', 'album': '4.0'}
	{'rank': 84, 'title': '사랑하지 않은 것처럼', 'artist': '버즈', 'album': '`Be One` - Buzz The 1st Mini Album'}
	{'rank': 85, 'title': '바람이 불었으면 좋겠어', 'artist': '길구봉구', 'album': '바람이 불었으면 좋겠어'}
	{'rank': 86, 'title': '우리 둘만 아는', 'artist': '윤건', 'album': '우리 둘만 아는'}
	{'rank': 87, 'title': '어디에도', 'artist': '엠씨더맥스', 'album': 'pathos'}
	{'rank': 88, 'title': '남이 될 수 있을까', 'artist': '볼빨간사춘기', 'album': '남이 될 수 있을까'}
	{'rank': 89, 'title': '팔레트 (Feat. G-DRAGON)', 'artist': '아이유', 'album': 'Palette'}
	{'rank': 90, 'title': 'Best Of Me', 'artist': '방탄소년단', 'album': 'LOVE YOURSELF 承 `Her`'}
	{'rank': 91, 'title': '빈차 (Feat. 오혁)', 'artist': '에픽하이 (EPIK HIGH)', 'album': 'WE`VE DONE SOMETHING WONDERFUL'}
	{'rank': 92, 'title': '있다면', 'artist': '뉴이스트 W', 'album': 'NU`EST W `있다면`'}
	{'rank': 93, 'title': 'Santa Tell Me', 'artist': 'Ariana Grande', 'album': 'Santa Tell Me'}
	{'rank': 94, 'title': '뻔한 이별 (PROD. 13)', 'artist': '소유 (SOYOU)', 'album': 'RE:BORN'}
	{'rank': 95, 'title': '바보에게 바보가', 'artist': '지아', 'album': '바보에게 바보가'}
	{'rank': 96, 'title': '가을 아침', 'artist': '아이유', 'album': '꽃갈피 둘'}
	{'rank': 97, 'title': '노땡큐 (Feat. MINO, 사이먼 도미닉, 더콰이엇)', 'artist': '에픽하이 (EPIK HIGH)', 'album': 'WE`VE DONE SOMETHING WONDERFUL'}
	{'rank': 98, 'title': '떠나지마요', 'artist': '블락비 (Block B)', 'album': 'Re:MONTAGE'}
	{'rank': 99, 'title': 'Closer (Feat. Halsey)', 'artist': 'The Chainsmokers', 'album': 'Collage EP'}
	{'rank': 100, 'title': '왜 날', 'artist': '인피니트', 'album': 'TOP SEED'}
]
"""