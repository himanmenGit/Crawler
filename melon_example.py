import re

source = '''<tr class="lst50" id="lst50" data-song-no="30853153">
                <td><div class="wrap t_right"><input type="checkbox" title="빛이 나 (Shinin`) 곡 선택" class="input_check " name="input_check" value="30853153"></div></td>
                <td><div class="wrap t_center"><span class="rank ">3</span><span class="none">위</span></div></td>
                    <!-- 차트순위 추가 -->
                    <td><div class="wrap">
                            <span title="1단계 상승" class="rank_wrap">
                                <span class="bullet_icons rank_up"><span class="none">단계 상승</span></span>
                                <span class="up">1</span>
                                </span>
                    </div></td>
                <td><div class="wrap">
                    <a href="javascript:melon.link.goAlbumDetail('10131646');" title="Poet｜Artist" class="image_typeAll">
                        <img onerror="WEBPOCIMG.defaultAlbumImg(this);" width="60" height="60" src="http://cdnimg.melon.co.kr/cm/album/images/101/31/646/10131646_500.jpg/melon/resize/120/quality/80/optimize" alt="Poet｜Artist - 페이지 이동">
                        <span class="bg_album_frame"></span>
                    </a>
                </div></td>
                <td><div class="wrap">
                    <a href="javascript:melon.link.goSongDetail('30853153');" title="빛이 나 (Shinin`) 곡정보" class="btn button_icons type03 song_info"><span class="none">곡정보</span></a>
                </div></td>
                <td><div class="wrap">
                    <div class="wrap_song_info">
                        <div class="ellipsis rank01"><span>
                            <a href="javascript:melon.play.playSong('19030101',30853153);" title="빛이 나 (Shinin`) 재생">빛이 나 (Shinin`)</a>
                        </span></div><br>
                        <div class="ellipsis rank02">
                            <a href="javascript:melon.link.goArtistDetail('544520');" title="종현 (JONGHYUN) - 페이지 이동">종현 (JONGHYUN)</a><span class="checkEllipsis" style="display: none;"><a href="javascript:melon.link.goArtistDetail('544520');" title="종현 (JONGHYUN) - 페이지 이동">종현 (JONGHYUN)</a></span>
                        </div>
                    </div>
                </div></td>
                <td><div class="wrap">
                    <div class="wrap_song_info">
                        <div class="ellipsis rank03">
                            <a href="javascript:melon.link.goAlbumDetail('10131646');" title="Poet｜Artist - 페이지 이동">Poet｜Artist</a>
                        </div>
                    </div>
                </div></td>
                <td><div class="wrap">
                    <button type="button" class="button_etc like" title="빛이 나 (Shinin`) 좋아요" data-song-no="30853153" data-song-menuid="19030101"><span class="odd_span">좋아요</span>
    <span class="cnt">
    <span class="none">총건수</span>
    21,034</span></button>
                </div></td>
                <td><div class="wrap t_center">
                    <button type="button" title="듣기" class="button_icons play " onclick="melon.play.playSong('19030101',30853153);"><span class="none">듣기</span></button>
                </div></td>
                <td><div class="wrap t_center">
                    <button type="button" title="담기" class="button_icons scrap " onclick="melon.play.addPlayList('30853153');"><span class="none">담기</span></button>
                </div></td>
                <td><div class="wrap t_center">
                    <button type="button" title="다운로드" class="button_icons download " onclick="melon.buy.goBuyProduct('frm', '30853153', '3C0001', '','0', '19030101');"><span class="none">다운로드</span></button>
                </div></td>
                <td><div class="wrap t_center">
                    <button type="button" title="뮤직비디오" class="button_icons video disabled" disabled="disabled" onclick="melon.link.goMvDetail('19030101', '30853153','song');"><span class="none">뮤직비디오</span></button>
                </div></td>
                <td><div class="wrap t_center">
                    <button type="button" title="링/벨" class="button_icons bell disabled" disabled="disabled" onclick="melon.buy.popPhoneDecorate('0010000000000000','30853153')"><span class="none">링/벨</span></button>
                </div></td>
            </tr>'''


PATTERN_TD = re.compile(r'<td.*?>.*?</td>', re.DOTALL)

td_list = re.findall(PATTERN_TD, source)
for index, td in enumerate(td_list):
    td_strip = re.sub(r'[\n\t]+|\s{2,}', '', td)
    print(f'{index:02}: {td_strip}')

td_img_cover = td_list[3]
PATTERN_IMG = re.compile(r'<img.*?src="(.*?)".*?>', re.DOTALL)
url_img_cover = re.search(PATTERN_IMG, td_img_cover).group(1)
print(url_img_cover)

td_title_author = td_list[5]
PATTERN_DIV_RANK01 = re.compile(r'<div class="ellipsis rank01">.*?</div>', re.DOTALL)
PATTERN_A_CONTENT = re.compile(r'<a.*?>(.*?)</a>')
title_author = re.search(PATTERN_DIV_RANK01, td_title_author).group()
title = re.search(PATTERN_A_CONTENT, title_author).group(1)
print(title)