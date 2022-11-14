from gc import enable
import json
import logging
import os

import azure.functions as func
import azure.cosmos as cosmos
import azure.cosmos.exceptions as exceptions
import config


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing Prompt request in progress....')

    # db_id = os.environ["db_id"]
    # db_key = os.environ["db_key"]
    # db_URI = os.environ["db_URI"]
    # users_container = os.environ["users_container"]
    # prompts_container = os.environ["prompts_container"]

    # # Create the needed proxy objects for CosmosDB account, database and tree container
    # client = cosmos.cosmos_client.CosmosClient(db_URI, db_key)

    # # Create a proxy object to the coursework1 Cosmos DB database
    # db_client = client.get_database_client(db_id)

    # # Create a proxy object to the users container
    # users_container = db_client.get_container_client(users_container)

    # prompts_container = db_client.get_container_client(prompts_container)

    client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'] )

    # Create a proxy object to the treehuggers Cosmos DB database
    db_client = client.get_database_client(config.settings['db_id'])

    # Create a proxy object to the trees container
    users_container = db_client.get_container_client(config.settings['users_container'])
    prompts_container = db_client.get_container_client(config.settings['prompts_container'])


    prompt = req.get_json()
    username = prompt['username']
    password = prompt['password']
    id = prompt['id']
    
    # return func.HttpResponse("", status_code=404)
    try:
        user_exists = list(users_container.query_items(query= "SELECT * FROM c WHERE c.username = '{0}'".format(username), enable_cross_partition_query = True))
        prompt_exists_id = list(prompts_container.query_items(query= "SELECT * FROM c WHERE c.id = '{0}'".format(id), enable_cross_partition_query = True))
        if len(user_exists) == 0 :
            return func.HttpResponse(body=json.dumps({"result": False, "msg": "bad username or password"}), status_code=409)
        elif user_exists[0]['password'] != password:
            return func.HttpResponse(body=json.dumps({"result": False, "msg": "bad username or password"}), status_code=409)
        elif len(prompt_exists_id) == 0:
            return func.HttpResponse(body=json.dumps({"result": False, "msg": "prompt id does not exist"}), status_code=409)
        elif prompt_exists_id[0]['username'] != username:
            return func.HttpResponse(body=json.dumps({"result": False, "msg": "access denied"}), status_code=409)
        else:
            prompts_container.delete_item(item = "{0}".format(id), partition_key = "{0}".format(id))
            return func.HttpResponse(body=json.dumps({"result" : True, "msg": "OK"}), status_code=200)
    except exceptions.CosmosHttpResponseError as e:
            print(e.message)
            return func.HttpResponse("", status_code=404)
    