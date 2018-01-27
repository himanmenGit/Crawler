import os
import re

import requests
from bs4 import NavigableString, BeautifulSoup

########################################################################################################################

# 프로젝트 컨테이너 폴더 경로
PATH_MODULE = os.path.abspath(__file__)

ROOT_DIR = os.path.dirname(os.path.dirname(PATH_MODULE))

# data/폴더 경로
DATA_DIR = os.path.join(ROOT_DIR, 'data')
DATA_SONG_DIR = os.path.join(DATA_DIR, 'song')
DATA_ARTIST_DIR = os.path.join(DATA_DIR, 'artist')

print(PATH_MODULE)
print(ROOT_DIR)
print(DATA_DIR)
print(DATA_SONG_DIR)
print(DATA_ARTIST_DIR)

########################################################################################################################
########################################################################################################################

class MelonCrawler:

    # search_song을 이 클래스의 인스턴스 메서드로 추가
    def get_song_search(self, song_title):
        """
            곡 명으로 멜론에서 검색한 결과 리스트를 리턴
            :param song_title: 검색할 곡 명
            :return: 결과 dict리스트
        """
        params = {
            'q': song_title,
            'section': 'song',
        }
        response = requests.get(f'https://www.melon.com/search/song/index.htm', params)
        soup = BeautifulSoup(response.text, 'lxml')

        result = list()

        tr_list = soup.select('form#frm_defaultList > div > table > tbody > tr')
        for tr in tr_list:
            # frm_defaultList > div > table > tbody > tr:nth-child(1) > td:nth-child(3) > div > div > a.fc_gray
            song_id = tr.select_one('td:nth-of-type(1) input[type=checkbox]').get('value')
            title = None
            title_a = tr.select_one('td:nth-of-type(3) a.fc_gray')
            title_s = tr.select_one('td:nth-of-type(3) > div > div > span')
            if title_a:
                title = title_a.get_text(strip=True)
            else:
                title = title_s.get_text(strip=True)
            artist = tr.select_one('td:nth-of-type(4) span.checkEllipsisSongdefaultList').get_text(strip=True)
            album = tr.select_one('td:nth-of-type(5) a').get_text(strip=True)

            # result.append(Song(song_id, title, artist, album))
            song = Song(song_id=song_id, title=title, artist=artist, album=album)
            result.append(song)
        return result

    def get_search_artist(self, artist):
        """
        http://www.melon.com/search/artist/index.htm?q=%EC%95%84%EC%9D%B4%EC%9C%A0&section=&
                                                     searchGnbYn=Y&kkoSpl=N&kkoDpType=&ipath=srch_form
        아티스트를 검색 하여 나온 아티스트들의 목록을 리턴
        :param artist: 검색 할 아티스트의 이름
        :return: 검색 한 Artist의 목록
        """
        params = {
            'q': artist,
            'section': '',
            'searchGnbYn': 'Y',
            'kkoSpl': 'N',
            'kkoDpType': '',
            'ipath': 'srch_form',
        }
        response = requests.get(f'https://www.melon.com/search/artist/index.htm', params)
        soup = BeautifulSoup(response.text, 'lxml')

        artist_list = list()

        for artist_li in soup.select('#pageList > div > ul > li'):

            artist_name = artist_li.select_one('div > div > dl > dt > a').get_text()
            artist_info = artist_li.select_one('div > div > dl > dd.gubun').get_text(strip=True)

            pattern = re.compile(r'(?P<conutry>.*)/(?P<gender>.*)/(?P<type>.*)', re.DOTALL)
            m = pattern.search(artist_info)

            artist_country = m.group('conutry')
            artist_gender = m.group('gender')
            artist_type = m.group('type')

            artist_genre_list = list()
            artist_genre_div = artist_li.select_one('div > div > dl > dd.gnr > div').find_all('span')
            if artist_genre_div:
                for genre in artist_genre_div:
                    artist_genre_list.append(genre.get_text())

            artist_title_song = None
            artist_title_span = artist_li.select_one('div > div > dl > dd.btn_play > a > span.songname12')
            if artist_title_span:
                artist_title_song = artist_title_span.get_text()

            artist_id = artist_li.select_one('div > div > dl > dd.wrap_btn > button')['data-artist-no']

            # 단순 정보 출력을 위한 리스트
            print_list = list()
            print_list.append({
                'artist_name': artist_name,
                'artist_country': artist_country,
                'artist_gender': artist_gender,
                'artist_type': artist_type,
                'artist_genre_list': artist_genre_list,
                'artist_title_song': artist_title_song,
                'artist_id': artist_id,
            })
            for print_artist in print_list:
                print(print_artist)

            # 아티스트 객체 만들기 (타이틀 곡은 상세정보와 상이 하여 제외)
            artist = Artist(
                artist_name=artist_name,
                artist_country=artist_country,
                artist_gender=artist_gender,
                artist_type=artist_type,
                artist_genre_list=artist_genre_list,
                artist_id=artist_id,
            )

            artist_list.append(artist)

        print("=" * 200)
        return artist_list


########################################################################################################################
########################################################################################################################


class Song:
    # __init__() 초기화 함수에
    # title, artist, album정보를 받을 수 있도록 함
    def __init__(self, song_id, title, artist, album):
        self.song_id = song_id
        self.title = title
        self.artist = artist
        self.album = album

        self._release_date = None
        self._lyrics = None
        self._genre = None
        self._producers = None

    def __str__(self):
        return f'{self.title} (아티스트: {self.artist}, 앨범: {self.album}, 노래번호: {self.song_id})'

    def get_detail(self, refresh_html=False):
        """
        자신의 _release_data, _lylics, _genre, _producers
        :param refresh_html: 강제 다운로드 여부
        :return:
        """
        os.makedirs(DATA_SONG_DIR, exist_ok=True)

        params = {
            'songId': self.song_id
        }

        source = ''

        file_path = os.path.join(DATA_SONG_DIR, f'song_detail_{self.song_id}.html')
        try:
            file_mode = 'wt' if refresh_html else 'xt'
            with open(file_path, file_mode) as f:
                response = requests.get(f'https://www.melon.com/song/detail.htm', params)
                source = response.text

                # 만약 받은 길이가 지나치게 짧은 경우 예외를 일으키고
                # 예외 블럭에서 기록한 파일을 삭제하도록 함
                file_length = f.write(source)
                if file_length < 10:
                    raise ValueError('파일이 너무 짧습니다.')
        except FileExistsError:
            print(f'"{file_path}" file is already exists!')
            source = open(file_path, 'rt').read()
        except ValueError:
            os.remove(file_path)

        soup = BeautifulSoup(source, 'lxml')

        # 해당 요소의 자식들은 content[index]로 가져 올수 있다.
        # 요소의 다음 요소를 가져 올떄는 next_sibling 이전 요소는 previus_sibling 을 사용한다.
        # get_text(strip=True)로 공백문자들을 없앨 수 있다.
        div_entry = soup.find('div', class_='entry')

        dl = div_entry.find('div', class_='meta').find('dl')
        items = [item.get_text(strip=True) for item in dl.contents if not isinstance(item, str)]
        it = iter(items)
        description_dict = dict(zip(it, it))
        album = description_dict.get('앨범')
        release_date = description_dict.get('발매일')
        genre = description_dict.get('장르')

        title = div_entry.find('div', class_='song_name').strong.next_sibling.strip()
        artist = div_entry.find('div', class_='artist').find('a').find('span').text

        div_lyrics = soup.find('div', id='d_video_summary')
        # lyrics_list = [item.strip() for item in div_lyrics if isinstance(item, NavigableString)]
        # lyrics = '\n'.join(lyrics_list)
        lyrics_list = list()
        for item in div_lyrics.contents:
            if item.name == 'br':
                lyrics_list.append('\n')
            elif type(item) is NavigableString:
                lyrics_list.append(item.strip())

        lyrics = ''.join(lyrics_list)

        producers = dict()

        artist_list_prdcr = soup.find('div', class_='section_prdcr')
        if artist_list_prdcr:
            artist_list = artist_list_prdcr.find_all('li')
            inner_dic = dict()
            for artist in artist_list:
                artist_name = artist.find('div', class_='entry').find('div', class_='artist').find('a').text
                artist_type = artist.find('div', class_='entry').find('div', class_='meta').find('span').text

                # dic 안에 리스트 만들어 리스트안에 dic를 추가

                if artist_type not in inner_dic.keys():
                    name_list = list()
                    name_list.append(artist_name)
                    inner_dic[artist_type] = name_list
                else:
                    inner_dic[artist_type].append(artist_name)

                producers['producers'] = inner_dic

        self.title = title
        self.artist = artist
        self.album = album

        self._release_date = release_date
        self._genre = genre
        self._lyrics = lyrics
        self._producers = producers

    @property
    def lyrics(self):
        if not self._lyrics:
            self.get_detail()
        return self._lyrics

########################################################################################################################
########################################################################################################################


class Artist:

    def __init__(self, **kwargs):
        """
        MelonCrawler의 get_search_artist에서 검색하여 가공 한 정보를 가지고
        Aritst 객체의 생성자에 정보를 전달
        :param kwargs: 아티스트의 기본정보를 가지고 있는 키워드 인자
        """

        # 생성자로 전달 받은 정보들
        self.name = kwargs['artist_name']
        self.country = kwargs['artist_country']
        self.gender = kwargs['artist_gender']
        self.type = kwargs['artist_type']
        self.genre_list = kwargs['artist_genre_list']
        self.artist_id = kwargs['artist_id']

        # 아티스트 검색후 채워 넣을 요약 정보들
        # self.simple_info_dic = dict()
        self.simple_debut_song = None
        self.simple_debut = None
        self.simple_birthday = None
        self.simple_company = None
        self.simple_award_history = None

        # 아티스트 검색후 상세 정보 페이지 정보
        self.detail_award_history = list()
        self.detail_artist_introduce = None
        self.detail_activity_info = dict()
        self.detail_info = dict()

    def get_detail(self, refresh_html=False):
        """
        http://www.melon.com/artist/detail.htm?artistId=261143
        artist_detail_{artist_id}.html
        :param refresh_html: 강제 다운로드 여부
        :return: None 자신의 속성 채우기
        """
        os.makedirs(DATA_ARTIST_DIR, exist_ok=True)

        params = {
            'artistId': self.artist_id
        }

        source = ''

        file_path = os.path.join(DATA_ARTIST_DIR, f'artist_detail_{self.artist_id}.html')
        try:
            file_mode = 'wt' if refresh_html else 'xt'
            with open(file_path, file_mode) as f:
                response = requests.get(f'https://www.melon.com/artist/detail.htm', params)
                source = response.text

                # 만약 받은 길이가 지나치게 짧은 경우 예외를 일으키고
                # 예외 블럭에서 기록한 파일을 삭제하도록 함
                file_length = f.write(source)
                if file_length < 10:
                    raise ValueError('파일이 너무 짧습니다.')
        except FileExistsError:
            print(f'"{file_path}" file is already exists!')
            source = open(file_path, 'rt').read()
        except ValueError:
            os.remove(file_path)

        soup = BeautifulSoup(source, 'lxml')

        # ==================== 간단 정보 ===================== #

        # 아티스트 간단 프로필 div
        artist_simple_div = soup.select_one('#conts > div.wrap_dtl_atist > div > div.wrap_atist_info')
        # 아티스트 본명
        artist_real_name = artist_simple_div.select_one('p > span').get_text()
        self.name += artist_real_name

        # 아티스트 요약 프로필 정보들(데뷔, 데뷔곡, 생일, 활동유형, 소속사, 수상이력,
        artist_info_dl = soup.select_one('#conts > div.wrap_dtl_atist > div > div.wrap_atist_info > dl.atist_info.clfix')

        # 데뷔
        artist_debut = artist_info_dl.select_one('dd > span').get_text()
        # 데뷔 곡
        artist_debut_title = artist_info_dl.select_one('a > span.songname12').get_text()
        # 생일
        artist_birthday = artist_info_dl.select_one('dd:nth-of-type(2)').get_text()
        # 활동 유형
        artist_type = artist_info_dl.select_one('dd:nth-of-type(3)').get_text()
        # 소속사
        artist_company = artist_info_dl.select_one('dd:nth-of-type(4)').get_text()
        # 수상 정보
        artist_award = artist_info_dl.select_one('dd.awarded > span').get_text()
        # print(artist_award)

        self.simple_debut_song = artist_debut_title
        self.simple_debut = artist_debut
        self.simple_birthday = artist_birthday
        self.simple_company = artist_type
        self.simple_award_history = artist_award

        # ==================== 상세 정보 ===================== #

        # 수상 정보들
        artist_detail_award_list = list()
        for award in soup.select('#d_artist_award > dl > dd'):
            artist_detail_award_list.append(award.get_text())

        # 아티스트 소개
        artist_detail_introduce_div = soup.find('div', id='d_artist_intro')
        introduce_list = list()
        for item in artist_detail_introduce_div.contents:
            if item.name == 'br':
                introduce_list.append('\n')
            elif type(item) is NavigableString:
                introduce_list.append(item.strip())

        artist_detail_introduce = ''.join(introduce_list)

        # 아티스트 활동 정보
        artist_active_info_dl = soup.select_one('#conts > div.section_atistinfo03 > dl')
        active_dt_dd_list = list()
        for dt, dd in zip(artist_active_info_dl.find_all('dt'), artist_active_info_dl.find_all('dd')):
            active_dt_dd_list.append(dt.get_text(strip=True))
            active_dt_dd_list.append(dd.get_text(strip=True))

        active_dt_dd_iter = iter(active_dt_dd_list)
        artist_detail_active_info = dict(zip(active_dt_dd_iter, active_dt_dd_iter))

        # 아티스트 신상 정보
        artist_normal_info = soup.select_one('#conts > div.section_atistinfo04 > dl')
        normal_dt_dd_list = list()
        for dt, dd in zip(artist_normal_info.find_all('dt'), artist_normal_info.find_all('dd')):
            normal_dt_dd_list.append(dt.get_text(strip=True))
            normal_dt_dd_list.append(dd.get_text(strip=True))

        normal_dt_dd_iter = iter(normal_dt_dd_list)
        artist_detail_normal_info = dict(zip(normal_dt_dd_iter, normal_dt_dd_iter))

        self.detail_award_history = artist_detail_award_list
        self.detail_artist_introduce = artist_detail_introduce
        self.detail_activity_info = artist_detail_active_info
        self.detail_info = artist_detail_normal_info

    def get_songs(self):
        """
        http://www.melon.com/artist/song.htm?artistId=261143
        :param self: 자기 자신
        :return: Song의 List
        """
        song_list = list()

        params = {
            'artistId': self.artist_id,
        }
        response = requests.get(f'https://www.melon.com/artist/song.htm', params)
        soup = BeautifulSoup(response.text, 'lxml')

        song_tr_list = soup.select('#frm > div > table > tbody > tr')
        for tr in song_tr_list:
            title = tr.select_one('td:nth-of-type(3) > div > div > a.fc_gray').get_text()
            artist = tr.select_one('#artistName > a').get_text()
            album = tr.select_one('td:nth-of-type(5) > div > div > a').get_text()

            song_list.append({
                '곡명': title,
                '아티스트': artist,
                '앨범': album
            })

        return song_list

    def __str__(self):
        return f'\n기본 정보 1\n\t{self.name}\t(국적: {self.country}, 성별: {self.gender}, 활동정보: {self.type}, 장르: {self.genre_list}, 아티스트 번호: {self.artist_id})' \
               f'\n\n기본 정보 2\n\t데뷔: {self.simple_debut}, 데뷔곡: {self.simple_debut_song}, 생일: {self.simple_birthday}, 소속사: {self.simple_company}, 수상이력: {self.simple_award_history}' \
               f'\n\n상세 정보' \
               f'\n\n수상 이력: {self.detail_award_history}' \
               f'\n\n아티스트 소개: {self.detail_artist_introduce}' \
               f'\n\n활동 이력: {self.detail_activity_info}' \
               f'\n\n신상 정보: {self.detail_info}'

        pass


########################################################################################################################

"""
from utils.models import MelonCrawler

if __name__ == '__main__':
    print("=" * 200)
    crawler = MelonCrawler()
    q = input('검색할 곡 명을 입력해주세요: ')
    song_list = crawler.get_song_search(q)
    for song in song_list:
        print(song)
    print("="*200)

    q = input('검색할 아티스트를 입력해주세요: ')
    artist_list = crawler.get_search_artist('아이유')
    artist_list[0].get_detail()
    print(artist_list[0])
    print("=" * 200)

    song_list = artist_list[0].get_songs()
    for index, song in enumerate(song_list):
        print(f"{index} : [곡명: {song['곡명']}], [아티스트: {song['아티스트']}], [앨범: {song['앨범']}]")
    print("=" * 200)

========================================================================================================================================================================================================
검색할 곡 명을 입력해주세요: 가을 아침
가을 아침 (아티스트: 아이유, 앨범: 꽃갈피 둘, 노래번호: 30636089)
가을 아침 (아티스트: 양희은, 앨범: 양희은 1991, 노래번호: 1660728)
가을 아침(MR) (아티스트: Musicsum (뮤직섬), 앨범: 뮤직섬 MR반주 2017 최신인기가요 30, 노래번호: 30670727)
가을 아침 (아티스트: 김서영, 앨범: 하늘이 준 선물, 노래번호: 5824985)
가을 아침(Piano Ver.) (tvN `신혼일기2`) (아티스트: Various Artists, 앨범: 방금 그 곡! TV 예능프로에 자주 나오는 배경음악 (휴식,힐링,명상,뉴에이지), 노래번호: 30694298)
가을 아침(MR 원키) (아티스트: Musicen, 앨범: MR반주 뮤직엔 2017 Vol.43, 노래번호: 30674998)
가을 아침 (아티스트: Various Artists, 앨범: 감성발라드 피아노 콘서트 (최신가요, 인기가요, 휴식, 힐링, 매장음악), 노래번호: 30720056)
가을 아침(MR) (아티스트: 모두의MR, 앨범: 모두의 MR반주 89, 노래번호: 30692252)
가을 아침(Melody 포함 MR) (아티스트: Musicen, 앨범: MR반주 뮤직엔 2017 Vol.43, 노래번호: 30674999)
가을 아침(멜로디MR) (아티스트: Musicsum (뮤직섬), 앨범: 뮤직섬 MR반주 2017 최신인기가요 30, 노래번호: 30670728)
가을 아침 (아티스트: breadBox, 앨범: 요즘 내 마음을 적시는 K-POP 피아노 Vol.2 (휴식,힐링,명상,독서,매장음악), 노래번호: 30679484)
가을아침 (아티스트: 피아노자리표 (PianoClef), 앨범: 힐링 피아노 (Healing Piano), 노래번호: 30675298)
가을 아침(Melody MR) (아티스트: 모두의MR, 앨범: 모두의 MR반주 89, 노래번호: 30692253)
(MR 반주곡) 가을아침 (양희은) (아티스트: Various Artists, 앨범: MR반주곡  3집, 노래번호: 1980736)
가을 아침 (아티스트: 이현섭, 앨범: 가을 아침, 노래번호: 1944384)
가을아침 (아티스트: 얀새 (Yansae), 앨범: 가을아침, 노래번호: 30667612)
가을 아침 (아티스트: Purple Cotton, 앨범: 가을 아침, 노래번호: 30670129)
가을 아침 (아티스트: Various Artists, 앨범: 7080 가을빛 추억, 노래번호: 30692440)
가을 아침 (아티스트: Various Artists, 앨범: 제6회 울산동요사랑회 창작동요발표회 `해바라기`, 노래번호: 1859774)
가을 아침 (아티스트: MuziKart Kids Choir, 앨범: EQ야 놀자 - 우리아이 뇌, 감성 지능 (EQ) 깨우기 프로젝트, 노래번호: 8224000)
가을 아침 (아티스트: PIANOid, 앨범: 이별이 슬픈 이유, 노래번호: 30149380)
가을 아침 (아티스트: MuziKart Kids Choir, 앨범: 동심2 - 아이들이 부른 동화 같은 가요 2nd Edition, 노래번호: 30364201)
가을 아침 (아티스트: 홍지윤, 앨범: 낮에 나온 반달, 노래번호: 4075593)
가을 아침 (아티스트: 약기운, 앨범: 굼벵이, 노래번호: 2538608)
가을아침 (아티스트: PIANOid, 앨범: 가을아침, 노래번호: 30107398)
가을 향기의 아침 (아티스트: Various Artists, 앨범: 명상 뉴에이지 피아노와 함께하는 마음 비우기, 노래번호: 7847622)
가을, 조용한 아침 (아티스트: 피아노 태교, 앨범: 가을, 조용한 아침, 노래번호: 30052756)
Agnew : An Autumn Morning (애그뉴 : 어느가을 아침) (아티스트: Tamara Anna Cislowska, 앨범: Modernist Classics, 노래번호: 30455978)
가을 향기의 아침 (아티스트: 하늘정원, 앨범: 수험생에게 힐링을 주는 감성 피아노, 노래번호: 6736814)
늦은 가을아침 바다 (아티스트: 김영현, 앨범: 지금의 내생각처럼, 노래번호: 8112754)
가을 아침의 공기 (아티스트: 이선율, 앨범: 가을 아침의 공기, 노래번호: 30650664)
가을의 아침 (Morning In Fall) (아티스트: Sunset Glow, 앨범: 가을의 아침 (Morning In Fall), 노래번호: 30716464)
가을 아침에 널 보면 (아티스트: the newage, 앨범: 가을 아침에 널 보면, 노래번호: 30666041)
아침의 가을 하늘 (아티스트: 피아노 슈가, 앨범: 풍경이 아름다운 계절 가을의 정취를 담은 피아노 모음집, 노래번호: 30061145)
아침의 가을 하늘 (아티스트: 피아노 슈가, 앨범: 지친 마음에 여유로운 휴식을 선물하는 뉴에이지 피아노, 노래번호: 30084812)
아침의 가을 하늘 (아티스트: 피아노 슈가, 앨범: 태교를 위한 부드러운 피아노 모음집, 노래번호: 30082241)
아침의 가을 하늘 (아티스트: 피아노 슈가, 앨범: 달콤한 숙면으로 인도하는 편안한 뉴에이지 피아노, 노래번호: 30035119)
늦은가을 아침바다 (아티스트: 김영현, 앨범: 1994 Kim Young Hyun The End But Never End, 노래번호: 58544)
========================================================================================================================================================================================================
검색할 아티스트를 입력해주세요: 아이유
{'artist_name': '아이유', 'artist_country': '대한민국', 'artist_gender': '여성', 'artist_type': '솔로', 'artist_genre_list': ['Ballad', 'Dance', 'Drama'], 'artist_title_song': '잠 못 드는 밤 비는 내리고', 'artist_id': '261143'}
{'artist_name': 'IUV', 'artist_country': '대한민국', 'artist_gender': '여성', 'artist_type': '그룹', 'artist_genre_list': ['Dance', 'Rap / Hip-hop'], 'artist_title_song': '여기 와썹', 'artist_id': '560205'}
{'artist_name': '이유 갓지(GOD G) 않은 이유 (박명수, 아이유)', 'artist_country': '대한민국', 'artist_gender': '혼성', 'artist_type': '그룹', 'artist_genre_list': ['Dance'], 'artist_title_song': '레옹', 'artist_id': '889388'}
{'artist_name': '박명수', 'artist_country': '대한민국', 'artist_gender': '남성', 'artist_type': '솔로', 'artist_genre_list': ['Dance', 'Ballad', 'Electronica'], 'artist_title_song': 'Saxophone Magic (Feat. 유재환, 초희)', 'artist_id': '4263'}
{'artist_name': 'The Aiu', 'artist_country': '일본', 'artist_gender': '혼성', 'artist_type': '그룹', 'artist_genre_list': ['Rock'], 'artist_title_song': 'Loser', 'artist_id': '567934'}
{'artist_name': '로엔트리', 'artist_country': '대한민국', 'artist_gender': '혼성', 'artist_type': '그룹', 'artist_genre_list': [], 'artist_title_song': '', 'artist_id': '686375'}
{'artist_name': '아이유악대', 'artist_country': '중국', 'artist_gender': '남성', 'artist_type': '솔로', 'artist_genre_list': ['Rock'], 'artist_title_song': None, 'artist_id': '167076'}
========================================================================================================================================================================================================
"/home/sumin/projects/crawler/data/artist/artist_detail_261143.html" file is already exists!

기본 정보 1
	아이유 (이지은)	(국적: 대한민국, 성별: 여성, 활동정보: 솔로, 장르: ['Ballad', 'Dance', 'Drama'], 아티스트 번호: 261143)

기본 정보 2
	데뷔: 2008.09.18, 데뷔곡: 미아, 생일: 1993.05.16, 소속사: 솔로, 수상이력: 2017 하이원 서울가요대상|최고 앨범상

상세 정보

수상 이력: ['2017 하이원 서울가요대상|최고 앨범상', '2017 골든디스크 어워즈|음원 본상', '2017 골든디스크 어워즈|음원 대상', '2017 MelOn Music Awards|올해의 앨범', '2017 MelOn Music Awards|송 라이터상', '2017 MelOn Music Awards|TOP 10', '2017 Mnet Asian Music Awards|여자 가수상', '제13회 한국대중음악상|네티즌이 뽑은 올해의 음악인 (여자)', '2015 대한민국 대중문화예술상|국무총리 표창', '2014 Mnet Asian Music Awards|The Most Popular Vocalist', '2014 Mnet Asian Music Awards|여자 가수상', '2014 MelOn Music Awards|올해의 가수상', '2014 MelOn Music Awards|TOP10', '제3회 가온 차트 K-POP 어워드|올해의 가수상 음원 (10월)', '2013 MelOn Music Awards|TOP10', '2012 MelOn Music Awards|TOP10', '2012 Mnet Asian Music Awards|여자 가수상', '2012 한국PD대상|출연자상 가수 부문', '제1회 가온 차트 K-POP 어워드|올해의 가수상 음원 (12월)', '제1회 가온 차트 K-POP 어워드|올해의 가수상 음원 (2월)', '2012 아시아모델상시상식|BBF 인기 가수상', '제9회 한국대중음악상|올해의 노래', '제9회 한국대중음악상|네티즌이 뽑은 올해의 음악인 (여자 아티스트)', '제9회 한국대중음악상|최우수 팝 (노래부문)', '2011 Mnet Asian Music Awards|베스트 보컬 퍼포먼스 솔로', '2011 MelOn Music Awards|TOP10', '2011 MelOn Music Awards|SK플래닛 베스트송상', '2011 스타일 아이콘 어워즈|Style Icon상', '2011 하이원 서울가요대상|본상', '2011 하이원 서울가요대상|최고앨범상', '2010 MelOn Music Awards|TOP10', '2010 대한민국 연예예술상|신세대 가수상', '2010 하이원 서울가요대상|본상', '2010 하이원 서울가요대상|디지털음원상', '2010 골든디스크 어워즈|디지털음원 본상']

아티스트 소개: 21세기에 아이돌 가수의 기준과 성향을 분해 시키면서 큰 성공을 거둔 아이유(IU, 본명: 이지은)은 1993년5월16일생으로 20세가 되기 전에 가요계에서 빼놓을 수 없는 아이돌 가수로 빠른 시간 내에 성장했다. 귀여운 외모는 물론이고 누구에게도 뒤지지 않는 시원한 가창력과 무대 매너를 지닌 그녀는 흔히 기계적으로 육성된 범용 아이돌이 아닌 대중 음악사에서 하나의 기준점을 찍고 들어간 뉴-타입으로 각인된다.

자신을 뜻하는 'I'와 당신을 뜻하는 'You'를 합쳐서 만든 합성어로 '너와 내가 음악으로 하나가 된다'는 의미의 아이유가 첫 번째 앨범을 발표한 것은 2008년9월(당시15세)이었다. 6곡이 수록된 미니 앨범으로 타이틀은 [Lost And Found]였으며, "미아"와 "미운오리"가 청자들에게 어느 정도 각인을 시켜 주기에 충분 했었으며, 윤상을 비롯한 유희열, 휘성 같은 삼촌 선배 가수들에게까지 인정을 받는다. 그러나 이 데뷔 앨범은 발매 당시 아이유 입장에서는 자신의 디스코그래피에서 첫 칸을 채워놓았다는 것과 음악적인 취향이 적극적으로 반영되었다는 부분만으로 만족해야만 했을 정도로 상업적으로는 그리 큰 성과를 이뤄내진 못했다.

기대한 것보다 큰 효과를 거두지 못했던 2008년에 비해 2009년은 도약의 시기로 평가된다. 이전에 발표한 미니 앨범의 트랙을 포함 시킨 정규 풀 앨범 [Growing Up]을 통해 기존에 있던 정적인 느낌보다는 좀더 앳되고 귀여운 타입의 컨셉으로 활동을 시작한다. 음악 적인 부분에서도 어쿠스틱 사운드와 록 비트를 약간 섞어 낸 전작의 곡들에 비해서 이 앨범의 타이틀인 "Boo" 같은 소프트한 댄스 곡이나 Rock 버전을 따로 만들어 낼 정도로 발매 이전부터 기대를 건 "있잖아" 처럼 업템포 형식의 발랄한 곡들 위주로 앨범을 만들게 되었으며, 소수의 팬들의 만들어 내기도 했으나, 애초 기대한 만큼의 성공은 거두지 못한다. (후에 이 앨범들은 아이유가 자신의 신드롬을 찰지게 만들어낸 2010년에 다시 재평가를 받기 시작한다.)

그러나 2009년은 아이유의 활동 자체에 많은 노력과 투자가 꽤 활발하게 이어졌다고 보여진다. 만화가 이현세의 절대 히트작인 만화 외인구단의TV 드라마 물인 '2009 외인구단'에 발라드 "그러는 그대는"과 MBC드라마 '선덕여왕'에 "아라로"를 수록하면서 분위기를 올리고 연말 이전인 11월에는 두 번째 미니 앨범이자 EP [IU...IM]까지 발표한다. 이 앨범에서 아이유는 초기 활동의 히트작으로 확실히 명명되는 "마쉬멜로우"가 들어있었다. 경쾌한 댄스 팝의 이 곡은 귀여운 외모를 적절히 부각 시키는 뮤직 비디오와 각종 가요 프로그램에서 보여준 퍼포먼스가 전국의 오빠, 삼촌들의 심장을 겨냥하게 만든다.

"마쉬멜로우"의 전혀 아쉽지 않은 성공 이후 2010년은 순탄하고 탄탄한 활동과 지원이 기다리고 있음은 두 말할 필요가 없었다. 새로운 천 년의10년째를 맞이해서 [텔레시네마 프로젝트Vol.6]에 수록한 싱글 곡 "다섯째 손가락"은 그녀가 귀여운 감성의 발라드에서 탁월한 능력을 발휘한다는 것을 증명했고, 업템포 형식의 발라드 곡인 "잔소리"는 2AM의 슬옹과 함께해서 아이유 특유의 그 귀여운 마력을 더욱 증가 시키게 된다. 이후 MBC 드라마 '로드 넘버원'에 "여자라서", 유승호와 호흡을 맞춘 "사랑을 믿어요", 가요계 선배이지만 연배로는 삼촌뻘인 성시경이 군대에서 사회로 복귀한 사회 초년생으로 함께한 "그대네요" 까지 팬들의 절찬과 만족할 만한 호응을 끌어낸다.

여기에 연말인 12월에 드디어 아이유 자신 뿐만 아니라 팬들에게까지 그녀의 가수 인생 중 가장 뜻 깊게 한 획을 그어냈다고 영원히 평가 받고 회자 될 EP [Real]을 발표한다. 모든 곡들이 초유의 관심의 대상이었지만, 역시 가장 크게 확대되고 수많은 팬들을 추가 생산시킨 곡은 "좋은날"이었다. 워낙에 상큼하고 발랄한 곡이기도 했거니와 곡 중 후반의 뛰어난 고음 처리 방식을 일본 애니메이션의 주인공 철완소년 아톰이 하늘을 3단으로 가속하며 나르는 장면을 가지고 팬들이 만든 여러 가지 패러디 영상물들이 봇물을 이루면서 그녀의 인기와 주가는 최고의 수직 상승 곡선을 이루게 된다. 거기에 당시 나이는18세. 대중 음악계뿐만 아니라 연예계 전체에서 미래에 대해서 아이유에게 거는 기대감 자체는 '대세아이유'라는 말로 대변 할 정도로 하나의 신드롬을 완벽하게 형성했었다.

이 신드롬은 2011년 연예계 최고 핫 이슈의 드라마 '드림하이'에서도 이루어진다. 배용준과 박진영의 프로젝트였던 이 드라마에 아이유는 가요계를 이끄는 대거의 아이돌 가수들과 함께 출연 함으로 부실한 각본에 비해서 나름 큰 성공을 거두기도 하는데, 재미있는 점은 과거에 아이유가 박진영의 기획사인 JYP엔터테인먼트의 오디션에서 낙방을 하였다는 점이 여러 버라이어티 프로그램에서 이 드라마가 방영될 시에 공개되어 이미 성공을 거둔 인재를 놓친 안타까움을 박진영이 여러 곳에서 종종 드러냈다는 것과 당시 회사의 오디션 진행자가 후에 사직 위기까지 갔다는 농담 섞인 에피소드도 포함되어 있었다. 거기에 아이유는 이 드라마에서 초보 연기자 치고는 충분한 합격 점을 얻을 수 있었으며, 드라마에 삽입된 알앤비 타입의 발라드 "Someday"도 팬들의 끊임없는 관심과 호응을 이끌어냈다.

이후 전작이었던 [Real]의 큰 성공에 힙입어 2011년2월에 이어진 싱글 추가곡 형태로 나타낸 [Real+]에는 "나만 몰랐던 이야기"와 "잔혹동화"를 수록하면서 그녀의 음악적인 역량에 대한 기대치와 찬사는 연일 최고의 기록을 이뤄낸다. 이어진 활동으로는 5월경에 발표한 드라마 '최고의 사랑'에 삽입했던 싱글 "내 손을 잡아"를 발표하고, 피겨의 여왕 김연아와 함께하고 대한민국 록계의 프리미엄 기타리스트 김세황이 세션을 맡은 싱글 "얼음꽃"을 한달 뒤에 내 놓는다. 당시 아이유는 김연아의 인기를 동반했던 피겨 스케이팅 종목을 도입한 서바이벌 프로그램 'Kiss&Cry'에 김연아를 위시한 다른 예능인들과 출연 중이었는데, 그녀의 바쁜 스케줄 덕분이었는지 연습 부족으로 싱글 발표 한달 뒤인 7월 말경에 탈락하게 된다. 그러나 팬들은 오히려 당시의 탈락 상황을 반갑게 여길 정도로 그녀의 안정적인 휴지기를 바라며, 새롭게 다가올 음악 활동 자체 만을 더욱 크게 고대하고 있을 정도였다.

그런 기다림 속에서 피어난 정규 두 번째 풀 앨범 [Last Fantasy]는 2011년11월29일에 발표되어 유난히 일찍 찾아온 한파를 이겨낼 뜨거운 컨텐츠로 매우 빠르게 자리 잡힐 정도였으며, 윤상, 김광진, 이적, 김현철, Ra.D 등 가요계 삼촌들이 대거로 피처링으로 참여하면서 아이유에 대한 지원을 한 톨도 아끼지 않은 호화 앨범으로 실제 이적과는 "삼촌" 이라는 타이틀의 그루브 한 사운드의 곡을 발표해서 대한민국의 삼촌들에게 많은 사랑을 받으며, "좋은날"의 후속 격인 느낌의 "너랑 나"와 "사랑니", "비밀" 등이 팬들의 적극적인 사랑과 지원을 받았다. 거기에 이 앨범에서부터 아이유는 자신의 직접 작사, 작곡 능력을 발휘하기 시작했는데, 그 능력치가 바로 그녀의 인기만큼 부각 된 것은 아니지만, 약관 20세를 목전에 두고 있는 그녀의 미래에 대해서는 매우 긍정적인 반응을 이끌어 냈다.

그런 긍정적인 분위기에 이어진 2012년5월에 발표한 [스무 살의 봄]은 제목 그대로 정확히 20대에 접어든 그녀가 자신의 음악 자체를 자신이 완벽히 직접 만들고 부르는 싱어송라이터로서 곡을 발표했는데, 평소 좋아하던 Corinne Bailey Rae의 느낌이 묻어나는 "복숭아"였다. 거기에 "좋은날"의 성공 이후 아이유 신곡 중에서는 빠지지 않으며 하나의 정형성을 띄기 시작한 타입의 소프트 댄스 트랙인 "하루 끝"도 수록되어 정규 앨범을 기다리는 욕심 있는 팬들을 위로 하기도 했었다. 이런 욕심 많은 대중과 팬들에게 다시 한번 크게 어필한 것은 2012년6월 초에 거행된 첫 단독 콘서트인데 자그마한 체구에 비해 넘치는 에너지로 때로는 관객들을 압도하는 옹골진 모습과 사랑할 수 밖에 없는 귀여운 퍼포먼스로 수 많은 즐거움을 선사했던 공연으로 알려졌다. 이렇게 단순히 노래를 하는 가수로서의 성공뿐만 아니라 확실한 라이브 무대를 치러내는 경험과 능력의 적립. 거기에 곡을 만들고 그 곡으로 자신을 표현하는 뮤지션으로 도약하는 미래의 수순을 착실히 밟아 가고 있는 아이유에게 팬들과 가요계는 여전히 실망을 할 겨를이 없어 보인다.

활동 이력: {'데뷔': '2008.09.18', '활동년대': '2000, 2010 년대', '유형': '솔로|여성', '장르': 'Ballad, Dance, Drama, Electronica, Folk, Korean Movie, R&B / Soul, Rock, 기타', '소속사명': '(주)로엔엔터테인먼트', '소속그룹': '이유 갓지(GOD G) 않은 이유 (박명수, 아이유)'}

신상 정보: {'본명': '이지은', '별명': '산신령,은지은,짝지', '국적': '대한민국', '생일': '1993.05.16', '별자리': '황소자리', '혈액형': 'A형'}
========================================================================================================================================================================================================
0 : [곡명: 가을 아침], [아티스트: 아이유], [앨범: 꽃갈피 둘]
1 : [곡명: 비밀의 화원], [아티스트: 아이유], [앨범: 꽃갈피 둘]
2 : [곡명: 잠 못 드는 밤 비는 내리고], [아티스트: 아이유], [앨범: 꽃갈피 둘]
3 : [곡명: 어젯밤 이야기], [아티스트: 아이유], [앨범: 꽃갈피 둘]
4 : [곡명: 개여울], [아티스트: 아이유], [앨범: 꽃갈피 둘]
5 : [곡명: 매일 그대와], [아티스트: 아이유], [앨범: 꽃갈피 둘]
6 : [곡명: 이 지금], [아티스트: 아이유], [앨범: Palette]
7 : [곡명: 팔레트 (Feat. G-DRAGON)], [아티스트: 아이유], [앨범: Palette]
8 : [곡명: 이런 엔딩], [아티스트: 아이유], [앨범: Palette]
9 : [곡명: 잼잼], [아티스트: 아이유], [앨범: Palette]
10 : [곡명: Black Out], [아티스트: 아이유], [앨범: Palette]
11 : [곡명: 마침표], [아티스트: 아이유], [앨범: Palette]
12 : [곡명: 그렇게 사랑은], [아티스트: 아이유], [앨범: Palette]
13 : [곡명: 이름에게], [아티스트: 아이유], [앨범: Palette]
14 : [곡명: 사랑이 잘 (With 오혁)], [아티스트: 아이유], [앨범: 사랑이 잘]
15 : [곡명: 밤편지], [아티스트: 아이유], [앨범: 밤편지]
16 : [곡명: 새 신발], [아티스트: 아이유], [앨범: CHAT-SHIRE]
17 : [곡명: Zeze], [아티스트: 아이유], [앨범: CHAT-SHIRE]
18 : [곡명: 스물셋], [아티스트: 아이유], [앨범: CHAT-SHIRE]
19 : [곡명: 푸르던], [아티스트: 아이유], [앨범: CHAT-SHIRE]
20 : [곡명: Red Queen (Feat. Zion.T)], [아티스트: 아이유], [앨범: CHAT-SHIRE]
21 : [곡명: 무릎], [아티스트: 아이유], [앨범: CHAT-SHIRE]
22 : [곡명: 안경], [아티스트: 아이유], [앨범: CHAT-SHIRE]
23 : [곡명: 마음], [아티스트: 아이유], [앨범: 마음]
24 : [곡명: 소격동], [아티스트: 아이유], [앨범: 소격동]
25 : [곡명: 애타는 마음], [아티스트: 울랄라세션], [앨범: 애타는 마음]
26 : [곡명: 애타는 마음 (Inst.)], [아티스트: 울랄라세션], [앨범: 애타는 마음]
27 : [곡명: 나의 옛날이야기], [아티스트: 아이유], [앨범: 꽃갈피]
28 : [곡명: 꽃], [아티스트: 아이유], [앨범: 꽃갈피]
29 : [곡명: 삐에로는 우릴 보고 웃지], [아티스트: 아이유], [앨범: 꽃갈피]
30 : [곡명: 사랑이 지나가면], [아티스트: 아이유], [앨범: 꽃갈피]
31 : [곡명: 너의 의미 (Feat. 김창완)], [아티스트: 아이유], [앨범: 꽃갈피]
32 : [곡명: 여름밤의 꿈], [아티스트: 아이유], [앨범: 꽃갈피]
33 : [곡명: 꿍따리 샤바라 (Feat. 클론)], [아티스트: 아이유], [앨범: 꽃갈피]
34 : [곡명: 봄 사랑 벚꽃 말고], [아티스트: HIGH4 (하이포)], [앨범: 봄 사랑 벚꽃 말고]
35 : [곡명: 봄 사랑 벚꽃 말고 (Inst.)], [아티스트: HIGH4 (하이포)], [앨범: 봄 사랑 벚꽃 말고]
36 : [곡명: 금요일에 만나요 (Feat. 장이정 Of HISTORY)], [아티스트: 아이유], [앨범: Modern Times - Epilogue]
37 : [곡명: 크레파스 (드라마 `예쁜 남자` 삽입곡)], [아티스트: 아이유], [앨범: Modern Times - Epilogue]
38 : [곡명: 을의 연애 (With 박주원)], [아티스트: 아이유], [앨범: Modern Times - Epilogue]
39 : [곡명: 누구나 비밀은 있다 (Feat. 가인 Of Brown Eyed Girls)], [아티스트: 아이유], [앨범: Modern Times - Epilogue]
40 : [곡명: 입술 사이 (50cm)], [아티스트: 아이유], [앨범: Modern Times - Epilogue]
41 : [곡명: 분홍신], [아티스트: 아이유], [앨범: Modern Times - Epilogue]
42 : [곡명: Modern Times], [아티스트: 아이유], [앨범: Modern Times - Epilogue]
43 : [곡명: 싫은 날], [아티스트: 아이유], [앨범: Modern Times - Epilogue]
44 : [곡명: Obliviate], [아티스트: 아이유], [앨범: Modern Times - Epilogue]
45 : [곡명: 아이야 나랑 걷자 (Feat. 최백호)], [아티스트: 아이유], [앨범: Modern Times - Epilogue]
46 : [곡명: Havana], [아티스트: 아이유], [앨범: Modern Times - Epilogue]
47 : [곡명: 우울시계 (Feat. 종현 Of SHINee)], [아티스트: 아이유], [앨범: Modern Times - Epilogue]
48 : [곡명: 한낮의 꿈 (Feat. 양희은)], [아티스트: 아이유], [앨범: Modern Times - Epilogue]
49 : [곡명: 기다려], [아티스트: 아이유], [앨범: Modern Times - Epilogue]
========================================================================================================================================================================================================
"""