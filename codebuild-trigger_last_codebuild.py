import boto3
import argparse
import sys

REGION = "us-east-1"

def get_last_project_name(codebuild):
    builds = codebuild.list_builds(sortOrder="DESCENDING")["ids"]
    if not builds:
        print("❌ No builds found.")
        sys.exit(1)

    last_build_id = builds[0]
    build_info = codebuild.batch_get_builds(ids=[last_build_id])["builds"][0]
    return build_info["projectName"]

def start_build(codebuild, project_name):
    print(f"🚀 Starting a new build for project: {project_name}...")
    response = codebuild.start_build(projectName=project_name)
    build_id = response["build"]["id"]
    print(f"✅ Build triggered: {build_id}")
    print(f"🔗 View build: https://{REGION}.console.aws.amazon.com/codesuite/codebuild/{project_name}/build/{build_id}/")
    return build_id

def main():
    parser = argparse.ArgumentParser(description="Trigger AWS CodeBuild project")
    parser.add_argument("--project", help="Name of the CodeBuild project to trigger")
    args = parser.parse_args()

    codebuild = boto3.client("codebuild", region_name=REGION)

    if args.project:
        project_name = args.project
        print(f"📦 Using provided project: {project_name}")
    else:
        print("🔍 No project provided. Fetching last project that ran...")
        project_name = get_last_project_name(codebuild)
        print(f"📦 Last project: {project_name}")

    start_build(codebuild, project_name)

if __name__ == "__main__":
    main()

