from googleapiclient.discovery import build
from gcp_api_connector.resources.googleapis_auth import get_api_key
APIKEY = get_api_key()



def read_image(image_path):
    import base64
    with open(image_path, 'rb') as image:
        img_base64 = base64.b64encode(image.read())
    vservice = build('vision', 'v1', developerKey=APIKEY)
    request = vservice.images().annotate(body={
            'requests': [{
                    'image': {
                        'content': img_base64.decode('UTF-8')
                    },
                    'features': [{
                        'type': 'TEXT_DETECTION',
                        'maxResults': 3,
                    }]
                }],
            })
    responses = request.execute(num_retries=3)
    return responses['responses'][0]['textAnnotations'][0]['description']
