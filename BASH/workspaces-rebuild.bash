DIRECTORYID="d-9067f97177"
WORKSPACEIDS=`cat mig-w-1.in `

for workspaceid in $WORKSPACEIDS
do
	aws workspaces rebuild-workspace --rebuild-workspace-requests WorkspaceId=$workspaceid
	sleep .3
done
