cp $AWS_CRED_PLACE $AWS_CRED
read -p 'TOKEN: ' -s TOKEN
aws sts get-session-token --duration-seconds 3600 --serial-number  $ARN_AWS --token-code $TOKEN >> $AWS_TEMP_CRED
python3 $TOKEN_PY
rm -r $AWS_TEMP_CRED

