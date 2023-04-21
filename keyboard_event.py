import time
import keyboard
import threading

global comment
comment = 'hello world'

class agent():
    def __init__(self):
        self.comment = 'hello world'
        self.keyboard_thread = threading.Thread(target=self.keyboard_event_loop)
        self.keyboard_thread.daemon = True
        self.keyboard_thread.start()
        
    def keyboard_event_loop(self):
        while True:
            event = keyboard.read_event()
            self.comment = event.name
            #print(f'Key {event.name} {"pressed" if event.event_type == "down" else "released"}')

    
# Start the keyboard event detection loop in a separate thread


# Do some other work in the main thread
a = agent()
while True:
    print(a.comment)