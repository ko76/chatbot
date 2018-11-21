from flask import Flask, request, jsonify, Response
import requests
import json
import os
app = Flask(__name__)
url = "https://api.hfs.purdue.edu/menus/v2/locations/"
locations = ["Wiley", "Ford", "Hillenbrand", "The Gathering Place", "Earhart", "Windsor"]
verify_token = os.getenv("VERIFY_TOKEN")
access_token = os.getenv("ACCESS_TOKEN")
#print(verify_token)

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
        returnmessage = ""
        for entry in entries:
            m= entry.get('messaging')
            if(m=='None'):
                return "no message found"
            userm = m[0].get('message')
            if(userm=='None'):
                return "no message found"
            useri = m[0].get('sender')
            if(useri=='None'):
                return "no sender"
            
            user_message = userm.get('text')
            user_id = useri.get('id')
            if(user_id=='None'):
                return "no sender"
            loc = getLoc(user_message)
            if loc == "all":
                for l in locations:
                    returnmessage += l + " "
            elif loc == "none":
                returnmessage += "none"
            else:
                returnmessage += loc + ' '
            
            response = createRes(returnmessage,user_id)
            
            headers = {'Content-type': 'application/json'}
            requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + access_token, data=json.dumps(response),headers = headers)
    return "ok"



def createRes(message,userid):
    response = {
        'messaging_type': 'RESPONSE',
        'recipient': {'id': userid},
        'message': {'text': "hanzen sucks"}
    }
    return response

def getLoc(message):
    split_string = message.split(" ")
    if len(split_string) < 4:
        return "cannot " + message
    if message.lower() == "list all dining halls".lower():
        return "all"
    elif split_string[3] == "today":
        strn = split_string[1]
        
        for loc in locations:
            if loc == strn:
                return strn
        return "no such dining hall"
    return "cannot " + message

if __name__=='__main__':
    app.run(debug=True,use_reloader=True)