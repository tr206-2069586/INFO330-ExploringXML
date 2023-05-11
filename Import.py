import sqlite3
import sys
import xml.etree.ElementTree as ET

## this is extra credit import.py file

# Incoming Pokemon MUST be in this format
#
# <pokemon pokedex="" classification="" generation="">
#     <name>...</name>
#     <hp>...</name>
#     <type>...</type>
#     <type>...</type>
#     <attack>...</attack>
#     <defense>...</defense>
#     <speed>...</speed>
#     <sp_attack>...</sp_attack>
#     <sp_defense>...</sp_defense>
#     <height><m>...</m></height>
#     <weight><kg>...</kg></weight>
#     <abilities>
#         <ability />
#     </abilities>
# </pokemon>

# connect to pokemon sqlite 
conn = sqlite3.connect('pokemon.sqlite')
c = conn.cursor()

# Read pokemon XML file name from command-line
# (Currently this code does nothing; your job is to fix that!)
if len(sys.argv) < 2:
    print("You must pass at least one XML file name containing Pokemon to insert")

for i, arg in enumerate(sys.argv):
    # Skip if this is the Python filename (argv[0])
    if i == 0:
        continue

# parse XML file
try:
    tree = ET.parse(arg)
except:
    print(f"Unable to parse {arg} as an XML file")

# get the root element (pokemon)
root = tree.getroot()

# check if the pokemon already exists in the database
name = root.find('name').text
c.execute("SELECT * FROM pokemon WHERE name = ?", (name,))
row = c.fetchone()
if row is not None:
    print(f"Pokemon {name} already exists in the database")

# Extract data from the XML and insert into databasei
pokedex = root.attrib.get('pokedex', None)
classification = root.attrib.get('classification', None)
generation = root.attrib.get('generation', None)
hp = root.find('hp').text
attack = root.find('attack').text
defense = root.find('defense').text
speed = root.find('speed').text
sp_attack = root.find('sp_attack').text
sp_defense = root.find('sp_defense').text
height = root.find('height/m').text
weight = root.find('weight/kg').text

# Insert new Pokemon into the database
c.execute("INSERT INTO pokemon (pokedex_number, name, classification_id, generation, hp, attack, defense, speed, sp_attack, sp_defense, height_m, weight_kg) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (pokedex, name, classification, generation, hp, attack, defense, speed, sp_attack, sp_defense, height, weight))

# commit changes and close database connection
conn.commit()
conn.close()