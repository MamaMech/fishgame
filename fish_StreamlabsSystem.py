# ---------------------------
#   Import Libraries
# ---------------------------
import os
import sys
import json
import codecs
import clr
import random

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))  # point at lib folder for classes / references

clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

# ---------------------------
#   [Required] Script Information
# ---------------------------
ScriptName = "Fish Game"
Website = "https://www.twitch.tv/mamamech"
Description = "TODO"
Creator = "MamaMech"
Version = "1.0.0"

# ---------------------------
#   [Required] Initialize Data (Only called on load)
# ---------------------------
def Init():
    return

# ---------------------------
#   [Required] Execute Data / Process messages
# ---------------------------
def Execute(data):
    pockets = get_pockets()
    museum = get_museum()
    if data.IsChatMessage() and data.GetParam(0).lower() == "!fish" and not Parent.IsOnUserCooldown("Fish Game","!fish",data.User) and (data.UserName not in pockets or pockets[data.UserName]["last_action"] != "fished"):
        choices = []
        for item, weight in loot:
            choices.extend([item] * weight)
        fish = random.choice( choices )
        value = sea[fish]
        write_pockets(data.UserName, fish, "fished")
        Parent.AddUserCooldown("Fish Game", "!fish", data.UserName, 300)
        Parent.SendStreamMessage(
            "You caught a " + fish + "! Would you like to \"!sell\" it for " + str(value) + " bells or donate it to the community museum (!blathers)?")
    elif data.IsChatMessage() and data.GetParam(0).lower() == "!fish" and pockets[data.UserName]["last_action"] == "fished":
        Parent.SendStreamMessage("You already have a fish in your pocket. Please \"!sell\" or donate it to \"!blathers\".")
        return
    elif data.IsChatMessage() and data.GetParam(0).lower() == "!fish" and Parent.IsOnUserCooldown("Fish Game","!fish",data.User):
        Parent.SendStreamMessage("You are on cooldown. Please wait 5 mins between fishing attempts.")
    elif data.IsChatMessage() and data.GetParam(0).lower() == "!sell":
        if data.UserName in pockets and pockets[data.UserName]["last_action"] == "fished":
            fish = pockets[data.UserName]["fish"]
            value = sea[fish]
            Parent.AddPoints(data.User, data.UserName, value)
            remove_pocket(data.UserName, "sold")
            Parent.SendStreamMessage("Thank you for your patronage. Here is your " + str(value) + " bells")
        else:
            Parent.SendStreamMessage("You don't have any fish in your pockets. Try \"!fish\" first!")
        return
    elif data.IsChatMessage() and data.GetParam(0).lower() == "!blathers":
        if data.UserName in pockets and pockets[data.UserName]["last_action"] == "fished":
            if data.UserName in pockets and pockets[data.UserName]["fish"] in museum:
                Parent.SendStreamMessage("That has already been donated. You can \"!sell\" it for bells instead.")
            else:
                add_museum(data.UserName, pockets[data.UserName]["fish"])
                remove_pocket(data.UserName, "donated")
                Parent.SendStreamMessage("Yes! We will gladly take these off your hands! ...Ah, there's no need for you to pull them all out! I'll handle the rest from here! Hoot hoo!")
        else:
            Parent.SendStreamMessage("You don't have any fish in your pockets. Try \"!fish\" first!")
        return

def write_pockets(UserName, fish, last_action):
    pockets = get_pockets()
    pockets[UserName] = {
        "last_action": last_action,
        "fish": fish
    }
    with open("pockets.json", 'w') as f:
        json.dump(pockets, f)
def get_pockets():
    try:
        with open("pockets.json") as f:
            return json.load(f)
    except:
        return {}
def add_pocket(username):
    entries = get_pockets()
    if username not in entries:
        entries.append(username)
        return write_pockets(entries)
    return True
def remove_pocket(UserName, last_action):
    pockets = get_pockets()
    pockets[UserName] = {
        "last_action": last_action,
    }
    if UserName in pockets:
        with open("pockets.json", 'w') as f:
            json.dump(pockets, f)
    return True
def remove_all_pockets():
    return write_pockets()
def write_museum(fish):
    museum = get_museum()
    museum.append(fish)
    with open("museum.json", 'w') as f:
        json.dump(museum, f)
def get_museum():
    try:
        with open("museum.json") as f:
            return json.load(f)
    except:
        return {}
def add_museum(UserName, fish):
    museum = get_museum()
    museum[fish] = {
        "UserName": UserName
    }
    with open("museum.json", 'w') as f:
        json.dump(museum, f)
    return True
def remove_museum(username):
    entries = get_museum()
    if username in entries:
        return write_museum(filter(lambda name: name != username, entries))
    return True
def remove_all_museum():
    return write_museum([])
# ---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
# ---------------------------
def Tick():
    return

#there are plenty of fish in the...
sea = {"Tadpole":10,
"Frog":12,
"Horse Mackeral":15,
"Crucian Carp":16,
"Bluegill":18,
"Anchovy":20,
"Crawfish":20,
"Pale Chub":20,
"Dace":24,
"Puffer Fish":25,
"Carp":30,
"Dab":30,
"Killifish":30,
"Yellow Perch":30,
"Black Bass":40,
"Freshwater Goby":40,
"Loach":40,
"Pond Smelt":40,
"Sea Bass":40,
"Neon Tetra":50,
"Squid":50,
"Zebra Turkeyfish":50,
"Ribbon Eel":60,
"Clownfish":65,
"Salmon":70,
"Catfish":80,
"Olive Flounder":80,
"Rainbowfish":80,
"Tilapia":80,
"Bitterling":90,
"Sweetfish":90,
"Butterfly Fish":100,
"Cherry Salmon":100,
"Sea Butterfly":100,
"Surgeonfish":100,
"Sea Horse":110,
"Goldfish":130,
"Guppy":130,
"Pop-Eyed Goldfish":130,
"Coelacanth":150,
"Nibble Fish":150,
"Suckerfish":150,
"King Salmon":180,
"Pike":180,
"Mitten Crab":200,
"Moray Eel":200,
"Betta":250,
"Football Fish":250,
"Piranha":250,
"Angelfish":300,
"Ray":300,
"Red Snapper":300,
"Soft-Shelled Turtle":375,
"Char":380,
"Koi":400,
"Ocean Sunfish":400,
"Saddled Bichir":400,
"Giant Trevally":450,
"Ranchu Goldfish":450,
"Barred Knifejaw":500,
"Blowfish":500,
"Snapping Turtle":500,
"Giant Snakehead":550,
"Gar":600,
"Mahi-Mahi":600,
"Tuna":700,
"Hammerhead Shark":800,
"Oarfish":900,
"Arapaima":1000,
"Arowana":1000,
"Blue Marlin":1000,
"Napoleonfish":1000,
"Sturgeon":1000,
"Saw Shark":1200,
"Whale Shark":1300,
"Barreleye":1500,
"Dorado":1500,
"Golden Trout":1500,
"Great White Shark":1500,
"Stringfish":1500,
"khervenfish":1
 }

loot = [("Tadpole", 25),
("Frog", 25),
("Horse Mackeral", 25),
("Crucian Carp", 25),
("Bluegill", 25),
("Anchovy", 25),
("Crawfish", 25),
("Pale Chub", 25),
("Dace", 25),
("Puffer Fish", 25),
("Carp", 25),
("Dab", 25),
("Killifish", 25),
("Yellow Perch", 25),
("Black Bass", 32),
("Freshwater Goby", 25),
("Loach", 25),
("Pond Smelt", 25),
("Sea Bass", 32),
("Neon Tetra", 18),
("Squid", 18),
("Zebra Turkeyfish", 18),
("Ribbon Eel", 18),
("Clownfish", 18),
("Salmon", 18),
("Catfish", 18),
("Olive Flounder", 18),
("Rainbowfish", 18),
("Tilapia", 18),
("Bitterling", 18),
("Sweetfish", 18),
("Butterfly Fish", 18),
("Cherry Salmon", 18),
("Sea Butterfly", 18),
("Surgeonfish", 18),
("Sea Horse", 18),
("Goldfish", 18),
("Guppy", 18),
("Pop-Eyed Goldfish", 18),
("Coelacanth", 18),
("Nibble Fish", 18),
("Suckerfish", 18),
("King Salmon", 18),
("Pike", 18),
("Mitten Crab", 14),
("Moray Eel", 14),
("Betta", 14),
("Football Fish", 14),
("Piranha", 14),
("Angelfish", 14),
("Ray", 14),
("Red Snapper", 14),
("Soft-Shelled Turtle", 14),
("Char", 14),
("Koi", 14),
("Ocean Sunfish", 14),
("Saddled Bichir", 14),
("Giant Trevally", 14),
("Ranchu Goldfish", 14),
("Barred Knifejaw", 14),
("Blowfish", 14),
("Snapping Turtle", 14),
("Giant Snakehead", 14),
("Gar", 14),
("Mahi-Mahi", 14),
("Tuna", 14),
("Hammerhead Shark", 14),
("Oarfish", 14),
("Arapaima", 10),
("Arowana", 10),
("Blue Marlin", 10),
("Napoleonfish", 10),
("Sturgeon", 10),
("Saw Shark", 10),
("Whale Shark", 10),
("Barreleye", 10),
("Dorado", 10),
("Golden Trout", 10),
("Great White Shark", 10),
("Stringfish", 10),
("khervenfish", 1)]