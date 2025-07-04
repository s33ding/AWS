import subprocess
import json

REGION = "us-east-1"

def prompt_input(prompt, default=None):
    if default:
        response = input(f"{prompt} [{default}]: ").strip()
        return response if response else default
    return input(f"{prompt}: ").strip()

def choose_compute_type():
    options = [
        "BUILD_GENERAL1_SMALL",
        "BUILD_GENERAL1_MEDIUM",
        "BUILD_GENERAL1_LARGE"
    ]
    print("\n🧮 Choose compute type:")
    for idx, val in enumerate(options, 1):
        print(f"  {idx}) {val}")
    choice = input("Select [1-3]: ").strip()
    try:
        return options[int(choice) - 1]
    except (IndexError, ValueError):
        print("❌ Invalid choice, using default: BUILD_GENERAL1_SMALL")
        return "BUILD_GENERAL1_SMALL"

def run_aws_cli_update(project_name, image_uri, compute_type):
    environment_override = {
        "type": "LINUX_CONTAINER",
        "image": image_uri,
        "computeType": compute_type,
        "privilegedMode": True,
        "imagePullCredentialsType": "SERVICE_ROLE"
    }

    cmd = [
        "aws", "codebuild", "update-project",
        "--name", project_name,
        "--region", REGION,
        "--environment", json.dumps(environment_override)
    ]

    print("\n🛠️  Running AWS CLI to update project with privileged mode and custom image...")
    try:
        subprocess.run(cmd, check=True)
        print("✅ CodeBuild project updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ AWS CLI failed: {e}")

def main():
    print("🚀 Update CodeBuild Project with Custom Image and Privileged Mode")

    project_name = prompt_input("📝 Enter CodeBuild project name")
    image_uri = prompt_input("🖼️  Enter custom image URI (e.g., ECR URI)")
    compute_type = choose_compute_type()

    if not project_name or not image_uri:
        print("❌ Project name and image URI are required.")
        return

    run_aws_cli_update(project_name, image_uri, compute_type)

if __name__ == "__main__":
    main()

