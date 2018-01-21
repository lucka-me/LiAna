#!/usr/bin/env python3
# coding: utf-8

"""
LiAna
Author:     Lucka
Version:    0.4.0
Licence:    MIT
"""

# 命令行參數說明
# 終端顯示效果
#   Refrence: https://stackoverflow.com/questions/287871/print-in-terminal-with-colors
optionsHelp = """可使用的命令行參數：
    \033[1m-a --add\033[0m                  掃描新的 iTunes 音樂庫 XML 文件並保存數據
    \033[1m-r --report  <filename>\033[0m   生成指定音樂庫記錄的報告
    \033[1m-c --compare <filename>\033[0m   比較當前音樂庫和過去指定音樂庫記錄並生成報告
    \033[1m-u --update  <filename>\033[0m   更新指定記錄的數據文件
    \033[1m             --force\033[0m      強制更新
    \033[1m             --auto\033[0m       自動處理疑似相同的歌曲
    \033[1m-h --help\033[0m                 顯示本幫助文本
"""

# 庫
from datetime import datetime   # 處理日期
from datetime import timedelta  # 累計時間
import os                       # 建立文件夾、获取终端窗口尺寸
import pickle                   # 將對象存入文件
import sys, getopt              # 讀取命令行參數
import LAKit
from LAKit import MusicLibrary
from LAKit import Album
from LAKit import Music

def main():
    # 检查并创建 Library 文件夹
    if not os.path.exists("./Library"):
        os.mkdir("./Library")

    # 處理命令行參數
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "har:c:u:",
                                   ["help",
                                    "add",
                                    "report=",
                                    "compare=",
                                    "force",
                                    "auto"])
    except getopt.GetoptError as error:
        print("Error: {error}".format(error = error))
        print(optionsHelp)
        exit()

    print(__doc__)
    if len(opts) == 0:
        print("請在命令行中添加參數。")
        print(optionsHelp)
        exit()

    # 數據升級
    isUpdate = False
    isUpdateForced = False
    isUpdateAuto = False

    for opt, argv in opts:
        if opt in ("-h", "--help"):
            print(optionsHelp)
            return

        elif opt in ("-a", "--add"):
            XMLFilename = "iTunes Music Library.xml"
            try:
                XMLFile = open(XMLFilename, "r")
            except Exception as error:
                print("ERROR: {error}".format(error = error))
                return
            print("開始掃描 {filename}".format(filename = XMLFilename))
            library = LAKit.getLibrary(XMLFile)
            XMLFile.close()
            print("掃描完成，共掃描{musicCount}首歌曲，{albumCount}張專輯。\n"
                  .format(musicCount = len(library.musicList),
                          albumCount = len(library.albumList)))
            dataFilename = ("./Library/{date}.data"
                            .format(date = library.getDateStr()))
            dataFile = open(dataFilename, "wb")
            pickle.dump(library, dataFile)
            dataFile.close()
            print("已生成文件：{filename}\n".format(filename = dataFilename))
            return

        elif opt in ("-r", "--report"):
            dataFilename = argv
            dataFilename = "./Library/" + dataFilename
            try:
                dataFile = open(dataFilename, "rb")
            except Exception as error:
                print("ERROR: {error}".format(error = error))
                return
            library = pickle.load(dataFile)
            dataVersion = LAKit.detectDataVersion(library)
            if dataVersion != LAKit.lastDataVersion:
                print("記錄文件 {filename} 數據版本過低，請進行數據更新"
                      .format(filename = dataFilename))
                return
            reportFilename = ("{date} Report.txt"
                              .format(date = library.getDateStr()))
            reportFile = open(reportFilename, "w")
            LAKit.getReport(library, reportFile)
            reportFile.close()
            print("已生成報告文件：{filename}".format(filename = reportFilename))
            return

        elif opt in ("-c", "--compare"):
            XMLFilename = "iTunes Music Library.xml"
            try:
                XMLFile = open(XMLFilename, "r")
            except Exception as error:
                print("ERROR: {error}".format(error = error))
                return
            print("開始掃描 {filename}".format(filename = XMLFilename))
            libraryA = LAKit.getLibrary(XMLFile)
            XMLFile.close()
            print("掃描完成，共掃描{musicCount}首歌曲，{albumCount}張專輯。\n"
                  .format(musicCount = len(libraryA.musicList),
                          albumCount = len(libraryA.albumList)))
            # 載入記錄
            dataBFilename = argv
            dataBFilename = "./Library/" + dataBFilename
            try:
                dataBFile = open(dataBFilename, "rb")
            except Exception as error:
                print("ERROR: {error}".format(error = error))
                return
            libraryB = pickle.load(dataBFile)
            dataVersion = LAKit.detectDataVersion(libraryB)
            if dataVersion != LAKit.lastDataVersion:
                print("記錄文件 {filename} 數據版本過低，請運行數據更新工具"
                      .format(filename = dataBFilename))
                return
            reportFilename = ("{dateA} vs {dateB} Report.txt"
                              .format(dateA = libraryA.getDateStr(),
                                      dateB = libraryB.getDateStr()))
            reportFile = open(reportFilename, "w")
            LAKit.compare(libraryA, libraryB, reportFile)
            reportFile.close()
            print("已生成報告文件：{filename}".format(filename = reportFilename))
            return

        elif opt in ("-u", "--update"):
            isUpdate = True
            oldDataFilename = argv
            oldDataFilename = "./Library/" + oldDataFilename
        elif opt in ("--force"):
            isUpdateForced= True
        elif opt in ("--auto"):
            isUpdateAuto = True
            print("isUpdateAuto = {}".format(isUpdateAuto))
        else:
            print("參數 {opt} 不可用".format(opt))
            print(optionsHelp)

    # 升級數據
    if isUpdate:
        try:
            oldDataFile = open(oldDataFilename, "rb")
        except Exception as error:
            print("ERROR: {error}".format(error = error))
            exit()
        oldLibrary = pickle.load(oldDataFile)
        oldDataVersion = LAKit.detectDataVersion(oldLibrary)
        if oldDataVersion == LAKit.lastDataVersion:
            if isUpdateForced:
                print("{filename} 的數據版本為 {version}，強制升級"
                      .format(filename = oldDataFilename,
                              version = oldDataVersion))
                XMLFilename = "iTunes Music Library.xml"
                try:
                    XMLFile = open(XMLFilename, "r")
                except Exception as error:
                    print("ERROR: {error}".format(error = error))
                    return
                newLibrary = LAKit.update(oldLibrary, XMLFile, isUpdateAuto)
                newDataFilename = ("./Library/{date}-new.data"
                                   .format(date = newLibrary.getDateStr()))
                newDataFile = open(newDataFilename, "wb")
                pickle.dump(newLibrary, newDataFile)
                newDataFile.close()
                print("已生成文件：{filename}\n".format(filename = newDataFilename))
                return
            else:
                print("{filename} 的數據版本為 {version}，無須升級"
                      .format(filename = oldDataFilename,
                              version = oldDataVersion))
                return
        else:
            print("{filename} 的數據版本為 {version}，需要升級"
                  .format(filename = oldDataFilename,
                          version = oldDataVersion))
            XMLFilename = "iTunes Music Library.xml"
            try:
                XMLFile = open(XMLFilename, "r")
            except Exception as error:
                print("ERROR: {error}".format(error = error))
                return
            newLibrary = LAKit.update(oldLibrary, XMLFile, isUpdateAuto)
            newDataFilename = ("./Library/{date}-new.data"
                               .format(date = newLibrary.getDateStr()))
            newDataFile = open(newDataFilename, "wb")
            pickle.dump(newLibrary, newDataFile)
            newDataFile.close()
            print("已生成文件：{filename}\n".format(filename = newDataFilename))
            return

if __name__ == '__main__':
    main()
