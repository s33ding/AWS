import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import subprocess

def create_codeartifact_domain(domain_name):
    try:
        client = boto3.client('codeartifact')
        response = client.create_domain(
            domain=domain_name
        )
        print(f"Domain '{domain_name}' created.")
        return response
    except Exception as e:
        print(f"Error creating domain: {e}")


def create_codeartifact_repository(domain_name, repository_name):
    try:
        client = boto3.client('codeartifact')
        response = client.create_repository(
            domain=domain_name,
            repository=repository_name
        )
        print(f"Repository '{repository_name}' created in domain '{domain_name}'.")
        return response
    except Exception as e:
        print(f"Error creating repository: {e}")


def associate_external_connection(domain_name, repository_name, external_connection):
    try:
        client = boto3.client('codeartifact')
        response = client.associate_external_connection(
            domain=domain_name,
            repository=repository_name,
            externalConnection=external_connection
        )
        print(f"External connection '{external_connection}' associated with repository '{repository_name}'.")
        return response
    except Exception as e:
        print(f"Error associating external connection: {e}")


def associate_upstream_repository(domain_name, repository_name, upstream_repository_name):
    try:
        client = boto3.client('codeartifact')
        response = client.update_repository(
            domain=domain_name,
            repository=repository_name,
            upstreams=[
                {
                    'repositoryName': upstream_repository_name
                }
            ]
        )
        print(f"Upstream repository '{upstream_repository_name}' associated with repository '{repository_name}'.")
        return response
    except Exception as e:
        print(f"Error updating repository upstreams: {e}")

# Function to configure a tool using AWS CLI
def configure_codeartifact_tool(domain, repository, tool):
    """
    Configures the given tool (e.g., npm, pip, maven) using AWS CLI to connect to AWS CodeArtifact.
    """
    try:
        # Run the AWS CLI command to log in to CodeArtifact
        subprocess.run(
            [
                "aws", "codeartifact", "login",
                "--tool", tool,
                "--repository", repository,
                "--domain", domain
            ],
            check=True
        )
        print(f"Tool '{tool}' successfully configured with AWS CodeArtifact!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while configuring the tool: {e}")
        sys.exit(1)

def list_packages(domain_name, repository_name):
    try:
        client = boto3.client('codeartifact')
        response = client.list_packages(
            domain=domain_name,
            repository=repository_name
        )
        print(f"Packages in repository '{repository_name}': {response['packages']}")
        return response['packages']
    except Exception as e:
        print(f"Error listing packages: {e}")


def delete_repository(domain_name, repository_name):
    try:
        client = boto3.client('codeartifact')
        response = client.delete_repository(
            domain=domain_name,
            repository=repository_name
        )
        print(f"Repository '{repository_name}' deleted from domain '{domain_name}'.")
        return response
    except Exception as e:
        print(f"Error deleting repository: {e}")


def delete_domain(domain_name):
    try:
        client = boto3.client('codeartifact')
        response = client.delete_domain(
            domain=domain_name
        )
        print(f"Domain '{domain_name}' deleted.")
        return response
    except Exception as e:
        print(f"Error deleting domain: {e}")
