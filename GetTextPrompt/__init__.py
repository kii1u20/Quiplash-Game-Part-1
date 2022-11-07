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

    db_id = os.environ["db_id"]
    db_key = os.environ["db_key"]
    db_URI = os.environ["db_URI"]
    users_container = os.environ["users_container"]
    prompts_container = os.environ["prompts_container"]

    # Create the needed proxy objects for CosmosDB account, database and tree container
    client = cosmos.cosmos_client.CosmosClient(db_URI, db_key)

    # Create a proxy object to the coursework1 Cosmos DB database
    db_client = client.get_database_client(db_id)

    # Create a proxy object to the users container
    users_container = db_client.get_container_client(users_container)

    prompts_container = db_client.get_container_client(prompts_container)

    input = req.get_json()
    c = input["exact"]
    word = input["word"]
    if c == True:
        sensitive = list(prompts_container.query_items(query="SELECT c.id, c.text, c.username FROM c WHERE c.text LIKE '% {0} %' OR c.text LIKE '{0} %' OR c.text LIKE '% {0}'".format(word), enable_cross_partition_query=True))
        return func.HttpResponse(body=json.dumps(sensitive))
    else:
        insensitive = list(prompts_container.query_items(query="SELECT c.id, c.text, c.username FROM c WHERE LOWER(c.text) LIKE LOWER('% {0} %') OR LOWER(c.text) LIKE LOWER('{0} %') OR LOWER(c.text) LIKE LOWER('% {0}')".format(word), enable_cross_partition_query=True))
        return func.HttpResponse(body=json.dumps(insensitive))
