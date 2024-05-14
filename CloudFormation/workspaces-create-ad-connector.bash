aws ds connect-directory \
    --name "corp.example.com" \
    --short-name "CORP" \
    --password "Pass@word1" \
    --description "AD Connector for corp.example.com" \
    --size "Small" \
    --connect-settings ConnectSettings="{VpcId='vpc-xxxxxxx', SubnetIds=['subnet-xxxxxxx', 'subnet-yyyyyyy'], CustomerDnsIps=['10.0.0.111', '10.0.0.112']}"
