import pinyin #https://pypi.org/project/pinyin/ to translate from chinese to pinyin and to english

'''
things to do:
no translation on the english
filter out all tags as well as the mojim.com thing
extract properly
'''
def translate_phrase(phrase):
    tl_phrases = []
    cur_phrase = ""
    for char in phrase:
        if pinyin.cedict.translate_word(cur_phrase+char) is not None:
            #somehow check ofr success
            cur_phrase += char
        else:
            tl_phrases.append(pinyin.cedict.translate_word(cur_phrase))
            cur_phrase = char
    tl_phrases.append(pinyin.cedict.translate_word(cur_phrase))
    return tl_phrases

def translate(lyrics):
    #lyrics is a collection of lines
    #each line may have spaces denoting separate phrases, we will further subdivide here
    tl_lines = []
    pinyin_lines = []
    #we want one mandarin line, one pinyin line, one definitions
    #main issue is with definitions
    #we want to make the mandarin line definitions friendloy
    #consider frontend side first b4 figuring tihs out
    #

    ########THIS FUNCTION OUGHT TO RETURN PROPER HTML OUTPUT WITH TAGS & STUFF
    #first 3 lines of lyrics is always going to be ignored
    