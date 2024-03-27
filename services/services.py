import json
# from pprint import pprint

with open('shops_and_legals.json', 'r', encoding='utf') as j_file:
    shops_and_legals = json.load(j_file)

# pprint(shops_and_legals)
bot_messages_ids = {}
