from flask import Flask, request, jsonify, Response
import requests
import json
import os
app = Flask(__name__)

verify_token = os.getenv("VERIFY_TOKEN")
access_token = os.getenv("ACCESS_TOKEN")


@app.route("/")
def default():
    return "default"

@app.route("/webhook",methods=['GET'])
def verify():
    if request.args.get('hub.verify_token') == verify_token:
        return request.args.get('hub.challenge')
    return "Wrong verify token"

@app.route("/webhook",methods=['POST'])
def webhook():
    return "hi"