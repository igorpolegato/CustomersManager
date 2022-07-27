import configparser

config = configparser.ConfigParser()
config.read("config/config.ini")

perm_users = []

bt = config['bot']
msgens = config['mensagens']

api_id = bt['api_id']
api_hash = bt['api_hash']
bot_token = bt['bot_token']
bot_name = bt['name']

for user in msgens['users'].split(","):
    perm_users.append(user.strip())

pmu = list(map(int, perm_users))
gp_id = int(msgens['grupo'])
