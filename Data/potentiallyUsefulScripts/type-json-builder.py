import json

# Open the text file and read the contents into a string
with open('pokedex.txt', 'r') as f:
    data = f.readlines()

    pokedex = {}
    
    type2 = None
    
    for line in data[3:]:
        if line.startswith("Name"):
            name  = line[7:].strip()
        if line.startswith("Type1"):
            type1 = line[8:].strip()
        if line.startswith("Type2"):
            type2 = line[8:].strip()
        if line.startswith("["):
            record = { name : {
                 'type1': type1,
                 'type2': type2,
            }}
            pokedex.update(record)
            type2 = None

json_data = json.dumps(pokedex, indent=2, separators=(',', ': '))
# Write the JSON string to a new file
with open('dex_of_types.json', 'w') as f:
    f.write(json_data)