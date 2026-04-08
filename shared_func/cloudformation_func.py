import boto3
from botocore.exceptions import ClientError

def list_cloudformation_stacks():
    """
    Lists all CloudFormation stacks in the AWS account.

    Returns:
        A list of dictionaries containing stack names and their statuses.
    """
    try:
        client = boto3.client('cloudformation')
        response = client.list_stacks(StackStatusFilter=[
            'CREATE_COMPLETE', 'UPDATE_COMPLETE', 'ROLLBACK_COMPLETE', 
            'DELETE_FAILED', 'CREATE_FAILED', 'UPDATE_ROLLBACK_FAILED',
        ])
        
        stacks = []
        for stack in response.get('StackSummaries', []):
            stacks.append({
                'StackName': stack['StackName'],
                'StackStatus': stack['StackStatus']
            })

        return stacks

    except ClientError as e:
        print(f"Error listing CloudFormation stacks: {e}")
        return []

def delete_cloudformation_stack(stack_name):
    """
    Deletes a CloudFormation stack.

    Args:
        stack_name (str): The name of the CloudFormation stack to delete.

    Returns:
        bool: True if deletion was initiated successfully, False otherwise.
    """
    try:
        client = boto3.client('cloudformation')
        client.delete_stack(StackName=stack_name)
        print(f"Deletion of stack '{stack_name}' initiated successfully.")
        return True

    except ClientError as e:
        print(f"Error deleting CloudFormation stack '{stack_name}': {e}")
        return False


def interactive_delete_menu():
    """
    Interactive menu for selecting and deleting CloudFormation stacks.
    """
    print("\nFetching the list of CloudFormation stacks...\n")
    stacks = list_cloudformation_stacks()

    if not stacks:
        print("No stacks found or an error occurred.")
        return

    print("Available CloudFormation stacks:")
    for i, stack in enumerate(stacks):
        print(f"{i + 1}. {stack['StackName']} - {stack['StackStatus']}")

    print("\nSelect a stack to delete (enter the number), or type 'q' to quit:")

    while True:
        choice = input("Your choice: ")
        if choice.lower() == 'q':
            print("Exiting...")
            break

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(stacks):
                stack_to_delete = stacks[choice - 1]['StackName']
                print(f"\nYou selected to delete the stack: {stack_to_delete}")
                success = delete_cloudformation_stack(stack_to_delete)
                if success:
                    print(f"Stack '{stack_to_delete}' deletion initiated.")
                    break
                else:
                    print(f"Failed to delete the stack '{stack_to_delete}'. Please try again.")
            else:
                print(f"Invalid choice. Please select a number between 1 and {len(stacks)}, or 'q' to quit.")
        else:
            print("Invalid input. Please enter a number or 'q' to quit.")

