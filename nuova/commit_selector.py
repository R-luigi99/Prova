import json

with open('dubbo-annotations.json', 'r') as f:
  data = json.load(f)
cms={}
for key in data.keys():
  s=data[key][0]['introdates']
  for c in s.keys():
    cm = {}
    cm['idBadCommit'] = c
    cms[c] = cm

  json_object = json.dumps(cms, indent=2)

    # Writing to sample.json
  with open("idBadCommits.json", "w") as outfile:
      outfile.write(json_object) 
