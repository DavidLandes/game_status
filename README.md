# game_status
Monitor Steam and get notified when the price reaches a set threshold

## Required Dependencies...
- install python
- Pythonw    `pip3 install pythonw`
- Systray    `pip3 install infi.systray`

## Getting Started...
A json object full of config variables is required as a commandline argument to properly execute the script.
- The config contains sensitive info: phone #, email, email password, etc... 

1. Open `Starter.py`. It should look like this:

```py
import subprocess as sub
import json

# Object containing all the config variables we need.
# INSERT your data here and replace the example data.
conf = {
    "STEAM_URL": "https://store.steampowered.com/app/1466860/Age_of_Empires_IV/",  # This is the steam webpage for your game. The one with the green 'Add to Cart' buttons!
    "GAME_TITLE_PRETTY": "Age of Empires IV", 
    "PROV_SMS_EXT": "vtext.com",        # The phone service provider.
    "PHONE_NUM": "1234567899",          # The phone number to receive notification texts.
    "EMAIL": "exampleEmail@gmail.com",  # Email that will send the message.
    "EMAIL_PASS": "mY_$ecREt_pA$swoRd", # Password for the email account.
    "NOTIFY_PRICE": 50.00,              # Notify at this price or below.
    "QUERY_INTERVAL_SEC": 6 * 3600      # How often should the website be checked?
}

# This was my pythonwPath for example. This may be different on your machine, depending on your installed version of python.
pythonwPath = "C:/Users/<your-user>/AppData/Local/Programs/Python/Python38/pythonw.exe"
scriptPath = "game_status.pyw"

# Start the game watcher in a separate process
sub.Popen([pythonwPath, scriptPath, json.dumps(conf) ])
```

2. Fill in the config variables with your own info.
3. Execute `Starter.py` with python. A tray application appears. Hover over it to see the latest price of your game.
4. A `log.txt` file will be generated when the app begins. You can also look here for information. Any bugs can be reported on Github.

### Option 2
- Remove the `loadArgs()` function and manually hard-code the config variables, defined at the top of `game_status.pyw`.
    - Look at the config example in `Starter.py` for help.
- Execute the script

