from flask import Flask, request, jsonify, Response
import requests
import json
import os
app = Flask(__name__)

verify_token = os.getenv("VERIFY_TOKEN")
access_token = os.getenv("ACCESS_TOKEN")
print(verify_token)

@app.route("/",methods=['GET','POST'])
def default():
    return "def"

@app.route("/webhook",methods=['GET'])
def verify():
    if request.args.get('hub.verify_token') == verify_token:
        return request.args.get('hub.challenge')
    return "Wrong verify token"

@app.route("/webhook",methods=['POST'])
def webhook():
    data = json.loads(request.data)
    entries = data["entry"]
    if data["object"] == "page":
        for entry in entries:
            user_message = entry['messaging'][0]['message']['text']
            user_id = entry['messaging'][0]['sender']['id']
            response = createRes(user_message,user_id)
            
            requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + access_token, data=response)
    return "ok"


def createRes(message,userid):
    response = {
        'recipient': {'id': userid},
        'message': {'text': message}
    }
    return response


if __name__=='__main__':
    app.run(debug=True,use_reloader=True)