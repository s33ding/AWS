cp $aws_cred_place ~/.aws/credentials
token_py=~/ADM/aws/token.py
read -p 'TOKEN: ' -s token
aws sts get-session-token --duration-seconds 3600 --serial-number  $arn_aws --token-code $token >> ~/.aws/.tmp.json
python3 $token_py
rm -r ~/.aws/.tmp.json
