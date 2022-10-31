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

    top = req.get_json()
    numOfUsers = top['top']

    try:
        leaderboard = list(users_container.query_items(query=
            "SELECT TOP {0} c.username, c.total_score as {1}, c.games_played FROM c ORDER BY c.total_score DESC, c.username ASC".format(numOfUsers, "score"), 
            enable_cross_partition_query=True))
        print(leaderboard)
        return func.HttpResponse(body = json.dumps(leaderboard), status_code=200)
    except exceptions.CosmosHttpResponseError as e:
            print(e.message)
            return func.HttpResponse("", status_code=404)
    