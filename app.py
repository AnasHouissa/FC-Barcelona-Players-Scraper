import json
from bs4 import BeautifulSoup 
import requests as req 
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/getPlayers', methods=['GET'])
def _getAllPlayer():
    Web = req.get('https://www.fcbarcelona.fr/fr/football/equipe-premiere/joueurs') 
    soup = BeautifulSoup(Web.text, 'lxml') 

    images = soup.find_all('img',class_='team-person__image')
    player_names = soup.find_all('span',class_='team-person__last-name js-team-list-player-last-name')
    player_numbers = soup.find_all('span',class_='team-person__number')
    player_positions = soup.find_all('li',class_='team-person__position-meta')

    data_list = []

    i=0
    while i < len(player_names):
        data_list.append({"image":     images[i].get("data-image-src")
    , "position":     player_positions[i].text
    , "name":     player_names[i].text
    , "number":     player_numbers[i].text
    })  
        i+=1

    json_data = json.dumps(data_list, indent=2,ensure_ascii=False)

    return(json_data)

if __name__ == '__main__':
    app.run(debug=True)
