python3 $TOKEN_A
read -p 'TOKEN: ' -s TOKEN
aws sts get-session-token --duration-seconds 4600 --serial-number  $ARN_AWS --token-code $TOKEN > $AWS_TEMP_CRED
python3 $TOKEN_B
