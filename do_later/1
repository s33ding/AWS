import boto3

# Initialize Boto3 Rekognition client
rekognition_client = boto3.client('rekognition')

def confirm_identity(source_image, target_image):
    # Load images
    with open(source_image, 'rb') as source_image_file, open(target_image, 'rb') as target_image_file:
        source_image_bytes = source_image_file.read()
        target_image_bytes = target_image_file.read()

    # Call Amazon Rekognition's compare_faces API
    response = rekognition_client.compare_faces(
        SourceImage={'Bytes': source_image_bytes},
        TargetImage={'Bytes': target_image_bytes}
    )

    # Check if any faces are matched
    if response['FaceMatches']:
        matched_faces = response['FaceMatches']
        confidence = matched_faces[0]['Similarity']
        return True, confidence
    else:
        return False, 0

# Example usage
if __name__ == "__main__":
    source_image_path = 'source_image.jpg'
    target_image_path = 'target_image.jpg'

    identity_confirmed, confidence = confirm_identity(source_image_path, target_image_path)
    if identity_confirmed:
        print("Identity confirmed with confidence:", confidence)
    else:
        print("Identity not confirmed.")

