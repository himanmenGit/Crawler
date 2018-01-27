# from utils import *
#
# if __name__ == '__main__':
#     # result = get_top100_list()
#     # get_song_detail(result)
#     result = get_song_search('빨간맛')
#
#     for item in result:
#         print(item)

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


# ==================================================================================================================== #