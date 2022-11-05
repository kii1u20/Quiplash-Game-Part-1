from gc import enable
import json
import logging
import os

import azure.functions as func
import azure.cosmos as cosmos
import azure.cosmos.exceptions as exceptions
import config
import random

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

    # note the config.settings to access configuration defined in config.py
    client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'] )

    # Create a proxy object to the treehuggers Cosmos DB database
    db_client = client.get_database_client(config.settings['db_id'])

    # Create a proxy object to the trees container
    users_container = db_client.get_container_client(config.settings['users_container'])

    prompts_container = db_client.get_container_client(config.settings['prompts_container'])

    input = req.get_json()
    c = not input["exact"]
    case_sensitive = ""
    if c == False:
        case_sensitive = "false"
    else:
        case_sensitive = "true"
    word = input["word"]

    # prompts = list(prompts_container.query_items(
    #     query = "SELECT c.id, c.text, c.username FROM c WHERE CONTAINS(c.text, '{0}', {1})".format(word, case_sensitive), enable_cross_partition_query=True))
    prompts = list(prompts_container.query_items(
        query = "SELECT c.id, c.text, c.username FROM c WHERE RegexMatch(c.text, '{0}', 'i')".format(word), enable_cross_partition_query=True))
    print("The reposnse is: {0}".format(prompts))
    return func.HttpResponse(body=json.dumps(prompts), status_code=200)
