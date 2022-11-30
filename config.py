import json
import os

supported_languages = ["en", "es"]
firebaseApiKey = 'AIzaSyCi2SKYmTpmfaoZJsRwK3Nfm_FQZqgb7L0'
text = {}
with open('config/es.json','r') as h:
    text['es'] = json.loads(h.read())
with open('config/en.json','r') as h:
    text['en'] = json.loads(h.read())

with open('config/api_config.json','r') as h:
    api_config = json.loads(h.read())
with open('config/db_config.json','r') as h:
    db_config = json.loads(h.read())
schemas = {}
for path, subdirs, files in os.walk("schemas"):
    for name in files:
        if(name.endswith('.schema.json')):
            with open(os.path.join(path, name),'r') as h:
                schema = json.loads(h.read())
            schemas[schema['$id']] = schema