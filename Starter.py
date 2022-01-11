import subprocess as sub
import json

# Object containing all the config variables we need.
# INSERT your data here and replace the example data.
conf = {
    "STEAM_URL": "https://store.steampowered.com/app/1466860/Age_of_Empires_IV/",  # This is the steam webpage for your game. The one with the green 'Add to Cart' buttons!
    "GAME_TITLE_PRETTY": "Age of Empires IV", 
    "PROV_SMS_EXT": "vtext.com", 
    "PHONE_NUM": "1234567899",
    "EMAIL": "exampleEmail@gmail.com",
    "EMAIL_PASS": "mY_$ecREt_pA$swoRd",
    "NOTIFY_PRICE": 50.00,
    "QUERY_INTERVAL_SEC": 6 * 3600
}
# This was my pythonwPath for example. This may be different on your machine, depending on your installed version of python.
pythonwPath = "C:/Users/<your-user>/AppData/Local/Programs/Python/Python38/pythonw.exe"
scriptPath = "game_status.pyw"

# Start the game watcher in a separate process
sub.Popen([pythonwPath, scriptPath, json.dumps(conf) ])