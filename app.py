from flask import Flask
from flask import request
from twilio.rest import Client
from marketstack import get_stock_price ##bring it from 'marketstack.py'
import os

app = Flask(__name__)

ACCOUNT_ID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_TOKEN = os.environ['TWILIO_AUTH_TOKEN']

TWILIO_NUMBER = 'whatsapp:+14155238886'
client = Client(ACCOUNT_ID, TWILIO_TOKEN)

#******FIRST TEST ONLY TO SEE IF IT WORKS******
@app.route("/")
def hello():
    return{
        "Result": "You successfully created the first route!"
    }

def send_msg(msg, recipient):
    client.messages.create(
        from_=TWILIO_NUMBER,
        body=msg,
        to=recipient
    )


def process_msg(msg):
    response = ""
    if msg == "hi":
        response = "Hello, Welcome to the stock market bot!"
        response += "Type 'sym:<stock_symbol>' to know the price of the stock."
    elif 'sym:' in msg:
        data = msg.split(":")
        stock_symbol = data[1]
        stock_price = get_stock_price(stock_symbol)
        last_price = stock_price['last_price']
        response = "The stock price of " + stock_symbol + " is: $" + str(last_price)
    else:
        response = "Please type hi to get started"
    return response

#
@app.route("/webhook", methods=["POST"])
def webhook():
    #**************TEST ONLY*****************
    # message = request.form["message"]
    # return{
    #    "Result": message
    # }

    #python Debugger and when connect ngrok to Twilio
    # import pdb
    # pdb.set_trace()
    # return "ok", 200

    f = request.form
    msg = f['Body']
    sender = f['From']
    response = process_msg(msg)
    send_msg(response, sender)
    return "ok", 200

#Steps

# 0. get account id and token from Twilio and set in venv
# -> export TWILIO_ACCOUNT=<number>, export TWILIO_TOKEN=<number>

# 1. import Client from twilio -> done
# 2. initialise client -> done

# 3. write a function to process msg -> done
# 4. write a function to send message -> done
# 6. generate a response -> done

# 7. check response in Whatsapp


