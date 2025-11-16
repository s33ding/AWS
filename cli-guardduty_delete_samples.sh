#!/bin/bash

# Get detector ID
DETECTOR_ID=$(aws guardduty list-detectors --query 'DetectorIds[0]' --output text)

# List sample findings
aws guardduty get-findings --detector-id $DETECTOR_ID --finding-ids $(aws guardduty list-findings --detector-id $DETECTOR_ID --finding-criteria '{"sample":{"Eq":["true"]}}' --query 'FindingIds' --output text)

# Archive sample findings (this effectively removes them from active view)
aws guardduty archive-findings --detector-id $DETECTOR_ID --finding-ids $(aws guardduty list-findings --detector-id $DETECTOR_ID --finding-criteria '{"sample":{"Eq":["true"]}}' --query 'FindingIds' --output text)
