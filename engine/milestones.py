from json import loads, dumps
# Handles milestones

milestones = {
    "blob_unlocks": {},
    "cosmetic_unlocks": {},
    "milestones": {},
    "medals": {},
}

def add_milestone(cwd, event):
    global milestones
    try:
        with open(cwd + "/saves/notices.txt", "r") as milestonedoc:
            milestones = loads(milestonedoc.readline())
    except:
        with open(cwd + "/saves/notices.txt", "w") as milestonedoc:
            milestonedoc.write(dumps(milestones))

    pop_type_to_category = {
        0: "blob_unlocks",
        1: "cosmetic_unlocks",
        2: "milestones",
        3: "medals",
    }

    blurb = ""
    if(event.pop_up_type == 0):
        blurb = f"You unlocked {event.info[1]}"
    elif(event.pop_up_type == 1):
        blurb = f"You unlocked {event.info[1]}"
    elif(event.pop_up_type == 3):
        blurb = f"You achieved {event.info[1]}"

    try:
        milestones[pop_type_to_category[event.pop_up_type]][event.time_notified] = {"blurb": blurb, "time": event.time_notified}
    except Exception as ex:
        print(ex)

    with open(cwd + "/saves/notices.txt", "w") as milestonedoc:
            milestonedoc.write(dumps(milestones))
