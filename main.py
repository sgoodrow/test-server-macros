print("""
Before running this script, log into your character on P99 and
run this command (replacing "Charname" with your character name):

/outputfile inventory Charname_inventory.txt

Then edit the variables in the script for your personal configuration!
Close EQ completely before running this script.

After you've run this script:
1) log into the test server and create your character with the same
   name as on P1999.
2) Delete your starter gear.
3) Go to your Social tab, page 8 and click each button.
4) Click a bunch on your class logo in your inventory to auto-equip
   all the items that are on your cursor.
""")

###################################
# CHANGE THESE FOR YOUR CHARACTER #
###################################
EVERQUEST_DIRECTORY = "D:\\EverQuest"
# EVERQUEST_DIRECTORY = "C:\\Program Files (x86)\\Sony\\EverQuest"
CHARACTER_NAME = "Toald"
NEW_SERVER = "VPS"  # Probably no need to change this

##########################
# DO NOT EDIT BELOW THIS #
##########################

import csv
import os

# Copy UI file for character
GREEN_UIFILE = "UI_{}_P1999Green.ini".format(CHARACTER_NAME)
VENTEST_UIFILE = "UI_{}_{}.ini".format(CHARACTER_NAME, NEW_SERVER)
with open(os.path.join(EVERQUEST_DIRECTORY, GREEN_UIFILE), 'r') as ui_file:
    with open(os.path.join(EVERQUEST_DIRECTORY, VENTEST_UIFILE), 'w') as ui_file_new:
        ui_file_new.write(ui_file.read())

# Load Macro file for character
GREEN_MACROFILE = "{}_P1999Green.ini".format(CHARACTER_NAME)
with open(os.path.join(EVERQUEST_DIRECTORY, GREEN_MACROFILE), 'r') as macro_file:
    macro_data = macro_file.read()

# Load inventory data
INVENTORY_FILE = CHARACTER_NAME + "_inventory.txt"
with open(os.path.join(EVERQUEST_DIRECTORY, INVENTORY_FILE)) as inventory_file:
    data = csv.DictReader(inventory_file, delimiter='\t')
    items = [
        a['ID'] for a in data
        if 'General' not in a['Location'] and
           'Bank' not in a['Location'] and
           a['ID'] != '0'
    ]

PAGE = 8
BUTTON = 1
LINE = 6
hotkey_data = "[Socials]"
hotkey_data = "\n".join((hotkey_data, "Page{page}Button{button}Name=Setup".format(page=PAGE, button=BUTTON)))
hotkey_data = "\n".join((hotkey_data, "Page{page}Button{button}Color=16".format(page=PAGE, button=BUTTON)))
hotkey_data = "\n".join((hotkey_data, "Page{page}Button{button}Line1=/pause 5, /say #level 50".format(page=PAGE, button=BUTTON)))
hotkey_data = "\n".join((hotkey_data, "Page{page}Button{button}Line2=/pause 5, /say #scribespells 50".format(page=PAGE, button=BUTTON)))
hotkey_data = "\n".join((hotkey_data, "Page{page}Button{button}Line3=/pause 5, /target {name}".format(page=PAGE, button=BUTTON, name=CHARACTER_NAME)))
hotkey_data = "\n".join((hotkey_data, "Page{page}Button{button}Line4=/pause 5, /say #setskillall 200".format(page=PAGE, button=BUTTON, name=CHARACTER_NAME)))
hotkey_data = "\n".join((hotkey_data, "Page{page}Button{button}Line5=/pause 5, /say #heal".format(page=PAGE, button=BUTTON, name=CHARACTER_NAME)))
for item in items:
    if LINE > 5:
        BUTTON += 1
        LINE = 1
        hotkey_data = "\n".join(
            (hotkey_data, "Page{page}Button{button}Name=ItemGen{id}".format(page=PAGE, button=BUTTON, id=BUTTON-1)))
        hotkey_data = "\n".join((hotkey_data, "Page{page}Button{button}Color=13".format(page=PAGE, button=BUTTON)))
    item_line = "Page{page}Button{button}Line{line}=/pause 5, /say #si {id}"
    item_line = item_line.format(page=PAGE, button=BUTTON, line=LINE, id=item)
    hotkey_data = "\n".join((hotkey_data, item_line))
    LINE += 1

macro_data = macro_data.replace('[Socials]', hotkey_data)

# Write out macro data
VENTEST_MACROFILE = "{}_{}.ini".format(CHARACTER_NAME, NEW_SERVER)
with open(os.path.join(EVERQUEST_DIRECTORY, VENTEST_MACROFILE), 'w') as new_macro_file:
    new_macro_file.write(macro_data)

print("Done!")
