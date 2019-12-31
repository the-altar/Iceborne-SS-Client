import json
import copy

data = None
armor = None
charms = None
deco = None
with open('skillmap.json', 'r') as f:
    data = json.load(f)
with open('armormap.json', 'r') as f:
    armor = json.load(f)
with open('charmmap.json', 'r') as f:
    charms = json.load(f)
with open('decomap.json', 'r') as f:
    deco = json.load(f)
search = {
    'critical-eye':7,
    'attack-boost':7,
    'peak-performance':3
}   

limit = 200
inventory = {
    'head':[],
    'chest':[],
    'gloves':[],
    'waist':[],
    'legs':[],
    'charm': []
}

for s in search:
    for a in data['master'][s]:
        inventory[a[1]].append(a)
        inventory[a[1]].append

inventory['head'].append([0,0,0])
inventory['chest'].append([0,0,0])
inventory['gloves'].append([0,0,0])
inventory['waist'].append([0,0,0])
inventory['legs'].append([0,0,0])
inventory['charm'].append([0,0,0])

product = 1
for i in inventory:
    inventory[i] = sorted(inventory[i], key=lambda x: x[2], reverse=True)    
    product *= len(inventory[i])
print(f'Total combinations are: {product}')

def check_levels(total):
    for skill in search:
        if skill in total['skills'] and total['skills'][skill] == search[skill]:
            pass
        else:            
            return False
      
    return True        

def equip_deco(armor, level, skill, total):
    if skill in deco[level]:
        for effects in deco[level][skill]:
            if total['slots'][level] <= 0:
                return

            temporary = {}

            for s in effects[1]:
                temporary[s[1]] = s[0]
                if s[1] in total['skills']:
                    temporary[s[1]] += total['skills'][s[1]]

            if temporary[skill] <= search[skill]:
                for key in temporary:
                    total['skills'][key] = temporary[key]
                total['slots'][level] -= 1
                armor['decos'].append(effects[0])     

    else:
        return    
    pass

def fill_decoration(armorset, total):
    #print(total)
    total_copy = copy.deepcopy(total)
    armorset_copy = copy.deepcopy(armorset)

    for skill in total['skills']:

        if skill in search and total['skills'][skill] < search[skill]:
            for slot_level, _ in enumerate(total['slots']):

                equip_deco(armorset_copy, slot_level, skill, total_copy)
                if total_copy['skills'][skill] == search[skill]:
                    break
    return armorset_copy, total_copy                
    #for slot_level, qtd in enumerate(total['slots']):
    #    print(deco[slot_level])
    #print(armorset)

def fits(armorset, piece, piece_type, total):
    if piece[0] == 0:
        return (total, True, armorset)
    
    d = None
    if piece_type == 'charm':
        d = charms[piece[0]] 
    else:
        d = armor[piece[0]] 

    armor_copy = copy.deepcopy(armorset)
    armor_copy[piece_type] = piece[0]
    
    tcopy = copy.deepcopy(total)
    
    for slot in piece[3]:
        tcopy['slots'][slot-1] += 1
    for i in d:
        if i[2] in tcopy['skills']:
            tcopy['skills'][i[2]] += i[1]
        else:
            tcopy['skills'][i[2]] = i[1]

    if tcopy['skills'][piece[4]] > search[piece[4]]:
        return (total, False, armorset)
    return (tcopy, True, armor_copy)    

def get_all_possibilities(armory, key, key_size, armor, total, check, sets):
    
    if not check:
        return
    if len(sets)>limit:
        return
    if key_size > 5:
        a1, t1 = fill_decoration(armor, total)
        if check_levels(t1):
            print(t1)
            print()
            sets.append((t1,a1))
        return    

    for piece in inventory[key[key_size]]:
        t,c,a  = fits(armor, piece, key[key_size], total)
        get_all_possibilities(armory, key, key_size+1, a, t, c, sets)
            
        

           
def subset(trials):

    return get_all_possibilities(inventory, ['charm','head', 'chest', 'gloves', 'waist', 'legs'], 0, {'decos':[]}, {'slots':[0,0,0,0], 'skills':{}}, True, []) 

subset(0)