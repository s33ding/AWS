import json
import os
import boto3
from botocore.exceptions import ClientError

# Initialize the ECR client
ecr_client = boto3.client('ecr')

def delete_ecr_repository(repo_name):
    """
    Delete a specific repository in ECR by name.
    """
    try:
        ecr_client.delete_repository(repositoryName=repo_name, force=True)
        print(f"Repository {repo_name} deleted successfully.")
    except Exception as e:
        print(f"Error deleting repository {repo_name}: {e}")



def list_ecr_images(repository_name):
    """
    List all images (tags/digests) in a specific ECR repository.
    """
    try:
        images = []
        paginator = ecr_client.get_paginator('list_images')
        for page in paginator.paginate(repositoryName=repository_name):
            for image in page['imageIds']:
                images.append(image)
        return images
    except Exception as e:
        print(f"Error listing images in repository {repository_name}: {e}")
        return []

def delete_ecr_image(repository_name, image_digest=None, image_tag=None):
    """
    Delete a specific image from an ECR repository by digest or tag.
    """
    try:
        if image_digest:
            ecr_client.batch_delete_image(
                repositoryName=repository_name,
                imageIds=[{'imageDigest': image_digest}]
            )
            print(f"Image with digest {image_digest} deleted successfully from {repository_name}.")
        elif image_tag:
            ecr_client.batch_delete_image(
                repositoryName=repository_name,
                imageIds=[{'imageTag': image_tag}]
            )
            print(f"Image with tag {image_tag} deleted successfully from {repository_name}.")
        else:
            print("Error: Provide either image_digest or image_tag.")
    except Exception as e:
        print(f"Error deleting image from repository {repository_name}: {e}")

def delete_images_menu(repository_name):
    """
    Presents a menu of images in the repository for the user to select and delete.
    """
    images = list_ecr_images(repository_name)
    if not images:
        print(f"No images found in repository {repository_name}.")
        return

    # Create a menu
    print(f"\nImages in repository '{repository_name}':")
    menu = {}
    for idx, image in enumerate(images):
        # Assign a letter to each image
        option = chr(ord('a') + idx)
        menu[option] = image
        image_desc = f"Tag: {image.get('imageTag', 'None')} | Digest: {image.get('imageDigest', 'None')}"
        print(f"  {option}) {image_desc}")

    # Input loop
    while True:
        choice = input("\nEnter the letter of the image to delete (or 'q' to quit): ").strip().lower()
        if choice == 'q':
            print("Exiting menu.")
            break
        elif choice in menu:
            selected_image = menu[choice]
            image_tag = selected_image.get('imageTag')
            image_digest = selected_image.get('imageDigest')

            # Delete the selected image
            delete_ecr_image(repository_name, image_digest=image_digest, image_tag=image_tag)
            break  # Exit after deleting
        else:
            print("Invalid choice. Please select a valid option.")

