# AssignBackupPolicy-fn
This template shows an example how to automate configuration of backup policy for OCI block storage based on volume tags. It uses OCI Event and Function services. An event is emitted when a new boot or block volume is created and it triggers OCI Function that configures backup policy based on the volume tag.
