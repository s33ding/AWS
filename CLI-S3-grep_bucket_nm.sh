read -p "BUCKET: " bucket
aws s3 ls | grep $bucket | awk '{print $3}'
x=$(aws s3 ls | grep $bucket | awk '{print $3}')

read -p "ls [y/N]:" choice

if [[ $choice = y ]]
  then
	  echo "aws s3 ls $x"
	  x2=$(aws s3 ls $x)
	  echo $x2
fi

