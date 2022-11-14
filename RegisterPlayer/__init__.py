import json
import logging
import os

import azure.functions as func
import azure.cosmos as cosmos
import azure.cosmos.exceptions as exceptions
import config


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing Register request in progress....')

    # db_id = os.environ["db_id"]
    # db_key = os.environ["db_key"]
    # db_URI = os.environ["db_URI"]
    # users_container = os.environ["users_container"]

    # # Create the needed proxy objects for CosmosDB account, database and tree container
    # client = cosmos.cosmos_client.CosmosClient(db_URI, db_key)

    # # Create a proxy object to the coursework1 Cosmos DB database
    # db_client = client.get_database_client(db_id)

    # # Create a proxy object to the users container
    # users_container = db_client.get_container_client(users_container)

    client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'] )

    # Create a proxy object to the treehuggers Cosmos DB database
    db_client = client.get_database_client(config.settings['db_id'])

    # Create a proxy object to the trees container
    users_container = db_client.get_container_client(config.settings['users_container'])

    user = req.get_json()
    username = user['username']
    password = user['password']
    user['id'] = username
    user['games_played'] = 0
    user['total_score'] = 0

    try:
        user_exists = list(users_container.query_items(query= "SELECT * FROM users WHERE users.username = '{0}'".format(username), 
                            enable_cross_partition_query=True))
        if len(user_exists) == 0:
            if len(username) < 4 or len(username) > 16:
                return func.HttpResponse(body=json.dumps({"result": False, "msg": "Username less than 4 characters or more than 16 characters"}), status_code=409)
            elif len(password) < 8 or len(password) > 24:
                return func.HttpResponse(body=json.dumps({"result": False, "msg": "Password less than 8 characters or more than 24 characters"}), status_code=409)
            else:
                users_container.create_item(body=user)
                return func.HttpResponse(body=json.dumps({"result" : True, 'msg' : 'OK'}), status_code=200)
        else:
            return func.HttpResponse(body=json.dumps({"result": False, "msg": "Username already exists" }), status_code=409)
    except exceptions.CosmosHttpResponseError as e:
        #  if "specified id already exists" in e.message:
        #     return func.HttpResponse(body=json.dumps({'msg' : 'Tree already exists'}), status_code=409)
        #  else:
            print(e.message)
            return func.HttpResponse("", status_code=404)
    