import boto3
import sys

DEFAULT_TAIL_LOG_LINES = 200

def get_latest_builds(limit, project_name=None):
    codebuild = boto3.client('codebuild')

    if project_name:
        response = codebuild.list_builds_for_project(projectName=project_name)
        build_ids = response.get('ids', [])[:limit]
    else:
        response = codebuild.list_builds(sortOrder='DESCENDING')
        build_ids = response.get('ids', [])[:limit]

    return build_ids

def get_build_details(build_ids):
    codebuild = boto3.client('codebuild')
    return codebuild.batch_get_builds(ids=build_ids)['builds']

def show_build_info(build, show_logs=False, log_lines=DEFAULT_TAIL_LOG_LINES):
    print("=" * 60)
    print(f"Build ID   : {build['id']}")
    print(f"Status     : {build['buildStatus']}")
    print(f"Start Time : {build['startTime']}")
    print(f"Project    : {build['projectName']}")
    print(f"Phases     : {[p['phaseType'] for p in build['phases']]}")
    print("=" * 60)

    if show_logs and build.get('logs', {}).get('cloudWatchLogsArn'):
        log_group = build['logs']['groupName']
        log_stream = build['logs']['streamName']
        print(f"Log Group  : {log_group}")
        print(f"Log Stream : {log_stream}")
        print(f"--- Last {log_lines} Log Lines ---")
        print_tail_logs(log_group, log_stream, lines=log_lines)
        print("=" * 60 + "\n")

def print_tail_logs(group, stream, lines):
    logs = boto3.client('logs')
    try:
        response = logs.get_log_events(
            logGroupName=group,
            logStreamName=stream,
            limit=lines,
            startFromHead=False
        )
        for event in response['events']:
            print(event['message'].rstrip())
    except logs.exceptions.ResourceNotFoundException:
        print("Log stream not found.")

def main():
    try:
        limit = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    except ValueError:
        print("Usage: python codebuild-get_status.py [build_count] [--logs] [log_lines] [project_name]")
        sys.exit(1)

    show_logs = "--logs" in sys.argv

    try:
        log_lines_index = sys.argv.index("--logs") + 1
        log_lines = int(sys.argv[log_lines_index]) if len(sys.argv) > log_lines_index else DEFAULT_TAIL_LOG_LINES
    except (ValueError, IndexError):
        log_lines = DEFAULT_TAIL_LOG_LINES

    # Check if project name is passed (as last arg)
    project_name = None
    if len(sys.argv) >= 4:
        last_arg = sys.argv[-1]
        if not last_arg.startswith("--") and not last_arg.isdigit():
            project_name = last_arg

    build_ids = get_latest_builds(limit, project_name)
    if not build_ids:
        print("No builds found.")
        return

    builds = get_build_details(build_ids)
    for build in builds:
        show_build_info(build, show_logs, log_lines)

if __name__ == "__main__":
    main()

