import boto3
import sys

REGION = "us-east-1"  # You can change this or prompt if needed

def prompt_input(prompt, default=None):
    if default:
        response = input(f"{prompt} [{default}]: ").strip()
        return response if response else default
    else:
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

def update_codebuild_image(project_name, image_uri, compute_type):
    client = boto3.client("codebuild", region_name=REGION)

    print(f"\n🔧 Updating CodeBuild project: {project_name}")
    print(f"🖼️  Using image: {image_uri}")
    print(f"⚙️  Compute type: {compute_type}")
    print("🔐 Privileged mode: ENABLED")

    try:
        client.update_project(
            name=project_name,
            environment={
                "type": "LINUX_CONTAINER",
                "image": image_uri,
                "computeType": compute_type,
                "privilegedMode": True,
                "imagePullCredentialsType": "SERVICE_ROLE"
            }
        )
        print("✅ CodeBuild project updated successfully.")
    except Exception as e:
        print(f"❌ Failed to update project: {e}")
        sys.exit(1)

def main():
    print("🚀 CodeBuild Custom Image Setup")
    project_name = prompt_input("📝 Enter CodeBuild project name")
    image_uri = prompt_input("🖼️  Enter custom image URI (ECR or Docker Hub)")
    compute_type = choose_compute_type()

    if not project_name or not image_uri:
        print("❌ Project name and image URI are required.")
        sys.exit(1)

    update_codebuild_image(project_name, image_uri, compute_type)

if __name__ == "__main__":
    main()

