from flask import Flask,render_template,jsonify,request
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests,certifi

app = Flask(__name__)
client = MongoClient('mongodb+srv://sparta:jungle@cluster0.jxnelzd.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=certifi.where())
db = client.notepad

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/memo",methods=['GET'])
def get_articles():
    articles = list(db.article.find({},{'_id': 0}))
    return jsonify({'result':'success','articles' : articles});

@app.route("/memo",methods=['POST'])
def post_articles():
    data = scrapping(request.form['url_give'],request.form['comment_give'])
    db.article.insert_one(data)
    return jsonify({'result':'success'})

@app.route("/memo/delete",methods=['POST'])
def delete_articles():
    print(request.form['url_give'])
    db.article.delete_one({'url':request.form['url_give']})
    return jsonify({'result':'success'})

def scrapping(url,comment):
    print(url)
    print(comment)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(requests.get(url, headers=headers).text,'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']
    img = soup.select_one('meta[property="og:image"]')['content']

    article = {'url':url,'title':title,'desc':desc,'img':img,'comment':comment}
    return article

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)