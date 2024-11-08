import requests
from prettytable.colortable import ColorTable, Themes
import json

def lambda_handler(event, context):
    vpc = "non-live"
    env = "dev"
    try:
        if (event['queryStringParameters']) and (event['queryStringParameters']['vpc'] is not None):
            vpc = event['queryStringParameters']['vpc']
    except KeyError:
        print('No VPC')

    try:
        if (event['queryStringParameters']) and (event['queryStringParameters']['env'] is not None):
            env = event['queryStringParameters']['env']
    except KeyError:
        print('No env')

    url = 'https://gitlab.com/api/v4/projects/64220655/repository/files/{0}%2FABC-{1}%2Facquisition.yml/raw'.format(vpc, env)
    print(url)
    get = requests.get(url)
    response = get.text
    res = dict(item.split(": ") for item in response.split("\n"))

    table = ColorTable(theme=Themes.OCEAN)
    table.field_names = ["Application", "version"]
    table.sortby = "Application"

    for key, value in res.items():
        table.add_row([key, value])

    return {
        "statusCode": 200,
        "body": table.get_formatted_string('text')
    }

def client(path):
    url = 'https://gitlab.com/api/v4/{0}'.format(path)
    return url

def get_url(vpc, env):
    url = client('projects/64220655/repository/files/{0}%2Fabc-{1}%2Facquisition.yml/raw'.format(vpc, env))
    return url
