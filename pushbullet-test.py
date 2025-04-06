from pushbullet import Pushbullet 
from datetime import datetime  # Import datetime module
import json

with open('realconfig.json') as jason: # format in fakeconfig.json
    config = json.load(jason)

pb = Pushbullet(config['PB_API_KEY'])


formatted_time = datetime.now().strftime('%I:%M %p')  # Format time as 12-hour clock with AM/PM
pb.push_note('hoon alert', f'hi baby {formatted_time}')
