import os

import pandas as pd
import requests
import sys
import re


def addAudio(lang, wordPos, phonPos, audioPos, csvIn, csvOut, suffix):
    baseURL = "https://translate.google.com/translate_tts?ie=UTF-&&client=tw-ob&tl=" + lang + "&q="
    f = pd.read_csv('~/Documents/' + csvIn, sep='\t', header=None, on_bad_lines='skip')
    destination = '/home/thomas/.local/share/Anki2/User 1/collection.media/'
    kanji = f[wordPos]
    phon = f[phonPos]  # kana/pinyin slot

    s = requests.Session()
    for i, word in enumerate(kanji):
        if pd.isnull(f.loc[i, audioPos]):
            p = phon[i]
            if pd.isnull(f.loc[i, phonPos]):  # if phonetic section is null use kanji
                p = word

            if word[0] == "<":
                word = re.sub('<[^<]+?>', '', word)
            url = baseURL + str(p)
            print(word, url)
            try:
                audio = s.get(url)

            except:
                print("error getting " + word)

            fileName = str(i) + "_" + word + "_" + suffix + ".mp3"
            try:

                open(destination + fileName, 'wb').write(audio.content)
                f[audioPos][i] = "[sound:" + fileName + "]"
            except:
                print("error writing file " + fileName + " to " + destination)

    f.to_csv('/home/thomas/Documents/' + csvOut, sep="\t", header=None, index=False)


def clearMP3s():
    confirm = input("Clear MP3s by suffix? Y/N: ")
    if confirm == "yes" or confirm == "Yes" or confirm == "y" or confirm == "Y":
        suffix = input("Clear all MP3s with suffix: ")
        for file in os.listdir("/home/thomas/.local/share/Anki2/User 1/collection.media/"):
            if file.endswith("_" + suffix + ".mp3"):
                try:
                    os.remove("/home/thomas/.local/share/Anki2/User 1/collection.media/" + file)
                    print("Removed file " + file)
                except:
                    print("Error removing file " + file)


def clearTags(csvIn, csvOut):
    f = pd.read_csv('~/Documents/' + csvIn, sep='\t', header=None, on_bad_lines='skip')
    kanjiList = f[0]
    for i, kanji in enumerate(kanjiList):
        k = re.sub('<[^<]+?>', '', kanji)
        if k != kanji:
            f[0][i] = k
    f.to_csv('/home/thomas/Documents/' + csvOut, sep="\t", header=None, index=False)


def main():
    languages = [["ja", "japan", "jpn", "japanese", "japn"],
                 ["zh-CN", "chinese", "simplified", "china", "chin"]
                 ]

    wP = 0
    sP = 1
    aP = 3

    if len(sys.argv) > 1 and sys.argv[1] == 'clear':
        clearMP3s()
    elif len(sys.argv) > 1 and sys.argv[1] == 'ct':
        csvIn = input("CSV file name: ")
        csvOut = input("Modified csv file name: ")
        clearTags(csvIn, csvOut)
    else:
        if len(sys.argv) > 2:
            wP = int(sys.arv[2])
        if len(sys.argv) > 3:
            sP = int(sys.argv[3])
        if len(sys.argv) > 4:
            aP = int(sys.argv[4])
        if len(sys.argv) > 1:
            l = sys.argv[1]
            lang = None
            for language in languages:
                if l in language:
                    lang = language[0]

            if lang:
                csvIn = input("CSV file name: ")
                csvOut = input("Modified csv file name: ")
                suffix = input("MP3 suffix: ")
                addAudio(lang, wP, sP, aP, csvIn, csvOut, suffix)


main()
