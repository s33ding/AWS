cp $aws_cred_place $aws_cred
read -p 'TOKEN: ' -s token
aws sts get-session-token --duration-seconds 3600 --serial-number  $arn_aws --token-code $token >> $aws_temp_cred
python3 $token_py
rm -r $aws_temp_cred

