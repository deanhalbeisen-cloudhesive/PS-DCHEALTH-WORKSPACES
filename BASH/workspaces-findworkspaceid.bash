WORKSPACEID=`echo $1`
for WORKSPACE in $WORKSPACEID
	do
		aws workspaces describe-workspaces --query "Workspaces[?UserName=='$1'].WorkspaceId" --output text
	done
