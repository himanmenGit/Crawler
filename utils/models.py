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
            song_id = tr.select_one('td:nth-of-type(1) input[type=checkbox]').get('value')
            title = tr.select_one('td:nth-of-type(3) a.fc_gray').get_text(strip=True)

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
            # for print_artist in print_list:
            #     print(print_artist)

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
        self.simple_title_song = None
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

        artist_detail_intoruduce = ''.join(introduce_list)

        # 아티스트 활동 정보
        artist_active_info_dl = soup.select_one('#conts > div.section_atistinfo03 > dl')
        active_dt_dd_list = list()
        for dt, dd in zip(artist_active_info_dl.find_all('dt'), artist_active_info_dl.find_all('dd')):
            active_dt_dd_list.append(dt.get_text(strip=True))
            active_dt_dd_list.append(dd.get_text(strip=True))

        active_dt_dd_iter = iter(active_dt_dd_list)
        artist_detail_active_info = dict(zip(active_dt_dd_iter, active_dt_dd_iter))
        # print(artist_detail_active_info)

        # 아티스트 신상 정보
        artist_normal_info = soup.select_one('#conts > div.section_atistinfo04 > dl')
        nromal_dt_dd_list = list()
        for dt, dd in zip(artist_normal_info.find_all('dt'), artist_normal_info.find_all('dd')):
            nromal_dt_dd_list.append(dt.get_text(strip=True))
            nromal_dt_dd_list.append(dd.get_text(strip=True))

        normal_dt_dd_iter = iter(nromal_dt_dd_list)
        artist_detail_normal_info = dict(zip(normal_dt_dd_iter, normal_dt_dd_iter))
        # print(artist_detail_normal_info)

    def get_songs(self):
        """
        http://www.melon.com/artist/song.htm?artistId=261143
        :param self: 자기 자신
        :return: Song의 List
        """
        pass

########################################################################################################################
