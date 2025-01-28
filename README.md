# text_message_service

Install Flask:
```bash
pip3 install flask
```

Install pycurl:
```bash
pip3 install pycurl
```

## style checking
Install pycodestyle:
```bash
pip3 install pycodestyle
```

## run webserver
Execute "webserver.py" script to start managing requests from clients. The server acts like a broker.

The server will run on localhost port 8080

You can use curl to view messages for a number/email:
curl http://127.0.0.1:8080/messages/<id>

You can use curl to submit a new message: 
curl -X POST -H "Content-Type: application/json" -d '{"uni_id": "<id>"}' http://127.0.0.1:8080/uni_id

## run txtmsgs
Execute "txtmsgs.py" script to start receiving/sending messages. You can run many clients in parallel. Follow the prompts on the console.

## Future improvments TBD
 - Limit multiple clients with the same client ID so that we do not run into race conditions for messages.
 - Use date/time sorting instead of integer sorting to make the project more realistic.
 - Improve the graceful shutdown.