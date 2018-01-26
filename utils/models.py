import os

import requests
from bs4 import NavigableString, BeautifulSoup

########################################################################################################################

# 프로젝트 컨테이너 폴더 경로
PATH_MODULE = os.path.abspath(__file__)

ROOT_DIR = os.path.dirname(os.path.dirname(PATH_MODULE))

# data/폴더 경로
DATA_DIR = os.path.join(ROOT_DIR, 'data')
DATA_SONG_DIR = os.path.join(DATA_DIR, 'song')

print(PATH_MODULE)
print(ROOT_DIR)
print(DATA_DIR)
print(DATA_SONG_DIR)

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


