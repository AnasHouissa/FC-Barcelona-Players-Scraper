import json
from bs4 import BeautifulSoup 
import requests as req 
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def scrape_players_data():
     result = []
     web = req.get('https://www.fcbarcelona.fr/fr/football/equipe-premiere/joueurs') 
     soup = BeautifulSoup(web.text, 'lxml')  
     images = soup.find_all('img',class_='team-person__image')
     player_names = soup.find_all('span',class_='team-person__last-name js-team-list-player-last-name')
     player_numbers = soup.find_all('span',class_='team-person__number')
     player_positions = soup.find_all('li',class_='team-person__position-meta') 
     player_link = soup.find_all('a',class_="team-person js-focus-container")
     
     for i in range(len(player_names)):
         webImage = req.get(player_link[i].get("href")) 
         soupImage = BeautifulSoup(webImage.text, 'lxml')  
         image =soupImage.find('img',class_='player-hero__img')
         player_data = {
             "image": image["src"],
             "position": player_positions[i].text,
             "name": player_names[i].text,
             "number": player_numbers[i].text
         }
         result.append(player_data)
 
     return result
    

@app.route('/getPlayers', methods=['GET'])
def _getAllPlayers():
    try:
        data_list = scrape_players_data()
        return jsonify(data_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

def scrape_standings_data():
     result = []
     standings = []
     played=0
     win=0
     draw=0
     lost=0
     webStandings = req.get('https://www.fcbarcelona.com/en/football/first-team/standings') 
     soupStandings = BeautifulSoup(webStandings.text, 'lxml')  
     images = soupStandings.find_all('img',class_='badge-image badge-image--40 js-badge-image')
     pts = soupStandings.find_all('td',class_='table-stat-row table-stat-row--points')
     numbers = soupStandings.find_all('td',class_='table-stat-row')
     team_names = soupStandings.find_all('span',class_='team-row__name--short')
     last_updated = soupStandings.find('div',class_='standings-pane-header__last-updated')
     result.append({"date":last_updated.text})
    
     for i in range(len(images)):
        
        if(i<1):
         played=i+1
         win=i+2
         draw=i+3
         lost=i+4
        elif (i>=1):
         played=played+8
         win=win+8
         draw=draw+8
         lost=lost+8

        
        data = {
             "image": "https:"+(images[i]["src"]).replace(";",""),
             "pts": pts[i].text.replace("\n","").replace(" ",""),
             "played": numbers[played].text.replace("\n","").replace(" ",""),
             "win": numbers[win].text.replace("\n","").replace(" ",""),
             "draw": numbers[draw].text.replace("\n","").replace(" ",""),
             "lost": numbers[lost].text.replace("\n","").replace(" ",""),
             "team": team_names[i].text.replace("\n","").replace(" ",""),
                }
        standings.append(data)
     result.append({"standings":standings})
     
     return result

@app.route('/standings', methods=['GET'])
def _getStandings():
    try:
        
        return jsonify(scrape_standings_data())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
