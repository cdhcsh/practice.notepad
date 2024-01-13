from flask import Flask, render_template,jsonify,request,pymongo
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/memo",methods=['GET'])
def get_articles():
    
    return jsonify({'result':'success','msg':'GET'});

@app.route("/memo",methods=['POST'])
def post_articles():
    return jsonify({'result':'success','msg':'POST'});





if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)