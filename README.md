# text_message_service

Install Flask:
```bash
pip3 install flask
```

Install pycurl:
```bash
pip3 install pycurl
```

Install iso8601:
```bash
pip3 install iso8601
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

## unit tests
Install pytest:
```bash
pip3 install pytest
```

Install pytest-cov:
```bash
pip3 install pytest-cov
```

Run tests:
```bash
./tools/unit_test.sh
```

## Future improvments TBD
 - Limit multiple clients with the same client ID so that we do not run into race conditions for messages.
 - Improve the graceful shutdown.