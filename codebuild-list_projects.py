import boto3

REGION = "us-east-1"  # change if needed

def main():
    codebuild = boto3.client("codebuild", region_name=REGION)

    print(f"📦 Listing CodeBuild projects in region: {REGION}...\n")

    try:
        paginator = codebuild.get_paginator("list_projects")
        project_names = []

        for page in paginator.paginate():
            project_names.extend(page["projects"])

        if not project_names:
            print("❌ No CodeBuild projects found.")
            return

        for i, name in enumerate(sorted(project_names), 1):
            print(f"{i:2}. {name}")

        print(f"\n✅ Total projects: {len(project_names)}")

    except Exception as e:
        print(f"❌ Error fetching projects: {e}")

if __name__ == "__main__":
    main()

