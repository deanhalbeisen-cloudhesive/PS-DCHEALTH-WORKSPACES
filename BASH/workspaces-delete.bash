#set -x
WORKSPACESIDS=`cat deleteall.in`
#echo $WORKSPACESIDS
for WORKSPACE in $WORKSPACESIDS
do
	aws workspaces terminate-workspaces --terminate-workspace-requests $WORKSPACE
	sleep 2
done
