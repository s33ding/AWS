from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

def upload_file_to_shared_drive(file_name, shared_drive_id, folder_id, gdrive_cred):
    # Retrieve the service account JSON key from AWS Secrets Manager
    service_account_json = gdrive_cred  # Assuming the JSON key is stored directly in the secret

    # Create credentials from the service account JSON key
    credentials = service_account.Credentials.from_service_account_info(
        service_account_json, scopes=['https://www.googleapis.com/auth/drive']
    )

    # Create the Drive service
    drive_service = build('drive', 'v3', credentials=credentials)

    # Create file metadata
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]  # Here folder should be in the shared drive
    }

    media = MediaFileUpload(file_name, mimetype='text/plain')

    # List all files in the folder to check if file with same name already exists
    results = drive_service.files().list(
        q=f"name='{file_name}' and '{folder_id}' in parents and trashed=false",
        spaces='drive',
        fields='files(id, name)',
        supportsAllDrives=True,
        includeItemsFromAllDrives=True
    ).execute()

    items = results.get('files', [])

    if items:  # If file already exists, delete it
        file_id = items[0]['id']  # Get ID of the first file with matching name

        drive_service.files().delete(
            fileId=file_id,
            supportsAllDrives=True
        ).execute()

        print('Existing file deleted.')

    # Upload the file to the specified folder within the shared drive
    try:
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            supportsAllDrives=True
        ).execute()

        print('File uploaded successfully.')
        #print('Title: %s, ID: %s' % (file['name'], file['id']))
    except Exception as e:
        print('An error occurred during file upload:', str(e))

