from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi

ca = certifi.where(

)
client = MongoClient('mongodb+srv://test:sparta@cluster0.wlcw8cv.mongodb.net/luster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.trabucket

@app.route('/')
def home():
    return render_template('main.html')


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://travel.naver.com/domestic', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')



trabuckets = soup.select('#DomesticHome > div.season_Seasonals__3IGq4 > ul > li')


for trabucket in trabuckets:
    code = trabucket.select_one('div > a > div.item_head__eQx5Y > b').text
    title = trabucket.select_one('div > a > div.item_head__eQx5Y > span').text
    sub_title = trabucket.select_one('div > a > div.item_head__eQx5Y > i').text
    desc = trabucket.select_one('div > a > div.item_description__1ENSh').text
    tag = trabucket.select_one('div > a > div.item_keywords__ZF5rC').text
    image = trabucket.select_one('div > div.item_images__3k522 > a')

    doc = {
        'code':code,
        'title':title,
        'sub_title':sub_title,
        'desc':desc,
        'tag':tag,
        'image':image,
    }

    # db.travel.delete_one(doc)
    # db.travel.insert_one(doc)


@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/hi', methods=["GET"])
def trabucket_get():
    travel_list = list(db.travel.find({}, {'_id': False}))
    return jsonify({'trabuckets':travel_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=3000, debug=True)