#!/usr/bin/python3
import pycurl
import time
import json
import collections
import datetime
import iso8601
import uuid
from collections import namedtuple
from flask import Flask, request
import socket
import logging
from werkzeug.serving import make_server
import threading

#class Phone is a definition of scalable client.
# We can create many Phone Objects within this program
# the class wraps the logic needs to store the user's number and recieve/send messsages in parallel
class Phone:
    unique_id =""
    port = '8080'
    host = '127.0.0.1'
    url_conn = 'http://' + host + ':' + port
    dict_messages = collections.OrderedDict()
    TextMessage = namedtuple('TextMessage', ['message', 'time'])

    def __init__(self):
        self.app = Flask(__name__)
        logging.getLogger('werkzeug').disabled = True
        self.app.logger.disabled = True
        self.server = None
        self.thread = None

    def set_uid(self, uid):
        self.unique_id = str(uid)
        self.m_port = get_free_port()
        #enroll the number/email in the webserver
        data = {'uni_id': self.unique_id, 'port': self.m_port}
        body_as_json_string = json.dumps(data)

        send_post(self.url_conn +'/uni_id', body_as_json_string)

        self.app.add_url_rule(
            rule='/phone/' + self.unique_id,   # Dynamic route
            endpoint='recv',                   # Unique name for the route
            view_func=self.recv,               # Function to handle requests
            methods=['POST']                   # Allowed HTTP methods
        )
    
    def recv(self):
        json_str = request.data.decode('utf-8')
        json_obj = json.loads(json_str.strip())

        for lst_item in json_obj:
            self.dict_messages[str(uuid.uuid4())] = self.TextMessage(lst_item['mess'], lst_item['time'])
        return 'success\n'
    
    def show_min_max_key(self):
        print('Min index =%s, Max index =%s' % (min(list(self.dict_messages.keys())),max(list(self.dict_messages.keys()))))

    def show_msgs_start_stop(self, start_idx, stop_idx):
        for key, value in self.dict_messages.items():
            if (int(key) >= int(start_idx) and int(key) <= int(stop_idx)):
                print(key,value)
    
    def show_msgs(self):
        for key, value in self.dict_messages.items():
            print(f"message ID:{key} message time:{value.time} message: {value.message}")

    def del_msg(self, del_key):
        if del_key in self.dict_messages:
            del self.dict_messages[del_key]
        else:
            print(f"could not delete message {del_key} because it could not be found")

    #submit a message to a defined recipient 
    def sendmsg(self, tonumber, themsg):
        data = {'uni_id': str(tonumber), 'mess': str(themsg), 'time': datetime.datetime.utcnow().isoformat()}
        body_as_json_string = json.dumps(data)

        send_post(self.url_conn +'/sent_message', body_as_json_string)

    # start receiving messages
    def start(self):
        self.server = make_server(self.host, self.m_port, self.app)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()

    def shutdown(self):
        if self.server:
            self.server.shutdown()
            self.thread.join()

#send a post request using pycurl
def send_post(url_str, data):
    crl = pycurl.Curl()
    crl.setopt(crl.URL, url_str)
    crl.setopt(pycurl.HTTPHEADER, ['Content-Type:application/json'])
    crl.setopt(pycurl.POST, 1)
    crl.setopt(pycurl.POSTFIELDS, data)
    crl.perform()
    crl.close()

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))  # Let the OS choose a free port
        return s.getsockname()[1]

#accepts a Phone object and waits for keyboard input
def get_input_from_user(device):
    quit = False

    try:
        while not quit:
            inp = input("Please enter your operation (s=(submit message), f=(fetch all inbox messages), L=(fetch messages using start stop index), d=(delete message), q=(quit)):\n")
            if inp == "s":
                number_value = input("Please enter the recipient phone number:\n")
                message_value = input("Please enter the message you would like to send:\n")
                device.sendmsg(number_value, message_value)
            elif inp == "f":
                device.show_msgs()
            elif inp == "d":
                del_value = input("Please enter the message ID you would like to delete:\n")
                device.del_msg(del_value)
            elif inp == "L":
                device.show_min_max_key()
                min_value = input("Please enter the start index:\n")
                max_value = input("Please enter the stop index:\n")
                print("Messages:\n")
                device.show_msgs_start_stop(min_value,max_value)
                print("\n")
            elif inp == "q":
                quit = True
                device.shutdown()
            else:
                print("unknown input")
    except:
        pass

#main currently supports only one Phone object
def main():

    print("Welcome to your text message service.\n")
    uid_value = input("Please enter your phone number:\n")

    current_user = Phone()
    current_user.set_uid(uid_value)
    current_user.start()
    get_input_from_user(current_user)

main()