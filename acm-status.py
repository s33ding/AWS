import boto3
import sys
import json
import os
import time

# Global variable to track ACM status
acm_status = None

def check_acm_certificate_status_by_id(certificate_id, region='us-east-1'):
    global acm_status

    client = boto3.client('acm', region_name=region)

    try:
        paginator = client.get_paginator('list_certificates')
        for page in paginator.paginate():
            for cert_summary in page['CertificateSummaryList']:
                arn = cert_summary['CertificateArn']
                if certificate_id == arn.split('/')[-1]:
                    cert_detail = client.describe_certificate(CertificateArn=arn)['Certificate']
                    acm_status = cert_detail.get('Status')
                    return {
                        'CertificateArn': arn,
                        'DomainName': cert_detail.get('DomainName'),
                        'Status': acm_status,
                        'NotBefore': str(cert_detail.get('NotBefore')),
                        'NotAfter': str(cert_detail.get('NotAfter')),
                        'IssuedAt': str(cert_detail.get('IssuedAt')),
                        'Type': cert_detail.get('Type')
                    }

        return {'Error': 'Certificate ID not found in ACM'}

    except Exception as e:
        return {'Error': str(e)}

def play_alarm():
    if os.name == 'posix':
        if sys.platform == 'darwin':
            # macOS: built-in system sound
            os.system('afplay /System/Library/Sounds/Glass.aiff')
        else:
            # Linux: use a standard desktop sound
            os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga')
    elif os.name == 'nt':
        import winsound
        winsound.MessageBeep()

# Main program logic
if __name__ == "__main__":
    if len(sys.argv) < 2:
        certificate_id = input("Enter the ACM certificate ID: ").strip()
    else:
        certificate_id = sys.argv[1].strip()

    result = check_acm_certificate_status_by_id(certificate_id)
    print(json.dumps(result, indent=2))

    # Ring sound alarm if cert status is "ISSUED"
    if acm_status == "ISSUED":
        play_alarm()

