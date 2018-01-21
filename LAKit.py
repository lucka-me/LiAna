#!/usr/bin/env python3
# coding: utf-8

"""
LAKit for LiAna
Author:     Lucka
Version:    0.4.0
Licence:    MIT
"""

# 庫
from datetime import datetime   # 處理日期
from datetime import timedelta  # 累計時間

# 全局變量
## 時間字符串格式
dateFormat = "%Y-%m-%dT%H:%M:%SZ"
# 最新數據版本
lastDataVersion = "0.3.0"
# 起點時間
zeroTime = datetime.fromtimestamp(0)

# 類
class Music:
    """
    class Music
    Version 0.1.0
    對應版本
        MusicAnaly      0.1.0   -   0.1.1
        MusicLibrary    0.1.0
    成員變量
        trackID     int         唯一序列號
        totalTime   timedelta   歌曲時長
        discNumber  int         光盤序號
        trackNumber int         音軌序號
        year        int         歌曲年份
        dateAdded   datetime    加入音樂庫的時間
        playCount   int         播放次數
        name        str         歌曲標題
        artist      str         藝術家
        album       str         專輯名稱

    Version 0.2.0
    對應版本
        MusicAnaly      0.1.0   -   0.2.2
        MusicLibrary    0.1.0   -   0.2.2
    新增成員變量
        genre       str 音樂類型
        location    str 音頻文件路徑

    Version 0.3.0
    對應版本
        MusicAnaly      0.1.0   -   0.3.1
        MusicLibrary    0.1.0   -   0.3.0
    新增成員變量
        albumArtist str         專輯藝術家
    """
    def __init__(self,
                 trackID,
                 totalTime,
                 discNumber, trackNumber,
                 year, dateAdded,
                 playCount,
                 name, artist, albumArtist, album, genre,
                 location):
        self.trackID = trackID
        self.totalTime = totalTime
        self.discNumber = discNumber
        self.trackNumber = trackNumber
        self.year = year
        self.dateAdded = dateAdded
        self.playCount = playCount
        self.name = name
        self.artist = artist
        self.albumArtist = albumArtist
        self.album = album
        self.genre = genre
        self.location = location

class Album:
    """
    class Album
    Version 0.1.0
    對應版本
        MusicAnaly      0.1.0   -   0.1.1
        MusicLibrary    0.1.0   -   0.2.0
    成員變量
        albumID     int         唯一序列號
        totalTime   timedelta   專輯總時長
        name        str         專輯
        trackCount  int         音軌數量
        dateAdded   datetime    加入音樂庫的時間
        playCount   int         總播放次數

    Version 0.2.1
    對應版本
        MusicAnaly      0.1.0   -   0.2.2
        MusicLibrary    0.1.0   -   0.2.1
    新增成員變量
        playTime    timedelta   總播放時長

    Version 0.3.0
    對應版本
        MusicAnaly      0.1.0   -   0.3.1
        MusicLibrary    0.1.0   -   0.3.0
    新增成員變量
        artist      str         專輯藝術家
    """
    def __init__(self,
                 albumID,
                 totalTime,
                 name, artist,
                 trackCount,
                 dateAdded,
                 playCount, playTime):
        self.albumID = albumID
        self.totalTime = totalTime
        self.name = name
        self.artist = artist
        self.trackCount = trackCount
        self.dateAdded = dateAdded
        self.playCount = playCount
        self.playTime = playTime

class MusicLibrary:
    """
    class MusicLibrary
    Version 0.1.0
    對應版本
        MusicAnaly  0.1.0   -   0.1.1
        Music       0.1.0
        Album       0.1.0
    成員變量
        musicList   [Music]     音樂列表
        albumList   [Album]     專輯列表
        date        datetime    音樂庫修改時間

    Version 0.2.0
    對應版本
        MusicAnaly  0.2.0
        Music       0.2.0
        Album       0.1.0
    新增成員變量
        version     str    MusicLibrary 數據版本

    Version 0.2.1
    對應版本
        MusicAnaly  0.1.0   -   0.2.1
        Music       0.2.0
        Album       0.2.1

    Version 0.3.0
    對應版本
        MusicAnaly  0.1.0   -   0.3.1
        Music       0.3.0
        Album       0.3.0
    """
    def __init__(self, musicList, albumList, date):
        self.version = "0.3.0"
        self.musicList = musicList
        self.albumList = albumList
        self.date = date

    def getDateStr(self):
        return ("{year:0>4}-{month:0>2}-{day:0>2}"
                .format(year = self.date.year,
                        month = self.date.month,
                        day = self.date.day))


# 函数
def getLibrary(XMLFile):
    """
    讀取 iTunes 音樂庫 XML 文件
    參數列表:
        XMLFile file    XML 文件
    返回:
        MusicLibrary    掃描得到的音樂庫
    """

    # 讀取音樂庫修改時間並拋棄頭部
    XMLLine = XMLFile.readline()
    while "<key>Date</key>" not in XMLLine:
        XMLLine = XMLFile.readline()
    XMLLine = XMLLine.replace("\t<key>Date</key><date>", "")
    XMLLine = XMLLine.replace("</date>\n", "")
    libraryDate = datetime.strptime(XMLLine, dateFormat)
    while "<key>Tracks</key>" not in XMLLine:
        XMLLine = XMLFile.readline()
    XMLFile.readline()

    # 讀取
    """
    歌曲信息示例
    <key>1152</key>
    <dict>
        <key>Track ID</key><integer>...</integer>
        ...
        <key>Total Time</key><integer>...</integer>
        <key>Disc Number</key><integer>...</integer>
        <key>Track Number</key><integer>...</integer>
        <key>Year</key><integer>...</integer>
        ...
        <key>Date Added</key><date>...</date>
        ...
        <key>Play Count</key><integer>...</integer>
        ...
        <key>Name</key><string>...</string>
        <key>Artist</key><string>...</string>
        <key>Album Artist</key><string>...</string>
        ...
        <key>Album</key><string>...</string>
        <key>Genre</key><string>...</string>
        ...
        <key>Location</key><string>...</string>
        ...
    </dict>
    """

    # 音樂列表
    musicList = []
    # 專輯列表
    albumList = []

    XMLLine = XMLFile.readline()
    while "<key>Playlists</key>" not in XMLLine:
        trackID = 0
        totalTime = zeroTime
        discNumber = 0
        trackNumber = 0
        year = 0
        dateAdded = zeroTime
        playCount = 0
        name = ""
        artist = ""
        albumArtist = ""
        album = ""
        genre = ""
        location = ""
        while "</dict>" not in XMLLine:
            if "<key>Track ID</key>" in XMLLine:
                XMLLine = XMLLine.replace("\t\t\t<key>Track ID</key><integer>", "")
                XMLLine = XMLLine.replace("</integer>\n", "")
                trackID = int(XMLLine)
            if "<key>Total Time</key>" in XMLLine:
                XMLLine = XMLLine.replace("\t\t\t<key>Total Time</key><integer>", "")
                XMLLine = XMLLine.replace("</integer>\n", "")
                totalTime = datetime.fromtimestamp(int(XMLLine) / 1000) - zeroTime
            if "<key>Disc Number</key>" in XMLLine:
                XMLLine = XMLLine.replace("\t\t\t<key>Disc Number</key><integer>", "")
                XMLLine = XMLLine.replace("</integer>\n", "")
                discNumber = int(XMLLine)
            if "<key>Track Number</key>" in XMLLine:
                XMLLine = XMLLine.replace("\t\t\t<key>Track Number</key><integer>", "")
                XMLLine = XMLLine.replace("</integer>\n", "")
                trackNumber = int(XMLLine)
            if "<key>Year</key>" in XMLLine:
                XMLLine = XMLLine.replace("\t\t\t<key>Year</key><integer>", "")
                XMLLine = XMLLine.replace("</integer>\n", "")
                year = int(XMLLine)
            if "<key>Date Added</key>" in XMLLine:
                XMLLine = XMLLine.replace("\t\t\t<key>Date Added</key><date>", "")
                XMLLine = XMLLine.replace("</date>\n", "")
                dateAdded = datetime.strptime(XMLLine, dateFormat)
            if "<key>Play Count</key>" in XMLLine:
                XMLLine = XMLLine.replace("\t\t\t<key>Play Count</key><integer>", "")
                XMLLine = XMLLine.replace("</integer>\n", "")
                playCount = int(XMLLine)
            if "<key>Name</key>" in XMLLine:
                XMLLine = XMLLine.replace("\t\t\t<key>Name</key><string>", "")
                XMLLine = XMLLine.replace("</string>\n", "")
                name = XMLLine
            if "<key>Artist</key>" in XMLLine:
                XMLLine = XMLLine.replace("\t\t\t<key>Artist</key><string>", "")
                XMLLine = XMLLine.replace("</string>\n", "")
                artist = XMLLine
            if "<key>Album Artist</key>" in XMLLine:
                XMLLine = XMLLine.replace("\t\t\t<key>Album Artist</key><string>", "")
                XMLLine = XMLLine.replace("</string>\n", "")
                albumArtist = XMLLine
            if "<key>Album</key>" in XMLLine:
                XMLLine = XMLLine.replace("\t\t\t<key>Album</key><string>", "")
                XMLLine = XMLLine.replace("</string>\n", "")
                album = XMLLine
            if "<key>Genre</key>" in XMLLine:
                XMLLine = XMLLine.replace("\t\t\t<key>Genre</key><string>", "")
                XMLLine = XMLLine.replace("</string>\n", "")
                genre = XMLLine
            if "<key>Location</key>" in XMLLine:
                XMLLine = XMLLine.replace("\t\t\t<key>Location</key><string>", "")
                XMLLine = XMLLine.replace("</string>\n", "")
                XMLLine = XMLLine.replace("%20", " ")
                location = XMLLine
            XMLLine = XMLFile.readline()
            XMLLine = XMLLine.replace("&#38;", "&")

        # 拋棄有聲書和最後一行
        if genre != "Books" and trackID != 0:
            # 加入歌曲列表
            newMusic = Music(trackID,
                             totalTime,
                             discNumber, trackNumber,
                             year, dateAdded,
                             playCount,
                             name, artist, albumArtist, album, genre,
                             location)
            musicList.append(newMusic)

            # 更新專輯列表
            # 若列表中存在專輯則更新專輯信息
            isAlbumExist = False
            for album in albumList:
                if (album.name == newMusic.album and
                    album.artist == newMusic.albumArtist):
                    album.totalTime += totalTime
                    album.trackCount += 1
                    album.playCount += playCount
                    # 應當選取較早的添加時間
                    if album.dateAdded > dateAdded:
                        album.dateAdded = dateAdded
                    album.playTime += totalTime * playCount
                    isAlbumExist = True
                    break
            # 若列表中不存在專輯則將新專輯加入
            if not isAlbumExist:
                newAlbum = Album(newMusic.trackID,
                                 newMusic.totalTime,
                                 newMusic.album, newMusic.albumArtist,
                                 1,
                                 newMusic.dateAdded,
                                 newMusic.playCount,
                                 newMusic.totalTime * newMusic.playCount)
                albumList.append(newAlbum)
        XMLLine = XMLFile.readline()

    library = MusicLibrary(musicList, albumList, libraryDate)
    return library

def getReport(library, saveFile = False):
    """
    輸出音樂庫的報告，可保存至文件。
    參數列表:
        library     MusicLibrary    要輸出報告的音樂庫
        saveFile    file            輸出報告的文件，默認為不輸出
    """

    # 總時長
    totalTime = zeroTime - zeroTime
    for music in library.musicList:
        totalTime += music.totalTime
    # 總播放次數和時長
    totalPlayCount = 0
    totalPlayTime = zeroTime - zeroTime
    for music in library.musicList:
        totalPlayCount += music.playCount
        totalPlayTime += music.totalTime * music.playCount
    # 按播放次數排序
    # 用 lambda 函數進行排序
    #   Refrence: https://docs.python.org/3/howto/sorting.html
    musicListByPlayCount = sorted(library.musicList,
                                  key = lambda music: music.playCount,
                                  reverse = True)
    albumListByPlayCount = sorted(library.albumList,
                                  key = lambda album: album.playCount,
                                  reverse = True)
    # 按播放時長排序
    musicListByPlayTime = sorted(library.musicList,
                                 key = lambda music: music.playCount * music.totalTime,
                                 reverse = True)
    albumListByPlayTime = sorted(library.albumList,
                                 key = lambda album: album.playTime,
                                 reverse = True)
    # 報告文本
    # 開頭
    reportText = ("音樂庫報告\n" + getSplitLine() + '\n' +
                  "音乐库日期：{date}\n".format(date = library.getDateStr()) +
                  "共{musicCount}首音樂，{albumCount}張專輯，全部播放一遍要{totalTime:.0f}小時。\n"
                  .format(musicCount = len(library.musicList),
                          albumCount = len(library.albumList),
                          totalTime = getHours(totalTime)) +
                  "總共播放了{totalPlayCount}遍，共計{totalPlayTime:.0f}小時。\n"
                  .format(totalPlayCount = totalPlayCount,
                          totalPlayTime = getHours(totalPlayTime)) +
                  getSplitLine() + '\n')
    # 播放次數 TOP 10
    # 歌曲排行
    reportText += ("播放次數 TOP 10\n" + getSplitLine('-') + '\n' +
                   "歌曲排行\n" + "排名\t播放次數\t標題\n")
    for scanner in range(0, 10):
        reportText += ("#{num:0>2}\t{playCount:0>4}\t{name}\n"
                       .format(num = scanner + 1,
                               playCount = musicListByPlayCount[scanner].playCount,
                               name = musicListByPlayCount[scanner].name))
    # 專輯排行
    reportText += (getSplitLine('-') + '\n' +
                   "專輯排行\n" + "排名\t播放次數\t標題\n")
    for scanner in range(0, 10):
        reportText += ("#{num:0>2}\t{playCount:0>4}\t{name}\n"
              .format(num = scanner + 1,
                      playCount = albumListByPlayCount[scanner].playCount,
                      name = albumListByPlayCount[scanner].name))
    reportText += getSplitLine() + '\n'
    # 播放時長 TOP 10
    # 歌曲排行
    reportText += ("播放時長 TOP 10\n" + getSplitLine('-') + '\n' +
                   "歌曲排行\n" + "排名\t播放小時數\t標題\n")
    for scanner in range(0, 10):
        playHours = getHours(musicListByPlayTime[scanner].playCount *
                             musicListByPlayTime[scanner].totalTime)
        reportText += ("#{num:0>2}\t{playHours:0>4.0f}\t{name}\n"
                       .format(num = scanner + 1,
                               playHours = playHours,
                               name = musicListByPlayTime[scanner].name))
    # 專輯排行
    reportText += (getSplitLine('-') + '\n' +
                   "專輯排行\n" + "排名\t播放小時數\t標題\n")
    for scanner in range(0, 10):
        playHours = getHours(albumListByPlayTime[scanner].playTime)
        reportText += ("#{num:0>2}\t{playHours:0>4.0f}\t{name}\n"
              .format(num = scanner + 1,
                      playHours = playHours,
                      name = albumListByPlayTime[scanner].name))
    reportText += getSplitLine() + '\n'
    print(reportText)
    # 報告文件
    if saveFile != False:
        saveFile.write(reportText)

def compare(libraryA, libraryB, saveFile = False):
    """
    對比兩個音樂庫紀錄，生成報告
    參數列表:
        libraryA    MusicLibrary    第一個音樂庫
        libraryB    MusicLibrary    第二個音樂庫
    """
    # 確定 libraryA 比 libraryB 更新
    if libraryA.date < libraryB.date:
        temp = libraryA
        libraryA = libraryB
        libraryB = temp
    # 時間差
    timeInterval = libraryA.date - libraryB.date
    # 期間播放次數和期間播放時間
    totalPlayCount = 0
    totalPlayTime = zeroTime - zeroTime
    # 列表直接賦值是引用而非複製
    #   Refrence: http://blog.csdn.net/lovelyaiq/article/details/55102518
    #   refrence: http://www.cnblogs.com/ifantastic/p/3811145.html
    newMusicList = []
    newAlbumList = []
    changedMusicList = []
    changedAlbumList = []

    # 匹配歌曲
    for musicA in libraryA.musicList:
        isMatched = False
        for musicB in libraryB.musicList:
            if (musicA.name == musicB.name and
                musicA.album == musicB.album and
                musicA.trackNumber == musicB.trackNumber and
                musicA.discNumber == musicB.discNumber):
                if musicA.playCount > musicB.playCount:
                    changedMusic = Music(musicA.trackID,
                                         musicA.totalTime,
                                         musicA.discNumber, musicA.trackNumber,
                                         musicA.year, musicA.dateAdded,
                                         musicA.playCount - musicB.playCount,
                                         musicA.name, musicA.artist,
                                         musicA.albumArtist, musicA.album,
                                         musicA.genre,
                                         musicA.location)
                    changedMusicList.append(changedMusic)
                    totalPlayTime += changedMusic.totalTime * changedMusic.playCount
                    totalPlayCount += changedMusic.playCount
                isMatched = True
                break
        # 未有匹配成功且加入時間較 libraryB 更晚的才是真的新加入歌曲
        if isMatched == False and musicA.dateAdded > libraryB.date:
            newMusicList.append(musicA)
            changedMusicList.append(musicA)
            totalPlayCount += musicA.playCount
            totalPlayTime += musicA.totalTime * musicA.playCount
    # 匹配專輯
    for albumA in libraryA.albumList:
        isMatched = False
        for albumB in libraryB.albumList:
            if albumA.name == albumB.name and albumA.artist == albumB.artist:
                if albumA.playCount > albumB.playCount:
                    changedAlbum = Album(albumA.albumID,
                                         albumA.totalTime,
                                         albumA.name, albumA.artist,
                                         albumA.trackCount,
                                         albumA.dateAdded,
                                         albumA.playCount - albumB.playCount,
                                         albumA.playTime - albumB.playTime)
                    changedAlbumList.append(changedAlbum)
                isMatched = True
                break
        if isMatched == False and albumA.dateAdded > libraryB.date:
            newAlbumList.append(albumA)
            changedAlbumList.append(albumA)
    # 按播放次數排序
    # 歌曲排行
    musicListByPlayCount = sorted(changedMusicList,
                                  key = lambda music: music.playCount,
                                  reverse = True)
    # 專輯排行
    albumListByPlayCount = sorted(changedAlbumList,
                                  key = lambda album: album.playCount,
                                  reverse = True)
    # 按播放時長排序
    # 歌曲排行
    musicListByPlayTime = sorted(changedMusicList,
                                 key = lambda music: music.playCount * music.totalTime,
                                 reverse = True)
    # 專輯排行
    albumListByPlayTime = sorted(changedAlbumList,
                                 key = lambda album: album.playTime,
                                 reverse = True)
    # 報告文本
    # 開頭
    reportText = ("音樂庫對比報告\n" + getSplitLine() + '\n' +
                  "音乐库日期：{start} -> {end}，共{interval}天。\n"
                  .format(start = libraryB.getDateStr(),
                          end = libraryA.getDateStr(),
                          interval = timeInterval.days))
    reportText += ("共新增{musicAdded}首音樂，{albumAdded}張專輯。\n"
                   .format(musicAdded = len(newMusicList),
                           albumAdded = len(newAlbumList)))
    reportText += ("聽了來自{albumPlayed}張專輯的{musicPlayed}首音樂，共聽了{playCount}次，{totalPlayTime:.0f}小時。\n"
                   .format(albumPlayed = len(changedAlbumList),
                           musicPlayed = len(changedMusicList),
                           playCount = totalPlayCount,
                           totalPlayTime = getHours(totalPlayTime)) +
                   getSplitLine() + '\n')
    reportText += ("播放次數 TOP 10\n" + getSplitLine('-') + '\n' +
                   "歌曲排行\n" + "排名\t播放次數\t標題\n")
    count = 0
    for music in musicListByPlayCount:
        count += 1
        reportText += ("#{num:0>2}\t{playCount:0>4}\t{name}\n"
                       .format(num = count,
                               playCount = music.playCount,
                               name = music.name))
        if count == 10:
            break
    reportText += getSplitLine('-') + '\n' + "專輯排行\n" + "排名\t播放次數\t標題\n"
    count = 0
    for album in albumListByPlayCount:
        count += 1
        reportText += ("#{num:0>2}\t{playCount:0>4}\t{name}\n"
              .format(num = count,
                      playCount = album.playCount,
                      name = album.name))
        if count == 10:
            break
    reportText += getSplitLine() + '\n'
    # 播放時長 TOP 10
    # 歌曲排行
    reportText += ("播放時長 TOP 10\n" + getSplitLine('-') + '\n' +
                   "歌曲排行\n" + "排名\t播放小時數\t標題\n")
    count = 0
    for music in musicListByPlayTime:
        count += 1
        reportText += ("#{num:0>2}\t{playHours:0>4.0f}\t{name}\n"
                       .format(num = count,
                               playHours = getHours(music.playCount *
                                                    music.totalTime),
                               name = music.name))
        if count == 10:
            break
    # 專輯排行
    reportText += (getSplitLine('-') + '\n' +
                   "專輯排行\n" + "排名\t播放小時數\t標題\n")
    count = 0
    for album in albumListByPlayTime:
        count += 1
        reportText += ("#{num:0>2}\t{playHours:0>4.0f}\t{name}\n"
              .format(num = count,
                      playHours = getHours(album.playTime),
                      name = album.name))
        if count == 10:
            break
    reportText += getSplitLine() + '\n'
    print(reportText)
    # 報告文件
    if saveFile != False:
        saveFile.write(reportText)

def update(oldLibrary ,sampleFile, isAuto = True):
    """
    更新音樂庫數據版本
    參數列表:
        oldLibrary  MusicLibrary    需要升級的音樂庫
        sampleFile  file            樣本 XML 文件
        isAuto      bool            是否自動確認疑似相同歌曲，默認為 True
    返回:
        MusicLibrary
    """
    print("開始更新")
    print("正在獲取最新版的樣本⋯")
    sampleLibrary = getLibrary(sampleFile)
    print("獲取成功")

    # 檢測 trackID 的偏差
    print("正在檢測偏差…")
    deviation = 0
    # 總共檢測5次
    matchCount = 0
    for oldMusic in oldLibrary.musicList:
        didMatch = False;
        for sampleMusic in sampleLibrary.musicList:
            if (sampleMusic.name == oldMusic.name and
                sampleMusic.album == oldMusic.album):
                newDeviation = sampleMusic.trackID - oldMusic.trackID
                didMatch = True
                matchCount += 1
                break
        if didMatch:
            if matchCount == 1:
                deviation = newDeviation
            else:
                if deviation != newDeviation:
                    print("匹配異常，偏差不一致")
                    return
            if matchCount == 5:
                break
    print("偏差檢測完成，偏差為 {deviation}".format(deviation = deviation))

    changedMusicList = []
    version = detectDataVersion(oldLibrary)
    print("開始更新數據 {oldDataVersion} -> {lastDataVersion}"
          .format(oldDataVersion = version, lastDataVersion = lastDataVersion))

    newMusicList = []
    newAlbumList = []
    for sampleMusic in sampleLibrary.musicList:
        for oldMusic in oldLibrary.musicList:
            if (sampleMusic.trackID == oldMusic.trackID + deviation and
                sampleMusic.totalTime == oldMusic.totalTime and
                (sampleMusic.name != oldMusic.name or
                 sampleMusic.album != oldMusic.album)):
                if not isAuto:
                    print("檢測到疑似為同一首歌曲的兩首歌曲：")
                    print("\t樣本數據：\n\t\t歌曲名稱：{name}\n\t\t專輯名稱:{album}"
                          .format(name = sampleMusic.name,
                                  album = sampleMusic.album))
                    print("\t舊數據：\n\t\t歌曲名稱：{name}\n\t\t專輯名稱:{album}"
                          .format(name = oldMusic.name,
                                  album = oldMusic.album))
                    answer = input("是否需要更新名稱和專輯為樣本數據 (Y/N): ")
                    answer = answer.upper()
                    while answer != "Y" and answer != "N" and answer != "":
                        print("警告: 輸入錯誤")
                        answer = input("是否需要更新名稱和專輯為樣本數據 (Y/N): ")
                        answer = answer.upper()
                    if answer == "Y" or answer == "":
                        oldMusic.name = sampleMusic.name
                        oldMusic.album = sampleMusic.album
                else:
                    oldMusic.name = sampleMusic.name
                    oldMusic.album = sampleMusic.album
            if (sampleMusic.name == oldMusic.name and
                sampleMusic.album == oldMusic.album and
                sampleMusic.trackNumber == oldMusic.trackNumber and
                sampleMusic.discNumber == oldMusic.discNumber):
                # 加入歌曲列表
                newMusic = Music(sampleMusic.trackID,
                                 sampleMusic.totalTime,
                                 sampleMusic.discNumber,
                                 sampleMusic.trackNumber,
                                 sampleMusic.year,
                                 oldMusic.dateAdded,
                                 oldMusic.playCount,
                                 sampleMusic.name,
                                 sampleMusic.artist,
                                 sampleMusic.albumArtist,
                                 sampleMusic.album,
                                 sampleMusic.genre,
                                 sampleMusic.location)
                newMusicList.append(newMusic)
                # 更新專輯列表
                isAlbumExist = False
                for album in newAlbumList:
                    if album.name == newMusic.album:
                        album.totalTime += newMusic.totalTime
                        album.trackCount += 1
                        album.playCount += newMusic.playCount
                        if album.dateAdded > newMusic.dateAdded:
                            album.dateAdded = newMusic.dateAdded
                        album.playTime += newMusic.totalTime * newMusic.playCount
                        isAlbumExist = True
                        break
                if not isAlbumExist:
                    newAlbum = Album(newMusic.trackID,
                                     newMusic.totalTime,
                                     newMusic.album, newMusic.albumArtist,
                                     1,
                                     newMusic.dateAdded,
                                     newMusic.playCount,
                                     newMusic.totalTime * newMusic.playCount)
                    newAlbumList.append(newAlbum)
                break

    newLibrary = MusicLibrary(newMusicList,
                              newAlbumList,
                              oldLibrary.date)
    return newLibrary

def detectDataVersion(library):
    """
    檢測音樂庫記錄的數據版本
    參數列表：
        library MusicLibrary    需檢測版本的音樂庫
    返回：
        str     版本號字符串
    """
    version = "0"
    try:
        version = library.version
    except Exception as error:
        # 僅 0.1.0 版的數據內無版本變量
        version = "0.1.0"
    return version

def getSplitLine(char = '=', length = 80):
    """
    生成分割線
    參數列表:
        [char]      str 分割線的字符串，默認為 "="
        [length]    int 分割線長度，默認為80
    返回:
        str         分割線字符串
    """
    result = ""
    for i in range(0, length):
        result += char
    return result

def getHours(timeInterval):
    """
    獲取 timedelta 的小時數
    參數列表:
        timeInterval    timedelta
    返回:
        double          浮點小時數
    """
    return timeInterval.days * 24 + timeInterval.seconds / 3600

# 不應直接運行模塊
if __name__ == '__main__':
    print("ERROR: 請勿直接運行模塊。")
