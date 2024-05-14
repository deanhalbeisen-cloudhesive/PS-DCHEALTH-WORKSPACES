DIRECTORYID="d-9067f97177"
for DIRECTORY in $DIRECTORYID
do
	aws workspaces import-client-branding --cli-input-json file://./workspaces-branding.json  --region us-east-1
done
