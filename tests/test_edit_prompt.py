import unittest
import json
import requests 

import azure.functions as func
import azure.cosmos as cosmos
import config
#Important for the import name to match the case of the Function folder
from RegisterPlayer import main

class TestFunction(unittest.TestCase):

    # note the config.settings to access configuration defined in config.py
    client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'] )

    # Create a proxy object to the treehuggers Cosmos DB database
    db_client = client.get_database_client(config.settings['db_id'])

    # Create a proxy object to the trees container
    users_container = db_client.get_container_client(config.settings['users_container'])

    def test_add_user(self):
        payload = {"id": 5, "text": "This prompt has to more than 30 characters", "username" : "alpha" , "password": "test1234"}


        resp = requests.get(
                'https://coursework1-kii1u20.azurewebsites.net/api/EditPrompt?code=XZcwcdCqnz4CfI7lpxzIpqxfkzqVu_WRtugi0-eo1EZEAzFusSO6Cw==', 
                json = payload)


        self.assertEqual({"result" : True, 'msg' : 'OK'}, resp.json())

        # all_trees = list(self.users_container.read_all_items())
        # self.assertEqual(len(all_trees),1)
        # the_tree_in_the_db = all_trees[0]


        # result = dict(itertools.islice(the_tree_in_the_db.items(), 4))

        # current = result['id']
        # result['id'] = int(current)

        # self.assertEqual(payload['tree'], result)

