import datetime as dt
import time
import sys
import requests
import smtplib as mail
from html.parser import HTMLParser as parse
import json

# Default data. should be filled in with the config file read in from commandline args.
STEAM_URL = ""
GAME_TITLE_PRETTY = ""
PROV_SMS_EXT = ""
PHONE_NUM = ""
EMAIL = ""
EMAIL_PASS = ""
NOTIFY_PRICE = 0.0
QUERY_INTERVAL_SEC = -1
# AS of now, start has to be higher than the end time.. which should work fine for nighttime hours
QUIET_TIME_START = 22
QUIET_TIME_END = 6


# Store a purchase action taken from the website. 
# description - the title and version of the game.
# price - the listed cost of this version of the game.
class PurchaseAction:
    def __init__(self):
        self.description = ""
        self.price = "$0.00"

    def __str__(self):
        return f"{self.description}: {self.price}"


# Parser handles reading in all the data from the steam webpage.
# Create a Parse object and call Parser.feed("webpageHtmlString") to scrape out the price data.
# TODO ALERT: bad design calls for a new Parser to be created to reset all the flags after each feed(). We need a way to reset all the flags & the actions when complete, without clearing the actions before a user can access them.
class Parser(parse):

    def __init__(self):
        super().__init__()
        self.base_action = False
        self.descrip_flag = False
        self.price_flag = False
        self.newAction: PurchaseAction = None
        self.actions: list = []

    # Parse data within the html start tag.
    def handle_starttag(self, tag, attrs):
        try:
            # Find action.
            if tag == "div":
                for tup in attrs:
                    # Found the action.
                    if tup[0] == "class" and tup[1] == "game_area_purchase_game":
                        # Set a flag to tell handle_data() we've reached the game purchase action in the html.
                        self.base_action = True
                        self.newAction = PurchaseAction()

            # Found the description h1.
            if self.base_action and tag == "h1":
                # Set a flag to tell handle_data() we've reached the game title/description.
                self.descrip_flag = True


            if tag == "div":
                for tup in attrs:
                    # Found the price. game_purchase_price is when it's not on sale... discount_final_price is on sale after the discount.
                    if tup[0] == "class" and ("game_purchase_price" in tup[1] or "discount_final_price" in tup[1]):
                        # Set a flag to tell handle_data() we've reached the game price.
                        self.price_flag = True
                        self.base_action = False
        except Exception as e:
            print(f"There was an error handling start tag: {e}")

    # Parse content between a start tag and end tag.
    def handle_data(self, data):
        try:
            if self.descrip_flag:
                # Title/description has been reached in the html. parse out the data.
                self.newAction.description = str(data).strip()
                self.descrip_flag = False

            if self.price_flag:
                # price has been reached in the html. parse out the data.
                self.newAction.price = str(data).strip()
                self.price_flag = False

                # Price is last, make sure these are unset..
                self.descrip_flag = False
                self.base_action = False

                # Append the new Action.
                self.actions.append(self.newAction)
                self.newAction = None
        except Exception as e:
            print(f"There was an error handling data: {e}")
    
    # Handle data within the end tag.
    def handle_endtag(self, data):
        pass

# Log a message to the output file.
def log(message="", hasTimestamp=True):
    try:
        with open("./watcher_log.txt", "a") as f:
            if hasTimestamp:
                f.write(f"[{dt.datetime.now()}] - {message}\n")
            else:
                f.write(f"{message}\n")
    except Exception as e:
        print(f"There was a logging error: {e}")


# Read data stored in a list of PurchaseActions, log the game information, then send out a text message if the price condition is met.
def update_sources(purchaseActions: list):
    global NOTIFIER
    try: 
        actionsOnSale = ""
        # Log Actions.
        for action in purchaseActions:
            log(action)
            price = action.price.replace("$", "")
            if float(price) <= NOTIFY_PRICE:
                actionsOnSale += f"{action}\n\n"
                log("Price Condition Met!")
        
        # Notify user if necessary.
        if len(actionsOnSale) > 0 and not quiet_time_active():
            NOTIFIER.sendmail("Python Steam Notifier", f"{PHONE_NUM}@{PROV_SMS_EXT}", f"\r\n\r\n{dt.datetime.now().hour}:{dt.datetime.now().minute} - {GAME_TITLE_PRETTY} is on sale at Steam!\n{actionsOnSale}")
            time.sleep(5)
    except Exception as e:
        log(f"There was an error parsing the sources: {e}")
    
# Return if the current time is within quiet time hours. Quiet time prevents text messages from sending during a time interval.
# TODO: this if condition is fragile. the QUIET_TIME_START must be greater than QUIET_TIME_END to work correctly. this needs improved.
def quiet_time_active():
    if dt.datetime.now().hour >= QUIET_TIME_START or dt.datetime.now().hour <= QUIET_TIME_END:
        log("quiet time active")
        return True
    else:
        return False


# Load commandline args required for the app to run correctly. Expected argument is a json object with these config variables... all of them are required.
# {
#     "STEAM_URL": "<my-steam-game-web-url-here>", #web url of the steam game. the correct webpage contains the game info and importantly the purchase buttons with prices.

#     "GAME_TITLE_PRETTY": "My Game's Name", #the name of the game you will see when you get a notification message.

#     "PROV_SMS_EXT": "vtext.com", #other ISPs have different addresses.. verizon uses <phone-number@vtext.com>, just enter the domain only

#     "PHONE_NUM": "1234567899", #phone number no extra spaces or characters, just the number 

#     "EMAIL": "exampleEmail123@gmail.com", #this email is used to send the notification message to the given phone number.

#     "EMAIL_PASS": "<my-secret-email-password>",

#     "NOTIFY_PRICE": 50.00, #Maximum price reached to be notified 

#     "QUERY_INTERVAL_SEC": 6 * 3600, #How often should steam be checked for price changes
# }
def loadArgs():
    global STEAM_URL
    global GAME_TITLE_PRETTY
    global PROV_SMS_EXT
    global PHONE_NUM
    global EMAIL
    global EMAIL_PASS
    global NOTIFY_PRICE
    global QUERY_INTERVAL_SEC
    try:
        if len(sys.argv) == 2:
            config = json.loads(str(sys.argv[1]))
            STEAM_URL = config["STEAM_URL"]
            GAME_TITLE_PRETTY = config["GAME_TITLE_PRETTY"]
            PROV_SMS_EXT = config["PROV_SMS_EXT"]
            PHONE_NUM = config["PHONE_NUM"]
            EMAIL = config["EMAIL"]
            EMAIL_PASS = config["EMAIL_PASS"]
            NOTIFY_PRICE = float(config["NOTIFY_PRICE"])
            QUERY_INTERVAL_SEC = int(config["QUERY_INTERVAL_SEC"])
        else:
            raise Exception("Parsing error")
    except Exception as e:
        log(f"Argument error. Expected 1 argument, a config json string.\n{e}")
        exit()









#########################################################
#                     Main Entry
#########################################################

# Get commandline args.
loadArgs()

# Setup SMS notifier.
NOTIFIER = mail.SMTP("smtp.gmail.com", 587)
NOTIFIER.starttls()
NOTIFIER.login(EMAIL, EMAIL_PASS)

# Log the beginning of the session.
log(f"\n[LOG START {STEAM_URL}]", False)

# Continuously scrape the URL at the given interval.
while True:
    try:
        res = requests.get(STEAM_URL)
        p = Parser()
        p.feed(res.text)
        update_sources(p.actions)
        
    except Exception as e:
        log(f"Error: {e}")

    time.sleep(QUERY_INTERVAL_SEC)

