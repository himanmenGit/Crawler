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
    crawler = MelonCrawler()
    q = input('검색할 곡 명을 입력해주세요: ')
    song_list = crawler.get_song_search(q)
    # for song in song_list:
    #     print(song_list)
    song_list[0].get_detail()
    print(song_list[0].lyrics)