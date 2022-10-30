import json
import logging
import os

import azure.functions as func
import azure.cosmos as cosmos
import azure.cosmos.exceptions as exceptions
import config


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing Login request in progress....')

    db_id = os.environ["db_id"]
    db_key = os.environ["db_key"]
    db_URI = os.environ["db_URI"]
    users_container = os.environ["users_container"]

    # Create the needed proxy objects for CosmosDB account, database and tree container
    client = cosmos.cosmos_client.CosmosClient(db_URI, db_key)

    # Create a proxy object to the coursework1 Cosmos DB database
    db_client = client.get_database_client(db_id)

    # Create a proxy object to the users container
    users_container = db_client.get_container_client(users_container)

    user = req.get_json()
    username = user['username']
    password = user['password']

    try:
        user_exists = list(users_container.query_items(query= "SELECT * FROM users WHERE users.username = '{0}'".format(username), 
                            enable_cross_partition_query=True))
        if len(user_exists) == 0:
            return func.HttpResponse(body=json.dumps({"result": False , "msg": "Username or password incorrect"}), status_code=400)
        else:
            if user_exists[0]['username'] == username and user_exists[0]['password'] == password:
                return func.HttpResponse(body=json.dumps({"result": True , "msg" : "OK"}), status_code=200)
            else:
                return func.HttpResponse(body=json.dumps({"result": False , "msg": "Username or password incorrect"}), status_code=400)
    except exceptions.CosmosHttpResponseError as e:
            print(e.message)
            return func.HttpResponse("", status_code=404)
    