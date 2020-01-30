import sqlite3

conn = sqlite3.connect("rpg_db.sqlite3")
# h/t: https://kite.com/python/examples/3884/sqlite3-use-a-row-factory-to-access-values-by-column-name
conn.row_factory = sqlite3.Row
curs = conn.cursor()
query = """
SELECT COUNT(name) FROM charactercreator_character;
"""
results = curs.execute(query).fetchall()
print("Total characters:", results[0]['COUNT(name)'])

subclass = ['charactercreator_cleric', 'charactercreator_fighter', 'charactercreator_mage', 'charactercreator_thief']
for character_class in subclass:
    query = f"SELECT COUNT(character_ptr_id) FROM {character_class}"
    results = curs.execute(query).fetchall()
    print(f'Characters in class {character_class[17:]}:', results[0]['COUNT(character_ptr_id)'])

query = "SELECT COUNT(mage_ptr_id) FROM charactercreator_necromancer"

results = curs.execute(query).fetchall()
print('Characters in class necromancer:', results[0]['COUNT(mage_ptr_id)'])

query = "SELECT COUNT(item_id) FROM armory_item"
results = curs.execute(query).fetchall()

print(results[0]['COUNT(item_id)'])
items = results[0]['COUNT(item_id)']

query = "SELECT COUNT(item_ptr_id) FROM armory_weapon"
weapons = (curs.execute(query).fetchall())[0]['COUNT(item_ptr_id)']
print('Weapons =', weapons)
print('Items which are not weapons =', (items - weapons))

query = """SELECT
character_id,
COUNT(item_id)
FROM
    charactercreator_character_inventory
GROUP BY
    character_id
LIMIT
    20;"""
results = curs.execute(query).fetchall()
for i in range(len(results)):
    print('Character ID', results[i][0], 'has', results[i][1], 'items.')

query = """
SELECT
character_id,
COUNT(item_id)
FROM
    (charactercreator_character_inventory 
    JOIN armory_weapon ON charactercreator_character_inventory.item_id 
    = armory_weapon.item_ptr_id)
GROUP BY
    character_id
LIMIT
    20;"""
results = curs.execute(query).fetchall()
for i in range(len(results)):
    print('Character ID', results[i][0], 'has', results[i][1], 'weapons')

query = """
SELECT COUNT(item_id) 
FROM charactercreator_character_inventory
GROUP BY character_id;"""

results = curs.execute(query).fetchall()
items = 0
for i in range(len(results)):
    items += results[i][0]
average = items / len(results)
print('Average items per character is', average)

query = """
SELECT
COUNT(item_id)
FROM
    (charactercreator_character_inventory 
    JOIN armory_weapon ON charactercreator_character_inventory.item_id 
    = armory_weapon.item_ptr_id)
GROUP BY
    character_id
"""
results = curs.execute(query).fetchall()
weapons = 0
for i in range(len(results)):
    weapons += results[i][0]
average_weapons = weapons / len(results)
print('Average weapons per character who has weapons is:', average_weapons)