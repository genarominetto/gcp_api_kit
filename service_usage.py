#Service Usage API
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def enable_services(project_id, service_account_file, service_list):
    """Enable a list of APIs for a specific project."""
    
    # Load the credentials from the service account file
    credentials = Credentials.from_service_account_file(service_account_file)

    # Build the service
    service = build('serviceusage', 'v1beta1', credentials=credentials)

    # Iterate over the service_list and enable each API for the project
    for api in service_list:
        service_name = f'{api}.googleapis.com'

        request = service.services().enable(
            name=f'projects/{project_id}/services/{service_name}'
        )

        try:
            request.execute()
            print(f'Successfully enabled {service_name} for project {project_id}')
        except Exception as e:
            print(f'Error enabling {service_name} for project {project_id}: {str(e)}')


def list_services(project_id, service_account_file, filter_google_apis=True):
    """List all services that are available to be enabled for a project."""

    # Load the credentials from the service account file
    credentials = Credentials.from_service_account_file(service_account_file)

    # Build the service
    service_resource = build('serviceusage', 'v1beta1', credentials=credentials)

    # Page token for fetching the next set of results
    next_page_token = None

    services_dict = {}

    while True:
        request = service_resource.services().list(
            parent=f'projects/{project_id}',
            pageToken=next_page_token
        )

        response = request.execute()

        for individual_service in response.get('services', []):
            service_name = individual_service['config']['name']
            title = individual_service['config']['title']

            if filter_google_apis and not service_name.endswith('.googleapis.com'):
                continue

            # Format the service name
            formatted_name = service_name.split('.')[0] if filter_google_apis else service_name
            
            # Add the service to the dictionary
            services_dict[formatted_name] = title

        next_page_token = response.get('nextPageToken')

        # If there is no next page token, we have fetched all results
        if not next_page_token:
            break

    # Return the dictionary of services
    return services_dict


def get_service_name(api_title, services_dict):
    """Given an API title and a dictionary of services, returns its service name."""

    for service_name, title in services_dict.items():
        if title == api_title:
            return service_name

    # If the API title was not found in the dictionary, return None
    return None
