#!/usr/bin/env python3
import boto3

def delete_samples():
    client = boto3.client('guardduty')
    
    # Get detectors
    detectors = client.list_detectors()['DetectorIds']
    if not detectors:
        print("No GuardDuty detectors found")
        return
    
    for detector_id in detectors:
        print(f"Processing detector: {detector_id}")
        
        # Keep archiving until no more sample findings
        total_archived = 0
        while True:
            # Get active findings only
            response = client.list_findings(
                DetectorId=detector_id,
                FindingCriteria={'Criterion': {'service.archived': {'Eq': ['false']}}}
            )
            findings = response['FindingIds']
            
            if not findings:
                break
            
            # Get finding details to check for samples
            finding_details = client.get_findings(
                DetectorId=detector_id,
                FindingIds=findings
            )
            
            # Filter for sample findings
            sample_findings = []
            for f in finding_details['Findings']:
                additional_info = f.get('Service', {}).get('AdditionalInfo', {}).get('Value', '')
                if '"sample":true' in additional_info:
                    sample_findings.append(f['Id'])
            
            if not sample_findings:
                break
                
            print(f"Archiving {len(sample_findings)} sample findings")
            
            client.archive_findings(
                DetectorId=detector_id,
                FindingIds=sample_findings
            )
            
            total_archived += len(sample_findings)
            
        print(f"Completed detector {detector_id} - Total archived: {total_archived}")

if __name__ == "__main__":
    delete_samples()
