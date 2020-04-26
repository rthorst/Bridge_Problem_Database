'''
For ID <= 50 hide EW
For ID > 50 hide SE
'''
import json

# Load hands.
f = open("data/hands.json", "r")
js = json.loads(f.read())

# Backup.
with open("data/hands_backup.json", "w") as of:
    of.write(json.dumps(js))

# Add hidden_hands field.
for idx, j in enumerate(js):

    hand_id = j["hand_id"]

    if hand_id <= 50: # declarer play.
        j["hidden_hands"] = "EW"
    else: # defense.
        j["hidden_hands"] = "SE"

    js[idx] = j

# Write.
with open("data/hands.json", "w") as of:
    of.write(json.dumps(js))
