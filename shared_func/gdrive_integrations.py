from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

def upload_file_to_shared_drive(self, file_name, shared_drive_id, folder_id, gdrive_cred):
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
    except Exception as e:
        print('An error occurred during file upload:', str(e))

def list_files_in_folder(folder_id, gdrive_cred):
    # Retrieve the service account JSON key
    service_account_json = gdrive_cred  # Assuming the JSON key is stored directly in the secret

    # Create credentials from the service account JSON key
    credentials = service_account.Credentials.from_service_account_info(
        service_account_json, scopes=['https://www.googleapis.com/auth/drive']
    )

    # Create the Drive service
    drive_service = build('drive', 'v3', credentials=credentials)

    try:
        # List files in the specified folder
        results = drive_service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            spaces='drive',
            fields='files(id, name)',
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()

        files = results.get('files', [])
        fl_nm = [x.get("name") for x in files]
        return fl_nm

    except Exception as e:
        print('An error occurred while listing files:', str(e))
        return None

def read_file_from_drive_by_extension(file_name, folder_id, gdrive_cred):
    # Retrieve the service account JSON key
    service_account_json = gdrive_cred  # Assuming the JSON key is stored directly in the secret

    # Create credentials from the service account JSON key
    credentials = service_account.Credentials.from_service_account_info(
        service_account_json, scopes=['https://www.googleapis.com/auth/drive']
    )

    # Create the Drive service
    drive_service = build('drive', 'v3', credentials=credentials)

    try:
        # Search for the file by name within the specified folder
        results = drive_service.files().list(
            q=f"'{folder_id}' in parents and name='{file_name}' and trashed=false",
            spaces='drive',
            fields='files(id, name)',
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()

        files = results.get('files', [])

        if not files:
            print(f"File with name '{file_name}' not found in the specified folder.")
            return None

        # Assuming there's only one file with this name in the folder, you can access it as files[0]
        file = files[0]

        # Download the file content to a temporary file
        file_id = file['id']
        temp_file_path = tempfile.mktemp()
        request = drive_service.files().get_media(fileId=file_id)
        with open(temp_file_path, 'wb') as temp_file:
            downloader = MediaIoBaseDownload(temp_file, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()

        # Determine the file's extension
        file_extension = file_name.split('.')[-1].lower()

        # Read the temporary file into a Pandas DataFrame based on its extension
        if file_extension == 'csv':
            df = pd.read_csv(temp_file_path)
        elif file_extension == 'xlsx':
            df = pd.read_excel(temp_file_path, engine='openpyxl')
        elif file_extension == 'parquet':
            df = pd.read_parquet(temp_file_path)
        elif file_extension == 'pkl':
            df = pd.read_pickle(temp_file_path)
        else:
            print(f"Unsupported file format: {file_extension}")
            return None

        return df
    except Exception as e:
        print(f'An error occurred while reading the file: {str(e)}')
        return None

def process_filenames_and_find_missing_tables(file_names, dct_tbl, pattern = r'_\d+-\d+\.xlsx$'):
    """
    Remove a specified pattern from each filename in the list and find missing tables.

    Args:
        file_names (list): List of filenames.
        dct_tbl (dict): Dictionary of table mappings.

    Returns:
        tuple: A tuple containing cleaned filenames and a list of missing tables.
    """
    # Define the pattern to remove

    cleaned_file_names = [re.sub(pattern, '', name) for name in file_names]

    missing_tables = []
    for table_name, table_abbr in dct_tbl.items():
        if table_abbr not in cleaned_file_names:
            missing_tables.append((table_name, table_abbr))

    return cleaned_file_names, missing_tables

def share_folder_with_email(self, folder_id, email_to_share, gdrive_cred, role='reader'):
    try:        
        # Create credentials from the service account JSON key
        credentials = service_account.Credentials.from_service_account_info(
            gdrive_cred, scopes=['https://www.googleapis.com/auth/drive']
        )

        # Create the Drive service
        drive_service = build('drive', 'v3', credentials=credentials)
        
        # Define the permission details
        permission = {
            'type': 'user',
            'role': role,
            'emailAddress': email_to_share
        }

        # Share the folder with the specified email address
        drive_service.permissions().create(
            fileId=folder_id,
            body=permission,
            fields='id',
            supportsAllDrives=True
        ).execute()
    
        print(f"Folder shared with {email_to_share} as {role}.")
    except Exception as e:
        print('An error occurred during folder sharing:', str(e))

