WORKSPACEUSERS=`cat workspaces-user.in`
KMSKEY="arn:aws:kms:us-east-1:647700013769:alias/Workspaces-useast1"
DIRECTORYID="d-9067f97177"
BUNDLEID="wsb-07yldwvb6"
for USER in $WORKSPACEUSERS
do
        aws workspaces create-workspaces --workspaces DirectoryId=$DIRECTORYID,UserName=$USER,BundleId=$BUNDLEID,VolumeEncryptionKey=$KMSKEY,UserVolumeEncryptionEnabled=true,RootVolumeEncryptionEnabled=true,WorkspaceProperties="{RunningMode=\"AUTO_STOP\",RunningModeAutoStopTimeoutInMinutes=60,RootVolumeSizeGib=80,UserVolumeSizeGib=10,Protocols=[WSP]}"
done
