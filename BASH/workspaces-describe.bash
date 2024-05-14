DIRECTORYID="d-9067f97177"
for DIRECTORY in $DIRECTORYID
do
	#aws workspaces describe-workspaces --directory-id $DIRECTORY --query 'Workspaces[*].[WorkspaceId]' --output=text | wc -l > worspacecpount.out 
	#echo "sleeping for 10"
	#sleep 10
	#aws workspaces describe-workspaces --directory-id $DIRECTORY --query 'Workspaces[*].[WorkspaceId]' --output=text > workspace-id.in
	#echo "sleeping for 10"
	#sleep 10
	aws workspaces describe-workspaces --directory-id $DIRECTORY --output=text > workspace-dump.out
done
