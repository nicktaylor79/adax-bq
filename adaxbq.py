# 2021-01-05 Nick Taylor | nick@nicktaylor.co.uk
# Script to collect heating status & temperature from Adax API, and put them in a BigQuery table

from google.cloud import bigquery
import json, requests, sanction, os


CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
API_URL           = "https://api-1.adax.no/client-api"

def get_token():
    # Authenticate and obtain JWT token
    oauthClient = sanction.Client(token_endpoint = API_URL + '/auth/token')
    oauthClient.request_token(grant_type = 'password', username = CLIENT_ID, password = CLIENT_SECRET)
    return oauthClient.access_token

def to_bigquery(dataset, table, document):
   #Write row to BQ 
   bigquery_client = bigquery.Client()
   dataset_ref = bigquery_client.dataset(dataset)
   table_ref = dataset_ref.table(table)
   table = bigquery_client.get_table(table_ref)
   errors = bigquery_client.insert_rows(table, [document])
   if errors != [] :
      print(errors, file=sys.stderr)


def get_homes_info(token):
    #Send JWT to get content API; parse each room for current temperature, target temperature, and write to insert_rows
    headers = { "Authorization": "Bearer " + token }
    response = requests.get(API_URL + "/rest/v1/content/", headers = headers)
    json = response.json()
    insert_rows = {}
    for room in json['rooms']:
        roomName = room['name']
        targetTemperature = room['targetTemperature'] / 100.0
        currentTemperature = 0
        if ('temperature' in room):
            currentTemperature = room['temperature'] / 100.0
            insert_rows['room'] = roomName
            insert_rows['targettemperature'] = targetTemperature
            insert_rows['currentTemperature'] = currentTemperature
            print(insert_rows)
            to_bigquery(os.environ['dataset'], os.environ['table'], insert_rows)

def adaxtobq(event):
    token = get_token()
    get_homes_info(token) 
    