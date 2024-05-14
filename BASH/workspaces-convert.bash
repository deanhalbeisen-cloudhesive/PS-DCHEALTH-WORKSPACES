WORKSPACEID=`echo $1`
for WORKSPACE in $WORKSPACEID
	do
		aws workspaces modify-workspace-properties --workspace-id $WORKSPACE --workspace-properties "Protocols=[WSP]"
	done
