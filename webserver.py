#!/usr/bin/python3

from flask import Flask, jsonify, request
from copy import copy, deepcopy
import pycurl
from io import BytesIO
import json

app = Flask(__name__)

#should include a mutex lock for messages structure
messages = []

phones = []

phoneToPort = {}
host = '127.0.0.1'

@app.route("/messages", methods=["GET"])
def getMsgs():
    return jsonify(messages)

@app.route("/messages/<id>", methods=["GET"])
def getMsg(id):

    mylist=list(filter(lambda x: x['uni_id'] == id, messages))
    mylistcpy = deepcopy(mylist)
    #only send the message to the phone, not who sent it
    for item in mylistcpy:
        item.pop('uni_id', None)

    #remove message from broker after distribution to phone
    for i in range(len(messages)-1, -1, -1):
        if messages[i]["uni_id"] == id:
            messages.pop(i)

    return jsonify(mylistcpy)

@app.route("/uni_id", methods=["POST"])
def addPhone():
    uni = request.json['uni_id']
    port = request.json['port']
    data = {'uni_id': uni}
    phones.append(data)
    phoneToPort[uni] = port

    return 'success\n'

@app.route("/sent_message", methods=["POST"])
def addMessage():
    uni = request.json['uni_id']
    mess = request.json['mess']
    t = request.json['time']
    port = phoneToPort.get(uni)
    data = [{'uni_id': uni, 'mess': mess, 'time': t}]
    
    messages.append(data)

    url_conn = 'http://' + host + ':' + str(port)
    send_post(url_conn + '/phone/' + uni, json.dumps(data))

    return 'success\n'

#send a post request using pycurl
def send_post(url_str, data):
    crl = pycurl.Curl()
    crl.setopt(crl.URL, url_str)
    crl.setopt(pycurl.HTTPHEADER, ['Content-Type:application/json'])
    crl.setopt(pycurl.POST, 1)
    crl.setopt(pycurl.POSTFIELDS, data)
    crl.perform()
    crl.close()


if __name__ == '__main__':
    app.run(port=8080)