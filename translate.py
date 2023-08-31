from googleapiclient.discovery import build
from gcp_api_connector.resources.googleapis_auth import get_api_key
APIKEY = get_api_key()
service = build('translate', 'v2', developerKey=APIKEY)

def en_sp(text):
  outputs = service.translations().list(source='en', target='es', q=[text]).execute()
  return outputs['translations'][0]['translatedText']

def sp_en(text):
  outputs = service.translations().list(source='es', target='en', q=[text]).execute()
  return outputs['translations'][0]['translatedText']
