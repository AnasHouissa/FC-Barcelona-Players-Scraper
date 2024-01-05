import json
from bs4 import BeautifulSoup 
import requests as req 
from flask import Flask, request, jsonify

app = Flask(__name__)

def scrape_players_data():
     web = req.get('https://www.fcbarcelona.fr/fr/football/equipe-premiere/joueurs') 
     soup = BeautifulSoup(web.text, 'lxml')  
     images = soup.find_all('img',class_='team-person__image')
     player_names = soup.find_all('span',class_='team-person__last-name js-team-list-player-last-name')
     player_numbers = soup.find_all('span',class_='team-person__number')
     player_positions = soup.find_all('li',class_='team-person__position-meta') 
     return  [{
     "image": images[i].get("data-image-src"),
     "position": player_positions[i].text,
     "name": player_names[i].text,
     "number": player_numbers[i].text}
     for i in range(len(player_names))]

@app.route('/getPlayers', methods=['GET'])
def _getAllPlayer():
    try:
        data_list = scrape_players_data()
        return jsonify(data_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
