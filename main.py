import pandas as pd
import requests
import sys


def addAudio(lang, wordPos, phonPos, audioPos, csvIn, csvOut, suffix):
    baseURL = "https://translate.google.com/translate_tts?ie=UTF-&&client=tw-ob&tl=" + lang + "&q="
    f = pd.read_csv('~/Documents/' + csvIn, sep='\t', header=None, on_bad_lines='skip')
    destination = '/home/thomas/.local/share/Anki2/User 1/collection.media/'
    kanji = f[wordPos]
    phon = f[phonPos]

    s = requests.Session()
    for i, word in enumerate(kanji):
        if pd.isnull(f.loc[i, audioPos]):
            url = baseURL + phon[i]
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


def main():
    languages = [["ja", "japan", "jpn", "japanese", "japn"],
                 ["zh-CN", "chinese", "simplified", "china", "chin"]
                 ]

    wP = 0
    sP = 1
    aP = 3
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
