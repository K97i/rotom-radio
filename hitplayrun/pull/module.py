import requests
from bs4 import BeautifulSoup
from ..songClass import Song
import tkinter as tk
from tkinter import filedialog
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

lists = {
    "magic": "https://magic899.com",
    "billboard": "https://billboardphilippines.com/chart/philippines-hot-100",
    "monster": "https://www.rx931.com/CountdownTop7"
}

implemented = [ "magic", "billboard", "monster" ]

SONG_LIMIT = 20

# MAGIC

def magicParseForm(form):
    finalList = {}
    
    # Get Number one
    numberone = form.select_one("*:first-child")
    numberoneparent = numberone.find("span", string="This Week").find_parent('div').find_parent('div')
    numberonesong = numberoneparent.find_all(recursive=False)[1]
    finalList["1"] = Song(title=numberonesong.find("h2").text, artist=numberonesong.find("p").text).to_dict()

    # Rest of list
    sidelist = form.find_all(recursive=False)[1].find("ul")

    for song in sidelist.find_all(recursive=False):
        songcontents = song.find_all(recursive=False)
        songitems = songcontents[1].find("button").find_parent('div').find_parent('div').find("div")
        songmetadata = songitems.find_all(recursive=False)
        finalList[songcontents[0].find("p").text] = Song(title=songmetadata[0].text, artist=songmetadata[1].text).to_dict()

    return finalList

def getmagic(html):
    header = html.find("h2", string="Magic Pop 30")

    if header:
        formdiv = header.find_parent('div')

        if formdiv:
            form = formdiv.find('form')
            
            if form:
                return magicParseForm(form=form)

        else:
            print("[ERROR]: Div containing form not found.")
        
    else:
        print("[ERROR]: Header not found")

# Billboard

def getbillboard(html):
    finalList = {}
    chart = html.find("div", class_="charts__container")
    
    idx = 1

    for song in chart.children:
        if song.name == "div" and song.get("class") == ['row', 'g-0', 'b-bottom', 'ad-selector']:
            idx += 1
            weekRank = song.find("span").text
            titles = song.find("div", class_="title__container")

            finalList[weekRank] = Song(title=titles.find("h4").text, artist=titles.find("span").text).to_dict()

        if idx > SONG_LIMIT:
            break

    return finalList

# Monster

def getmonster(html):
    finalList = {}
    chart = html.find("div", class_="col-12 col-sm-12 col-md-12 col-lg-9 col-xl-9 col-xxl-9 mb-4")

    # Visible
    songs = chart.find_all(class_="card bg-medium-gray text-light", recursive=False)
    
    for song in songs:
        rank = song.find("div", class_="col-2 col-sm-1 align-self-center text-center").text.strip()
        titles = list(song.find("div", class_="col-5 col-sm-5 col-md-5 col-lg-5 col-xl-5 col-xxl-5 text-center").find("div", class_="text-light").stripped_strings)
        finalList[rank] = Song(title=titles[0], artist=titles[1]).to_dict()

    # Invisible
    songs = chart.select_one("#more-charts").find_all(class_="card bg-medium-gray text-light", recursive=False)
    
    for song in songs:
        rank = song.find("div", class_="col-2 col-sm-1 align-self-center text-center").text.strip()
        titles = list(song.find("div", class_="col-5 col-sm-5 col-md-5 col-lg-5 col-xl-5 col-xxl-5 text-center").find("div", class_="text-light").stripped_strings)
        finalList[rank] = Song(title=titles[0], artist=titles[1]).to_dict()

    return finalList

# Main Func

def pull():
    collated = dict()
    for item, value in lists.items():
        if item in implemented:
            response = requests.get(value, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                collated[item] = globals()[f"get{item}"](soup)
                
        else:
            print(f"{item} is not implemented yet.")

    root = tk.Tk()
    root.withdraw()

    filePath = filedialog.asksaveasfilename(
        title="Save final list",
        filetypes=[("JSON files", "*.json")]
    )

    if filePath:
        with open(filePath, "w", encoding="utf-8") as file:
            json.dump(collated, file)

    return collated

