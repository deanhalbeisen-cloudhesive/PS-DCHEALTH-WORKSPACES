DIRECTORYID="d-9067f97177"
BUNDLEID="wsb-fv2nqxmsb"
TARGETBUNDLE="wsb-07yldwvb6"
WORKSPACEIDS=`cat mig-w-1.in `

for workspaceid in $WORKSPACEIDS
do
	aws workspaces migrate-workspace --source-workspace-id $workspaceid --bundle-id $TARGETBUNDLE
	sleep .3
done
