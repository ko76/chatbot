from flask import Flask, request, jsonify, Response
import requests
import json
import os
import xml.etree.ElementTree as ET
import datetime
app = Flask(__name__)
url = "https://api.hfs.purdue.edu/menus/v2/locations/"
locations = ["Wiley", "Ford", "Hillenbrand", "The Gathering Place", "Earhart", "Windsor"]
verify_token = os.getenv("VERIFY_TOKEN")
ti1 = datetime.datetime.now()
time = ti1.strftime("%m-%d-%Y")
access_token = os.getenv("ACCESS_TOKEN")

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
            if(m==None):
                return "no message found"
            userm = m[0].get('message')
            if(userm==None):
                return "no message found"
            useri = m[0].get('sender')
            if(useri==None):
                return "no sender"
            
            user_message = userm.get('text')
            user_id = useri.get('id')
            if(user_id==None):
                return "no sender"
            returnmessage = purdueInfo(user_message)
            
            response = createRes(returnmessage,user_id)
            headers = {'Content-type': 'application/json'}
            requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + access_token, data=json.dumps(response),headers = headers)
    return "ok"


def createRes(message,userid):
    response = {
        'messaging_type': 'RESPONSE',
        'recipient': {'id': userid},
        'message': {'text': 'hanzen sucks' }
    }
    return response

def purdueInfo(message):
    split_string = message.split(" ")
    mess = ""
    if len(split_string) < 4:
        mess = "none"
    elif message.lower() == "list all dining halls".lower():
        mess = "all"
    elif split_string[3] == "today":
        strn = split_string[1]
        mess = "does not exist"
        for loc in locations:
            if loc == strn:
                mess = loc
    else:
        mess = "none"
    if mess == "none":
        return "could not understand " + message
    elif mess == "does not exist":
        return mess
    return purdueDining(mess)

def purdueDining(text):
    message =  ""
    if text == "all":
        for loc in locations:
            message += loc
    else:
        header={"Accept":"application/json"}
        res = requests.get(url+text+"/"+time,headers=header).json()
        message = text
        print(res["Location"])
        mealjson = res["Meals"]
        for x in list(range(len(mealjson))):
            print(mealjson[x]["Name"].encode('ascii', 'ignore'))
            for y in list(range(len(mealjson[x]["Stations"]))):
                print("-------")
                print("----"+mealjson[x]["Stations"][y]["Name"].encode('ascii', 'ignore') + "| font=HelveticaNeue-Bold")
                for z in list(range(len(mealjson[x]["Stations"][y]["Items"]))):
                    print("----"+mealjson[x]["Stations"][y]["Items"][z]["Name"].encode('ascii', 'ignore'))
                print(" ")
        
        

    return message

if __name__=='__main__':
    app.run(debug=True,use_reloader=True)