USERID="pacificon"
DIVISON="IT"
for USER in $USERID
do
	aws workspaces describe-workspaces --query "Workspaces[?UserName=='$USER']" --output json
	sleep 5
	WORKSPACEID=`aws workspaces describe-workspaces --query "Workspaces[?UserName=='$USER'].WorkspaceId" --output json | jq -r '.[]'`
	sleep 10
	aws workspaces create-tags --resource-id $WORKSPACEID --tags Key=Divison,Value=$DIVISON
done
