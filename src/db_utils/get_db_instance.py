import json

import boto3
from botocore.exceptions import ClientError

from src.db_utils.mongo_db_utils import MongoDBUtils


def get_db_instance():
    credentials = get_db_secret()
    return MongoDBUtils(host=credentials["host"], username=credentials["user_name"], password=credentials["password"],
                        db_name=credentials["db_name"])


def get_db_secret():
    secret_name = "zechem_atlas_config"
    region_name = "eu-west-1"

    session = boto3.session.Session(profile_name="zechem")
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    return json.loads(secret)
