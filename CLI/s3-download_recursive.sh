read -p "BUCKET: " bucket
read -p "PREFIX: " prefix

cmd="aws s3 cp s3://$bucket/$prefix . --recursive"
echo $cmd
$cmd


