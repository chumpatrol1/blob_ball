# This isn't tied to any specific game state - instead it can pop up at any time

class Node:
    def __init__(self, entry, timer = 60):
        self.entry = entry # This is the popup contained
        self.surface = None
        self.timer = timer # This is the time left on this particular entry
        self.next = None # This is the next Node

    def create_surface(self):
        pass # Creates a Pygame Surface that gets assigned to self.surface

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def process(self):
        pass

class ControllerPopUp:
    def __init__(self, controller, event_id):
        self.controller_number = controller
        self.event_id = event_id
        self.controller_name = controller

    def __str__(self):
        return f"Event: {self.event_id}, Controller: {self.controller_number}"

def create_controller_pop_up(controller, event_id):
    if(event_id == 9 or event_id == -2): # Event ID 9 is ignored
        return
    new_pop_up = ControllerPopUp(controller, event_id)
    print(new_pop_up)

controller_popup_queue = Queue()

# Intended Control Flow
# Create Controller Pop Up is called
# A new ControllerPopUp is created based off of the Joystick Event
# > Stores the Controller ID
# > Stores an integer determining what event happened
# > > -2: No Connection Event
# > > -1: Controller disconnected (P)
# > > 0: Controller detected (P)
# > > 1: Controller assigned to Port 1 without affecting Port 2 (P)
# > > 2: Controller assigned to Port 2 without affecting Port 1 (P)
# > > 3: Controller assigned to Port 1, unbinding from Port 2 (P)
# > > 4: Controller assigned to Port 2, unbinding from Port 1 (P)
# > > 5: Controller assigned to Port 1, replacing old Port 1. Generates either Event 2 or event 7. (P)
# > > 6: Controller assigned to Port 2, replacing old Port 2. Generate Event 1 or Event 8. (P)
# > > 7: Controller assigned to Port 1, unbinding the old Port 1 Controller without updating Port 2. (P)
# > > 8: Controller assigned to Port 2, unbinding the old Port 2 Controller without updating Port 1. (P)
# > > 9: Controllers swapped. Ignored. Might also be empty
# > > 10+: Controllers swapped. Event number is sum of Port 1 (stored), Port 2 and 10. (P)
# > > EX: Swap controllers 2 (P1) and 1 (P2). Controller is 2, Event # is 13.
# > Stores the Controller's Name
# A new Node is created with the ControllerPopUp as the entry
# > The Node starts by containing the ControllerPopUp
# > The timer is set to the specified start value (this is different for different events)
# Queue appends the new Node to the tail of the Queue
# > If the Queue is empty, head and tail are assigned to the Node
# > Otherwise, the tail.next gets updated (it normally is None)

# Once per frame, Queue.process() is called by a function in display_pop_up.py
# > Get the Head Node
# > Check if the Surface is not None. If it is None, generate the surface based on the PopUp type
# > > Display Pop Up py will run a function that converts event ID's into templates
# > > Game Surface will return and be stored by the Node
# > Grab its Surface and Timer - this controls the appearance and position of the popup
# > Reduce the Node Timer by 1
# > If the Node Timer is 0, remove references to the current Head and reassign
# > Return Surface and Timer
# > Display the Surface at the position specified by the timer