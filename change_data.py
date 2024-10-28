import json
import main

with open('users_id.json') as f:
    id_data = json.load(f)

id_data['6100927801'] = main.id_default_dict

#for i in id_data:
#   id_data[i]['premium_access_time'] = None

with open('users_id.json', 'w') as f:
    json.dump(id_data, f, indent=4)


