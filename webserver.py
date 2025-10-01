#!/usr/bin/python3

from flask import Flask, jsonify, request
from copy import copy, deepcopy

app = Flask(__name__)

#should include a mutex lock for messages structure
messages = []

phones = []

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

    print(mylistcpy)

    return jsonify(mylistcpy)

@app.route("/uni_id", methods=["POST"])
def addPhone():
    uni = request.json['uni_id']
    data = {'uni_id': uni}
    phones.append(data)

    return 'success\n'

@app.route("/sent_message", methods=["POST"])
def addMessage():
    uni = request.json['uni_id']
    mess = request.json['mess']
    t = request.json['time']
    data = {'uni_id': uni, 'mess': mess, 'time': t}
    messages.append(data)

    return 'success\n'

if __name__ == '__main__':
    app.run(port=8080)