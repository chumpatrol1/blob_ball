# This isn't tied to any specific game state - instead it can pop up at any time

class Node:
    def __init__(self, entry, timer = 120):
        self.entry = entry # This is the popup contained
        self.surface = None
        self.surface2 = None
        self.fade_in = 8
        self.timer = timer # This is the time left on this particular entry
        self.next = None # This is the next Node

    def create_surface(self):
        pass # Creates a Pygame Surface that gets assigned to self.surface

    def __str__(self):
        return str(self.entry) + f"\nTimer: {self.timer}\n"

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def process(self):
        if(self.head):
            
            self.head.timer -= 1

            if(self.head.fade_in >= 0):
                self.head.fade_in -= 1

            if(self.head.timer <= 0):
                self.head = self.head.next
            
        return self.head

    def add_item(self, entry):
        if(self.head == None):
            self.head = self.tail = entry
        else:
            self.tail.next = entry # Update the pointer of the tail.
            self.tail = entry # Update the tail.

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def __str__(self):
        ret_str = ""
        for i in self:
            ret_str += str(i)
        return ret_str

class GenericPopUp:
    def __init__(self, event_id):
        self.pop_type = "Generic"
        self.event_id = event_id

    def __str__(self):
        return f"Event: {self.event_id}"

class ControllerPopUp:
    def __init__(self, controller, event_id, name):
        # TODO: Declare a type? If I run type(ControllerPopUp) it should return something like "Controller Pop Up"
        self.pop_type = "Controller"
        self.controller_number = controller
        self.event_id = event_id
        self.controller_name = name

    def __str__(self):
        return f"Event: {self.event_id}, Controller: {self.controller_number}"

def create_generic_pop_up(event_id = 0):
    new_pop_up = GenericPopUp(event_id)
    new_entry = Node(new_pop_up)
    #print(new_pop_up)
    controller_popup_queue.add_item(new_entry)
    #print(controller_popup_queue)

def create_controller_pop_up(controller, name = "GCCA", event_id = -2):
    if(event_id == 9 or event_id == -2): # Event ID 9 is ignored
        return
    new_pop_up = ControllerPopUp(controller, event_id, name)
    new_entry = Node(new_pop_up)
    #print(new_pop_up)
    controller_popup_queue.add_item(new_entry)
    #print(controller_popup_queue)

controller_popup_queue = Queue()
#create_controller_pop_up(0, event_id = -1)
#create_controller_pop_up(0, event_id = 0)
#create_controller_pop_up(0, event_id = 1)
#create_controller_pop_up(0, event_id = 2)
#create_controller_pop_up(0, event_id = 3)
#create_controller_pop_up(0, event_id = 4)
#create_controller_pop_up(0, event_id = 5)
#create_controller_pop_up(0, event_id = 6)
#create_controller_pop_up(0, event_id = 7)
#create_controller_pop_up(0, event_id = 8)
#create_controller_pop_up(0, event_id = 11)
#create_generic_pop_up(0)
# Intended Control Flow
# Create Controller Pop Up is called
# A new ControllerPopUp is created based off of the Joystick Event
# > Stores the Controller ID
# > Stores an integer determining what event happened
# > > -2: No Connection Event
# > > -1: Controller disconnected (P)
# > > > "Disconnected Controller #/Name/from game"
# > > 0: Controller detected (P)
# > > > "Connected Controller #/Name/Press DPad L/R to assign to port"
# > > 1: Controller assigned to Port 1 without affecting Port 2 (P)
# > > 2: Controller assigned to Port 2 without affecting Port 1 (P)
# > > > "Successfully assigned # to P"
# > > 3: Controller assigned to Port 1, unbinding from Port 2 (P)
# > > 4: Controller assigned to Port 2, unbinding from Port 1 (P)
# > > > "Successfully reassigned # to P"
# > > 5: Controller assigned to Port 1, replacing old Port 1. Generates either Event 2 or event 7. (P)
# > > 6: Controller assigned to Port 2, replacing old Port 2. Generates either Event 1 or Event 8. (P)
# > > > "Successfully replaced controller at P1 with #"
# > > 7: Controller assigned to Port 1, unbinding the old Port 1 Controller without updating Port 2. (P)
# > > 8: Controller assigned to Port 2, unbinding the old Port 2 Controller without updating Port 1. (P)
# > > > "Successfully unbound # from P"
# > > 9: Controllers swapped. Ignored. Might also be empty
# > > 10+: Controllers swapped. Event number is sum of Port 1 (stored), Port 2 and 10. (P)
# > > > "Successfully swapped # and #"
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

# Generic Popups
# > -1: Replay possibly corrupt
# > 0: Replay failed to load (incompatible version)
# > 1: Update available (available to download, that is!)
# > 2: Update unavailable (we are somehow on a developer build or are up to date)
# > 3: Failed to check for update (network connection error)