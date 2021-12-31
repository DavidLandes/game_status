# game_status
Monitor Steam and get notified when the price reaches a set threshold


## Getting Started...
A json object full of config variables is required as a commandline argument to properly execute the script.
- The config contains sensitive info: phone #, email, email password, etc... 

### Option 1
- Create a separate python 'startup' script to provide the config & execute. Example shown below...
- Execute this 'starter' script to handle passing in the sensitive config data.

```py
import subprocess as sub
import json

# Object containing all the config variables we need.
# INSERT your data here and replace the example data.
conf = {
    "STEAM_URL": "https://store.steampowered.com/app/1466860/Age_of_Empires_IV/", 
    "GAME_TITLE_PRETTY": "Age of Empires IV", 
    "PROV_SMS_EXT": "vtext.com", 
    "PHONE_NUM": "1234567899",
    "EMAIL": "exampleEmail@gmail.com", # sorry, for now this has to be a 'gmail' account
    "EMAIL_PASS": "mY_$ecREt_pA$swoRd",
    "NOTIFY_PRICE": 50.00,
    "QUERY_INTERVAL_SEC": 6 * 3600
}

# This is the absolute path where pythonw is stored on your machine. 
# pythonw.exe is the same as python.exe exxcept it executes without an open terminal window.
pythonwPath = "C:/Users/<your-user>/AppData/Local/Programs/Python/Python38/pythonw.exe"

# Path to the game_status script to be executed.. This example uses relative path, but can also be absolute path.
scriptPath = "game_watcher/game_status.pyw"

# Start the game watcher in a new separate process
sub.Popen([pythonwPath, scriptPath, json.dumps(conf) ])
```

### Option 2
- Remove the 'loadArgs()' function and manually hard-code the config variables, defined at the top of the script.
- Execute the script

