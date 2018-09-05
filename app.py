from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import json
import os
import random
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    return '챗 봇 페이지 입니다!!'
    
@app.route('/keyboard')
def keyboard():
    keyboard =  {
                  "type" : "buttons",
                "buttons" : ["메뉴", "로또", "고양이", "영화"]
                }
    json.keyboard = json.dumps(keyboard)
    return json.keyboard
    
@app.route("/message", methods=["POST"])
def message():
    # content라는 key value를 msg에 저장
    msg = request.json["content"]
    img_bool = False
    
    if msg == "메뉴":
        menu = ["20층", "멀캠식당", "찹쌀탕수육", "급식"]
        return_msg = random.choice(menu)
    
    elif msg == "로또":
        numbers = list(range(1,46))
        pick = random.sample(numbers, 6)
        return_msg = str(sorted(pick))
    
    elif msg == "고양이":
        img_bool = True
        url = "https://api.thecatapi.com/v1/images/search?mime_types=jpg"
        req = requests.get(url).json()
        img_url = req[0]['url']
        return_msg = "고양"
    
    elif msg == "영화":
        img_bool = True
        url = "https://movie.naver.com/movie/running/current.nhn"
        req = requests.get(url).text
        doc = BeautifulSoup(req, 'html.parser')

        title_tag = doc.select("dt.tit > a")
        star_tag = doc.select("div.star_t1 > a > span.num")
        reserve_tag = doc.select("div.star_t1.b_star > span.num")
        img_tag = doc.select('div.thumb > a > img')

        movie_dic = {}
        for i in range (0,10):
            movie_dic[i] = {
               "title":title_tag[i].text,
                "star":star_tag[i].text,
                "reserve":reserve_tag[i].text,
                "img":img_tag[i].get("src")
           }
    
        pick_movie = movie_dic[random.randrange(0,10)]
        
        return_msg = "%s/평점:%s/예매율:%s" % (pick_movie['title'],pick_movie['star'],pick_movie['reserve'])
        img_url = pick_movie["img"]
    
    else:
        return_msg = "현재 지원하지 않는 기능입니다."
        
    if img_bool == True:
        json_return = {
        "message": {
            "text": return_msg,
            "photo":{
                "url": img_url,
                "width":720,
                "height":900
            }
        },
        "keyboard": {
            "type" : "buttons",
            "buttons" : ["메뉴", "로또", "고양이", "영화"]
        }
    }
    # 카톡에서 명령어 입력시 text 에 있는 문구가 출력됨
    else:
        json_return = {
            "message": {
                "text":return_msg
            },
            "keyboard": {
                "type" : "buttons",
                "buttons" : ["메뉴", "로또", "고양이", "영화"]
            }
        }
    return jsonify(json_return)
    
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))