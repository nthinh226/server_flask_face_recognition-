## Run server:
    FLASK_APP=src/server.py flask run

## Run ngrok:
# Docker:
    docker run -it -e NGROK_AUTHTOKEN=2F2U0uArZ2hQa4xGqf7gJKRqdhN_7rnDG3RXmHe2fsFN9nJZy ngrok/ngrok http 5000

# Local:
    ngrok config add-authtoken 2F2U0uArZ2hQa4xGqf7gJKRqdhN_7rnDG3RXmHe2fsFN9nJZy
    ngrok http 5000