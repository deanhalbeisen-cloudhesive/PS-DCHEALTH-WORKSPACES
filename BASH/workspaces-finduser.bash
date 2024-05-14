WORKSPACEID=`echo $1`
for WORKSPACE in $WORKSPACEID
	do
		aws workspaces describe-workspaces --workspace-ids $WORKSPACE --query 'Workspaces[*].UserName' --output text

	done
