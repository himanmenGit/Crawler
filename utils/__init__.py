# import requests
# import re
# from bs4 import BeautifulSoup
# import os.path
#
# from bs4 import NavigableString
#
# __all__ = (
#     'get_top100_list',
#     'get_song_detail',
#     'get_song_search'
# )
#
# # 프로젝트 컨테이너 폴더 경로
# PATH_MODULE = os.path.abspath(__file__)
#
# ROOT_DIR = os.path.dirname(PATH_MODULE)
#
# # data/폴더 경로
# DATA_DIR = os.path.join(ROOT_DIR, 'data')
# DATA_SONG_DIR = os.path.join(DATA_DIR, 'song')
#
#
# def get_top100_list(refresh_html=False):
#     """
#     실시간 차트 1~100위의 리스트 반환
#     :파일위치:
#         현재 파일(모듈)의 위치를 사용한 상위 디렉토리 경로(crawler디렉토리):
#             os.path.dirname(os.path.abspath(__name__))
#         os.path.join()
#         data/chart_realtile_100.html
#     :param refresh_html: True일 경우, 무조건 새 HTML을 받아와 저장
#     :return: 100위 까지의 dict list를 반환
#     """
#
#     # 만약에 path_data_dir에 해당하는 폴더가 없을 경우 생성해 준다.
#     # 실행시 crawler/data폴더가 생성되어야 함.
#     os.makedirs(DATA_DIR, exist_ok=True)
#
#     # 1-100위 주소
#     url_chart_realtime = 'https://www.melon.com/chart/index.htm'
#
#     # 1~100위에 해당하는 웹페이지 HTML을
#     # data/chart_realtime_html에 저장
#     source = ''
#
#     file_path = os.path.join(DATA_DIR, 'chart_realtime.html')
#     try:
#         file_mode = 'wt' if refresh_html else 'xt'
#         with open(file_path, file_mode) as f:
#             response = requests.get(url_chart_realtime)
#             source = response.text
#             f.write(source)
#     except FileExistsError:
#         print(f'"{file_path}" file is already exists!')
#         source = open('melon.html', 'rt').read()
#
#     soup = BeautifulSoup(source, 'lxml')
#
#     result = list()
#
#     for tr in soup.find_all('tr', class_=['lst50', 'lst100']):
#         rank = tr.find('span', class_='rank').text
#         title = tr.find('div', class_='rank01').find('a').text
#         artist = tr.find('div', class_='rank02').find('a').text
#         album = tr.find('div', class_='rank03').find('a').text
#         url_img_cover = tr.find('a', class_='image_typeAll').find('img').get('src')
#         # .* -> 임의 문자의 최대 반복
#         # \. -> '.' 문자
#         # .*?. -> '/'이 나오기 전까지의 최소 반복
#         p = re.compile(r'(.*\..*?)/')
#         url_img_cover = re.search(p, url_img_cover).group(1)
#         song_id = tr.find(attrs={'data-song-no': True})['data-song-no']
#
#         # 정규 표현식
#         # song_id_href = tr.find('a', class_='song_info').get('href')
#         # song_id = re.search(r"\('(\d+)'\)", href).group(1)
#
#         result.append({
#             'rank': rank,
#             'title': title,
#             'url_img_cover': url_img_cover,
#             'artist': artist,
#             'album': album,
#             'song_id': song_id
#         })
#     return result
#
#
# # def get_song_detail(song_list, refresh_html=False):
# #     """
# #     song_id에 해당하는 곡 정보 dict를 반환
# #     위의 get_top100_list의 각 곡 정보에도 song_id가 들어가도록 추가
# #
# #     http://www.melon.com/song/detail.htm?songId=30851703
# #     위 링크를 참조
# #
# #     파일명
# #         song_detail_{song_id}.html
# #
# #     :param song_list: 곡 정보 list
# #     :param refresh_html: 이미 다운받은 HTML데이터가 있을 때 기존 데이터를 덮어씌울지 여
# #     :return:
# #     """
# #     os.makedirs(DATA_SONG_DIR, exist_ok=True)
# #
# #     result = list()
# #
# #     for song in song_list:
# #         song_id = song['song_id']
# #
# #         base_url = f'https://www.melon.com/song/detail.htm'
# #         params = {
# #             'songId': song_id
# #         }
# #
# #         filename = 'song_detail_'+song_id+'.html'
# #         file_path = os.path.join(DATA_SONG_DIR, filename)
# #         try:
# #             file_mode = 'wt' if refresh_html else 'xt'
# #             with open(file_path, file_mode) as f:
# #                 response = requests.get(base_url, params)
# #                 source = response.text
# #
# #                 # 만약 받은 길이가 지나치게 짧은 경우 예외를 일으키고
# #                 # 예외 블럭에서 기록한 파일을 삭제하도록 함
# #                 file_length = f.write(source)
# #                 if file_length < 10:
# #                     raise ValueError('파일이 너무 짧습니다.')
# #         except FileExistsError:
# #             print(f'"{file_path}" file is already exists!')
# #             source = open(file_path, 'rt').read()
# #         except ValueError:
# #             os.remove(file_path)
# #             continue
# #
# #         soup = BeautifulSoup(source, 'lxml')
# #
# #         dic_song_info = dict()
# #
# #         # 해당 요소의 자식들은 content[index]로 가져 올수 있다.
# #         # 요소의 다음 요소를 가져 올떄는 next_sibling 이전 요소는 previus_sibling 을 사용한다.
# #         # get_text(strip=True)로 공백문자들을 없앨 수 있다.
# #         div_entry = soup.find('div', class_='entry')
# #
# #         dl = div_entry.find('div', class_='meta').find('dl')
# #         items = [item.get_text(strip=True) for item in dl.contents if not isinstance(item, str)]
# #         it = iter(items)
# #         description_dict = dict(zip(it, it))
# #
# #         album = description_dict.get('앨범')
# #         release_date = description_dict.get('발매일')
# #         genre = description_dict.get('장르')
# #
# #         dic_song_info['album'] = album
# #         dic_song_info['release_date'] = release_date
# #         dic_song_info['genre'] = genre
# #
# #         title = div_entry.find('div', class_='song_name').strong.next_sibling.strip()
# #         artist = div_entry.find('div', class_='artist').find('a').find('span').text
# #
# #         div_lyrics = soup.find('div', id='d_video_summary')
# #         # lyrics_list = [item.strip() for item in div_lyrics if isinstance(item, NavigableString)]
# #         # lyrics = '\n'.join(lyrics_list)
# #         lyrics_list = list()
# #         for item in div_lyrics.contents:
# #             if item.name == 'br':
# #                 lyrics_list.append('\n')
# #             elif type(item) is NavigableString:
# #                 lyrics_list.append(item.strip())
# #
# #         lyrics = ''.join(lyrics_list)
# #
# #         dic_song_info['title'] = title
# #         dic_song_info['artist'] = artist
# #         dic_song_info['lyrics'] = lyrics
# #         dic_song_info['song_id'] = song_id
# #
# #         artist_list_prdcr = soup.find('div', class_='section_prdcr')
# #         if artist_list_prdcr:
# #             artist_list = artist_list_prdcr.find_all('li')
# #             inner_dic = dict()
# #             for artist in artist_list:
# #                 artist_name = artist.find('div', class_='entry').find('div', class_='artist').find('a').text
# #                 artist_type = artist.find('div', class_='entry').find('div', class_='meta').find('span').text
# #
# #                 # dic 안에 리스트 만들어 리스트안에 dic를 추가
# #
# #                 if artist_type not in inner_dic.keys():
# #                     name_list = list()
# #                     name_list.append(artist_name)
# #                     inner_dic[artist_type] = name_list
# #                 else:
# #                     inner_dic[artist_type].append(artist_name)
# #
# #                 dic_song_info['producers'] = inner_dic
# #
# #         result.append(dic_song_info)
#
#
# def get_song_search(song_title):
#     """
#         곡 명으로 멜론에서 검색한 결과 리스트를 리턴
#         :param song_title: 검색할 곡 명
#         :return: 결과 dict리스트
#     """
#     """
#     1. http://www.melon.com/search/song/index.htm
#         에 q={title}, section=song으로 parameter를 준 URL에
#         requests를 사용해 요청
#     2. response.text를 사용해 BeautifulSoup인스턴스 soup생성
#     3. soup에서 적절히 결과를 가공
#     4. 결과 1개당 dict한개씩 구성
#     5. 전부 리스트에 넣어 반환
#     6. 완☆성
#     """
#
#     base_url = f'https://www.melon.com/search/song/index.htm'
#     params = {
#         'q': song_title,
#         'section': 'song',
#     }
#     response = requests.get(base_url, params)
#     soup = BeautifulSoup(response.text, 'lxml')
#
#     result = list()
#
#     tr_list = soup.select('form#frm_defaultList > div > table > tbody > tr')
#     for tr in tr_list:
#         title = tr.select_one('td:nth-of-type(3) a.fc_gray').get_text(strip=True)
#
#         artist = tr.select_one('td:nth-of-type(4) span.checkEllipsisSongdefaultList').get_text(strip=True)
#         album = tr.select_one('td:nth-of-type(5) a').get_text(strip=True)
#
#         result.append({
#             'title': title,
#             'artist': artist,
#             'album': album,
#         })
#     return result
