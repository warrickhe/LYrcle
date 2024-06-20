from bs4 import BeautifulSoup
import requests
import re

#idea: create a web scraper
website = "mojim.com"
#https://mojim.com/{search name}.html?g3

def parse_lyrics(lyrics):
    lyrics = lyrics.replace("\n",'')
    lyrics = lyrics.replace("更多更详尽歌词 在 ※ Mojim.com　魔镜歌词网 <br/>", '')
    lyrics = re.sub(r'(<br\/>)+', '<br/>', lyrics)
    lyrics = lyrics.replace('<dl class="fsZx1" id="fsZx1">蓝心羽<br/><dt class="fsZx2" id="fsZx2"></dt>晴天<br/>','')
    lyrics = lyrics.replace('<ol><li></li></ol></dl>','')
    lyrics = lyrics.replace('<br/>','\n')
    return lyrics

def parse_name(name):
    #<span class="shx_ss4"> 1.一碗<font color="#D34805">苦茶</font></span>
    #we want to remvoe the 1. whatever and also the <font> whatever
    name = name.replace('<font color="#D34805">','')
    name = name.replace ("</font>",'')
    name = name[name.index('.')+1:]
    return name

def make_song_dict(soup):
    song_data = {}
    song_data["artist"] = soup.contents[3].text
    song_data["album"] = soup.contents[5].text
    song_data["song_name"] = parse_name(soup.contents[7].text)
    song_data["link"] = soup.contents[7].contents[0].get('href')
    return song_data

def search_song(song_name):
    #should return results, list of tuples (artist, album, song name)
    html = requests.get(f"https://mojim.com/{song_name}.html?g3").text
    soup = BeautifulSoup(html,"html.parser")
    results = []
    for s in soup.select(".mxsh_dd1, .mxsh_dd2"):
        song_data = make_song_dict(s)
        if song_data["song_name"] == song_name:
            results.append(song_data)
    return results

def get_lyrics(link):
    #https://mojim.com/cny100951x42x10.htm
    #remove all lyrics of form 更多更详尽歌词 在 ※ Mojim.com　魔镜歌词网 <br/>
    html = requests.get(f"https://mojim.com/{link}").text
    soup = BeautifulSoup(html,"html.parser")
    return parse_lyrics(str(soup.select_one("#fsZx1")))


if __name__ == "__main__":
    print(get_lyrics(search_song("晴天")[6]["link"]))