import requests
from bs4 import BeautifulSoup
from ..songClass import Song

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

lists = {
    "magic": "https://magic899.com",
    "billboard": "https://billboardphilippines.com/chart/philippines-hot-100",
    "monster": "https://www.rx931.com/CountdownTop7"
}

implemented = [ "magic", "billboard" ]

SONG_LIMIT = 20

# MAGIC

def magicParseForm(form):
    finalList = {}
    
    # Get Number one
    numberone = form.select_one("*:first-child")
    numberoneparent = numberone.find("span", string="This Week").find_parent('div').find_parent('div')
    numberonesong = numberoneparent.find_all(recursive=False)[1]
    finalList["1"] = Song(title=numberonesong.find("h2").text, artist=numberonesong.find("p").text)

    # Rest of list
    sidelist = form.find_all(recursive=False)[1].find("ul")

    for song in sidelist.find_all(recursive=False):
        songcontents = song.find_all(recursive=False)
        songitems = songcontents[1].find("button").find_parent('div').find_parent('div').find("div")
        songmetadata = songitems.find_all(recursive=False)
        finalList[songcontents[0].find("p").text] = Song(title=songmetadata[0].text, artist=songmetadata[1].text)

    return finalList

def getmagic(html):
    header = html.find("h2", string="Magic Pop 30")

    if header:
        formdiv = header.find_parent('div')

        if formdiv:
            form = formdiv.find('form')
            
            if form:
                magicParseForm(form=form)

        else:
            print("[ERROR]: Div containing form not found.")
        
    else:
        print("[ERROR]: Header not found")

# Billboard

def getbillboard(html):
    finalList = {}
    chart = html.find("div", class_="charts__container")
    
    idx = 0

    for song in chart.children:
        if song.name == "div" and song.get("class") == ['row', 'g-0', 'b-bottom', 'ad-selector']:
            idx += 1
            weekRank = song.find("span").text
            titles = chart.find("div", class_="title__container")

            finalList[weekRank] = Song(title=titles.find("h4").text, artist=titles.find("span").text)

        if idx > SONG_LIMIT:
            break

    return finalList

# Main Func

def pull():
    collated = dict()
    for item, value in lists.items():
        if item in implemented:
            response = requests.get(value, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                collated[item] = globals()[f"get{item}"](soup)
                
        else:
            print(f"{item} is not implemented yet.")

